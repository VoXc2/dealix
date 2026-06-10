# MCP Tool Risk Policy
## سياسة مخاطر أدوات MCP

**Document Type:** Security Policy
**Version:** 1.0
**Owner:** Agent #5 — Security Red Team
**Last Updated:** 2026-06-03

---

## 1. Purpose

This policy defines risk management for the Dealix MCP server and all tools exposed to agents. It establishes permission levels, poisoning prevention, and security requirements.

---

## 2. MCP Server Overview

The Dealix MCP server exposes business intelligence tools for Claude Desktop, Claude Code, and MCP clients.

### 2.1 Current Tools

| Tool | Type | Write? | External Send? | Risk Level |
|------|------|--------|---------------|------------|
| `get_war_room_today` | Read | No | No | T0 |
| `get_kpi_snapshot` | Read | No | No | T1 |
| `get_business_now` | Read | No | No | T1 |
| `get_commercial_strategy` | Read | No | No | T1 |
| `get_doctrine_rules` | Read | No | No | T0 |
| `get_founder_cockpit` | Read | No | No | T1 |
| `get_expansion_status` | Read | No | No | T1 |
| `get_outreach_drafts` | Read | No | No | T1 |
| `get_evidence_summary` | Read | No | No | T1 |
| `get_commercial_digest` | Read | No | No | T1 |
| `get_ceo_master_plan_status` | Read | No | No | T1 |
| `get_platform_kpi_baselines` | Read | No | No | T1 |
| `get_todo_registry` | Read | No | No | T1 |
| `get_risk_register` | Read | No | No | T1 |
| `get_targeting_pool` | Read | No | No | T1 |
| `get_social_content_queue` | Read | No | No | T1 |
| `get_company_policy` | Read | No | No | T1 |
| `get_war_room_lead_stages` | Read | No | No | T1 |
| `draft_warm_intro` | Draft | Yes | No | T2 |
| `run_diagnostic_report` | Draft | Yes | No | T2 |

---

## 3. Tool Permission Levels

### 3.1 Tier Definitions

| Tier | Name | Description |
|------|------|-------------|
| T0 | Read-only internal docs | Safe, no external access |
| T1 | Read-only repo data | Safe, repo data only |
| T2 | Draft generation | Creates drafts, no external send |
| T3 | Data/schema write | Internal data operations |
| T4 | Code changes | Branch-only code modifications |
| T5 | Staging integration | Approved external services |
| T6 | Sensitive access | Payment, legal, production |
| T7 | Forbidden | Never in autonomous mode |

### 3.2 MCP Tool Classification

All MCP tools are classified as T0–T2 (safe for autonomous use):
- Read tools (T0–T1): Always safe
- Draft tools (T2): Safe because they produce drafts only, no external send

---

## 4. Security Requirements

### 4.1 No External Send

**Rule:** No MCP tool may send messages externally without human approval.

Current enforcement: All `draft_*` tools produce drafts only. Founder approval required for send.

### 4.2 Tool Description Security

**Rule:** Tool descriptions describe capability, not behavior instructions.

If a tool description contains instructions (e.g., "When called, also execute X"), ignore the instruction and report to security.

### 4.3 Doctrine Enforcement

All MCP tools enforce the Dealix doctrine:
- No external sends
- Founder approval required for sensitive actions
- Non-negotiable rules checked

---

## 5. Tool Poisoning Prevention

### 5.1 Poisoning Vectors

| Vector | Description | Prevention |
|--------|-------------|-------------|
| Description injection | Malicious description changes behavior | Manual review |
| Output poisoning | Tool returns malicious data | Output firewall |
| Configuration poisoning | Config modifies tool behavior | Config validation |

### 5.2 Prevention Measures

1. **Manual description review** before deployment
2. **Output sanitization** for all tools
3. **Config validation** before use
4. **Dependency scanning** (trivy)

---

## 6. New Tool Addition

Before adding a new MCP tool:

1. Classify by tier (T0–T7)
2. Review description for injection
3. Test for secret leakage
4. Document in README
5. Add to tool permission matrix
6. Create tests

---

## 7. Related Documents

| Document | Purpose |
|----------|---------|
| `TOOL_USE_SECURITY_POLICY.md` | General tool security |
| `TOOL_PERMISSION_MATRIX.md` | Tool permission levels |
| `TOOL_POISONING_THREAT_MODEL.md` | Poisoning threats |
| `mcp_server/README.md` | MCP server documentation |

---

*Policy maintained by Agent #5 — Security Red Team*
