"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";

export type ValuePlanTarget = {
  company?: string;
  status?: string;
  next_action_ar?: string;
};

export type ValuePlanPayload = {
  north_star?: { first_paid_verdict?: string; proof_packs_week?: number };
  evidence?: { today_total?: number; week_total?: number };
  evening?: { logged_today?: boolean; reminder_ar?: string };
  motion_a?: { targets?: ValuePlanTarget[]; focus_ar?: string[] };
  warnings_ar?: string[];
  targeting?: {
    agency_pool_rows?: number;
    min_rows_soft?: number;
    min_rows_soft_strict?: number;
    min_rows_wave2?: number;
    min_rows_wave3?: number;
    social_posts_target?: number;
    social_cycle_weeks?: number;
  };
  expansion_status?: {
    targeting?: {
      pool_rows?: number;
      wave2_ready?: boolean;
      wave3_prep_ready?: boolean;
      wave4_prep_ready?: boolean;
      motion_counts?: Record<string, number>;
    };
    social?: { posts?: number; cycle_weeks?: number; queue_ready_24w?: boolean };
    next_actions_ar?: string[];
  };
  commercial_value_map?: { doc_path?: string; market_intel_index?: string };
  first_paid_diagnostic?: {
    verdict?: string;
    payment_received_real?: number;
    proof_pack_delivered_real?: number;
  };
};

type Props = {
  valuePlan: ValuePlanPayload;
  variant?: "full" | "compact";
  showWarnings?: boolean;
};

export function ValuePlanPanel({ valuePlan, variant = "full", showWarnings = true }: Props) {
  const locale = useLocale();
  const isAr = locale === "ar";
  const verdict =
    valuePlan.first_paid_diagnostic?.verdict ?? valuePlan.north_star?.first_paid_verdict ?? "—";

  if (variant === "compact") {
    return (
      <Card className="p-3 border-emerald-500/30 bg-emerald-500/5">
        <p className="text-sm font-medium">
          {isAr ? "خطة القيمة" : "Value Plan"} · <span className="font-mono">{verdict}</span>
        </p>
        <p className="text-xs text-muted-foreground mt-1">
          {isAr ? "أدلة اليوم" : "Evidence"}: {valuePlan.evidence?.today_total ?? 0} ·{" "}
          {isAr ? "Proof أسبوع" : "Proof/wk"}: {valuePlan.north_star?.proof_packs_week ?? 0}
        </p>
        <Link href={`/${locale}/ops/founder`} className="text-xs text-primary underline mt-2 inline-block">
          {isAr ? "مركز المؤسس" : "Founder ops"}
        </Link>
      </Card>
    );
  }

  return (
    <>
      {showWarnings && (valuePlan.warnings_ar?.length ?? 0) > 0 && (
        <Card className="p-4 border-amber-500/40 bg-amber-500/5 mb-4">
          <h3 className="font-semibold mb-2 text-sm">
            {isAr ? "تنبيهات خريطة القيمة" : "Value map warnings"}
          </h3>
          <ul className="text-sm space-y-1 list-disc mr-5">
            {(valuePlan.warnings_ar ?? []).map((w) => (
              <li key={w}>{w}</li>
            ))}
          </ul>
        </Card>
      )}

      <Card className="p-4 border-emerald-500/30 bg-emerald-500/5">
        <h2 className="font-semibold mb-2">
          {isAr ? "خريطة القيمة (Motion A)" : "Commercial value map (Motion A)"}
        </h2>
        {valuePlan.targeting && (
          <p className="text-xs text-muted-foreground mb-2">
            {isAr ? "قائمة وكالات:" : "Agency pool:"} {valuePlan.targeting.agency_pool_rows ?? 0}
            {isAr ? " صف · سوشال " : " rows · social "}
            {valuePlan.targeting.social_posts_target ?? 120}
            {isAr ? " منشور / " : " posts / "}
            {valuePlan.targeting.social_cycle_weeks ?? 28}
            {isAr ? " أسبوع" : "w"}
          </p>
        )}
        {valuePlan.expansion_status?.targeting?.motion_counts && (
          <p className="text-xs text-muted-foreground mb-2">
            Motions: A={valuePlan.expansion_status.targeting.motion_counts.A ?? 0} · B=
            {valuePlan.expansion_status.targeting.motion_counts.B ?? 0} · C=
            {valuePlan.expansion_status.targeting.motion_counts.C ?? 0} · D=
            {valuePlan.expansion_status.targeting.motion_counts.D ?? 0}
          </p>
        )}
        {valuePlan.expansion_status && (
          <div className="text-xs rounded-md bg-sky-500/10 border border-sky-500/20 p-2 mb-2 space-y-1">
            <p>
              {isAr ? "موجة 2 (150):" : "Wave 2 (150):"}{" "}
              {valuePlan.expansion_status.targeting?.wave2_ready
                ? isAr
                  ? "جاهز"
                  : "ready"
                : isAr
                  ? "قيد التوسعة"
                  : "expand"}
              {" · "}
              {isAr ? "موجة 3 (200):" : "Wave 3 (200):"}{" "}
              {valuePlan.expansion_status.targeting?.wave3_prep_ready
                ? isAr
                  ? "جاهز"
                  : "ready"
                : "—"}
            </p>
            <ul className="list-disc mr-4">
              {(valuePlan.expansion_status.next_actions_ar ?? []).slice(0, 3).map((a) => (
                <li key={a}>{a}</li>
              ))}
            </ul>
          </div>
        )}
        <p className="text-sm mb-2">
          {isAr ? "بوابة Diagnostic:" : "Diagnostic gate:"}{" "}
          <span className="font-mono">{verdict}</span>
        </p>
        <div className="grid gap-2 sm:grid-cols-3 text-sm mt-2">
          <div>
            <p className="text-xs text-muted-foreground">{isAr ? "أدلة اليوم" : "Evidence today"}</p>
            <p className="font-semibold">{valuePlan.evidence?.today_total ?? 0}</p>
          </div>
          <div>
            <p className="text-xs text-muted-foreground">{isAr ? "Proof أسبوع" : "Proof week"}</p>
            <p className="font-semibold">{valuePlan.north_star?.proof_packs_week ?? 0}</p>
          </div>
          <div>
            <p className="text-xs text-muted-foreground">{isAr ? "دفع حقيقي" : "Real pay"}</p>
            <p className="font-semibold">{valuePlan.first_paid_diagnostic?.payment_received_real ?? 0}</p>
          </div>
        </div>
        {!valuePlan.evening?.logged_today && valuePlan.evening?.reminder_ar && (
          <p className="text-xs text-amber-700 dark:text-amber-400 mt-2">{valuePlan.evening.reminder_ar}</p>
        )}
        <ul className="text-sm space-y-1 mt-3 list-disc mr-5">
          {(valuePlan.motion_a?.targets ?? []).slice(0, 5).map((row) => (
            <li key={`${row.company}-${row.status}`}>
              <span className="font-medium">{row.company}</span>
              <span className="text-muted-foreground">
                {" "}
                · {row.status} — {row.next_action_ar}
              </span>
            </li>
          ))}
        </ul>
        <div className="flex flex-wrap gap-3 mt-3 text-xs">
          <Link href={`/${locale}/dealix-diagnostic`} className="text-primary underline">
            Diagnostic
          </Link>
          <Link href={`/${locale}/proof-pack`} className="text-primary underline">
            Proof Pack
          </Link>
          <Link href={`/${locale}/ops/war-room`} className="text-primary underline">
            {isAr ? "غرفة الإيراد" : "War Room"}
          </Link>
          <Link href={`/${locale}/ops/evidence`} className="text-primary underline">
            {isAr ? "الأدلة" : "Evidence"}
          </Link>
        </div>
      </Card>
    </>
  );
}
