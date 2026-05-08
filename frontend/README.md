# Dealix Frontend

Production-grade Next.js 15 dashboard for the Dealix AI RevOps platform, built for Saudi enterprise clients.

## Stack

- **Framework**: Next.js 15 App Router + TypeScript
- **Styling**: Tailwind CSS + shadcn/ui components
- **i18n**: next-intl (Arabic primary / English secondary)
- **Charts**: Recharts
- **Animations**: Framer Motion
- **Auth**: JWT via FastAPI backend
- **Real-time**: SSE-ready hook (`useSSE`)

## Design

- **Arabic-first**: RTL layout with `dir="rtl"`, Noto Sans Arabic font
- **Color palette**: Deep navy dark mode, Gold (#C9A96E) + Emerald green accents
- **Dark/Light mode**: via next-themes
- **Responsive**: Mobile-friendly

## Pages

| Route | Page |
|-------|------|
| `/ar/dashboard` | Executive Dashboard (KPIs, Revenue Chart, Pipeline) |
| `/ar/pipeline` | Lead Pipeline (Kanban Board) |
| `/ar/agents` | Agent Activity Feed (real-time) |
| `/ar/approvals` | Approval Center (approve/reject AI decisions) |
| `/ar/clients` | Client Management |
| `/ar/analytics` | Analytics & Reports |
| `/ar/settings` | Settings |
| `/ar/login` | Login |
| `/ar/register` | Register |

Replace `ar` with `en` for English versions.

## Getting Started

```bash
# Install dependencies
npm install

# Copy environment file
cp .env.local.example .env.local

# Edit .env.local - set NEXT_PUBLIC_API_URL to your FastAPI backend

# Start development server
npm run dev

# Type check
npm run typecheck

# Build for production
npm run build
```

## Environment Variables

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project Structure

```
src/
├── app/[locale]/      # Next.js App Router pages
├── components/
│   ├── ui/            # shadcn/ui base components
│   ├── layout/        # Sidebar, Header, AppLayout
│   ├── dashboard/     # KPI, Revenue, Pipeline charts
│   ├── pipeline/      # Kanban board
│   ├── agents/        # Activity feed
│   ├── approvals/     # Approval center
│   ├── clients/       # Client management
│   ├── analytics/     # Charts & reports
│   ├── settings/      # Settings tabs
│   └── shared/        # Login/Register forms
├── lib/
│   ├── api/           # Axios client + API modules
│   ├── hooks/         # useAuth, useSSE
│   └── utils.ts       # Helpers
├── i18n/              # next-intl config
├── types/             # TypeScript types
└── middleware.ts      # Locale routing
messages/
├── ar.json            # Arabic strings
└── en.json            # English strings
```
