"""
T6 example — discover Skills, pick a Vertical, register a custom Agent.

Demonstrates the canonical flow for a new tenant onboarding into the
T6 surface:

  1. List the Skills catalogue.
  2. Pick a Vertical bundle.
  3. Register a BYOA agent that composes two Skills.
  4. Install a marketplace workflow.

Run against a live deployment when DEALIX_API_BASE + DEALIX_API_KEY
are set.
"""

from __future__ import annotations

import os

import httpx

BASE = os.environ.get("DEALIX_API_BASE", "https://api.dealix.me").rstrip("/")
API_KEY = os.environ.get("DEALIX_API_KEY", "")

HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}


def list_skills() -> list[dict]:
    r = httpx.get(f"{BASE}/api/v1/skills", headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()["skills"]


def list_verticals() -> list[dict]:
    r = httpx.get(f"{BASE}/api/v1/verticals", headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()["verticals"]


def apply_vertical(vertical_id: str) -> dict:
    r = httpx.post(
        f"{BASE}/api/v1/verticals/apply",
        json={"vertical_id": vertical_id},
        headers=HEADERS,
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def register_agent(manifest: dict) -> dict:
    r = httpx.post(
        f"{BASE}/api/v1/agents", json=manifest, headers=HEADERS, timeout=10
    )
    r.raise_for_status()
    return r.json()


def install_workflow(template_id: str) -> dict:
    r = httpx.post(
        f"{BASE}/api/v1/workflows/install",
        json={"template_id": template_id},
        headers=HEADERS,
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    skills = list_skills()
    print(f"Catalogue has {len(skills)} skills:")
    for s in skills:
        print(f"  - {s['id']}: {s['description']}")

    verticals = list_verticals()
    print(f"\n{len(verticals)} verticals shipped:")
    for v in verticals:
        print(f"  - {v['id']} (plan {v['pricing_default_plan']})")

    print("\nApplying 'real-estate' bundle...")
    print(apply_vertical("real-estate"))

    agent = {
        "id": "real-estate-qualifier",
        "name": "Real-estate Saudi qualifier",
        "model": "claude-haiku-4-5",
        "tools": ["sales_qualifier", "compliance_reviewer"],
        "prompt_override": (
            "You are an Arabic-Khaliji real-estate sales qualifier. "
            "Score the lead 0..1 using BANT and the PDPL contactability gate."
        ),
        "max_usd_per_request": 0.5,
        "locale": "ar",
    }
    print("\nRegistering custom agent...")
    print(register_agent(agent))

    print("\nInstalling lead_to_booking workflow template...")
    print(install_workflow("lead_to_booking"))
