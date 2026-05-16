"""Workflow versioning helpers."""

from __future__ import annotations


def parse_semver(version: str) -> tuple[int, int, int]:
    major, minor, patch = version.split('.')
    return int(major), int(minor), int(patch)


def valid_workflow_upgrade(current_version: str, next_version: str) -> bool:
    return parse_semver(next_version) > parse_semver(current_version)


__all__ = ['parse_semver', 'valid_workflow_upgrade']
