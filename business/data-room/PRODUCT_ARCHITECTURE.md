# Product Architecture (Dealix)

## الطبقات
1. **Data Sources** — CSV, manual research, open data, official APIs
2. **Adapters** — normalize to internal schema
3. **CRM** — accounts, drafts, proposals, deals, proof
4. **Outreach** — drafts + review queue (no auto-send)
5. **Delivery** — workflow + proof + retention
6. **Reporting** — daily CEO brief, weekly review, monthly review

## المكوّنات الرئيسية
- `apps/web` — Next.js 15 (17+ premium pages)
- `apps/web/lib/company-os` — Company OS backbone
- `apps/web/lib/sales-machine` — Ultimate Sales OS
- `apps/web/lib/sales-automation` — Lead sources
- `apps/web/lib/generated` — Static dashboards
- `business/_data/*.json` — Demo data layer
- `business/**/*.md` — Operating docs
- `scripts/*.py` — Daily operators
- `connectors/*.py` — Plan only for V1
