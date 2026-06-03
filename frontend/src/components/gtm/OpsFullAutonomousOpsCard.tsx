"use client";

import { useLocale } from "next-intl";
import { useCallback, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { getAdminApiKey, isOpsConfigured } from "@/lib/opsAdmin";

import type { ComprehensivePlanPayload } from "@/components/gtm/OpsComprehensivePlanCard";

export type AutonomousOpsPayload = {
  automation_readiness?: {
    verdict?: string;
    blockers_ar?: string[];
    automated_layers_ar?: string[];
    human_layers_ar?: string[];
  };
  research_alignment?: {
    verdict_ar?: string;
    external_consensus?: string[];
    sources_2026?: string[];
  };
  founder_only_actions_ar?: string[];
  morning_run?: { verdict?: string };
  comprehensive_plan?: ComprehensivePlanPayload;
  commands?: Record<string, string>;
};

export type GovernedAutopilotSlice = {
  verdict?: { level?: string; summary_ar?: string };
  queue?: { priority?: number; title_ar?: string; blocking?: boolean }[];
  customer_stage?: { band?: string; focus_ar?: string; paid_customers_real?: number };
  pls_readiness?: { verdict?: string; recommendation_ar?: string };
};

export type CockpitPayload = {
  cockpit_verdict?: string;
  cockpit_summary_ar?: string;
  governed_autopilot?: GovernedAutopilotSlice;
  automation_readiness?: AutonomousOpsPayload["automation_readiness"];
  founder_only_actions_ar?: string[];
  comprehensive_plan?: ComprehensivePlanPayload;
  research_alignment?: AutonomousOpsPayload["research_alignment"];
  next_actions_ar?: string[];
  benchmark_rows?: { dimension?: string; dealix?: string; verdict?: string }[];
  hitl_spectrum_2026_ar?: { level?: string; dealix?: string; when_ar?: string }[];
  complete_autonomous_day?: { verdict?: string; artifact_path?: string; research_verdict_ar?: string };
  strongest_ops?: {
    verdict?: string;
    tasks_today_count?: number;
    warnings_ar?: string[];
  };
  max_ops_backlog?: {
    percent_done?: number;
    done?: number;
    total?: number;
    verdict?: string;
  };
  morning_run?: { verdict?: string };
  unified_day_run?: { verdict?: string; artifact_path?: string };
  evening_run?: { verdict?: string };
  weekly_run?: { verdict?: string };
  daily_cadence?: { evidence_logged_today?: boolean; is_friday_run_scorecard?: boolean };
};

type Props = {
  data?: AutonomousOpsPayload | null;
  cockpit?: CockpitPayload | null;
  onRefresh?: () => void;
};

const verdictStyle: Record<string, string> = {
  AUTONOMOUS_READY: "text-emerald-600",
  AUTONOMOUS_PARTIAL: "text-amber-600",
  NEEDS_FOUNDER: "text-destructive",
  BLOCKED: "text-destructive",
};

export function OpsFullAutonomousOpsCard({ data, cockpit, onRefresh }: Props) {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [running, setRunning] = useState(false);
  const [runningCore, setRunningCore] = useState(false);
  const [runningUnified, setRunningUnified] = useState(false);
  const [runningEvening, setRunningEvening] = useState(false);
  const [runningWeekly, setRunningWeekly] = useState(false);
  const [runningComplete, setRunningComplete] = useState(false);
  const [runErr, setRunErr] = useState("");
  const [localCockpit, setLocalCockpit] = useState<CockpitPayload | null>(null);

  const c = localCockpit ?? cockpit;
  const readiness = data?.automation_readiness;
  const verdict = c?.cockpit_verdict ?? readiness?.verdict;
  if (!verdict && !c && !data) return null;

  const vClass = verdictStyle[verdict ?? ""] ?? "text-muted-foreground";
  const backlog = c?.max_ops_backlog;
  const tasksToday = c?.strongest_ops?.tasks_today_count;

  const runMorning = useCallback(async () => {
    if (!isOpsConfigured()) return;
    setRunning(true);
    setRunErr("");
    try {
      const key = getAdminApiKey() || "";
      const res = await api.postFounderCockpitRunMorning(key, { top_n: 15 });
      setLocalCockpit(res.data as CockpitPayload);
      onRefresh?.();
    } catch {
      setRunErr(isAr ? "فشل تشغيل الصباح." : "Morning run failed.");
    } finally {
      setRunning(false);
    }
  }, [isAr, onRefresh]);

  const runCoreAutopilot = useCallback(async () => {
    if (!isOpsConfigured()) return;
    setRunningCore(true);
    setRunErr("");
    try {
      const key = getAdminApiKey() || "";
      await api.postFounderFullAutonomousOpsRun(key, {
        top_n: 15,
        dry_run: false,
        run_optional_scripts: true,
      });
      onRefresh?.();
    } catch {
      setRunErr(isAr ? "فشل نواة الأتمتة." : "Core autopilot run failed.");
    } finally {
      setRunningCore(false);
    }
  }, [isAr, onRefresh]);

  const runEvening = useCallback(async () => {
    if (!isOpsConfigured()) return;
    setRunningEvening(true);
    setRunErr("");
    try {
      const key = getAdminApiKey() || "";
      const res = await api.postFounderCockpitRunEvening(key, { top_n: 15 });
      setLocalCockpit(res.data as CockpitPayload);
      onRefresh?.();
    } catch {
      setRunErr(isAr ? "فشل المساء." : "Evening run failed.");
    } finally {
      setRunningEvening(false);
    }
  }, [isAr, onRefresh]);

  const runWeekly = useCallback(async () => {
    if (!isOpsConfigured()) return;
    setRunningWeekly(true);
    setRunErr("");
    try {
      const key = getAdminApiKey() || "";
      const res = await api.postFounderCockpitRunWeekly(key, {
        top_n: 15,
        run_optional_scripts: true,
      });
      setLocalCockpit(res.data as CockpitPayload);
      onRefresh?.();
    } catch {
      setRunErr(isAr ? "فشل الأسبوع." : "Weekly run failed.");
    } finally {
      setRunningWeekly(false);
    }
  }, [isAr, onRefresh]);

  const runUnifiedDay = useCallback(async () => {
    if (!isOpsConfigured()) return;
    setRunningUnified(true);
    setRunErr("");
    try {
      const key = getAdminApiKey() || "";
      const res = await api.postFounderCockpitRunUnifiedDay(key, {
        top_n: 15,
        quick: false,
        run_optional_scripts: true,
      });
      setLocalCockpit(res.data as CockpitPayload);
      onRefresh?.();
    } catch {
      setRunErr(isAr ? "فشل اليوم الموحّد." : "Unified day run failed.");
    } finally {
      setRunningUnified(false);
    }
  }, [isAr, onRefresh]);

  const runCompleteDay = useCallback(async () => {
    if (!isOpsConfigured()) return;
    setRunningComplete(true);
    setRunErr("");
    try {
      const key = getAdminApiKey() || "";
      const res = await api.postFounderCompleteAutonomousDayRun(key, {
        top_n: 15,
        skip_commercial_day: false,
        use_unified_in_process: true,
      });
      setLocalCockpit(res.data as CockpitPayload);
      onRefresh?.();
    } catch {
      setRunErr(isAr ? "فشل اليوم الذاتي الكامل." : "Complete autonomous day failed.");
    } finally {
      setRunningComplete(false);
    }
  }, [isAr, onRefresh]);

  const autopilotQueue = c?.governed_autopilot?.queue ?? [];
  const customerStage = c?.governed_autopilot?.customer_stage;
  const plsReadiness = c?.governed_autopilot?.pls_readiness;

  return (
    <Card className="p-4 border-violet-500/30 bg-violet-500/5" dir={isAr ? "rtl" : "ltr"}>
      <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
        <h2 className="font-semibold text-sm">
          {isAr ? "فل أوبس ذاتي (بحوكمة)" : "Full autonomous ops (governed)"}
        </h2>
        <span className={`text-xs font-mono ${vClass}`}>{verdict}</span>
      </div>

      {(c?.cockpit_summary_ar || data?.research_alignment?.verdict_ar) && (
        <p className="text-xs text-muted-foreground mb-2">
          {c?.cockpit_summary_ar || data?.research_alignment?.verdict_ar}
        </p>
      )}

      <div className="flex flex-wrap gap-2 text-xs mb-3">
        {tasksToday != null && (
          <span className="rounded bg-muted px-2 py-0.5">
            {isAr ? "مهام اليوم" : "Tasks today"}: {tasksToday}
          </span>
        )}
        {backlog?.total != null && (
          <span className="rounded bg-muted px-2 py-0.5">
            Backlog: {backlog.done}/{backlog.total} ({backlog.percent_done}%)
          </span>
        )}
        {(c?.morning_run?.verdict || data?.morning_run?.verdict) && (
          <span className="rounded bg-muted px-2 py-0.5">
            {isAr ? "صباح" : "Morning"}: {c?.morning_run?.verdict ?? data?.morning_run?.verdict}
          </span>
        )}
        {c?.unified_day_run?.verdict && (
          <span className="rounded bg-muted px-2 py-0.5">
            {isAr ? "يوم موحّد" : "Unified"}: {c.unified_day_run.verdict}
          </span>
        )}
        {c?.complete_autonomous_day?.verdict && (
          <span className="rounded bg-muted px-2 py-0.5">
            {isAr ? "يوم كامل" : "Complete"}: {c.complete_autonomous_day.verdict}
          </span>
        )}
        {c?.daily_cadence && (
          <span
            className={`rounded px-2 py-0.5 ${
              c.daily_cadence.evidence_logged_today ? "bg-emerald-500/15" : "bg-amber-500/15"
            }`}
          >
            {isAr ? "أدلة اليوم" : "Evidence"}: {c.daily_cadence.evidence_logged_today ? "✓" : "—"}
          </span>
        )}
      </div>

      {isOpsConfigured() && (
        <div className="flex flex-wrap gap-2 mb-3">
          <Button
            type="button"
            size="sm"
            variant="default"
            disabled={
              runningComplete ||
              runningUnified ||
              running ||
              runningCore ||
              runningEvening ||
              runningWeekly
            }
            onClick={() => void runCompleteDay()}
          >
            {runningComplete
              ? isAr
                ? "أقصى أتمتة…"
                : "Max automation…"
              : isAr
                ? "يوم ذاتي كامل (أقصى)"
                : "Complete autonomous day"}
          </Button>
          <Button
            type="button"
            size="sm"
            variant="outline"
            disabled={
              runningComplete ||
              runningUnified ||
              running ||
              runningCore ||
              runningEvening ||
              runningWeekly
            }
            onClick={() => void runUnifiedDay()}
          >
            {runningUnified
              ? isAr
                ? "اليوم الموحّد…"
                : "Unified day…"
              : isAr
                ? "يوم موحّد (in-process)"
                : "Unified day (in-process)"}
          </Button>
          <Button
            type="button"
            size="sm"
            variant="secondary"
            disabled={
              runningComplete ||
              running ||
              runningUnified ||
              runningCore ||
              runningEvening ||
              runningWeekly
            }
            onClick={() => void runMorning()}
          >
            {running ? (isAr ? "صباح…" : "Morning…") : isAr ? "صباح" : "Morning"}
          </Button>
          <Button
            type="button"
            size="sm"
            variant="outline"
            disabled={
              runningComplete ||
              runningCore ||
              runningUnified ||
              runningEvening ||
              runningWeekly ||
              running
            }
            onClick={() => void runCoreAutopilot()}
          >
            {runningCore
              ? isAr
                ? "أتمتة…"
                : "Autopilot…"
              : isAr
                ? "أتمتة تجارية"
                : "Commercial autopilot"}
          </Button>
          <Button
            type="button"
            size="sm"
            variant="outline"
            disabled={
              runningComplete ||
              runningEvening ||
              runningUnified ||
              runningWeekly ||
              running ||
              runningCore
            }
            onClick={() => void runEvening()}
          >
            {runningEvening ? (isAr ? "مساء…" : "Evening…") : isAr ? "مساء" : "Evening"}
          </Button>
          <Button
            type="button"
            size="sm"
            variant="outline"
            disabled={runningWeekly || runningUnified || runningEvening || running || runningCore}
            onClick={() => void runWeekly()}
          >
            {runningWeekly ? (isAr ? "أسبوع…" : "Weekly…") : isAr ? "أسبوع" : "Weekly"}
          </Button>
        </div>
      )}
      {runErr && <p className="text-destructive text-xs mb-2">{runErr}</p>}

      {customerStage && (
        <p className="text-xs text-muted-foreground mb-2">
          {isAr ? "شريحة عملاء" : "Customer band"}:{" "}
          <span className="font-medium">{customerStage.band}</span>
          {" — "}
          {customerStage.focus_ar}
        </p>
      )}

      {plsReadiness && (
        <p className="text-xs text-muted-foreground mb-2">
          PLS: {plsReadiness.verdict} — {plsReadiness.recommendation_ar}
        </p>
      )}

      {autopilotQueue.length > 0 && (
        <>
          <p className="text-xs font-medium">{isAr ? "طابور اليوم (آلي):" : "Autopilot queue:"}</p>
          <ol className="text-xs space-y-1 list-decimal mr-5 mt-1 mb-2">
            {autopilotQueue.slice(0, 5).map((q) => (
              <li key={q.priority} className={q.blocking ? "font-medium" : ""}>
                {q.title_ar}
              </li>
            ))}
          </ol>
        </>
      )}

      {(c?.next_actions_ar ?? data?.founder_only_actions_ar ?? []).length > 0 && (
        <>
          <p className="text-xs font-medium">{isAr ? "إجراءاتك التالية:" : "Your next actions:"}</p>
          <ul className="text-xs space-y-1 list-disc mr-5 mt-1">
            {(c?.next_actions_ar ?? data?.founder_only_actions_ar ?? [])
              .slice(0, 6)
              .map((a) => (
                <li key={a}>{a}</li>
              ))}
          </ul>
        </>
      )}

      {(readiness?.blockers_ar ?? []).length > 0 && (
        <ul className="text-xs mt-2 space-y-1 list-disc mr-5 text-amber-700 dark:text-amber-400">
          {(readiness?.blockers_ar ?? []).map((b) => (
            <li key={b}>{b}</li>
          ))}
        </ul>
      )}

      {(data?.research_alignment?.external_consensus ?? []).length > 0 && (
        <details className="mt-3 text-xs">
          <summary className="cursor-pointer font-medium">
            {isAr ? "توافق بحث GTM 2026" : "2026 GTM research alignment"}
          </summary>
          <ul className="mt-2 space-y-1 text-muted-foreground list-disc mr-5">
            {(data?.research_alignment?.external_consensus ?? []).slice(0, 5).map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ul>
          {(data?.research_alignment?.sources_2026 ?? []).length > 0 && (
            <div className="mt-2 text-muted-foreground space-y-0.5">
              {(data?.research_alignment?.sources_2026 ?? []).map((url) => (
                <a key={url} href={url} className="underline block truncate text-[11px]" target="_blank" rel="noreferrer">
                  {url.replace(/^https?:\/\//, "")}
                </a>
              ))}
            </div>
          )}
        </details>
      )}

      {(c?.hitl_spectrum_2026_ar ?? []).length > 0 && (
        <details className="mt-3 text-xs" open>
          <summary className="cursor-pointer font-medium">
            {isAr ? "طيف HITL 2026 (أفضل من إرسال كامل)" : "HITL spectrum 2026"}
          </summary>
          <ul className="mt-2 space-y-1 text-muted-foreground">
            {(c?.hitl_spectrum_2026_ar ?? []).map((row) => (
              <li key={row.level}>
                <strong>{row.level}</strong> — Dealix: {row.dealix}
              </li>
            ))}
          </ul>
        </details>
      )}

      {(c?.benchmark_rows ?? []).length > 0 && (
        <details className="mt-3 text-xs">
          <summary className="cursor-pointer font-medium">
            {isAr ? "مقارنة RevOps" : "RevOps benchmark"}
          </summary>
          <ul className="mt-2 space-y-1 text-muted-foreground">
            {(c?.benchmark_rows ?? []).slice(0, 4).map((row) => (
              <li key={row.dimension}>
                <strong>{row.dimension}</strong>: {row.dealix} — <em>{row.verdict}</em>
              </li>
            ))}
          </ul>
        </details>
      )}
    </Card>
  );
}
