# Dealix Release Notes v1.0.0

**Release Date:** June 22, 2026  
**Status:** Production Ready

## Overview

Dealix v1.0.0 is the first production-ready release of the AI Operating Systems platform for Saudi B2B companies. This release provides a complete, deployable platform for managing revenue operations, decision-making, client communication, and compliance.

## Core Systems

### Revenue Command Room OS
- Daily pipeline management dashboard
- Draft message approval workflow
- WhatsApp conversation tracking
- Booking flow for inbound leads
- Revenue scoring and prioritization

### Company Brain OS
- Signal capture and management
- Decision logging with context
- Risk register tracking
- Opportunity pipeline
- Assumption documentation

### WhatsApp Follow-up OS
- WhatsApp Cloud API integration
- Template management
- Conversation tracking
- **Draft-only mode by default** (safety-first design)
- Webhook support for status updates

### Client Delivery OS
- 6-phase delivery lifecycle templates
- Intake → Diagnosis → Blueprint → Sprint → Training → Proof Pack
- Standardized delivery process
- Client handoff documentation

### AI Trust & Compliance OS
- PDPL (Saudi Personal Data Protection Law) compliance checklist
- SDAIA AI Ethics alignment
- Human approval gates for all outbound communication
- Audit-friendly event logging

## Key Features

### Safety-First Architecture
- **Draft-only mode**: No outbound messages sent without human approval
- **Approval workflows**: All sensitive actions require review
- **Safety gates**: Automated checks before deployment
- **Compliance documentation**: Clear guidelines for PDPL and SDAIA

### Developer Experience
- **Code-splitting**: Optimized bundle sizes (main bundle 103KB)
- **Type-safe**: Full TypeScript coverage
- **Hot reload**: Fast development feedback loop
- **Comprehensive scripts**: 20+ operational commands

### Operational Excellence
- **Production checks**: Automated readiness verification
- **Health monitoring**: Built-in health endpoints
- **Structured logging**: Clear, actionable logs
- **Error handling**: Graceful degradation

## Technical Stack

### Frontend
- React 19 with TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- shadcn/ui components
- Radix UI primitives

### Backend
- Hono framework
- tRPC for type-safe APIs
- Drizzle ORM
- MySQL 8.0 (PlanetScale compatible)

### Infrastructure
- Docker + Docker Compose
- Node.js 20+
- Python 3.11+ (for operational scripts)

## Deployment Options

### Docker Compose (Recommended)
```bash
docker compose up -d
```

### Manual Deployment
```bash
npm install
npm run build
npm run db:push
node dist/boot.js
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete guide.

## Configuration

Required environment variables:
- `DATABASE_URL`: MySQL connection string
- `APP_ID`: Application identifier
- `APP_SECRET`: Application secret

Optional (for WhatsApp features):
- `WHATSAPP_ACCESS_TOKEN`
- `WHATSAPP_PHONE_NUMBER_ID`
- `WHATSAPP_WEBHOOK_VERIFY_TOKEN`

See [docs/ops/ENVIRONMENT_VARIABLES.md](docs/ops/ENVIRONMENT_VARIABLES.md) for complete reference.

## Performance

### Bundle Sizes
- Main application: 103KB (gzipped: 20KB)
- Vendor React: 220KB (gzipped: 70KB)
- Vendor UI: 41KB (gzipped: 14KB)
- Vendor Misc: 176KB (gzipped: 55KB)
- CSS: 33KB (gzipped: 6KB)

### Build Time
- Development: ~2 seconds
- Production: ~4 seconds

### Startup Time
- Cold start: ~2 seconds
- Warm start: ~500ms

## Known Limitations

1. **WhatsApp dry-run only**: Live sending requires manual approval workflow
2. **No email integration**: Email sending is not yet implemented
3. **Single-tenant**: Multi-tenancy not yet supported
4. **No SSO**: Single Sign-On not yet implemented

## Migration Guide

### From v0.x to v1.0.0

This is the first production release. For existing development installations:

1. Pull latest code:
   ```bash
   git pull origin main
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Update environment variables:
   - Review new safety flags in `.env`
   - Ensure `DATABASE_URL` is correct

4. Push schema updates:
   ```bash
   npm run db:push
   ```

5. Rebuild:
   ```bash
   npm run build
   ```

6. Verify:
   ```bash
   npm run production-check
   ```

## Security

### Safety Defaults
All outbound communication is disabled by default:
- `EXTERNAL_SEND_ENABLED=false`
- `EMAIL_SEND_ENABLED=false`
- `WHATSAPP_SEND_ENABLED=false`
- `WHATSAPP_ALLOW_LIVE_SEND=false`
- `OUTBOUND_MODE=draft_only`

### Compliance
- PDPL checklist available in [docs/compliance/PDPL_CHECKLIST.md](docs/compliance/PDPL_CHECKLIST.md)
- SDAIA AI Ethics alignment in [docs/compliance/SDAIA_AI_COMPLIANCE.md](docs/compliance/SDAIA_AI_COMPLIANCE.md)

## Support

### Documentation
- [README.md](README.md) - Setup and usage
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
- [docs/ops/GO_LIVE_CHECKLIST.md](docs/ops/GO_LIVE_CHECKLIST.md) - Pre-launch checklist

### Scripts
- `npm run production-check` - Verify deployment readiness
- `npm run outbound-dry` - Verify safety gates
- `npm run company-day` - Daily operational workflow
- `npm run command-room` - Generate command room report

## What's Next

### Planned for v1.1.0
- Email integration (draft + send)
- Multi-tenant support
- SSO integration
- Advanced reporting dashboard
- Mobile app companion

### Roadmap
- Q3 2026: Email integration + advanced analytics
- Q4 2026: Multi-tenant + SSO
- Q1 2027: Mobile app + API marketplace

## Contributors

- Dealix Team

## License

Proprietary - See LICENSE file for details.

---

**Release Status:** ✅ Production Ready  
**Safety Gates:** ✅ PASS  
**Compliance:** ✅ Reviewed  
**Documentation:** ✅ Complete
