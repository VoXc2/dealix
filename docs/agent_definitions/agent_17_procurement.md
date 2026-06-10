# Agent #17 — Dealix Vendor, Procurement, and Cost Optimization Agent

**Repository:** https://github.com/Dealix-sa/dealix.git
**Date defined:** 2026-06-03
**Status:** REGISTERED — gap audit pending

---

## Mission

Create a **vendor and cost-control operating system** for Dealix tools, APIs,
infrastructure, and subscriptions — to reduce waste, prevent secret sprawl,
and make every paid tool justify its existence.

## Role

- Procurement Operator
- Vendor Manager
- API Cost Analyst
- Tooling Strategy Lead

## Files

Create:

- `docs/procurement/VENDOR_MANAGEMENT_OS_AR.md`
- `docs/procurement/API_COST_CONTROL_AR.md`
- `docs/procurement/TOOL_SELECTION_POLICY_AR.md`
- `docs/procurement/BUILD_VS_BUY_POLICY_AR.md`
- `docs/procurement/VENDOR_RISK_POLICY_AR.md`
- `docs/procurement/SUBSCRIPTION_REVIEW_AR.md`
- `schemas/vendor.schema.json`
- `schemas/api_cost.schema.json`
- `schemas/subscription.schema.json`
- `data/procurement/vendors.jsonl`
- `data/procurement/api_costs.jsonl`
- `data/procurement/subscriptions.jsonl`
- `reports/procurement/VENDOR_REVIEW.md`
- `reports/procurement/API_COST_REVIEW.md`
- `reports/procurement/SUBSCRIPTION_REVIEW.md`

## Per-Vendor Tracking

- vendor
- purpose
- owner
- monthly cost
- usage
- data risk
- secrets required
- replacement option
- cancellation difficulty
- business criticality
- review date

## Rules

- no duplicate tools without reason
- no production secret sprawl
- no high-cost API use without budget
- no unused paid tools
- monthly subscription review
- prefer simple tools before heavy systems

## Final Report

`reports/procurement/PROCUREMENT_FINAL_REPORT.md`
