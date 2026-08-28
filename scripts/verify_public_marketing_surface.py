#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen

FORBIDDEN = (
    "499 SAR",
    "499 ر.س",
    "٤٩٩",
    "7-Day",
    "7-day",
    "7 day",
    "12,000 ريال",
    "2,999",
    "7,999",
    "1,500–2,500",
    "1,500-2,500",
    "استرجاع كامل",
    "money-back",
    "price-lock",
    "47+",
    "شهادات معتمدة",
)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def forbidden_hits(text: str) -> list[str]:
    low = text.lower()
    return [item for item in FORBIDDEN if item.lower() in low]


def local_check(root: Path) -> list[str]:
    errors: list[str] = []
    landing = root / "landing"
    manifest_path = landing / "public-surface-manifest.json"
    if not manifest_path.is_file():
        return ["missing public-surface-manifest.json"]

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    canonical = manifest.get("canonical_indexable", [])
    retired = manifest.get("retired_redirect", {})
    robots = (landing / "robots.txt").read_text(encoding="utf-8")
    sitemap = (landing / "sitemap.xml").read_text(encoding="utf-8")

    for name in canonical:
        path = landing / name
        if not path.is_file():
            fail(errors, f"canonical_missing:{name}")
            continue
        hits = forbidden_hits(path.read_text(encoding="utf-8"))
        if hits:
            fail(errors, f"canonical_legacy_claim:{name}:{','.join(hits)}")
        url = "https://dealix.me/" if name == "index.html" else f"https://dealix.me/{name}"
        if f"<loc>{url}</loc>" not in sitemap:
            fail(errors, f"canonical_missing_from_sitemap:{name}")

    for name in retired:
        url = f"https://dealix.me/{name}"
        if f"<loc>{url}</loc>" in sitemap:
            fail(errors, f"retired_in_sitemap:{name}")
        if f"Disallow: /{name}" not in robots:
            fail(errors, f"retired_not_quarantined_in_robots:{name}")

    return errors


def fetch_follow(url: str, timeout: float) -> tuple[int, str, str]:
    req = Request(url, headers={"User-Agent": "DealixPublicSurfaceVerifier/1.0"})
    with urlopen(req, timeout=timeout) as response:
        return (
            int(response.status),
            response.geturl(),
            response.read().decode("utf-8", errors="replace"),
        )


def fetch_no_redirect(url: str, timeout: float) -> tuple[int, str | None, str]:
    opener = build_opener(NoRedirect)
    req = Request(url, headers={"User-Agent": "DealixPublicSurfaceVerifier/1.0"})
    try:
        with opener.open(req, timeout=timeout) as response:
            return (
                int(response.status),
                response.headers.get("Location"),
                response.read().decode("utf-8", errors="replace"),
            )
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        return int(exc.code), exc.headers.get("Location"), body


def live_check(root: Path, base: str, timeout: float) -> list[str]:
    errors: list[str] = []
    manifest = json.loads(
        (root / "landing/public-surface-manifest.json").read_text(encoding="utf-8")
    )
    base = base.rstrip("/") + "/"

    for name in manifest.get("canonical_indexable", []):
        rel = "" if name == "index.html" else name
        url = urljoin(base, rel)
        try:
            status, final_url, body = fetch_follow(url, timeout)
        except (HTTPError, URLError, TimeoutError) as exc:
            fail(errors, f"live_canonical_fetch:{name}:{exc}")
            continue
        if status != 200:
            fail(errors, f"live_canonical_status:{name}:{status}")
        hits = forbidden_hits(body)
        if hits:
            fail(errors, f"live_canonical_legacy_claim:{name}:{','.join(hits)}")
        if urlparse(final_url).netloc != urlparse(base).netloc:
            fail(errors, f"live_canonical_cross_domain:{name}:{final_url}")

    for name, expected in manifest.get("retired_redirect", {}).items():
        url = urljoin(base, name)
        try:
            status, location, body = fetch_no_redirect(url, timeout)
        except (URLError, TimeoutError) as exc:
            fail(errors, f"live_retired_fetch:{name}:{exc}")
            continue

        if status in (301, 302, 307, 308):
            if not location:
                fail(errors, f"live_retired_redirect_missing_location:{name}")
            else:
                actual_path = urlparse(urljoin(url, location)).path
                if actual_path != expected:
                    fail(
                        errors,
                        f"live_retired_wrong_redirect:{name}:{actual_path}!={expected}",
                    )
        elif status in (404, 410):
            pass
        elif status == 200:
            low = body.lower()
            if 'name="robots"' not in low or "noindex" not in low:
                fail(errors, f"live_retired_still_indexable:{name}")
            hits = forbidden_hits(body)
            if hits:
                fail(errors, f"live_retired_legacy_claim:{name}:{','.join(hits)}")
        else:
            fail(errors, f"live_retired_unexpected_status:{name}:{status}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--live-base-url")
    parser.add_argument("--timeout", type=float, default=12.0)
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    errors = local_check(root)
    if args.live_base_url:
        errors.extend(live_check(root, args.live_base_url, args.timeout))

    if errors:
        print("DEALIX_PUBLIC_MARKETING_SURFACE=FAIL")
        for item in errors:
            print(f"- {item}")
        return 1

    print("DEALIX_PUBLIC_MARKETING_SURFACE=PASS")
    print(f"LIVE_CHECK={'ON' if args.live_base_url else 'OFF'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
