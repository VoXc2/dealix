# Rollback Plan (Dealix)

## Frontend (Vercel)
1. Open Deployments
2. Find the last working deploy
3. Promote to production

## Backend (Railway)
1. Open Deployments
2. Click "..." on the previous deploy
3. Redeploy

## Database
- If migration is the cause: revert via Alembic
  `alembic downgrade -1`
- If data is the cause: restore from backup
  `python3 scripts/restore_business_data.py --from backup.zip`

## Communication
- Email clients if SLA was missed
- Update status page
- Post in founder channel
