"use client";

import { Card } from "@/components/ui/card";
import { useLocale } from "next-intl";

export type AutopilotQueueItem = {
  priority?: number;
  title_ar?: string;
  command?: string;
  kind?: string;
  blocking?: boolean;
};

export type FounderAutopilotPayload = {
  verdict?: { level?: string; summary_ar?: string; policy_ar?: string };
  queue?: AutopilotQueueItem[];
  customer_stage?: { band?: string; focus_ar?: string; paid_customers_real?: number };
  pls_readiness?: { verdict?: string; recommendation_ar?: string; signals_met?: number };
  benchmark_ar?: string;
};

type Props = {
  autopilot: FounderAutopilotPayload | null | undefined;
};

const levelClass: Record<string, string> = {
  GREEN: "text-emerald-600",
  YELLOW: "text-amber-600",
  RED: "text-destructive",
};

export function OpsFounderAutopilotPanel({ autopilot }: Props) {
  const locale = useLocale();
  const isAr = locale === "ar";
  if (!autopilot?.verdict) return null;

  const v = autopilot.verdict;
  const level = v.level ?? "YELLOW";
  const queue = autopilot.queue ?? [];
  const stage = autopilot.customer_stage;
  const pls = autopilot.pls_readiness;

  return (
    <Card className="p-4 space-y-3 border-primary/20">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h2 className="text-lg font-semibold">
          {isAr ? "تشغيل ذاتي كامل (حوكمة)" : "Full autopilot (governed)"}
        </h2>
        <span className={`text-sm font-mono font-semibold ${levelClass[level] ?? ""}`}>
          {level}
        </span>
      </div>
      <p className="text-sm text-muted-foreground">{v.summary_ar}</p>

      {stage && (
        <p className="text-xs text-muted-foreground">
          {isAr ? "شريحة:" : "Stage:"}{" "}
          <span className="font-medium text-foreground">{stage.band}</span>
          {" — "}
          {stage.focus_ar}
          {typeof stage.paid_customers_real === "number" && (
            <span className="ms-2">({stage.paid_customers_real} paid)</span>
          )}
        </p>
      )}

      {pls && (
        <p className="text-xs text-muted-foreground">
          PLS: <span className="font-medium">{pls.verdict}</span> — {pls.recommendation_ar}
        </p>
      )}

      {queue.length > 0 && (
        <ol className="list-decimal list-inside text-sm space-y-1">
          {queue.map((item) => (
            <li key={item.priority}>
              <span className={item.blocking ? "font-medium" : ""}>{item.title_ar}</span>
              {item.command && (
                <code className="block text-xs text-muted-foreground mt-0.5 truncate">
                  {item.command}
                </code>
              )}
            </li>
          ))}
        </ol>
      )}

      {autopilot.benchmark_ar && (
        <p className="text-[10px] text-muted-foreground leading-snug">{autopilot.benchmark_ar}</p>
      )}
    </Card>
  );
}
