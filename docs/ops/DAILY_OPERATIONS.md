# Dealix Daily Operations Guide

This guide defines the daily, weekly, and monthly operating procedures for running Dealix effectively.

---

## Daily Operations (15 minutes)

### Morning Command Room Review

**When**: First thing in the morning
**Duration**: 10-15 minutes
**Owner**: Founder / Daily Operator

#### Checklist:

1. **Open Command Room**
   ```bash
   npm run command-room
   ```
   Or navigate to `/command-room` in your browser

2. **Review Pipeline Changes**
   - Check new deals added overnight
   - Review stage transitions
   - Note any deals that need attention

3. **Process Draft Queue**
   - Review AI-generated message drafts
   - For each draft:
     - **Approve**: Message meets quality standards
     - **Edit**: Message needs adjustments
     - **Reject**: Message doesn't fit context
   - Priority: Handle urgent follow-ups first

4. **Check WhatsApp Conversations**
   - Review new conversations
   - Check for unread messages
   - Note conversations needing follow-up
   - Verify no messages sent without approval

5. **Log New Signals**
   - If you noticed market changes, log them in Brain OS
   - If you identified risks, add to risk register
   - If you see opportunities, capture them

#### Quick Actions:
- `npm run company-day` - Run full daily check
- `npm run outbound-dry` - Verify safety gates

---

## Weekly Operations (30 minutes)

### Brain OS Review

**When**: Monday morning or Friday afternoon
**Duration**: 20-30 minutes
**Owner**: Founder / Strategic Lead

#### Checklist:

1. **Review Signals**
   - Open Brain OS → Signals tab
   - Review signals from past week
   - Identify patterns or trends
   - Archive outdated signals

2. **Update Decisions**
   - Open Brain OS → Decisions tab
   - Update status of open decisions
   - Document outcomes of implemented decisions
   - Log new decisions made this week

3. **Assess Risks**
   - Open Brain OS → Risks tab
   - Review current risk register
   - Update risk severity if needed
   - Add new risks identified
   - Archive mitigated risks

4. **Capture Opportunities**
   - Open Brain OS → Opportunities tab
   - Review current opportunities
   - Update potential scores
   - Add new opportunities identified
   - Archive missed/expired opportunities

5. **Update Action Ownership**
   - Review action items from decisions
   - Ensure each action has an owner
   - Check if actions are on track
   - Reassign if needed

#### Governance Check:
```bash
npm run governance-check
```

---

## Monthly Operations (1 hour)

### Comprehensive Review

**When**: First Monday of each month
**Duration**: 45-60 minutes
**Owner**: Founder + Leadership Team

#### Checklist:

1. **Revenue Scorecard Review**
   ```bash
   npm run revenue-scorecard
   ```
   - Review conversion rates
   - Analyze pipeline velocity
   - Identify top-performing stages
   - Note bottlenecks

2. **Compliance Audit**
   ```bash
   npm run compliance-check
   ```
   - Review PDPL checklist
   - Verify SDAIA alignment
   - Check data retention policies
   - Audit approval logs

3. **Client Delivery Progress**
   ```bash
   npm run client-day
   ```
   - Review active client engagements
   - Check delivery milestones
   - Identify at-risk projects
   - Plan resource allocation

4. **System Optimization**
   - Review platform usage metrics
   - Identify underutilized features
   - Plan training for team
   - Configure new automations

5. **Strategic Planning**
   - Review monthly outcomes
   - Set goals for next month
   - Adjust strategy if needed
   - Plan major initiatives

---

## Safety Operations

### Daily Safety Check

**When**: Before any major changes
**Duration**: 2 minutes

```bash
npm run outbound-dry
```

**Expected Output**:
```
GATE RESULT: PASS
OUTBOUND_MODE: draft_only
```

**If FAIL**:
1. Stop all operations
2. Check `.env` file
3. Verify `OUTBOUND_MODE=draft_only`
4. Verify `WHATSAPP_ALLOW_LIVE_SEND=false`
5. Contact support if issue persists

### Weekly Safety Review

**When**: Part of weekly operations
**Duration**: 5 minutes

1. Review audit logs for unusual activity
2. Check approval history
3. Verify no unauthorized changes
4. Review WhatsApp message history

---

## Backup Operations

### Daily Backup (Automated)

**Setup** (one-time):
```bash
# Linux/Mac cron job
0 2 * * * cd /path/to/dealix && python scripts/backup_database.py --compress --keep-days 30

# Windows Task Scheduler
# Create daily task at 2:00 AM
# Action: python scripts/backup_database.py --compress --keep-days 30
```

**Manual Backup**:
```bash
python scripts/backup_database.py --compress --keep-days 30
```

**Verify Backup**:
- Check `backups/` directory for new file
- Verify file size > 0
- Test restore on staging environment monthly

---

## Monitoring Operations

### Health Checks

**Automated Monitoring** (recommended setup):
```bash
# Every 5 minutes (cron job)
*/5 * * * * curl -f http://localhost:3000/health || echo "ALERT: Dealix health check failed"
```

**Manual Health Check**:
```bash
# Check application health
curl http://localhost:3000/health

# Expected output:
# {"status":"healthy","timestamp":"...","version":"1.0.0",...}

# Check readiness (includes DB check)
curl http://localhost:3000/ready

# Expected output:
# {"status":"ready","checks":{"database":"connected",...}}
```

### Log Review

**Daily** (2 minutes):
```bash
# Docker deployment
docker compose logs --tail=50 dealix

# PM2 deployment
pm2 logs dealix --lines 50
```

**Weekly** (10 minutes):
- Review error patterns
- Identify recurring issues
- Check for security alerts
- Note performance bottlenecks

---

## Team Operations

### Onboarding New Team Members

**When**: New team member joins
**Duration**: 30 minutes
**Owner**: Admin / Team Lead

#### Checklist:

1. **Create Account**
   - Go to Settings → Team Management
   - Click "Add Team Member"
   - Enter email and assign role
   - Send invitation

2. **Initial Training**
   - Walk through Command Room
   - Explain draft approval process
   - Review Brain OS usage
   - Show reporting features

3. **Access Configuration**
   - Set appropriate permissions
   - Configure notification preferences
   - Set up WhatsApp access (if needed)

4. **First Week Check-in**
   - Review their activity
   - Answer questions
   - Provide additional training if needed

### Role Management

**Available Roles**:
- **Admin**: Full access to all features
- **Operator**: Can approve drafts, view all data
- **Reviewer**: Can view and comment, cannot approve
- **Viewer**: Read-only access

**Change Role**:
1. Settings → Team Management
2. Click on team member
3. Select new role from dropdown
4. Save changes

---

## Reporting Operations

### Generate Reports

**Daily Report**:
```bash
npm run command-room
```
Generates daily operating snapshot.

**Weekly Report**:
```bash
npm run brain-day
```
Generates weekly governance and strategy report.

**Monthly Report**:
```bash
npm run revenue-scorecard
```
Generates comprehensive revenue analysis.

**Full Day Report**:
```bash
npm run full-revenue-day
```
Generates complete operational report.

### Report Distribution

**Automated Distribution** (recommended):
- Configure email distribution in Settings → Reports
- Set schedule (daily/weekly/monthly)
- Add recipients
- Choose report format (PDF/CSV/JSON)

**Manual Distribution**:
1. Generate report
2. Download from Dashboard → Reports
3. Share via email or messaging

---

## Incident Response

### Severity Levels

**Critical** (Response: 1 hour):
- System down
- Data breach suspected
- All outbound messages failing
- Database corruption

**High** (Response: 4 hours):
- Major feature broken
- Performance severely degraded
- Security vulnerability discovered
- Backup failed

**Medium** (Response: 24 hours):
- Minor feature broken
- Performance slightly degraded
- Non-critical integration failing
- Report generation issues

**Low** (Response: 48 hours):
- Cosmetic issues
- Feature requests
- Documentation updates
- Minor bugs

### Incident Response Procedure

1. **Identify**
   - Detect issue (monitoring alert or user report)
   - Assess severity level
   - Document symptoms

2. **Contain**
   - If critical: Stop all operations
   - If data breach: Isolate affected systems
   - If outbound failing: Switch to draft-only mode

3. **Investigate**
   - Check logs
   - Review recent changes
   - Identify root cause

4. **Resolve**
   - Implement fix
   - Test resolution
   - Verify no side effects

5. **Communicate**
   - Notify affected users
   - Provide status updates
   - Share resolution details

6. **Review**
   - Conduct post-incident review
   - Document lessons learned
   - Update procedures if needed

### Emergency Contacts

- **Technical Support**: support@dealix.sa
- **WhatsApp**: +966 XX XXX XXXX (24/7 for critical issues)
- **Phone**: +966 XX XXX XXXX (9 AM - 5 PM AST)

---

## Continuous Improvement

### Feedback Collection

**Weekly**:
- Collect team feedback
- Review user suggestions
- Identify pain points

**Monthly**:
- Analyze feedback trends
- Prioritize improvements
- Plan enhancements

**Quarterly**:
- Review platform performance
- Assess ROI
- Plan strategic improvements

### Feature Requests

**Submit Request**:
1. Dashboard → Help → Feature Request
2. Describe feature and use case
3. Explain business value
4. Submit for review

**Track Request**:
- Check status in Dashboard → Settings → Feature Requests
- Vote on community requests
- Comment on proposed features

---

## Compliance Checklist

### Daily
- [ ] Verify draft-only mode active
- [ ] Review approval logs
- [ ] Check for unauthorized access attempts

### Weekly
- [ ] Review PDPL compliance status
- [ ] Audit data retention
- [ ] Verify backup integrity

### Monthly
- [ ] Full compliance audit
- [ ] Review SDAIA alignment
- [ ] Update compliance documentation
- [ ] Conduct security review

---

## Quick Reference

### Common Commands
```bash
npm run company-day          # Daily operations
npm run command-room         # Generate command room report
npm run brain-day            # Weekly governance review
npm run revenue-scorecard    # Monthly revenue analysis
npm run outbound-dry         # Safety verification
npm run production-check     # Full system check
```

### Key URLs
- **Dashboard**: `https://yourcompany.dealix.sa/`
- **Command Room**: `https://yourcompany.dealix.sa/command-room`
- **Brain OS**: `https://yourcompany.dealix.sa/brain`
- **Health Check**: `https://yourcompany.dealix.sa/health`
- **Documentation**: `https://docs.dealix.sa`

### Key Files
- **Configuration**: `.env`
- **Backups**: `backups/`
- **Reports**: `company_os/reports/`
- **Logs**: `logs/` (or Docker logs)

---

## Support

### Getting Help
- **Documentation**: [docs.dealix.sa](https://docs.dealix.sa)
- **FAQ**: See `docs/SUPPORT_FAQ.md`
- **Email**: support@dealix.sa
- **Community**: [community.dealix.sa](https://community.dealix.sa)

### Escalation Path
1. Check documentation
2. Review FAQ
3. Contact support via email
4. Emergency: Call/WhatsApp support line

---

**Remember**: Dealix is designed to be your daily operating system. Use it consistently, review regularly, and it will help you make better decisions, follow up reliably, and grow your revenue predictably.

**Last Updated**: 2026-06-22
**Version**: 1.0.0
