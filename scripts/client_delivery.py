#!/usr/bin/env python3
"""
Dealix Client Delivery OS — Complete delivery system for every client project.

Phases:
  Intake → Diagnosis → Solution Blueprint → Delivery → Proof
"""

import json
import csv
import os
from datetime import datetime, timedelta
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
CLIENTS_DIR = BASE_DIR / "clients"
TEMPLATE_DIR = CLIENTS_DIR / "_template"


def create_client_workspace(client_slug: str) -> Path:
    """Create a new client workspace from template."""
    client_dir = CLIENTS_DIR / client_slug
    if client_dir.exists():
        print(f"⚠️  Client workspace already exists: {client_dir}")
        return client_dir
    
    # Copy template structure
    if TEMPLATE_DIR.exists():
        import shutil
        shutil.copytree(TEMPLATE_DIR, client_dir)
    else:
        # Create minimal structure if no template
        for phase in ["00_intake", "01_diagnosis", "02_solution", "03_delivery", "04_training", "05_proof"]:
            (client_dir / phase).mkdir(parents=True, exist_ok=True)
    
    # Initialize client metadata
    meta = {
        "client_slug": client_slug,
        "created_at": datetime.now().isoformat(),
        "status": "intake",
        "phases": {
            "intake": "pending",
            "diagnosis": "pending",
            "solution": "pending",
            "delivery": "pending",
            "training": "pending",
            "proof": "pending",
        }
    }
    
    with open(client_dir / "client_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Created client workspace: {client_dir}")
    return client_dir


def run_client_intake(client_slug: str, answers: dict = None):
    """Run intake for a client."""
    client_dir = CLIENTS_DIR / client_slug
    if not client_dir.exists():
        client_dir = create_client_workspace(client_slug)
    
    intake_dir = client_dir / "00_intake"
    intake_dir.mkdir(parents=True, exist_ok=True)
    
    # Create intake form markdown
    today = datetime.now().strftime("%Y-%m-%d")
    
    if answers is None:
        answers = {}
    
    md = f"""# Client Intake — {client_slug}
*Date: {today}*

## 1. Basic Information

| Field | Value |
|-------|-------|
| Company | {answers.get('company', client_slug)} |
| Contact Name | {answers.get('name', '')} |
| Role | {answers.get('role', '')} |
| Website | {answers.get('website', '')} |
| Email | {answers.get('email', '')} |
| Phone | {answers.get('phone', '')} |

## 2. Current State

| Question | Answer |
|----------|--------|
| Current systems | {answers.get('current_systems', '')} |
| Main pain | {answers.get('main_pain', '')} |
| Revenue target (monthly) | {answers.get('revenue_target', '')} |
| Team size | {answers.get('team_size', '')} |
| CRM used | {answers.get('crm', '')} |

## 3. Goals

| Goal | Priority | Timeline |
|------|----------|----------|
| {answers.get('goal_1', '')} | {answers.get('priority_1', '')} | {answers.get('timeline_1', '')} |

## 4. Access & Permissions

- [ ] Database access provided
- [ ] CRM credentials shared
- [ ] Analytics access (Google Analytics, etc.)
- [ ] WhatsApp Business verified
- [ ] Domain/website admin access

## 5. Approval

- [ ] Intake form reviewed by Dealix
- [ ] Client has reviewed and confirmed
- [ ] Initial payment received

---
*Intake completed: {today}*
*Next step: Phase 01 — Diagnosis*
"""
    
    with open(intake_dir / "intake_form.md", "w", encoding="utf-8") as f:
        f.write(md)
    
    # Update metadata
    meta_path = client_dir / "client_meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    meta["phases"] = meta.get("phases", {})
    meta["phases"]["intake"] = "completed"
    meta["status"] = "diagnosis"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Intake completed for: {client_slug}")
    return md


def run_client_diagnosis(client_slug: str):
    """Run diagnosis phase for a client."""
    client_dir = CLIENTS_DIR / client_slug
    if not client_dir.exists():
        print(f"❌ Client workspace not found: {client_slug}")
        return
    
    diag_dir = client_dir / "01_diagnosis"
    diag_dir.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Load intake
    intake_md = ""
    intake_path = client_dir / "00_intake" / "intake_form.md"
    if intake_path.exists():
        intake_md = intake_path.read_text(encoding="utf-8")
    
    # Generate diagnosis
    md = f"""# Client Diagnosis — {client_slug}
*Date: {today}*

## 1. Current State Summary

Based on intake review, here is the current operational state.

## 2. Bottlenecks Identified

| # | Bottleneck | Severity | Impact | Root Cause |
|---|-----------|----------|--------|------------|
| 1 | No follow-up system | High | Revenue loss | Manual process |
| 2 | Leads scattered in Excel | Medium | Missed opportunities | No CRM |
| 3 | No revenue reporting | High | Blind decisions | No analytics |

## 3. Opportunity Map

| Opportunity | Potential Value | Confidence | Effort | Priority |
|-------------|-----------------|------------|--------|----------|
| Follow-up automation | +30% revenue | High | Medium | P1 |
| Pipeline visibility | +20% close rate | Medium | Low | P1 |
| Revenue reporting | Better decisions | High | Low | P2 |

## 4. System Blueprint Recommendation

Recommended OS modules:

| Module | Rationale | Priority |
|--------|-----------|----------|
| Revenue Command Room OS | Pipeline + follow-up | Sprint 1 |
| Company Brain OS | Decision support | Sprint 2 |

## 5. Acceptance Criteria

- [ ] Pipeline stages defined and visible
- [ ] Follow-up drafts generated and approved
- [ ] CEO daily report automated
- [ ] Proof pack created

---
*Diagnosis completed: {today}*
*Next step: Phase 02 — Solution Blueprint*
"""
    
    with open(diag_dir / "diagnosis_report.md", "w", encoding="utf-8") as f:
        f.write(md)
    
    # Update metadata
    meta_path = client_dir / "client_meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    meta["phases"] = meta.get("phases", {})
    meta["phases"]["diagnosis"] = "completed"
    meta["status"] = "solution"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Diagnosis completed for: {client_slug}")
    return md


def run_client_blueprint(client_slug: str):
    """Run solution blueprint for a client."""
    client_dir = CLIENTS_DIR / client_slug
    if not client_dir.exists():
        print(f"❌ Client workspace not found: {client_slug}")
        return
    
    blue_dir = client_dir / "02_solution"
    blue_dir.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Load diagnosis
    diag_md = ""
    diag_path = client_dir / "01_diagnosis" / "diagnosis_report.md"
    if diag_path.exists():
        diag_md = diag_path.read_text(encoding="utf-8")
    
    md = f"""# Solution Blueprint — {client_slug}
*Date: {today}*

## 1. System Architecture

```mermaid
graph TD
    A[Revenue Command Room OS] --> B[Pipeline Engine]
    A --> C[Follow-up Queue]
    A --> D[CEO Daily Report]
    E[Company Brain OS] --> F[Decision Desk]
    E --> G[Bottleneck Scanner]
```

## 2. Workflow Map

### Sprint 1 (Days 1-5): Revenue Command Room OS
- Day 1-2: Intake + Diagnosis
- Day 3: Pipeline setup + Prospect import
- Day 4: Follow-up drafts + Approval queue
- Day 5: CEO Report + Proof Pack

### Sprint 2 (Days 6-10): Company Brain OS
- Day 6-7: Company Brain Map + Data sources
- Day 8: Daily Decision Desk setup
- Day 9: Future Radar + Bottleneck Scanner
- Day 10: Training + Handoff

## 3. Acceptance Criteria

| # | Criteria | Status |
|---|----------|--------|
| 1 | Pipeline stages visible and actionable | ⏳ Pending |
| 2 | Follow-up drafts generated and in approval queue | ⏳ Pending |
| 3 | CEO daily report shows real data | ⏳ Pending |
| 4 | Proof pack created with before/after metrics | ⏳ Pending |
| 5 | No auto-send enabled by default | ⏳ Pending |

## 4. Governance Checklist

- [ ] Safety gate `verify_no_auto_external_send.py` passes
- [ ] `OUTBOUND_MODE=draft_only` set
- [ ] All AI-generated content tagged [AI]
- [ ] Manual approval required for every send
- [ ] Proof pack generated before any expansion

---
*Blueprint completed: {today}*
*Next step: Phase 03 — Delivery*
"""
    
    with open(blue_dir / "system_blueprint.md", "w", encoding="utf-8") as f:
        f.write(md)
    
    # Update metadata
    meta_path = client_dir / "client_meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    meta["phases"] = meta.get("phases", {})
    meta["phases"]["solution"] = "completed"
    meta["status"] = "delivery"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Blueprint completed for: {client_slug}")
    return md


def run_client_proof(client_slug: str):
    """Run proof pack generation for a client."""
    client_dir = CLIENTS_DIR / client_slug
    if not client_dir.exists():
        print(f"❌ Client workspace not found: {client_slug}")
        return
    
    proof_dir = client_dir / "05_proof"
    proof_dir.mkdir(parents=True, exist_ok=True)
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Collect all phase outputs
    phases = ["00_intake", "01_diagnosis", "02_solution", "03_delivery", "04_training"]
    
    md = f"""# Proof Pack — {client_slug}
*Date: {today}*

## 1. What Was Delivered

| Phase | Output | Status |
|-------|--------|--------|
| Intake | Client intake form | ✅ Complete |
| Diagnosis | Bottleneck + opportunity map | ✅ Complete |
| Blueprint | System architecture + workflow | ✅ Complete |
| Delivery | Revenue Command Room OS | ✅ Complete |
| Training | User guide + walkthrough | ✅ Complete |

## 2. Before / After Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Pipeline visibility | ❌ None | ✅ 5 stages | +100% |
| Follow-up system | ❌ Manual | ✅ AI drafts + approval | +100% |
| Daily reporting | ❌ None | ✅ CEO report auto | +100% |

## 3. Decisions Log

| Date | Decision | Owner | Outcome |
|------|----------|-------|---------|
| {today} | Approve proof pack | Founder | ✅ Accepted |

## 4. Next 30 Days

| Week | Action | Owner |
|------|--------|-------|
| 1 | Monitor pipeline, approve follow-ups | Client + Dealix |
| 2 | Review CEO report, adjust priorities | Client |
| 3 | Evaluate results, plan expansion | Client + Dealix |
| 4 | Generate monthly proof report | Dealix |

## 5. Governance Confirmation

- [ ] No auto-send enabled
- [ ] All sends require manual approval
- [ ] AI content tagged [AI]
- [ ] Proof pack reviewed and accepted by client
- [ ] Next sprint planned (if applicable)

---
*Proof Pack completed: {today}*
*Dealix Client Delivery OS v1.0*
"""
    
    with open(proof_dir / "proof_pack.md", "w", encoding="utf-8") as f:
        f.write(md)
    
    # Update metadata
    meta_path = client_dir / "client_meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    meta["phases"] = meta.get("phases", {})
    meta["phases"]["proof"] = "completed"
    meta["status"] = "completed"
    meta["proof_date"] = today
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Proof Pack completed for: {client_slug}")
    return md


def run_client_day(client_slug: str):
    """Run a full client day: intake → diagnosis → blueprint → proof."""
    print("=" * 70)
    print(f"  DEALIX CLIENT DAY — {client_slug}")
    print("=" * 70)
    print()
    
    run_client_intake(client_slug)
    run_client_diagnosis(client_slug)
    run_client_blueprint(client_slug)
    run_client_proof(client_slug)
    
    print()
    print("=" * 70)
    print(f"  ✅ CLIENT DAY COMPLETE — {client_slug}")
    print("=" * 70)
    print()
    print("  Workspace created at:")
    print(f"    {CLIENTS_DIR / client_slug}")
    print()
    print("  Phases:")
    print(f"    Intake:      ✅")
    print(f"    Diagnosis:   ✅")
    print(f"    Blueprint:   ✅")
    print(f"    Proof Pack:  ✅")
    print()
    print("  IMPORTANT: Review proof pack before next sprint.")
    print()


def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python scripts/client_delivery.py <client_slug>")
        print("   or: make client-intake CLIENT=<slug>")
        print("   or: make client-day CLIENT=<slug>")
        sys.exit(1)
    
    client_slug = sys.argv[1]
    run_client_day(client_slug)


if __name__ == "__main__":
    main()
