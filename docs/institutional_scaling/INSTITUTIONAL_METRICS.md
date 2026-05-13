# Institutional Metrics

Three families: company, trust, market. Each family has a scaling-safety threshold.

## 1. Company

MRR, Gross Margin, Proof Packs delivered, Proof-to-Retainer Conversion, Capital Assets Created, Manual Steps Productized, Governance Incidents, AI Run Audit Coverage, Client Health, Business Unit Maturity.

## 2. Trust

% sources with Source Passport, % outputs with governance decision, % AI runs logged, % external actions approved, PII flags detected, unsafe actions blocked.

## 3. Market

Inbound Diagnostics, Partner Referrals, Proof Pack Requests, Capability Score Mentions, Benchmark Downloads, Academy Waitlist, Enterprise Trust Inquiries.

## 4. Rules

- If trust metrics are weak → do not scale.
- If proof metrics are weak → do not raise claims.
- If productization is weak → you are becoming an agency.
- If market metrics are weak → you have not earned the language.

## 5. Typed surface

`institutional_scaling_os.institutional_metrics.is_scaling_safe()` evaluates the gate.

## 6. The principle

> Institutional metrics measure trust before they measure revenue.
