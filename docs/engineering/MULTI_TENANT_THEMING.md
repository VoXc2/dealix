# Multi-Tenant Theming Engineering Notes (W3.8)

> **Scope:** how white-label / agency-reseller theming is structured in Dealix.
> **Activates:** R6 (Agency White-Label) — customer #10 milestone.
> **Files:** `landing/assets/css/theme.css` (W3.2), tenant config (TBD), this doc.

---

## Goals (in order of priority)

1. **Tenants can re-skin Dealix surfaces** with their own logo, color palette, and tenant name
2. **Falling back to Dealix defaults** is automatic — partial overrides work
3. **No client-side JS** required for theming (server-side render only)
4. **Compatible with PDPL** — tenant data isolation is enforced regardless of theming
5. **Zero impact on existing tenants** — overrides are scoped, no global mutations

## The Approach: CSS Custom Properties + Tenant Inline Override

Dealix uses CSS variables defined in `landing/assets/css/theme.css`. Every UI surface reads from these variables. Tenants override the variables via a small inline `<style>` tag rendered server-side before the main stylesheet loads.

### Why CSS variables (vs. per-tenant compiled stylesheets)?

- **Cache-friendly:** one shared `theme.css` cached globally, only the tiny inline `<style>` is per-tenant.
- **Fast:** no build step per tenant. New tenant brand is config-only.
- **Resilient:** if tenant override is malformed, the CSS variable falls back to its declared default.
- **Audit-friendly:** the override is visible in page source (no opaque compiled CSS).

### Why server-side render (not client-side JS)?

- **PDPL:** zero PII in client-side JS context (the tenant name is non-PII but the principle stands)
- **Performance:** no FOUC (flash of unstyled content)
- **Bots/SEO:** crawlers see the tenant brand
- **Email rendering:** same theming approach works in email templates

## Tenant Config Schema

Stored in `tenants` table (TBD migration when R6 activates):

```python
class TenantTheme(Base):
    __tablename__ = "tenant_themes"

    tenant_handle: Mapped[str] = mapped_column(primary_key=True)
    brand_primary: Mapped[str] = mapped_column(default="#0f172a")      # CSS color
    brand_accent: Mapped[str] = mapped_column(default="#10b981")
    brand_muted: Mapped[str] = mapped_column(default="#64748b")
    brand_surface: Mapped[str] = mapped_column(default="#ffffff")
    brand_bg: Mapped[str] = mapped_column(default="#f8fafc")
    font_arabic: Mapped[str] = mapped_column(default="IBM Plex Sans Arabic")
    font_english: Mapped[str] = mapped_column(default="Inter")
    logo_url: Mapped[str | None] = mapped_column(default=None)
    favicon_url: Mapped[str | None] = mapped_column(default=None)
    display_name: Mapped[str] = mapped_column(default="Dealix")
    custom_domain: Mapped[str | None] = mapped_column(default=None)  # e.g. ai.partner.com
    created_at: Mapped[datetime] = mapped_column(...)
    updated_at: Mapped[datetime] = mapped_column(...)
```

## Render-Time Wiring

In the FastAPI route handler that serves a tenant's landing surface:

```python
@router.get("/p/{tenant_handle}")
async def tenant_landing(tenant_handle: str, request: Request) -> Response:
    theme = await load_tenant_theme(tenant_handle)
    return templates.TemplateResponse(
        "tenant_landing.html.j2",
        {
            "request": request,
            "theme": theme,
            "tenant_name": theme.display_name,
            "logo_url": theme.logo_url or "",
        },
    )
```

In the Jinja2 template:

```html
<style>
  :root {
    --dealix-brand-primary: {{ theme.brand_primary }};
    --dealix-brand-accent:  {{ theme.brand_accent }};
    --dealix-brand-muted:   {{ theme.brand_muted }};
    --dealix-brand-surface: {{ theme.brand_surface }};
    --dealix-brand-bg:      {{ theme.brand_bg }};
    --dealix-tenant-name:   "{{ theme.display_name | e }}";
    --dealix-font-ar:       "{{ theme.font_arabic | e }}", system-ui, sans-serif;
    {% if theme.logo_url %}
    --dealix-tenant-logo-url: url("{{ theme.logo_url | e }}");
    {% endif %}
  }
</style>
<link rel="stylesheet" href="/assets/css/theme.css">
```

## Color Validation

Tenant-supplied colors go through `core.theming.validators`:

- Must be a valid CSS hex / rgb() / hsl() / oklch() value
- Hex must be 3, 4, 6, or 8 chars after `#`
- RGB tuple values 0–255
- Reject `url(...)`, `expression(...)`, `javascript:` (XSS prevention)
- WCAG AA contrast check between `brand_primary` and `text_on_brand` (warn, not block)
- Brand colors must NOT contain control chars or escape sequences

Validation rejection returns 400 with a clear error message. Saved theme is always lint-clean.

## Custom Domain Support

For agency partners that want `ai.partner.com` instead of `dealix.me/p/partner`:

- DNS: partner adds CNAME `ai.partner.com → tenants.dealix.me`
- Dealix: serves matching tenant theme based on Host header
- TLS: ACME wildcard cert on `*.tenants.dealix.me` + per-partner subdomain certs via Caddy

**Not built yet.** Defer until first agency partner asks. Until then, all partners served at `dealix.me/p/<handle>`.

## Security Considerations

- Tenant-supplied logo URLs are validated for HTTPS-only, valid scheme, no `data:` URIs (XSS)
- Tenant-supplied font family names are escaped via Jinja2's `| e` filter
- Tenant CSS values pass through a sanitizer before reaching the stylesheet inline
- No tenant can inject CSS that targets other tenants (CSS variables are scoped to the rendered page)

## Email Theming (TBD)

The same CSS variable approach works in email templates with inlining:

```html
<table style="background-color: {{ theme.brand_bg }};">
  <tr>
    <td style="background: {{ theme.brand_primary }}; color: white;">
      <h1>{{ theme.display_name }}</h1>
    </td>
  </tr>
</table>
```

Use Premailer (already in deps) to inline these at email send time.

## Out of Scope (this iteration)

- Per-tenant font file uploads (only Google Fonts approved list)
- Per-tenant component re-arrangement (e.g. "hide pricing section")
- Per-tenant locale beyond ar/en (i18n re-architecture if needed)
- Per-tenant full CSS injection (security risk + maintenance nightmare)

## Migration Path When R6 Activates

1. Apply migration to create `tenant_themes` table
2. Add `core/theming/` package with validators + loader
3. Add 2 tenant_landing.html.j2 templates (one for Arabic-default, one for English-default)
4. Add admin endpoint `POST /api/v1/admin/tenants/{handle}/theme` (founder-only key required)
5. Add Storybook-style preview page so partners see their theme before going live
6. Document partner onboarding workflow in `docs/ops/AGENCY_PARTNER_KIT.md`
