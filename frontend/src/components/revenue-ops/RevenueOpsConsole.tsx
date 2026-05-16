"use client";

/**
 * Revenue Ops Console — the operational heart of the Governed Revenue & AI
 * Operations repositioning. Shows clients, pipeline files, opportunities, deal
 * risks, next actions, follow-up drafts, decision passports, and proof events.
 *
 * Doctrine: there is deliberately NO "Send automatically" button. Every
 * external action runs through the governed engagement state machine and
 * requires an explicit founder approval.
 */

import { useState } from "react";
import { useTranslations } from "next-intl";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

const ENGAGEMENT_STATES = [
  "draft",
  "approved",
  "sent",
  "used_in_meeting",
  "scope_requested",
  "invoice_sent",
  "invoice_paid",
] as const;

type EngagementState = (typeof ENGAGEMENT_STATES)[number];

interface ConsoleAction {
  key: string;
  labelKey: string;
}

// NOTE: no "send automatically" action — by doctrine.
const CONSOLE_ACTIONS: ConsoleAction[] = [
  { key: "create_diagnostic", labelKey: "actions.createDiagnostic" },
  { key: "upload_crm", labelKey: "actions.uploadCrm" },
  { key: "generate_review", labelKey: "actions.generateReview" },
  { key: "create_passport", labelKey: "actions.createPassport" },
  { key: "draft_followup", labelKey: "actions.draftFollowup" },
  { key: "mark_approved", labelKey: "actions.markApproved" },
  { key: "create_invoice", labelKey: "actions.createInvoice" },
  { key: "generate_proof", labelKey: "actions.generateProof" },
];

export function RevenueOpsConsole() {
  const t = useTranslations("revenueOps");
  const [activeState, setActiveState] = useState<EngagementState>("draft");

  return (
    <div className="space-y-6">
      {/* Action bar — explicitly no auto-send */}
      <section className="rounded-xl border border-slate-200 bg-white p-4">
        <h2 className="mb-3 text-sm font-semibold text-slate-700">
          {t("console.actionsTitle")}
        </h2>
        <div className="flex flex-wrap gap-2">
          {CONSOLE_ACTIONS.map((a) => (
            <Button key={a.key} variant="outline" size="sm">
              {t(a.labelKey)}
            </Button>
          ))}
        </div>
        <p className="mt-3 text-xs text-slate-500">{t("console.noAutoSend")}</p>
      </section>

      {/* Engagement state machine */}
      <section className="rounded-xl border border-slate-200 bg-white p-4">
        <h2 className="mb-3 text-sm font-semibold text-slate-700">
          {t("console.stateMachineTitle")}
        </h2>
        <div className="flex flex-wrap items-center gap-2">
          {ENGAGEMENT_STATES.map((s, i) => (
            <span key={s} className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setActiveState(s)}
                className={
                  s === activeState
                    ? "rounded-full bg-slate-900 px-3 py-1 text-xs font-medium text-white"
                    : "rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600"
                }
              >
                {t(`states.${s}`)}
              </button>
              {i < ENGAGEMENT_STATES.length - 1 && (
                <span className="text-slate-300">→</span>
              )}
            </span>
          ))}
        </div>
        <p className="mt-3 text-xs text-slate-500">{t("console.stateMachineNote")}</p>
      </section>

      {/* Console panels */}
      <div className="grid gap-4 md:grid-cols-2">
        <ConsolePanel title={t("console.clientsTitle")} empty={t("console.empty")} />
        <ConsolePanel title={t("console.pipelineFilesTitle")} empty={t("console.empty")} />
        <ConsolePanel title={t("console.opportunitiesTitle")} empty={t("console.empty")} />
        <ConsolePanel title={t("console.dealRisksTitle")} empty={t("console.empty")} />
        <ConsolePanel title={t("console.nextActionsTitle")} empty={t("console.empty")} />
        <ConsolePanel title={t("console.followupDraftsTitle")} empty={t("console.empty")}>
          <Badge variant="outline">{t("console.draftOnly")}</Badge>
        </ConsolePanel>
        <ConsolePanel title={t("console.passportsTitle")} empty={t("console.empty")} />
        <ConsolePanel title={t("console.proofEventsTitle")} empty={t("console.empty")} />
      </div>

      <p className="text-xs text-slate-400">{t("disclaimer")}</p>
    </div>
  );
}

function ConsolePanel({
  title,
  empty,
  children,
}: {
  title: string;
  empty: string;
  children?: React.ReactNode;
}) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4">
      <div className="mb-2 flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-700">{title}</h3>
        {children}
      </div>
      <p className="text-xs text-slate-400">{empty}</p>
    </section>
  );
}
