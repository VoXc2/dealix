-- ============================================================================
-- Dealix Opportunity Graph — v1.0 schema
-- ============================================================================
-- This is the "AI CRO" moat layer. Not a lead list — a relational graph of
-- companies, decision-makers, signals, and opportunity edges. Runs on
-- Postgres 16+ with pgvector for semantic queries.
--
-- Design principles:
--   1. Every node has confidence + source attribution (Wathq, Monsha'at, LinkedIn…)
--   2. Arabic-normalized names are separate columns (name_ar_norm, name_ar_display)
--   3. Edges carry signal_strength + decay_at so stale signals fade automatically
--   4. All writes audited (created_by_agent, created_at, source_url)
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- NODES
-- ============================================================================

-- Companies — the primary entity. Sourced from Wathq CR + Monsha'at + manual.
CREATE TABLE IF NOT EXISTS companies (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cr_number       VARCHAR(32) UNIQUE,                    -- Commercial Registration
    name_ar         TEXT NOT NULL,                         -- display name Arabic
    name_ar_norm    TEXT NOT NULL,                         -- normalized for matching
    name_en         TEXT,
    sector          TEXT,                                  -- real_estate, retail, fintech, construction, other
    subsector       TEXT,                                  -- free-form
    size_employees  INT,
    size_revenue_tier TEXT,                                -- micro, small, medium, large, enterprise
    region          TEXT,                                  -- Riyadh, Jeddah, Dammam, …
    city            TEXT,
    national_address_id TEXT,                              -- from العنوان الوطني
    website         TEXT,
    linkedin_url    TEXT,
    embedding       vector(1024),                          -- ALLaM/BGE embedding of company profile
    confidence      NUMERIC(4,3) NOT NULL DEFAULT 0.500,  -- 0.000 - 1.000
    source          TEXT NOT NULL,                         -- wathq, monshaat, manual, enrichment
    source_url      TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_by_agent TEXT,
    metadata        JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_companies_name_ar_trgm ON companies USING gin (name_ar_norm gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_companies_sector       ON companies (sector);
CREATE INDEX IF NOT EXISTS idx_companies_region       ON companies (region);
CREATE INDEX IF NOT EXISTS idx_companies_embedding    ON companies USING hnsw (embedding vector_cosine_ops);

-- People — decision-makers, influencers, contacts within companies.
CREATE TABLE IF NOT EXISTS people (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id      UUID REFERENCES companies(id) ON DELETE CASCADE,
    name_ar         TEXT,
    name_ar_norm    TEXT,
    name_en         TEXT,
    title_ar        TEXT,
    title_en        TEXT,
    role_seniority  TEXT,                                  -- ic, manager, director, vp, c_level, owner
    email           TEXT,
    phone_e164      TEXT,
    linkedin_url    TEXT,
    is_decision_maker BOOLEAN NOT NULL DEFAULT FALSE,
    confidence      NUMERIC(4,3) NOT NULL DEFAULT 0.500,
    source          TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    metadata        JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_people_company  ON people (company_id);
CREATE INDEX IF NOT EXISTS idx_people_decision ON people (is_decision_maker) WHERE is_decision_maker;

-- Events — conferences, launches, funding rounds, tenders.
CREATE TABLE IF NOT EXISTS events (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type      TEXT NOT NULL,                         -- conference, funding, product_launch, tender
    name_ar         TEXT,
    name_en         TEXT,
    event_date      DATE,
    location        TEXT,
    description     TEXT,
    source_url      TEXT,
    metadata        JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Signals — time-bound indicators of intent / relevance.
CREATE TABLE IF NOT EXISTS signals (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id      UUID REFERENCES companies(id) ON DELETE CASCADE,
    person_id       UUID REFERENCES people(id) ON DELETE SET NULL,
    signal_type     TEXT NOT NULL,                         -- intent, news, hiring, funding, website_visit, linkedin_post
    signal_strength NUMERIC(4,3) NOT NULL DEFAULT 0.500,  -- 0-1
    description     TEXT,
    evidence_url    TEXT,                                  -- link to primary source
    decay_at        TIMESTAMPTZ,                           -- when signal becomes stale
    source          TEXT NOT NULL,
    detected_by_agent TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Fresh-signals composite index (predicate avoids non-IMMUTABLE now()).
CREATE INDEX IF NOT EXISTS idx_signals_company_fresh
    ON signals (company_id, decay_at NULLS FIRST, created_at DESC);

-- ============================================================================
-- EDGES — the graph relationships
-- ============================================================================

-- Company <-> Company relationships (partners, competitors, suppliers, customers).
CREATE TABLE IF NOT EXISTS company_relations (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_company    UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    to_company      UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    relation_type   TEXT NOT NULL,                         -- partner, competitor, supplier, customer, acquirer, subsidiary
    confidence      NUMERIC(4,3) NOT NULL DEFAULT 0.500,
    evidence_url    TEXT,
    detected_by_agent TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CHECK (from_company <> to_company)
);

CREATE INDEX IF NOT EXISTS idx_company_rel_from ON company_relations (from_company, relation_type);
CREATE INDEX IF NOT EXISTS idx_company_rel_to   ON company_relations (to_company,   relation_type);

-- Person <-> Person (referrals, former colleagues, mutual connections).
CREATE TABLE IF NOT EXISTS person_relations (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    from_person     UUID NOT NULL REFERENCES people(id) ON DELETE CASCADE,
    to_person       UUID NOT NULL REFERENCES people(id) ON DELETE CASCADE,
    relation_type   TEXT NOT NULL,                         -- colleague, former_colleague, mutual_connection, mentor
    strength        NUMERIC(4,3) NOT NULL DEFAULT 0.500,
    evidence_url    TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CHECK (from_person <> to_person)
);

-- Opportunity — the synthesis node: combines a company + signals + suggested action.
CREATE TABLE IF NOT EXISTS opportunities (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id      UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    title_ar        TEXT NOT NULL,                         -- "فرصة شراكة مع النور العقارية"
    stage           TEXT NOT NULL DEFAULT 'identified',    -- identified, qualified, engaged, proposal, negotiation, won, lost
    expected_value_sar NUMERIC(14,2),
    win_probability NUMERIC(4,3),                          -- 0-1
    supporting_signals UUID[] NOT NULL DEFAULT '{}',       -- signal IDs
    suggested_action TEXT,                                  -- "أرسل LOI + احجز اجتماع"
    suggested_action_blocked BOOLEAN NOT NULL DEFAULT FALSE,
    blocked_reason  TEXT,                                   -- Policy Engine veto reason
    owner_approval_required BOOLEAN NOT NULL DEFAULT FALSE,
    evidence_summary TEXT,                                  -- "لماذا ظهرت" — Arabic rationale
    confidence      NUMERIC(4,3) NOT NULL DEFAULT 0.500,
    created_by_agent TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    resolved_at     TIMESTAMPTZ,
    metadata        JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_opportunities_company ON opportunities (company_id);
CREATE INDEX IF NOT EXISTS idx_opportunities_stage   ON opportunities (stage);
CREATE INDEX IF NOT EXISTS idx_opportunities_value   ON opportunities ((expected_value_sar * win_probability) DESC);

-- ============================================================================
-- AUDIT / OBSERVABILITY
-- ============================================================================

-- Every agent decision leaves a trail.
CREATE TABLE IF NOT EXISTS agent_audit_log (
    id              BIGSERIAL PRIMARY KEY,
    ts              TIMESTAMPTZ NOT NULL DEFAULT now(),
    agent           TEXT NOT NULL,
    action_type     TEXT NOT NULL,
    verdict         TEXT,                                   -- auto, approve, block (from Policy Engine)
    rule_id         TEXT,                                   -- P0001, P0002, ...
    opportunity_id  UUID REFERENCES opportunities(id) ON DELETE SET NULL,
    company_id      UUID REFERENCES companies(id) ON DELETE SET NULL,
    latency_ms      NUMERIC(10,2),
    trace_id        TEXT,                                   -- OpenTelemetry trace ID
    payload         JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_audit_ts    ON agent_audit_log (ts DESC);
CREATE INDEX IF NOT EXISTS idx_audit_agent ON agent_audit_log (agent, ts DESC);
CREATE INDEX IF NOT EXISTS idx_audit_trace ON agent_audit_log (trace_id);

-- ============================================================================
-- HELPER VIEW — prioritized open opportunities
-- ============================================================================

CREATE OR REPLACE VIEW v_priority_opportunities AS
SELECT
    o.id,
    o.title_ar,
    c.name_ar AS company_name,
    c.sector,
    o.stage,
    o.expected_value_sar,
    o.win_probability,
    (COALESCE(o.expected_value_sar, 0) * COALESCE(o.win_probability, 0)) AS weighted_value,
    o.suggested_action,
    o.owner_approval_required,
    o.evidence_summary,
    o.updated_at,
    (
        SELECT COUNT(*) FROM signals s
        WHERE s.company_id = c.id
          AND (s.decay_at IS NULL OR s.decay_at > now())
    ) AS fresh_signal_count
FROM opportunities o
JOIN companies c ON c.id = o.company_id
WHERE o.stage NOT IN ('won', 'lost')
ORDER BY weighted_value DESC NULLS LAST, o.updated_at DESC;

-- ============================================================================
-- done
-- ============================================================================
