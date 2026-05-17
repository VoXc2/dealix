-- 013_affiliate_program.sql
-- Affiliate / Partner Commission Machine — raw SQL reference.
-- Alembic owns the live schema (db/migrations/versions/20260517_013_affiliate_program.py);
-- this file mirrors it for review and manual inspection.
--
-- External affiliates/partners earn CASH commissions on referred deals,
-- paid only after a recorded invoice_paid event, with a 30-day clawback
-- window. Distinct from the customer-referral program in 010.
--
-- Tables:
--   affiliate_partners          — external partners, score + tier
--   affiliate_partner_links     — APT- referral codes issued on approval
--   affiliate_referrals         — leads submitted by partners
--   affiliate_commissions       — cash commission, gated on invoice_paid
--   affiliate_payouts           — settled cash payouts
--   affiliate_approved_assets   — vetted partner-facing messaging
--   affiliate_compliance_events — disclosure / spam / abuse events

BEGIN;

CREATE TABLE IF NOT EXISTS affiliate_partners (
    partner_id          VARCHAR(64) PRIMARY KEY,
    display_name        VARCHAR(255) NOT NULL,
    email_hash          VARCHAR(32),
    partner_category    VARCHAR(32) NOT NULL DEFAULT 'other',
    audience_type       VARCHAR(64),
    region              VARCHAR(64),
    score               INTEGER NOT NULL DEFAULT 0,
    score_breakdown     JSONB NOT NULL DEFAULT '{}',
    tier                VARCHAR(16),
    status              VARCHAR(16) NOT NULL DEFAULT 'scored',
        -- scored | approved | rejected | suspended
    disclosure_accepted BOOLEAN NOT NULL DEFAULT FALSE,
    plan_text           TEXT,
    rejected_reason     VARCHAR(256),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    scored_at           TIMESTAMPTZ,
    approved_at         TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS ix_affiliate_partners_status
    ON affiliate_partners (status);

CREATE TABLE IF NOT EXISTS affiliate_partner_links (
    code        VARCHAR(32) PRIMARY KEY,
    partner_id  VARCHAR(64) NOT NULL REFERENCES affiliate_partners(partner_id),
    tier        VARCHAR(16) NOT NULL,
    is_revoked  BOOLEAN NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_affiliate_links_partner
    ON affiliate_partner_links (partner_id);

CREATE TABLE IF NOT EXISTS affiliate_referrals (
    affiliate_referral_id VARCHAR(64) PRIMARY KEY,
    code               VARCHAR(32) NOT NULL REFERENCES affiliate_partner_links(code),
    partner_id         VARCHAR(64) NOT NULL,
    lead_company       VARCHAR(255) NOT NULL,
    lead_email_hash    VARCHAR(32),
    status             VARCHAR(16) NOT NULL DEFAULT 'submitted',
        -- submitted | qualified | rejected | invoice_paid | commissioned | clawed_back
    qualified          BOOLEAN NOT NULL DEFAULT FALSE,
    disclosure_present BOOLEAN NOT NULL DEFAULT FALSE,
    decline_reason     VARCHAR(256),
    invoice_id         VARCHAR(64),
    deal_amount_sar    INTEGER NOT NULL DEFAULT 0,
    created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    qualified_at       TIMESTAMPTZ,
    invoice_paid_at    TIMESTAMPTZ,
    UNIQUE (code, lead_email_hash)
);

CREATE INDEX IF NOT EXISTS ix_affiliate_referrals_partner
    ON affiliate_referrals (partner_id);
CREATE INDEX IF NOT EXISTS ix_affiliate_referrals_status
    ON affiliate_referrals (status);

CREATE TABLE IF NOT EXISTS affiliate_commissions (
    commission_id         VARCHAR(64) PRIMARY KEY,
    affiliate_referral_id VARCHAR(64) NOT NULL UNIQUE
        REFERENCES affiliate_referrals(affiliate_referral_id),
    partner_id            VARCHAR(64) NOT NULL,
    tier                  VARCHAR(16) NOT NULL,
    pct                   INTEGER NOT NULL DEFAULT 0,
    base_amount_sar       INTEGER NOT NULL DEFAULT 0,
    commission_sar        INTEGER NOT NULL DEFAULT 0,
    status                VARCHAR(16) NOT NULL DEFAULT 'calculated',
        -- calculated | approved | paid | clawed_back
    clawback_deadline     TIMESTAMPTZ,
    clawback_reason       VARCHAR(256),
    calculated_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    approved_at           TIMESTAMPTZ,
    payout_id             VARCHAR(64)
);

CREATE INDEX IF NOT EXISTS ix_affiliate_commissions_partner
    ON affiliate_commissions (partner_id);
CREATE INDEX IF NOT EXISTS ix_affiliate_commissions_status
    ON affiliate_commissions (status);

CREATE TABLE IF NOT EXISTS affiliate_payouts (
    payout_id      VARCHAR(64) PRIMARY KEY,
    partner_id     VARCHAR(64) NOT NULL REFERENCES affiliate_partners(partner_id),
    commission_ids JSONB NOT NULL DEFAULT '[]',
    total_sar      INTEGER NOT NULL DEFAULT 0,
    method         VARCHAR(32),
    reference      VARCHAR(128),
    status         VARCHAR(16) NOT NULL DEFAULT 'pending',
        -- pending | paid
    created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    paid_at        TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS ix_affiliate_payouts_partner
    ON affiliate_payouts (partner_id);

CREATE TABLE IF NOT EXISTS affiliate_approved_assets (
    asset_id   VARCHAR(64) PRIMARY KEY,
    kind       VARCHAR(32) NOT NULL,
    lang       VARCHAR(8) NOT NULL,
    body       TEXT NOT NULL,
    is_active  BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS affiliate_compliance_events (
    event_id   VARCHAR(64) PRIMARY KEY,
    partner_id VARCHAR(64) NOT NULL,
    event_type VARCHAR(64) NOT NULL,
        -- disclosure_missing | spam_flag | duplicate_lead | self_referral | unapproved_messaging
    severity   VARCHAR(16) NOT NULL DEFAULT 'low',
    detail     VARCHAR(512),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_affiliate_compliance_partner
    ON affiliate_compliance_events (partner_id);

COMMIT;
