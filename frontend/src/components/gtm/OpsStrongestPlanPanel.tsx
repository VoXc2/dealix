"use client";

import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import api from "@/lib/api";
import { getAdminApiKey, isOpsConfigured, opsMissingKeyMessage } from "@/lib/opsAdmin";

type TaskCompletion = {
  status?: string;
  done?: boolean;
  reason_ar?: string;
};

type PlanTask = {
  id?: string;
  n?: number;
  title_ar?: string;
  completion?: TaskCompletion;
};

type PlanSection = {
  id?: string;
  label_ar?: string;
  tasks?: PlanTask[];
};

type CompletionSummary = {
  total?: number;
  done?: number;
  due_today?: number;
  open?: number;
  percent_done?: number;
};

type FullOpsBridge = {
  research_verdict_ar?: string;
  automation_readiness?: { verdict?: string; blockers_ar?: string[] };
  founder_autopilot_verdict?: { level?: string; summary_ar?: string };
  founder_queue?: { priority?: number; title_ar?: string }[];
  commands?: Record<string, string>;
};

type StrongestPlanPayload = {
  status?: {
    ok?: boolean;
    task_count?: number;
    min_task_count?: number;
    missing_paths?: string[];
  };
  no_build_rule_ar?: string;
  policy_ar?: string;
  completion?: CompletionSummary;
  completion_policy_ar?: string;
  sections?: PlanSection[];
  full_ops_bridge?: FullOpsBridge | null;
};

const readinessStyle: Record<string, string> = {
  AUTONOMOUS_READY: "text-emerald-600",
  NEEDS_FOUNDER: "text-amber-600",
  BLOCKED: "text-destructive",
};

const taskStatusStyle: Record<string, string> = {
  done: "text-emerald-600",
  due_today: "text-amber-700",
  open: "text-muted-foreground",
};

function statusLabel(status: string | undefined, isAr: boolean): string {
  if (status === "done") return isAr ? "منجز" : "done";
  if (status === "due_today") return isAr ? "اليوم" : "due";
  return isAr ? "مفتوح" : "open";
}

export function OpsStrongestPlanPanel() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [data, setData] = useState<StrongestPlanPayload | null>(null);
  const [openSection, setOpenSection] = useState<string | null>(null);
  const [expandAll, setExpandAll] = useState(false);
  const [err, setErr] = useState("");
  const adminKey = getAdminApiKey();

  useEffect(() => {
    if (!isOpsConfigured()) {
      setErr(opsMissingKeyMessage(isAr));
      return;
    }
    const key = adminKey || "";
    api
      .getFounderStrongestPlan(key)
      .then((res) => setData(res.data as StrongestPlanPayload))
      .catch(() =>
        setErr(isAr ? "تعذّر تحميل أقوى خطة." : "Failed to load strongest plan."),
      );
  }, [isAr, adminKey]);

  const st = data?.status;
  const verdictOk = st?.ok === true;
  const bridge = data?.full_ops_bridge;
  const autoV = bridge?.automation_readiness?.verdict;
  const comp = data?.completion;

  return (
    <Card className="p-4 border-violet-500/30 bg-violet-500/5" dir={isAr ? "rtl" : "ltr"}>
      <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
        <h3 className="font-semibold text-sm">
          {isAr
            ? `أقوى خطة (${st?.task_count ?? 0}/${st?.min_task_count ?? 122})`
            : `Strongest plan (${st?.task_count ?? 0}/${st?.min_task_count ?? 122})`}
        </h3>
        <div className="flex flex-wrap items-center gap-2 text-xs font-mono">
          <span
            className={`px-2 py-0.5 rounded ${
              verdictOk ? "bg-emerald-500/20 text-emerald-700" : "bg-amber-500/20 text-amber-800"
            }`}
          >
            wiring {verdictOk ? "PASS" : "FAIL"}
          </span>
          {autoV && (
            <span className={readinessStyle[autoV] ?? ""}>{autoV}</span>
          )}
          {comp?.percent_done != null && (
            <span className="text-muted-foreground">
              {isAr ? "منجز" : "done"} {comp.done}/{comp.total} ({comp.percent_done}%)
            </span>
          )}
        </div>
      </div>
      {data?.no_build_rule_ar && (
        <p className="text-xs text-muted-foreground mb-2">{data.no_build_rule_ar}</p>
      )}
      {bridge?.research_verdict_ar && (
        <p className="text-xs text-muted-foreground mb-2 border-l-2 border-violet-400 pl-2">
          {bridge.research_verdict_ar}
        </p>
      )}
      {err && <p className="text-destructive text-xs mb-2">{err}</p>}
      {(st?.missing_paths?.length ?? 0) > 0 && (
        <p className="text-xs text-amber-700 mb-2">
          {isAr ? "مسارات ناقصة:" : "Missing:"} {st?.missing_paths?.join(", ")}
        </p>
      )}
      {(bridge?.founder_queue?.length ?? 0) > 0 && (
        <div className="mb-3 rounded-md bg-background/60 p-2">
          <p className="text-xs font-medium mb-1">
            {isAr ? "طابور المؤسس" : "Founder queue"}
          </p>
          <ul className="text-xs space-y-0.5 text-muted-foreground">
            {(bridge?.founder_queue ?? []).slice(0, 5).map((q) => (
              <li key={q.priority}>
                {q.priority}. {q.title_ar}
              </li>
            ))}
          </ul>
        </div>
      )}
      <button
        type="button"
        className="text-[10px] underline text-muted-foreground mb-2"
        onClick={() => setExpandAll((v) => !v)}
      >
        {expandAll
          ? isAr
            ? "طيّ الكل"
            : "Collapse all"
          : isAr
            ? "عرض كل الأقسام"
            : "Expand all"}
      </button>
      <div className="space-y-1 max-h-80 overflow-y-auto">
        {(data?.sections ?? []).map((sec) => {
          const sid = sec.id || "";
          const expanded = expandAll || openSection === sid;
          const count = sec.tasks?.length ?? 0;
          const doneInSec = (sec.tasks ?? []).filter((t) => t.completion?.done).length;
          return (
            <div key={sid} className="border rounded-md overflow-hidden">
              <button
                type="button"
                className="w-full text-start px-3 py-2 text-xs font-medium flex justify-between gap-2 hover:bg-muted/50"
                onClick={() => setOpenSection(expanded && !expandAll ? null : sid)}
              >
                <span>{sec.label_ar || sid}</span>
                <span className="text-muted-foreground">
                  {doneInSec}/{count}
                </span>
              </button>
              {expanded && (
                <ul className="px-3 pb-2 space-y-1">
                  {(sec.tasks ?? []).map((t) => {
                    const cs = t.completion?.status ?? "open";
                    return (
                      <li key={t.id || t.n} className="text-xs flex gap-2 justify-between">
                        <span className="text-muted-foreground flex-1">
                          <span className="font-mono text-foreground/80">{t.n}.</span>{" "}
                          {t.title_ar}
                        </span>
                        <span
                          className={`shrink-0 font-mono ${taskStatusStyle[cs] ?? ""}`}
                          title={t.completion?.reason_ar}
                        >
                          {statusLabel(cs, isAr)}
                        </span>
                      </li>
                    );
                  })}
                </ul>
              )}
            </div>
          );
        })}
      </div>
      {bridge?.commands?.unified_run && (
        <p className="text-[10px] font-mono mt-2 text-muted-foreground">
          {bridge.commands.unified_run}
        </p>
      )}
      {data?.completion_policy_ar && (
        <p className="text-[10px] text-muted-foreground mt-1">{data.completion_policy_ar}</p>
      )}
      {data?.policy_ar && (
        <p className="text-[10px] text-muted-foreground mt-2">{data.policy_ar}</p>
      )}
    </Card>
  );
}
