# Dealix Deployment Guide

Complete guide to deploying Dealix in production.

## Quick Deployment (Docker Compose)

### Prerequisites
- Docker 24+
- Docker Compose 2+
- At least 2GB RAM
- Domain name (optional, for production)

### Step 1: Clone and Configure

```bash
git clone https://github.com/your-org/dealix.git
cd dealix
```

### Step 2: Environment Setup

Create `.env` file in the project root:

```env
# Database
DB_ROOT_PASSWORD=your_secure_root_password
DB_NAME=dealix
DB_USER=dealix
DB_PASSWORD=your_secure_db_password
DATABASE_URL=mysql://dealix:your_secure_db_password@mysql:3306/dealix

# Application
NODE_ENV=production
APP_PORT=3000

# Authentication (required)
APP_ID=your_app_id
APP_SECRET=your_app_secret

# WhatsApp Business API (optional, for WhatsApp features)
WHATSAPP_ACCESS_TOKEN=your_whatsapp_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_webhook_verify_token

# Safety Settings (DO NOT CHANGE unless you understand the implications)
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
WHATSAPP_AGENT_MODE=dry_run
```

**Important:** Replace all placeholder values with actual secrets. Never commit `.env` to git.

### Step 3: Deploy

```bash
# Start all services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f app

# Verify health
curl http://localhost:3000/
```

### Step 4: Initialize Database

```bash
# Push schema to database
docker compose exec app npm run db:push

# Verify tables created
docker compose exec app npm run db:check
```

### Step 5: Production Verification

```bash
# Run all checks
docker compose exec app npm run check
docker compose exec app npm run production-check
docker compose exec app npm run outbound-dry
```

Expected output:
- `LAUNCH DECISION: GO`
- `GATE RESULT: PASS`

## Manual Deployment (Without Docker)

### Prerequisites
- Node.js 20+
- Python 3.11+
- MySQL 8.0+
- Git

### Step 1: Install Dependencies

```bash
git clone https://github.com/your-org/dealix.git
cd dealix
npm install
```

### Step 2: Configure Environment

Create `.env` file:

```env
DATABASE_URL=mysql://dealix:your_password@localhost:3306/dealix
NODE_ENV=production
PORT=3000
APP_ID=your_app_id
APP_SECRET=your_app_secret
```

### Step 3: Build

```bash
npm run build
```

### Step 4: Initialize Database

```bash
npm run db:push
```

### Step 5: Start Application

```bash
# Using PM2 (recommended for production)
npm install -g pm2
pm2 start dist/boot.js --name dealix
pm2 save
pm2 startup

# Or using systemd (Linux)
# Create /etc/systemd/system/dealix.service
```

### Step 6: Verify

```bash
npm run production-check
curl http://localhost:3000/
```

## Production Checklist

### Security
- [ ] `.env` file has strong, unique passwords
- [ ] `.env` is not committed to git
- [ ] HTTPS is configured (if using reverse proxy)
- [ ] Firewall rules restrict access to necessary ports
- [ ] MySQL is not exposed to public internet

### Database
- [ ] MySQL is running and accessible
- [ ] Database schema is pushed (`npm run db:push`)
- [ ] Database backups are configured (daily recommended)
- [ ] Connection pooling is enabled

### Application
- [ ] `NODE_ENV=production`
- [ ] All safety flags are set to `false` or `draft_only`
- [ ] Health check endpoint responds (`/health`)
- [ ] Logs are being captured and rotated

### WhatsApp (if enabled)
- [ ] WhatsApp Business API credentials are valid
- [ ] Webhook URL is accessible from Meta servers
- [ ] `WHATSAPP_ALLOW_LIVE_SEND=false` until manually approved
- [ ] Draft approval workflow is documented

### Monitoring
- [ ] Application logs are being monitored
- [ ] Error tracking is configured (e.g., Sentry)
- [ ] Uptime monitoring is set up
- [ ] Alert notifications are configured

## Environment Variables Reference

See [`docs/ops/ENVIRONMENT_VARIABLES.md`](docs/ops/ENVIRONMENT_VARIABLES.md) for complete reference.

## Troubleshooting

### Database Connection Failed

```bash
# Check if MySQL is running
docker compose ps mysql

# Check MySQL logs
docker compose logs mysql

# Verify DATABASE_URL format
# Should be: mysql://user:password@host:port/database
```

### Application Won't Start

```bash
# Check application logs
docker compose logs app

# Verify environment variables
docker compose exec app env | grep -E "DATABASE_URL|APP_ID|APP_SECRET"

# Run typecheck
docker compose exec app npm run check
```

### Safety Gate Fails

```bash
# Check outbound configuration
docker compose exec app npm run outbound-dry

# Verify .env safety flags
docker compose exec app cat .env | grep -E "SEND_ENABLED|ALLOW_LIVE|OUTBOUND_MODE"
```

## Scaling

### Horizontal Scaling

For multiple app instances:
- Use a load balancer (nginx, Traefik)
- Ensure all instances share the same database
- Configure session storage (Redis recommended)

### Vertical Scaling

Increase resources:
- Database: More CPU/RAM for MySQL
- Application: More CPU/RAM for Node.js
- Use Docker resource limits in `docker-compose.yml`

## Backup and Recovery

### Database Backup

```bash
# Automated daily backup (cron job)
docker compose exec mysql mysqldump -u dealix -p dealix > backup_$(date +%Y%m%d).sql

# Restore from backup
docker compose exec -T mysql mysql -u dealix -p dealix < backup_20260622.sql
```

### Application State

- All state is in the database
- No application state to backup
- Configuration is in `.env` (backup securely)

## Support

For issues and questions:
- Check [`docs/ops/GO_LIVE_CHECKLIST.md`](docs/ops/GO_LIVE_CHECKLIST.md)
- Review [`README.md`](README.md) for setup instructions
- See compliance docs in [`docs/compliance/`](docs/compliance/)

## License

Proprietary - See LICENSE file for details.
