"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { OpsComprehensivePlanCard } from "@/components/gtm/OpsComprehensivePlanCard";
import { OpsFounderWarRoom } from "@/components/gtm/OpsFounderWarRoom";
import { OpsStrongestPlanPanel } from "@/components/gtm/OpsStrongestPlanPanel";
import {
  OpsFullAutonomousOpsCard,
  type AutonomousOpsPayload,
  type CockpitPayload,
} from "@/components/gtm/OpsFullAutonomousOpsCard";
import { OpsGtmStrategyCard, type GtmStackPayload } from "@/components/gtm/OpsGtmStrategyCard";
import { ValuePlanPanel, type ValuePlanPayload } from "@/components/gtm/ValuePlanPanel";
import api from "@/lib/api";
import { getAdminApiKey, isOpsConfigured, opsMissingKeyMessage } from "@/lib/opsAdmin";

type TargetRow = {
  company?: string;
  channel?: string;
  next_action?: string;
  priority?: string;
};

type KpiRow = {
  key: string;
  value: number | null;
  computed: boolean;
};

type DailyPackPayload = {
  kpi_commercial?: {
    pending_count?: number;
    ready_count?: number;
    hint_ar?: string;
    import_file_exists?: boolean;
  };
  social_post_due_today?: { title_ar?: string; status?: string };
  checklist_ar?: string[];
  pack_index_path?: string;
  today_focus_ar?: string[];
  value_plan?: ValuePlanPayload;
  gtm_stack?: GtmStackPayload;
  expansion_status?: {
    targeting?: {
      pool_rows?: number;
      wave2_ready?: boolean;
      wave3_prep_ready?: boolean;
    };
    social?: { posts?: number; cycle_weeks?: number; queue_ready_24w?: boolean };
    next_actions_ar?: string[];
  };
};

export function OpsFounderCommandCenter() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const adminKey = getAdminApiKey();
  const [stages, setStages] = useState<Record<string, number>>({});
  const [mktStats, setMktStats] = useState<Record<string, number>>({});
  const [kpis, setKpis] = useState<KpiRow[]>([]);
  const [bridgeCount, setBridgeCount] = useState(0);
  const [targets, setTargets] = useState<TargetRow[]>([]);
  const [dailyPack, setDailyPack] = useState<DailyPackPayload | null>(null);
  const [valuePlan, setValuePlan] = useState<ValuePlanPayload | null>(null);
  const [gtmStack, setGtmStack] = useState<GtmStackPayload | null>(null);
  const [fullOps, setFullOps] = useState<AutonomousOpsPayload | null>(null);
  const [cockpit, setCockpit] = useState<CockpitPayload | null>(null);
  const [err, setErr] = useState("");

  const load = useCallback(() => {
    if (!isOpsConfigured()) {
      setErr(opsMissingKeyMessage(isAr));
      return;
    }
    setErr("");
    Promise.all([
      api.getSalesPipelineAutopilot(adminKey),
      api.getMarketingCalendar(adminKey),
      api.getFullOpsHealth(adminKey),
      api.getEvidenceLedger(adminKey, 120),
      api.getTargetingToday(adminKey, 5),
      api.getFounderDailyPack(adminKey),
      api.getFounderValuePlan(adminKey, 5),
      api.getFounderGtmStack(adminKey, 8),
      api.getFounderCockpit(adminKey, 15, "morning"),
    ])
      .then(([pipe, mkt, health, ev, tgt, pack, vp, gtm, cockpitRes]) => {
        setStages((pipe.data as { stages?: Record<string, number> }).stages ?? {});
        setMktStats((mkt.data as { stats?: Record<string, number> }).stats ?? {});
        const h = health.data as { kpis?: KpiRow[] };
        setKpis(h.kpis ?? []);
        const items = (ev.data as { items?: { event_type?: string }[] }).items ?? [];
        setBridgeCount(items.filter((e) => e.event_type === "external_lead_bridged").length);
        const t = (tgt.data as { targets?: { items?: TargetRow[] } }).targets?.items ?? [];
        setTargets(t);
        const packData = pack.data as DailyPackPayload;
        setDailyPack(packData);
        const vpData = (vp.data as ValuePlanPayload) ?? packData.value_plan ?? null;
        setValuePlan(vpData);
        setGtmStack(
          (gtm.data as GtmStackPayload) ?? packData.gtm_stack ?? (vpData as { gtm_stack?: GtmStackPayload })?.gtm_stack ?? null,
        );
        const cockpitData = cockpitRes.data as CockpitPayload;
        setCockpit(cockpitData);
        setFullOps({
          automation_readiness: cockpitData.automation_readiness,
          research_alignment: cockpitData.research_alignment,
          founder_only_actions_ar: cockpitData.founder_only_actions_ar,
          comprehensive_plan: cockpitData.comprehensive_plan,
        });
      })
      .catch(() => setErr(isAr ? "تعذّر تحميل مركز القيادة." : "Command center load failed."));
  }, [adminKey, isAr]);

  useEffect(() => {
    load();
  }, [load]);

  const guardKpi = kpis.find((k) => k.key === "approval_compliance_rate_pct");

  return (
    <div className="space-y-8" dir={isAr ? "rtl" : "ltr"}>
      <p className="text-sm text-muted-foreground">
        {isAr
          ? "مركز قيادة موحّد — مبيعات · تسويق · استهداف · صحة التشغيل · غرفة الإيراد."
          : "Unified command center — sales · marketing · targeting · ops health · war room."}
      </p>
      {err && <p className="text-destructive text-sm">{err}</p>}

      <OpsFullAutonomousOpsCard data={fullOps} cockpit={cockpit} onRefresh={load} />

      <OpsComprehensivePlanCard
        plan={fullOps?.comprehensive_plan}
        variant="full"
      />

      {valuePlan && <ValuePlanPanel valuePlan={valuePlan} />}

      <OpsGtmStrategyCard gtm={gtmStack} />

      {dailyPack?.kpi_commercial && (dailyPack.kpi_commercial.pending_count ?? 0) > 0 && (
        <Card className="p-4 border-amber-500/40 bg-amber-500/5">
          <p className="text-sm font-medium">
            {isAr ? "KPI تجاري معلّق من CRM" : "Commercial KPIs pending CRM import"}
          </p>
          <p className="text-xs text-muted-foreground mt-1">
            {dailyPack.kpi_commercial.hint_ar ||
              (isAr
                ? "عبّئ kpi_founder_commercial_import.yaml ثم apply_kpi_founder_commercial.py"
                : "Fill kpi_founder_commercial_import.yaml then run apply script")}
          </p>
          <p className="text-xs mt-2">
            {isAr ? "جاهز" : "Ready"}: {dailyPack.kpi_commercial.ready_count ?? 0} ·{" "}
            {isAr ? "معلق" : "Pending"}: {dailyPack.kpi_commercial.pending_count ?? 0}
          </p>
        </Card>
      )}

      {dailyPack && (
        <Card className="p-4 border-primary/30">
          <h2 className="font-semibold mb-2">
            {isAr ? "حزمة اليوم (إطلاق)" : "Today's launch pack"}
          </h2>
          {dailyPack.social_post_due_today?.title_ar && (
            <p className="text-sm text-muted-foreground mb-2">
              {isAr ? "سوشال:" : "Social:"} {dailyPack.social_post_due_today.title_ar} (
              {dailyPack.social_post_due_today.status})
            </p>
          )}
          <ul className="text-sm space-y-1 list-disc mr-5">
            {(dailyPack.checklist_ar ?? []).map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ul>
          {dailyPack.pack_index_path && (
            <p className="text-xs text-muted-foreground mt-3">
              {isAr ? "ملف:" : "File:"} {dailyPack.pack_index_path}
            </p>
          )}
          <div className="flex flex-wrap gap-3 mt-3 text-xs">
            <Link href={`/${locale}/ops/marketing`} className="text-primary underline">
              {isAr ? "مسودة LinkedIn" : "LinkedIn draft"}
            </Link>
            <Link href={`/${locale}/approvals`} className="text-primary underline">
              {isAr ? "الموافقات" : "Approvals"}
            </Link>
          </div>
        </Card>
      )}

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <Card className="p-3">
          <p className="text-xs text-muted-foreground">{isAr ? "جسر leads" : "Bridged leads"}</p>
          <p className="text-xl font-semibold">{bridgeCount}</p>
        </Card>
        <Card className="p-3">
          <p className="text-xs text-muted-foreground">{isAr ? "خانات تسويق" : "Marketing slots"}</p>
          <p className="text-xl font-semibold">{mktStats.calendar_total ?? 0}</p>
        </Card>
        <Card className="p-3">
          <p className="text-xs text-muted-foreground">Qualified A</p>
          <p className="text-xl font-semibold">{stages.qualified_A ?? 0}</p>
        </Card>
        <Card className="p-3">
          <p className="text-xs text-muted-foreground">{isAr ? "امتثال موافقات" : "Approval compliance"}</p>
          <p className="text-xl font-semibold">
            {guardKpi?.value != null ? `${guardKpi.value}%` : "—"}
          </p>
        </Card>
      </div>

      <Card className="p-4">
        <h2 className="font-semibold mb-3">{isAr ? "هدف اليوم (استهداف)" : "Today's targets"}</h2>
        <ul className="space-y-2 text-sm">
          {targets.map((row, i) => (
            <li key={`${row.company}-${i}`} className="border-b border-border/40 pb-2">
              <span className="font-medium">{row.company ?? "—"}</span>
              <span className="text-muted-foreground">
                {" "}
                · {row.channel ?? "—"} · {row.next_action ?? "—"}
              </span>
            </li>
          ))}
          {targets.length === 0 && (
            <li className="text-muted-foreground">
              {isAr ? "لا أهداف — استورد CSV من الاستهداف." : "No targets — import targeting CSV."}
            </li>
          )}
        </ul>
        <div className="flex flex-wrap gap-3 mt-3 text-xs">
          <Link href={`/${locale}/ops/sales`} className="text-primary underline">
            {isAr ? "خط المبيعات" : "Sales pipe"}
          </Link>
          <Link href={`/${locale}/ops/marketing`} className="text-primary underline">
            {isAr ? "التسويق" : "Marketing"}
          </Link>
          <Link href={`/${locale}/ops/war-room`} className="text-primary underline">
            {isAr ? "غرفة الإيراد" : "War Room"}
          </Link>
          <Link href={`/${locale}/approvals`} className="text-primary underline">
            {isAr ? "الموافقات" : "Approvals"}
          </Link>
          <Link href={`/${locale}/proof-pack`} className="text-primary underline">
            {isAr ? "عيّنة Proof" : "Sample Proof"}
          </Link>
          <Link href={`/${locale}/learn/post-lead-revenue-ops`} className="text-primary underline">
            {isAr ? "تعلّم AEO" : "Learn"}
          </Link>
        </div>
      </Card>

      <Card className="p-4">
        <h2 className="font-semibold mb-2">{isAr ? "مراحل المبيعات" : "Pipeline stages"}</h2>
        <div className="flex flex-wrap gap-2">
          {Object.entries(stages).map(([k, v]) => (
            <span key={k} className="text-xs rounded-md bg-muted px-2 py-1">
              {k}: {v}
            </span>
          ))}
        </div>
      </Card>

      <OpsStrongestPlanPanel />
      <OpsFounderWarRoom />
    </div>
  );
}
