# Dealix — AI Operating Systems for Saudi B2B Companies

**Arabic:** Dealix نبني أنظمة تشغيل (Operating Systems) مدعومة بالذكاء الاصطناعي لتشغيل الإيرادات والمتابعة والقرارات والحوكمة للشركات السعودية B2B.

---

## Problem
> 80% من القرارات التجارية اليومية لديها بيانات، لكن لا توجد لها workflows واضحة لتحويلها إلى نتائج موثقة.

## Solution
**Dealix = Operating Systems, not tools.**

| # | System | Duration | Price (SAR) |
|---|--------|----------|-------------|
| 1 | Revenue Command Room OS | 5 days | 5,000 |
| 2 | Company Brain OS | 7 days | 7,500 |
| 3 | Client Delivery OS | 10 days | 10,000 |
| 4 | AI Trust & Compliance OS | 7 days | 12,500 |
| 5 | WhatsApp / Inbox Follow-up OS | 5 days | 15,000 |

**Full Investment:** 50,000 SAR (35% discount)

---

## Getting Started

### Prerequisites
- Docker + Docker Compose
- Node.js 20+
- Python 3.11+
- MySQL 8.0

### Install
```bash
git clone https://github.com/Dealix-sa/dealix.git
cd dealix
cp .env.example .env
npm install
```

### Run
```bash
# Start MySQL + Redis
npm run services:up

# Run development
npm run dev

# Generate company-day report
npm run company-day

# Run safety checks
npm run production-check
```

---

## Project Structure

```
dealix/
├── api/                    # Hono + tRPC routers
│   ├── auth-router.ts
│   ├── brain-router.ts
│   ├── booking-router.ts
│   ├── command-room-router.ts
│   ├── deal-router.ts
│   ├── prospect-router.ts
│   └── activity-router.ts
├── src/                    # React + Vite + TailwindCSS
│   ├── pages/
│   │   ├── BrainOS.tsx
│   │   ├── CommandRoom.tsx
│   │   ├── Booking.tsx
│   │   └── Dashboard.tsx
│   └── sections/
│       └── Hero.tsx
├── db/
│   ├── schema.ts            # MySQL + Drizzle ORM
│   └── seed.ts
├── scripts/
│   ├── revenue_engine.py
│   ├── outreach_engine.py
│   ├── client_delivery.py
│   ├── verify_no_auto_external_send.py
│   └── verify_company_launch_ready.py
├── docs/
│   ├── brand/               # Brand OS, Voice, Positioning
│   ├── company/             # Company OS
│   └── compliance/          # SDAIA AI, PDPL
├── business/
│   └── products/            # Product specs
├── sales/
│   ├── ONE_PAGE_OFFER_AR.md
│   ├── DISCOVERY_SCRIPT_AR.md
│   ├── OBJECTION_HANDLING_AR.md
│   └── FOLLOW_UP_SEQUENCE_AR.md
├── clients/
│   └── _template/           # Client Delivery template
└── company_os/
    ├── command_room/
    ├── war_room/
    ├── ledgers/
    └── reports/
```

---

## Safety

Every AI-generated message is tagged with **[AI]** and requires manual Founder approval before sending.

| Gate | Command |
|------|---------|
| No auto-send | `OUTBOUND_MODE=draft_only` |
| Launch check | `npm run production-check` |
| Safety gate | `python scripts/verify_no_auto_external_send.py` |

---

## License
Proprietary — Dealix-sa

*Built for Saudi Arabia with governance first.*
