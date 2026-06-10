# Anti-Duplication Policy — Dealix

> **Last updated:** 2026-06-03 · **Owner:** Agent #35 (Final Integration) · **Version:** v1.0
> **Purpose:** explicit rules to prevent duplicate docs, conflicting naming, and orphan reports.

---

## 1) Core Rule (One-Liner)

> **Before creating a new file, search the existing repo (`grep`/`rg`) for the concept. If a similar file exists, cross-reference it; do not duplicate. If you must duplicate, file an `owner=engineer` issue with the merge plan.**

---

## 2) When Two Docs Cover the Same Concept

| Situation | Action | Authority |
|-----------|--------|-----------|
| New doc covers concept fully, old is a subset | **KEEP-NEW + LINK-OLD**: new becomes canonical; old has banner "see [new]" | system owner + founder |
| New doc is a subset of old | **LINK-NEW**: new has "see [old]" at top | system owner |
| Both are full but for different audiences | **KEEP-BOTH + LINK**: each explains "if you're X, read me" | both owners |
| Genuine duplicate (same content, different filenames) | **MERGE**: pick canonical filename (oldest), move new to `archive/<YYYY>/` | founder only |
| Conflicting facts in two docs | **FLAG**: open issue tagged `conflict-resolution` | founder decides |

> **Default = LINK, not MERGE.** Reasons: cross-references break easily; legacy files may be cited externally; cultural value of legacy.

---

## 3) Naming Conventions

### 3.1 Folder Names

- Use **singular** for system, **plural** for collections: `docs/governance/` (the system), `docs/case_studies/` (collection).
- **Suffix with role** when ambiguous: `enterprise_sales/` (motion), `enterprise/` (readiness), `enterprise_rollout/` (post-sale), `enterprise_architecture/` (system map), `enterprise_trust/` (pack).
- **No abbreviation**: `ai_governance/` not `ai_gov/` (except in code/script filenames where brevity matters).

### 3.2 File Names

- `<TOPIC>_<ASPECT>_<LANG>.md` format. Example: `OFFER_CTA_LIBRARY_AR.md`.
- **Aspect types:** `_OS` (operating system index), `_LIBRARY` (collection), `_PLAYBOOK` (procedures), `_POLICY` (rules), `_REPORT` (one-time analysis), `_STANDARD` (canonical).
- **Lang codes:** `_AR` (Arabic primary), `_EN` (English primary). Default = no suffix = Arabic.
- **No date in filename** — use git history.
- **No owner name in filename** — see `FILE_OWNERSHIP_MAP.md`.

### 3.3 Schema Names

- `<entity>.schema.json` (singular entity).
- Atomic (one entity per schema). No compound (e.g., `account_stakeholder` — split).

### 3.4 Data File Names

- `<entity_plural>.jsonl` (e.g., `accounts.jsonl`).
- One file per entity, append-only.
- Schema validation in `data_governance/schema_registry.jsonl`.

---

## 4) Where to Put Cross-References

| Reference type | Format | Where in file |
|----------------|--------|---------------|
| **Sibling doc** (same system) | `[NAME](NAME.md)` | Inline at first mention |
| **Parent doc** (system index) | `[OS_NAME](OS_NAME_AR.md)` | Top of file, after title |
| **Cross-system** | `[OS_NAME](../../<system>/OS_AR.md)` | "See also" section at bottom |
| **Schema** | `[schema.json](../../../schemas/<name>.schema.json)` | Inline when entity is referenced |
| **Data file** | `[data.jsonl](../../../data/<system>/<name>.jsonl)` | Inline when rows are referenced |
| **Report** | `[REPORT.md](../../reports/<system>/REPORT.md)` | "References" section at bottom |

> **Default location for "See also" section:** last section before "Open Questions for Founder".

---

## 5) Who Has Authority to Merge

| Scope | Authority | Approval |
|-------|-----------|----------|
| **Within a single system** (e.g., 2 docs in `docs/enterprise_sales/`) | System owner (sales_lead) | 1 sign-off |
| **Across 2 systems** | Both system owners | 2 sign-offs |
| **Cross-cutting** (touching index, founder guides, ownership) | founder | 1 sign-off (founder's) |
| **Touching legacy** | founder + legacy doc owner | 2 sign-offs |
| **Deleting any file** | founder only | explicit PR title: `DELETE: <path>` |

> **No silent deletes. No silent renames. No silent schema breaks.**

---

## 6) Conflict Resolution Process

1. **Detect:** automated check (`scripts/check_duplicates.py` — to be built) or human report.
2. **Tag:** open issue with `conflict-resolution` label.
3. **Triage:** founder + relevant owners (15 min, sync).
4. **Decide:** LINK / MERGE / KEEP-BOTH.
5. **PR:** one PR with banner, cross-references, and (if merge) move-to-archive.
6. **Verify:** 1 week after, check no broken cross-references.

---

## 7) Forbidden Patterns

- 🚫 **Same concept, 2+ files, no cross-reference** → file issue.
- 🚫 **Renaming legacy file** without deprecation notice + redirect → revert.
- 🚫 **Date-stamped filename** (e.g., `plan_v2.md`) → use git.
- 🚫 **Owner name in filename** (e.g., `ahmed_sales_notes.md`) → use `docs/memory/`.
- 🚫 **Schema with 2+ entities** → split.
- 🚫 **Data file mixing concerns** (e.g., `accounts_and_stakeholders.jsonl`) → split.
- 🚫 **Inconsistency: Arabic file mostly English or vice versa** → fix in PR.
- 🚫 **Missing "Open Questions for Founder"** at end of any .md → CI check.

---

## 8) Allowed Patterns

- ✅ **Cross-reference** at top or bottom of new doc to similar existing doc.
- ✅ **Banner** in old doc: "Superseded by [new] — kept for legacy reference."
- ✅ **"See also" section** in OS index files linking to specific sub-docs.
- ✅ **"Last updated YYYY-MM-DD"** at top of every .md.
- ✅ **"Open Questions for Founder"** at bottom of every .md.
- ✅ **Append-only data files** (no in-place edits; add a row, never delete).

---

## 9) Open Questions for Founder

1. هل تريد **CI check** (GitHub Action) يفرض هذه القواعد تلقائياً على كل PR، أم manual review؟
2. من يُقرّر **DEPRECATION** (banner "superseded by") — system owner أم founder؟
3. هل توافق على **"no silent deletes"** كقاعدة صارمة، أم exceptions لحالات نادرة (مثل PII leak)؟
