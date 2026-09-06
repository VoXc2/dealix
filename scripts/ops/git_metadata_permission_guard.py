#!/usr/bin/env python3
"""Audit and optionally repair Dealix Git metadata permissions.

This tool exists to prevent a repeat of root-owned, unreadable loose objects and
remote refs created when operational scripts invoke Git as root.

Safety properties:
- worktree files are never traversed or changed;
- only .git/objects, .git/refs, .git/logs and .git/packed-refs are in scope;
- ownership is never recursively reassigned;
- --repair changes group/mode only for root-owned metadata that is not usable by
  the configured Dealix group;
- secret values are never read or printed.

Default mode is read-only.  --repair requires uid 0.
"""

from __future__ import annotations

import argparse
import grp
import os
import pwd
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    path: Path
    kind: str
    mode: int
    uid: int
    gid: int
    needs_group_read: bool
    needs_group_write: bool
    needs_group_exec: bool


def git_dir(repo: Path) -> Path:
    proc = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--absolute-git-dir"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return Path(proc.stdout.strip()).resolve()


def shared_repository(repo: Path) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), "config", "--get", "core.sharedRepository"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    return proc.stdout.strip()


def in_scope_paths(gitdir: Path):
    for name in ("objects", "refs", "logs"):
        root = gitdir / name
        if not root.exists():
            continue
        yield root, name
        for path in root.rglob("*"):
            yield path, name
    packed = gitdir / "packed-refs"
    if packed.exists():
        yield packed, "packed-refs"


def finding_for(path: Path, kind: str, target_gid: int) -> Finding | None:
    try:
        st = path.lstat()
    except OSError:
        return None

    if st.st_uid != 0:
        return None

    mode = stat.S_IMODE(st.st_mode)
    is_dir = stat.S_ISDIR(st.st_mode)
    group_matches = st.st_gid == target_gid
    group_read = bool(mode & stat.S_IRGRP) and group_matches
    group_write = bool(mode & stat.S_IWGRP) and group_matches
    group_exec = (not is_dir) or (bool(mode & stat.S_IXGRP) and group_matches)

    # Loose objects are immutable: the Dealix group only needs read access.
    # Refs/logs and their directories must be writable so future Git operations
    # under the dealix account can advance them safely.
    need_write = kind in {"refs", "logs", "packed-refs"}
    need_exec = is_dir

    if group_read and (not need_write or group_write) and (not need_exec or group_exec):
        return None

    return Finding(
        path=path,
        kind=kind,
        mode=mode,
        uid=st.st_uid,
        gid=st.st_gid,
        needs_group_read=not group_read,
        needs_group_write=need_write and not group_write,
        needs_group_exec=need_exec and not group_exec,
    )


def apply_repair(item: Finding, target_gid: int) -> None:
    st = item.path.lstat()
    new_mode = stat.S_IMODE(st.st_mode) | stat.S_IRGRP
    if stat.S_ISDIR(st.st_mode):
        new_mode |= stat.S_IXGRP
        if item.kind in {"refs", "logs"}:
            new_mode |= stat.S_IWGRP | stat.S_ISGID
    elif item.kind in {"refs", "logs", "packed-refs"}:
        new_mode |= stat.S_IWGRP

    os.chown(item.path, -1, target_gid)
    os.chmod(item.path, new_mode)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default="/opt/dealix/workspace/dealix")
    parser.add_argument("--user", default="dealix")
    parser.add_argument("--group", default="dealix")
    parser.add_argument("--repair", action="store_true")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    target_uid = pwd.getpwnam(args.user).pw_uid
    target_gid = grp.getgrnam(args.group).gr_gid
    gdir = git_dir(repo)

    findings: list[Finding] = []
    root_owned = 0
    for path, kind in in_scope_paths(gdir):
        try:
            if path.lstat().st_uid == 0:
                root_owned += 1
        except OSError:
            continue
        item = finding_for(path, kind, target_gid)
        if item:
            findings.append(item)

    print(f"GITDIR={gdir}")
    print(f"CORE_SHARED_REPOSITORY={shared_repository(repo) or 'unset'}")
    print(f"ROOT_OWNED_METADATA={root_owned}")
    print(f"UNUSABLE_ROOT_OWNED_METADATA={len(findings)}")
    print("WORKTREE_MUTATION=false")
    print("SECRET_VALUES_PRINTED=false")

    if args.repair:
        if os.geteuid() != 0:
            print("GIT_METADATA_REPAIR=HOLD reason=root_required")
            return 3
        for item in findings:
            apply_repair(item, target_gid)
        print(f"GIT_METADATA_REPAIRED={len(findings)}")

        # Validate that the target account can traverse objects and resolve HEAD.
        proc = subprocess.run(
            [
                "sudo", "-u", args.user, "-H", "git", "-C", str(repo),
                "-c", f"safe.directory={repo}", "rev-parse", "HEAD",
            ],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if proc.returncode != 0:
            print("GIT_METADATA_REPAIR=HOLD reason=target_user_git_unusable")
            return 4
        print("GIT_METADATA_REPAIR=PASS")
        return 0

    if findings:
        print("GIT_METADATA_INTEGRITY=HOLD")
        print("NEXT=rerun_with_--repair_as_root")
        return 1

    if shared_repository(repo) not in {"group", "true", "1"}:
        print("GIT_METADATA_INTEGRITY=HOLD reason=core.sharedRepository_not_group")
        return 2

    print("GIT_METADATA_INTEGRITY=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
