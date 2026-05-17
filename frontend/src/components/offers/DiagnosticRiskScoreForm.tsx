"use client";

import { useMemo, useState } from "react";
import api from "@/lib/api";
import { Button } from "@/components/ui/button";

type RiskQuestionKey =
  | "has_crm"
  | "uses_ai"
  | "has_external_approval_gate"
  | "can_link_workflow_to_financial_outcome"
  | "follow_up_is_documented"
  | "source_clarity_for_decisions"
  | "has_evidence_pack";

interface RiskScoreResponse {
  risk_band: "low" | "medium" | "high";
  numeric_score: number;
  missing_controls: number;
  recommended_step: string;
  cta_primary: string;
  cta_secondary: string;
}

interface DiagnosticRiskScoreFormProps {
  locale: "ar" | "en";
}

const QUESTION_COPY: Record<
  RiskQuestionKey,
  { ar: string; en: string }
> = {
  has_crm: {
    ar: "1) هل عندكم CRM؟",
    en: "1) Do you have a CRM?",
  },
  uses_ai: {
    ar: "2) هل تستخدمون AI في المبيعات أو العمليات؟",
    en: "2) Are you using AI in sales or operations?",
  },
  has_external_approval_gate: {
    ar: "3) هل توجد موافقة قبل أي رسالة خارجية؟",
    en: "3) Do external messages require approval?",
  },
  can_link_workflow_to_financial_outcome: {
    ar: "4) هل تربطون workflow بنتيجة مالية قابلة للقياس؟",
    en: "4) Can you link workflows to financial outcomes?",
  },
  follow_up_is_documented: {
    ar: "5) هل الـfollow-up موثق؟",
    en: "5) Is follow-up documented?",
  },
  source_clarity_for_decisions: {
    ar: "6) هل تعرفون مصدر كل قرار؟",
    en: "6) Do you know the source behind each decision?",
  },
  has_evidence_pack: {
    ar: "7) هل عندكم evidence pack لمبادرات AI؟",
    en: "7) Do you keep an evidence pack for AI initiatives?",
  },
};

const QUESTION_ORDER: RiskQuestionKey[] = [
  "has_crm",
  "uses_ai",
  "has_external_approval_gate",
  "can_link_workflow_to_financial_outcome",
  "follow_up_is_documented",
  "source_clarity_for_decisions",
  "has_evidence_pack",
];

const INITIAL_VALUES: Record<RiskQuestionKey, boolean> = {
  has_crm: false,
  uses_ai: false,
  has_external_approval_gate: false,
  can_link_workflow_to_financial_outcome: false,
  follow_up_is_documented: false,
  source_clarity_for_decisions: false,
  has_evidence_pack: false,
};

export function DiagnosticRiskScoreForm({ locale }: DiagnosticRiskScoreFormProps) {
  const isAr = locale === "ar";
  const [values, setValues] = useState<Record<RiskQuestionKey, boolean>>(INITIAL_VALUES);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<RiskScoreResponse | null>(null);

  const formTitle = isAr ? "AI & Revenue Ops Risk Score" : "AI & Revenue Ops Risk Score";

  const riskBandLabel = useMemo(() => {
    if (!result) return "";
    if (isAr) {
      return {
        high: "مخاطر عالية",
        medium: "مخاطر متوسطة",
        low: "مخاطر منخفضة",
      }[result.risk_band];
    }
    return {
      high: "High risk",
      medium: "Medium risk",
      low: "Low risk",
    }[result.risk_band];
  }, [isAr, result]);

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await api.postSalesOpsRiskScore(values);
      setResult(response.data as RiskScoreResponse);
    } catch {
      setError(isAr ? "تعذر حساب النتيجة حالياً." : "Could not calculate score right now.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-2xl border border-border bg-card p-6 shadow-sm">
      <h3 className="text-xl font-semibold text-foreground">{formTitle}</h3>
      <p className="mt-2 text-sm text-muted-foreground">
        {isAr
          ? "اختر (نعم) لكل بند متحقق داخل فريقك."
          : "Mark each control that already exists in your team."}
      </p>

      <form onSubmit={onSubmit} className="mt-6 space-y-4">
        {QUESTION_ORDER.map((key) => (
          <label
            key={key}
            className="flex items-start gap-3 rounded-xl border border-border/80 p-3 hover:border-primary/40 transition-colors"
          >
            <input
              type="checkbox"
              checked={values[key]}
              onChange={(event) =>
                setValues((prev) => ({ ...prev, [key]: event.target.checked }))
              }
              className="mt-1 h-4 w-4 rounded border-border accent-primary"
            />
            <span className="text-sm text-foreground/90">
              {isAr ? QUESTION_COPY[key].ar : QUESTION_COPY[key].en}
            </span>
          </label>
        ))}

        <Button type="submit" disabled={loading} className="w-full sm:w-auto">
          {loading
            ? isAr
              ? "جارٍ الحساب..."
              : "Scoring..."
            : isAr
            ? "احسب النتيجة"
            : "Calculate score"}
        </Button>
      </form>

      {error && <p className="mt-4 text-sm text-red-400">{error}</p>}

      {result && (
        <div className="mt-6 rounded-xl border border-primary/30 bg-primary/5 p-4">
          <p className="text-sm text-muted-foreground">{isAr ? "التقييم" : "Assessment"}</p>
          <p className="mt-1 text-lg font-semibold text-foreground">{riskBandLabel}</p>
          <p className="mt-2 text-sm text-foreground/90">
            {isAr ? "الخطوة المقترحة:" : "Recommended step:"} {result.recommended_step}
          </p>
          <p className="mt-2 text-xs text-muted-foreground">
            {isAr ? "درجة المخاطر:" : "Risk score:"} {result.numeric_score}/100 ·{" "}
            {isAr ? "فجوات الضبط:" : "Missing controls:"} {result.missing_controls}
          </p>
        </div>
      )}
    </div>
  );
}
