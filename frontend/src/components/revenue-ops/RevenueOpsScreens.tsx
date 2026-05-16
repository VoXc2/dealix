"use client";

/**
 * The 5 supporting screens of the Governed Revenue & AI Operations
 * repositioning (the 6th — RevenueOpsConsole — lives in its own file):
 *
 *   1. FounderCommandCenter
 *   2. ServiceCatalog
 *   3. MarketProofConsole
 *   5. EvidenceLedger
 *   6. BillingInvoices
 *
 * All are governed/evidence-first. No screen offers an autonomous external
 * send. Invoices are drafts only — no charge is initiated from the UI.
 */

import { useTranslations } from "next-intl";
import { Badge } from "@/components/ui/badge";

function Panel({
  title,
  children,
}: {
  title: string;
  children?: React.ReactNode;
}) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4">
      <h3 className="mb-2 text-sm font-semibold text-slate-700">{title}</h3>
      {children}
    </section>
  );
}

function EmptyNote() {
  const t = useTranslations("revenueOps");
  return <p className="text-xs text-slate-400">{t("console.empty")}</p>;
}

function Disclaimer() {
  const t = useTranslations("revenueOps");
  return <p className="text-xs text-slate-400">{t("disclaimer")}</p>;
}

/** Screen 1 — Founder Command Center. */
export function FounderCommandCenter() {
  const t = useTranslations("revenueOps");
  return (
    <div className="space-y-4">
      <div className="grid gap-4 md:grid-cols-3">
        <Panel title={t("command.activeEngagements")}>
          <EmptyNote />
        </Panel>
        <Panel title={t("command.pendingApprovals")}>
          <EmptyNote />
        </Panel>
        <Panel title={t("command.proofPacks")}>
          <EmptyNote />
        </Panel>
      </div>
      <Panel title={t("command.metricsTitle")}>
        <ul className="space-y-1 text-xs text-slate-600">
          {[
            "sent_count",
            "reply_count",
            "meeting_count",
            "diagnostic_scope_requested",
            "invoice_sent",
            "invoice_paid",
            "proof_pack_created",
            "retainer_opportunity",
          ].map((m) => (
            <li key={m} className="flex justify-between">
              <span>{m}</span>
              <span className="font-medium text-slate-400">0</span>
            </li>
          ))}
        </ul>
        <p className="mt-2 text-xs text-slate-400">{t("command.metricsNote")}</p>
      </Panel>
      <Disclaimer />
    </div>
  );
}

const CATALOG = [
  { id: "governed_revenue_ops_diagnostic", price: "4,999–25,000 SAR", entry: true },
  { id: "revenue_intelligence_sprint", price: "from 25,000 SAR", entry: false },
  { id: "governed_ops_retainer", price: "4,999–15,000 SAR/mo", entry: false },
  { id: "ai_governance_for_revenue_teams", price: "scope-based", entry: false },
  { id: "crm_data_readiness_for_ai", price: "scope-based", entry: false },
  { id: "board_decision_memo", price: "scope-based", entry: false },
  { id: "trust_pack_lite", price: "on request", entry: false },
];

/** Screen 2 — Service Catalog (7-service Governed Revenue Ops catalog). */
export function ServiceCatalog() {
  const t = useTranslations("revenueOps");
  return (
    <div className="space-y-4">
      <div className="grid gap-4 md:grid-cols-2">
        {CATALOG.map((s) => (
          <Panel key={s.id} title={t(`catalog.${s.id}`)}>
            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-500">{s.price}</span>
              {s.entry ? (
                <Badge>{t("catalog.entryOffer")}</Badge>
              ) : (
                <Badge variant="outline">{t("catalog.catalogService")}</Badge>
              )}
            </div>
          </Panel>
        ))}
      </div>
      <Disclaimer />
    </div>
  );
}

/** Screen 3 — Market Proof Console. */
export function MarketProofConsole() {
  const t = useTranslations("revenueOps");
  return (
    <div className="space-y-4">
      <Panel title={t("marketProof.caseSafeTitle")}>
        <EmptyNote />
      </Panel>
      <Panel title={t("marketProof.proofOpportunitiesTitle")}>
        <EmptyNote />
      </Panel>
      <Disclaimer />
    </div>
  );
}

/** Screen 5 — Evidence Ledger. */
export function EvidenceLedger() {
  const t = useTranslations("revenueOps");
  return (
    <div className="space-y-4">
      <Panel title={t("evidence.trailTitle")}>
        <EmptyNote />
        <p className="mt-2 text-xs text-slate-400">{t("evidence.note")}</p>
      </Panel>
      <Disclaimer />
    </div>
  );
}

/** Screen 6 — Billing / Invoices (drafts only — no charge from the UI). */
export function BillingInvoices() {
  const t = useTranslations("revenueOps");
  return (
    <div className="space-y-4">
      <Panel title={t("billing.draftsTitle")}>
        <EmptyNote />
        <p className="mt-2 text-xs text-slate-400">{t("billing.note")}</p>
      </Panel>
      <Disclaimer />
    </div>
  );
}
