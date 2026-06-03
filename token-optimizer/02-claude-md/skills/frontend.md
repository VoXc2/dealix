# Dealix — Frontend Context (On-Demand Skill)

## Stack
Next.js 14+ · TypeScript · Tailwind CSS · shadcn/ui · next-intl (AR/EN)

## Structure
```
frontend/
├── app/             # Next.js App Router
│   ├── [locale]/    # AR/EN localized routes
│   ├── layout.tsx   # root layout
│   └── page.tsx     # home
├── components/      # shared React components
│   ├── ui/          # shadcn/ui primitives
│   └── [feature]/   # feature-specific components
├── messages/        # i18n strings (ar.json, en.json)
├── lib/             # utilities and API client
└── public/          # static assets
```

## Conventions
- All text: bilingual via `next-intl` (`t('key')`)
- Arabic messages: `messages/ar.json`, English: `messages/en.json`
- RTL support: automatic via `[locale]` layout
- API calls: `lib/api.ts` client wrapper → `NEXT_PUBLIC_API_URL`
- Components: use shadcn/ui primitives first, extend only when necessary
- Currency: always display in SAR with `Intl.NumberFormat`

## Key Commands
```bash
cd frontend && npm run dev       # dev server (port 3000)
cd frontend && npm run build     # production build
cd frontend && npm run lint      # ESLint check
cd frontend && npm run type-check # TypeScript check
```

## Adding a Page
```typescript
// frontend/app/[locale]/new-page/page.tsx
import { useTranslations } from 'next-intl';

export default function NewPage() {
  const t = useTranslations('NewPage');
  return <div>{t('title')}</div>;
}
```

## Adding i18n Keys
```json
// messages/ar.json — add under relevant section
{ "NewPage": { "title": "الصفحة الجديدة" } }

// messages/en.json
{ "NewPage": { "title": "New Page" } }
```
