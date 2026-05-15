# Client OS — الوحدات

## 1. Capability Dashboard

قدرات: Revenue · Customer · Operations · Knowledge · Data · Governance · Reporting — كل واحدة مستوى **0–5** (Absent → Optimized OS).

## 2. Data Readiness Panel

مصادر · Source Passport · جودة · duplicates · حقول ناقصة · PII · allowed use.

## 3. Governance Panel

مخرجات مسموحة · draft-only · تتطلب موافقة · redactions · مخاطر محظورة · audit.

## 4. Workflow Panel

اسم · مالك · مدخلات · خطوة AI · موافقة · QA · proof metric · cadence.

## 5. Draft Pack

مسودات لا تُرسل تلقائيًا — بريد · LinkedIn draft-only · واتساب draft-only مع موافقة/علاقة · سكربت · خطة متابعة.

## 6. Proof Timeline

أحداث proof · value · مخاطر محظورة · قبل/بعد · قيمة مؤكدة من العميل · estimated vs verified.

## 7. Next Actions

Continue · Expand · Pause — رابط مباشر بـ Retainer / Upsell.

**الكود:** `CAPABILITY_DOMAINS` · `capability_level_valid` — `client_os/capability_dashboard.py` · `DATA_READINESS_PANEL_SIGNALS` — `client_os/data_readiness_panel.py` · `GOVERNANCE_PANEL_SIGNALS` · `TRUST_OUTPUT_STRIP_SIGNALS` — `client_os/governance_panel.py` · `PROOF_TIMELINE_SIGNALS` — `client_os/proof_timeline.py` · `CLIENT_OS_USAGE_SIGNALS` — `client_os/workspace.py` · `MONTHLY_VALUE_REPORT_SECTIONS` — `client_os/monthly_value_report.py` · `client_expansion_recommendation` — `client_os/expansion_engine.py`

**صعود:** [`CLIENT_OPERATING_SYSTEM.md`](CLIENT_OPERATING_SYSTEM.md)
