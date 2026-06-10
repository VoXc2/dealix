-- 010_referral_program.sql
-- Wave 14 — Activates the referral program persistence layer.
-- Companion to api/routers/referral_program.py (W13.13).
--
-- Tables:
--   referral_codes      — one-time codes issued to existing paying customers
--   referrals           — referrer → referred customer link, plus credit state
--   referral_payouts    — credit applications against future invoices

BEGIN;

CREATE TABLE IF NOT EXISTS referral_codes (
    code            VARCHAR(32) PRIMARY KEY,
    referrer_id     VARCHAR(64) NOT NULL,
    plan_required   VARCHAR(64) DEFAULT 'managed_revenue_ops_starter',
    credit_sar      INTEGER NOT NULL DEFAULT 5000,
    discount_pct    INTEGER NOT NULL DEFAULT 50,
    valid_until     TIMESTAMPTZ,
    is_revoked      BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_referral_codes_referrer
    ON referral_codes (referrer_id);

CREATE TABLE IF NOT EXISTS referrals (
    referral_id     VARCHAR(64) PRIMARY KEY,
    code            VARCHAR(32) NOT NULL REFERENCES referral_codes(code),
    referrer_id     VARCHAR(64) NOT NULL,
    referred_id     VARCHAR(64) NOT NULL,
    status          VARCHAR(32) NOT NULL DEFAULT 'pending',
        -- pending | redeemed | invoice_paid | credit_issued | declined
    referred_invoice_id  VARCHAR(64),
    referred_first_amount_sar INTEGER,
    declined_reason  VARCHAR(256),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    redeemed_at     TIMESTAMPTZ,
    paid_at         TIMESTAMPTZ,
    credit_issued_at TIMESTAMPTZ,
    UNIQUE (referrer_id, referred_id)
);

CREATE INDEX IF NOT EXISTS idx_referrals_status
    ON referrals (status);
CREATE INDEX IF NOT EXISTS idx_referrals_referrer
    ON referrals (referrer_id);
CREATE INDEX IF NOT EXISTS idx_referrals_referred
    ON referrals (referred_id);

CREATE TABLE IF NOT EXISTS referral_payouts (
    payout_id       VARCHAR(64) PRIMARY KEY,
    referral_id     VARCHAR(64) NOT NULL REFERENCES referrals(referral_id),
    credit_sar      INTEGER NOT NULL,
    applied_to_invoice_id  VARCHAR(64),
    applied_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    notes           TEXT
);

CREATE INDEX IF NOT EXISTS idx_referral_payouts_referral
    ON referral_payouts (referral_id);

-- Seed: program metadata as comment row (referrers can query the active
-- program parameters without hard-coding in code).
--
-- INSERT statement deferred to admin tooling — the API computes terms
-- from environment defaults until a row is inserted here.

COMMIT;
