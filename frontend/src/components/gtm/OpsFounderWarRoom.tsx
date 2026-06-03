"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { getAdminApiKey, isOpsConfigured, opsMissingKeyMessage } from "@/lib/opsAdmin";

type CeoMasterPlanSlice = {
  overall_verdict?: string;
  daily_five_metrics?: {
    metrics?: Record<string, number | null>;
    founder_action_ar?: string;
    phase_0_1_verdict?: string;
  };
  p0_revenue_close?: { verdict?: string; phase_deal?: { company_filled?: boolean } };
  p0_production_trust?: { verdict?: string; production?: { overall_pct?: number } };
  p0_ceo_decision?: {
    verdict?: string;
    decision?: { one_decision_ar?: string; success_by_friday_ar?: string };
  };
  p0_gtm_blitz?: {
    verdict?: string;
    icp?: { eligible?: number };
    conversations?: { qualified?: number; proposals?: number };
  };
  p1_trust_pack?: { verdict?: string };
  p2_repeatability?: { verdict?: string; phase_2_hint_ar?: string };
};

type ComprehensivePlan = {
  weekly_one_decision?: {
    verdict?: string;
    week_id?: string;
    one_decision?: string;
    supports_phase?: string | number;
    stop_list?: string[];
    latest_path?: string;
  };
  phase_0_1_gate?: {
    verdict?: string;
    blockers_ar?: string[];
  };
  master_execution_phase?: {
    active_phase?: number;
    active_label_ar?: string;
    phases?: { phase: number; label_ar?: string; is_active?: boolean; is_complete?: boolean }[];
  };
  ceo_master_plan?: CeoMasterPlanSlice;
  max_ops_backlog?: {
    verdict?: string;
    percent_done?: number;
    done?: number;
    total?: number;
    doc?: string;
  };
  dogfooding?: {
    war_room_ready?: boolean;
    sync_script?: string;
    doc?: string;
  };
};

function CeoMasterPlanBlock({
  ceo,
  plan,
  isAr,
}: {
  ceo: CeoMasterPlanSlice;
  plan: ComprehensivePlan;
  isAr: boolean;
}) {
  const metrics = ceo.daily_five_metrics?.metrics ?? {};
  const workstreams = [
    ["revenue", ceo.p0_revenue_close?.verdict],
    ["production", ceo.p0_production_trust?.verdict],
    ["decision", ceo.p0_ceo_decision?.verdict],
    ["gtm", ceo.p0_gtm_blitz?.verdict],
    ["trust", ceo.p1_trust_pack?.verdict],
    ["repeat", ceo.p2_repeatability?.verdict],
  ] as const;
  const blockers = plan.phase_0_1_gate?.blockers_ar ?? [];

  return (
    <div className="rounded-lg border border-primary/20 bg-primary/5 p-3 space-y-3">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <p className="text-xs font-semibold">
          {isAr ? "CEO Master Plan" : "CEO Master Plan"} ·{" "}
          <span className="font-mono">{ceo.overall_verdict ?? "—"}</span>
        </p>
        <Link
          href="/docs/commercial/operations/TRUST_PACK_PROPOSAL_AR.md"
          className="text-xs text-primary hover:underline"
          target="_blank"
        >
          Trust Pack
        </Link>
      </div>
      <div className="flex flex-wrap gap-1">
        {workstreams.map(([key, verdict]) => (
          <span
            key={key}
            className={`text-[10px] px-1.5 py-0.5 rounded border font-mono ${
              verdict === "PASS"
                ? "border-emerald-500/50 text-emerald-700 dark:text-emerald-400"
                : "border-muted text-muted-foreground"
            }`}
          >
            {key}:{verdict ?? "—"}
          </span>
        ))}
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-2 text-[10px] font-mono">
        <span>paid today: {metrics["1_new_paid_revenue_events_today"] ?? 0}</span>
        <span>payments: {metrics["2_payment_received_real_total"] ?? 0}</span>
        <span>proofs: {metrics["3_proof_packs_delivered_total"] ?? 0}</span>
        <span>pipeline: {metrics["4_open_pipeline_leads_real"] ?? 0}</span>
        <span>layers: {metrics["5_production_layers_pct"] ?? "n/a"}%</span>
      </div>
      {ceo.p0_ceo_decision?.decision?.one_decision_ar && (
        <p className="text-xs">{ceo.p0_ceo_decision.decision.one_decision_ar}</p>
      )}
      {blockers.length > 0 && (
        <ul className="text-xs text-amber-700 dark:text-amber-400 list-disc mr-4 space-y-0.5">
          {blockers.slice(0, 3).map((b) => (
            <li key={b}>{b}</li>
          ))}
        </ul>
      )}
      {ceo.daily_five_metrics?.founder_action_ar && (
        <p className="text-xs text-muted-foreground">{ceo.daily_five_metrics.founder_action_ar}</p>
      )}
    </div>
  );
}

function MasterPhaseStrip({ plan, isAr }: { plan: ComprehensivePlan; isAr: boolean }) {
  const phases = plan.master_execution_phase?.phases ?? [];
  const active = plan.master_execution_phase?.active_phase ?? 0;
  if (phases.length === 0) {
    return (
      <p className="text-xs text-muted-foreground">
        {isAr ? `المرحلة النشطة: ${active}` : `Active phase: ${active}`}
      </p>
    );
  }
  return (
    <div className="flex flex-wrap gap-1" role="list">
      {phases.map((p) => (
        <span
          key={p.phase}
          className={`text-xs px-2 py-0.5 rounded border ${
            p.is_active
              ? "border-primary bg-primary/20 font-semibold"
              : p.is_complete
                ? "border-emerald-500/40 text-emerald-700 dark:text-emerald-400"
                : "border-muted text-muted-foreground"
          }`}
          title={p.label_ar}
        >
          {p.phase}
        </span>
      ))}
    </div>
  );
}

function WeeklyDecisionBlock({ plan, isAr }: { plan: ComprehensivePlan; isAr: boolean }) {
  const w = plan.weekly_one_decision;
  const decision = (w?.one_decision || "").trim();
  return (
    <div>
      <p className="text-xs text-muted-foreground mb-1">
        {isAr ? "قرار الأسبوع" : "Weekly decision"} · {w?.week_id ?? "—"} ·{" "}
        <span className="font-mono">{w?.verdict ?? "—"}</span>
      </p>
      <p className="text-sm">
        {decision ||
          (isAr ? "— املأ عبر founder_weekly_decision_init.py" : "— run founder_weekly_decision_init.py")}
      </p>
      {w?.supports_phase != null && w.supports_phase !== "" && (
        <p className="text-xs text-muted-foreground mt-1">
          {isAr ? "يدعم مرحلة" : "supports_phase"}: {String(w.supports_phase)}
        </p>
      )}
    </div>
  );
}

const CHECKLIST_90_AR = [
  "0–10: brief + digest",
  "10–25: War Room 10 لمسات",
  "25–40: موافقات",
  "40–55: LinkedIn يدوي",
  "55–70: ديمو / Calendly",
  "70–85: متابعات + شريك",
  "85–90: أدلة + KPI",
];

type SocialPost = {
  title_ar?: string;
  pillar?: string;
  status?: string;
  cta_ar?: string;
  calendar_date?: string;
};

type WarRoomTarget = {
  company?: string;
  target?: string;
  status?: string;
  next_action?: string;
  segment?: string;
  outreach_draft_ar?: string;
};

export function OpsFounderWarRoom() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const adminKey = getAdminApiKey();
  const [plan, setPlan] = useState<ComprehensivePlan | null>(null);
  const [targets, setTargets] = useState<WarRoomTarget[]>([]);
  const [social, setSocial] = useState<SocialPost[]>([]);
  const [err, setErr] = useState("");

  useEffect(() => {
    if (!isOpsConfigured()) {
      setErr(opsMissingKeyMessage(isAr));
      return;
    }
    const key = adminKey || "";
    setErr("");
    Promise.all([
      api.getFounderCockpit(key, 10, "morning"),
      api.getTargetingToday(key, 5),
      api.getWarRoomTodayPack(key),
      api.getMarketingSocialToday(key),
    ])
      .then(([cockpitRes, tgtRes, packRes, socialRes]) => {
        const cockpit = cockpitRes.data as { comprehensive_plan?: ComprehensivePlan };
        setPlan(cockpit.comprehensive_plan ?? null);
        const tgtItems =
          (tgtRes.data as { targets?: { items?: WarRoomTarget[] } })?.targets?.items ?? [];
        setTargets(tgtItems);
        const packTargets =
          (packRes.data as { targets?: WarRoomTarget[]; top_targets?: WarRoomTarget[] })
            ?.targets ??
          (packRes.data as { top_targets?: WarRoomTarget[] })?.top_targets;
        if (packTargets?.length) {
          setTargets((prev) => (prev.length ? prev : packTargets));
        }
        const posts =
          (socialRes.data as { posts?: SocialPost[]; items?: SocialPost[] })?.posts ??
          (socialRes.data as { items?: SocialPost[] })?.items ??
          [];
        setSocial(posts.slice(0, 3));
      })
      .catch(() => {
        setErr(isAr ? "تعذّر تحميل غرفة الإيراد المختصرة." : "War room summary load failed.");
      });
  }, [adminKey, isAr]);

  return (
    <Card className="p-4 space-y-4 border-muted">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h2 className="font-semibold text-sm">
          {isAr ? "غرفة الإيراد — 90 دقيقة" : "War room — 90 min"}
        </h2>
        <Button variant="outline" size="sm" asChild>
          <Link href={`/${locale}/ops/war-room`}>
            {isAr ? "الجدول الكامل" : "Full table"}
          </Link>
        </Button>
      </div>
      {err && <p className="text-destructive text-sm">{err}</p>}
      {plan?.ceo_master_plan && (
        <CeoMasterPlanBlock ceo={plan.ceo_master_plan} plan={plan} isAr={isAr} />
      )}
      {plan && (
        <>
          <MasterPhaseStrip plan={plan} isAr={isAr} />
          <WeeklyDecisionBlock plan={plan} isAr={isAr} />
        </>
      )}
      <div>
        <p className="text-xs font-medium text-muted-foreground mb-2">
          {isAr ? "قائمة 90 دقيقة" : "90-minute checklist"}
        </p>
        <ul className="text-xs space-y-1 list-disc mr-5">
          {CHECKLIST_90_AR.map((line) => (
            <li key={line}>{line}</li>
          ))}
        </ul>
      </div>
      {targets.length > 0 && (
        <div>
          <p className="text-xs font-medium text-muted-foreground mb-2">
            {isAr ? "أهداف اليوم" : "Today targets"}
          </p>
          <ul className="space-y-2">
            {targets.map((t, i) => (
              <li key={`${t.company ?? t.target ?? i}`} className="text-sm border rounded-md p-2">
                <span className="font-medium">{t.company ?? t.target ?? "—"}</span>
                {t.next_action && (
                  <p className="text-xs text-muted-foreground mt-1">{t.next_action}</p>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
      {social.length > 0 && (
        <div>
          <p className="text-xs font-medium text-muted-foreground mb-2">
            {isAr ? "محتوى اليوم" : "Social today"}
          </p>
          <ul className="text-xs space-y-1">
            {social.map((p, i) => (
              <li key={`${p.title_ar ?? i}`}>
                {p.title_ar ?? p.pillar ?? "—"} · {p.status ?? "—"}
              </li>
            ))}
          </ul>
        </div>
      )}
    </Card>
  );
}
