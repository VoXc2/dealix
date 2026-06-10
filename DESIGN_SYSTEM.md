# 🔷 Dealix Design System

**Version**: 1.0 · **Status**: ✅ Production Ready · **Updated**: May 2026

> Brand: Navy `#001F3F` + Gold `#D4AF37` — Built for Saudi B2B

---

## Quick Reference

### Colors
```
dealix-navy    #001F3F  — Primary background, headers
dealix-gold    #D4AF37  — Accents, CTAs, active states  
dealix-emerald #10B981  — Success
dealix-coral   #EF4444  — Error
dealix-amber   #F59E0B  — Warning
dealix-ocean   #0066FF  — Info, links
```

### Tailwind Classes
```tsx
bg-dealix-navy    text-dealix-gold    border-dealix-gold
shadow-gold       shadow-navy
hover-gold        gradient-text       glass
dot-pattern       navy-surface
animate-gold-pulse animate-fade-up
font-display      font-body           font-mono
```

---

## File Map

| File | Purpose |
|------|---------|
| `apps/company-os-vite/src/index.css` | CSS variables + Tailwind base |
| `apps/company-os-vite/tailwind.config.js` | `dealix.*` color palette |
| `design-systems/dealix/tokens/*.json` | Design tokens (JSON) |
| `design-systems/dealix/brand/BRAND_GUIDELINES.md` | Visual identity rules |
| `design-systems/dealix/styles/dealix-styles.css` | Standalone CSS (no Tailwind) |

---

## Pages Branded

| Page | Status |
|------|--------|
| `/` LandingPage | ✅ Full rebrand |
| `/dashboard` | ✅ Full rebrand |
| `/login` | ✅ Full rebrand |
| `/prospects` | ✅ Full rebrand |
| `/governance` | ✅ Full rebrand |
| `/finance` | ✅ Full rebrand |
| `404` NotFound | ✅ Full rebrand |
| AuthLayout Sidebar | ✅ Full rebrand |

---

## Usage Examples

```tsx
// Primary CTA button
<Button className="bg-dealix-gold text-dealix-navy hover:bg-yellow-400 font-bold shadow-gold">
  ابدأ الآن
</Button>

// Branded card
<Card className="bg-white/5 border-white/10 hover-gold shadow-none">
  <CardContent>...</CardContent>
</Card>

// Gold badge
<Badge className="bg-dealix-gold/20 text-dealix-gold border border-dealix-gold/30">
  Premium
</Badge>

// Gradient headline
<h1 className="font-black font-display">
  كُشف أين تضيع <span className="gradient-text">إيراداتك</span>
</h1>

// Glass navbar
<nav className="glass border-b border-white/10 sticky top-0 z-50">
```

---

## Contribution
See `design-systems/dealix/docs/CONTRIBUTING.md`

## CI/CD
See `.github/workflows/design-system.yml`
