"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface SprintStep {
  name: string;
  status: string;
  output: Record<string, unknown>;
}

interface SprintSample {
  engagement_id: string;
  customer_id: string;
  proof_score: number;
  proof_tier: string;
  retainer_eligible: boolean;
  steps: SprintStep[];
  proof_pack?: {
    score?: number;
    tier?: string;
    sections?: Record<string, string>;
  };
}

const API_URL =
  typeof window !== "undefined"
    ? (process.env.NEXT_PUBLIC_API_URL ?? "https://api.dealix.me")
    : "https://api.dealix.me";

function ScoreBadge({ score, tier }: { score: number; tier: string }) {
  const color =
    score >= 70
      ? "border-emerald-500 text-emerald-700 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/30"
      : score >= 40
      ? "border-amber-500 text-amber-700 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/30"
      : "border-red-500 text-red-700 dark:text-red-400 bg-red-50 dark:bg-red-950/30";
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full border text-xs font-semibold ${color}`}>
      {score}/100 · {tier}
    </span>
  );
}

export default function DemoPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [data, setData] = useState<SprintSample | null>(null);
  const [loading, setLoading] = useState(true);
  const [elapsed, setElapsed] = useState<number>(0);

  useEffect(() => {
    const t0 = Date.now();
    fetch(`${API_URL}/api/v1/sprint/sample`)
      .then((r) => r.json())
      .then((d: SprintSample) => {
        setData(d);
        setElapsed(Date.now() - t0);
      })
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, []);

  const top10 = (data?.steps.find((s) => s.name === "account_scoring")?.output?.top_10 as Array<{
    rank: number;
    company_name: string;
    score: number;
    reasons: string[];
  }>) ?? [];

  const govSummary = (data?.steps.find((s) => s.name === "governance_review")?.output?.summary ?? {}) as Record<string, number>;

  const packSections = data?.proof_pack?.sections ?? {};

  return (
    <div className="min-h-screen bg-background" dir={isAr ? "rtl" : "ltr"}>
      <div className="max-w-5xl mx-auto px-4 py-12 space-y-10">
        {/* Hero */}
        <header>
          <Badge variant="outline" className="mb-3 text-xs">
            {isAr ? "عرض توضيحي حقيقي — بيانات سعودية حقيقية" : "Live Demo — Real Saudi B2B Data"}
          </Badge>
          <h1 className="text-3xl font-bold tracking-tight">
            {isAr
              ? "شاهد Dealix في ٦٠ ثانية"
              : "See Dealix in 60 Seconds"}
          </h1>
          <p className="mt-2 text-muted-foreground max-w-2xl">
            {isAr
              ? "هذا تشغيل حقيقي للـ Sprint على بيانات شركات سعودية. النتائج محكومة بـ governance ومحمية بـ Source Passport."
              : "This is a live Sprint run on real Saudi B2B company data. Results are governance-controlled and Source Passport protected."}
          </p>
        </header>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 gap-3">
            <div className="w-10 h-10 border-4 border-primary/30 border-t-primary rounded-full animate-spin" />
            <p className="text-sm text-muted-foreground">
              {isAr ? "جاري تشغيل Sprint التجريبي..." : "Running demo Sprint..."}
            </p>
          </div>
        ) : !data ? (
          <Card className="p-8 text-center text-muted-foreground">
            {isAr ? "تعذّر تحميل البيانات. تأكد من الاتصال." : "Could not load demo. Check your connection."}
          </Card>
        ) : (
          <div className="space-y-8">
            {/* Score summary */}
            <Card className="p-6">
              <div className="flex flex-wrap items-center gap-4">
                <div>
                  <p className="text-xs text-muted-foreground mb-1">
                    {isAr ? "درجة الإثبات" : "Proof Score"}
                  </p>
                  <ScoreBadge score={data.proof_score ?? 0} tier={data.proof_tier ?? "—"} />
                </div>
                <div>
                  <p className="text-xs text-muted-foreground mb-1">
                    {isAr ? "مؤهّل للـ Retainer" : "Retainer Eligible"}
                  </p>
                  <Badge variant={data.retainer_eligible ? "default" : "secondary"}>
                    {data.retainer_eligible ? (isAr ? "نعم ✓" : "Yes ✓") : (isAr ? "بعد Sprint" : "After Sprint")}
                  </Badge>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground mb-1">
                    {isAr ? "زمن التحميل" : "Load Time"}
                  </p>
                  <Badge variant="outline" className={elapsed < 500 ? "border-emerald-400 text-emerald-600" : "border-amber-400 text-amber-600"}>
                    {elapsed}ms {elapsed < 500 ? "⚡" : ""}
                  </Badge>
                </div>
                <div className="flex-1 flex justify-end">
                  <Button asChild size="sm">
                    <Link href={`/${locale}/offer/lead-intelligence-sprint`}>
                      {isAr ? "ابدأ Sprint 499 SAR ←" : "Start Sprint 499 SAR →"}
                    </Link>
                  </Button>
                </div>
              </div>
            </Card>

            {/* Top 10 Accounts */}
            {top10.length > 0 && (
              <section>
                <h2 className="text-lg font-semibold mb-3">
                  {isAr ? "أعلى ١٠ حسابات مُصنَّفة" : "Top 10 Scored Accounts"}
                </h2>
                <div className="space-y-2">
                  {top10.slice(0, 5).map((acc) => (
                    <div
                      key={acc.rank}
                      className="flex items-center gap-3 p-3 rounded-lg border border-border/50 bg-card/50"
                    >
                      <span className="w-7 h-7 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center flex-shrink-0">
                        {acc.rank}
                      </span>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium truncate">{acc.company_name}</p>
                        <div className="flex gap-1 mt-0.5">
                          {acc.reasons.map((r) => (
                            <Badge key={r} variant="secondary" className="text-xs py-0">
                              {r}
                            </Badge>
                          ))}
                        </div>
                      </div>
                      <div className="text-right flex-shrink-0">
                        <div className="flex items-center gap-1">
                          <div
                            className="h-1.5 rounded-full bg-primary/20"
                            style={{ width: 60 }}
                          >
                            <div
                              className="h-1.5 rounded-full bg-primary"
                              style={{ width: `${(acc.score / 100) * 60}px` }}
                            />
                          </div>
                          <span className="text-xs text-muted-foreground">{acc.score}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {/* Governance Summary */}
            {Object.keys(govSummary).length > 0 && (
              <section>
                <h2 className="text-lg font-semibold mb-3">
                  {isAr ? "ملخص قرارات الحوكمة" : "Governance Decision Summary"}
                </h2>
                <div className="flex flex-wrap gap-3">
                  {Object.entries(govSummary).map(([decision, count]) => (
                    <Card key={decision} className="p-4 min-w-[120px] text-center">
                      <p className="text-2xl font-bold">{count}</p>
                      <p className="text-xs text-muted-foreground mt-0.5">{decision.replace(/_/g, " ")}</p>
                    </Card>
                  ))}
                </div>
              </section>
            )}

            {/* Proof Pack Preview */}
            {packSections.executive_summary && (
              <Card className="p-6 border-primary/20">
                <h2 className="text-lg font-semibold mb-3">
                  {isAr ? "ملخص تنفيذي — Proof Pack" : "Executive Summary — Proof Pack"}
                </h2>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {packSections.executive_summary}
                </p>
                {packSections.recommended_next_step && (
                  <div className="mt-4 p-3 rounded-lg bg-primary/5 border border-primary/20">
                    <p className="text-xs font-semibold text-primary mb-1">
                      {isAr ? "الخطوة التالية الموصى بها" : "Recommended Next Step"}
                    </p>
                    <p className="text-sm">{packSections.recommended_next_step}</p>
                  </div>
                )}
              </Card>
            )}

            {/* Sprint Steps Status */}
            <section>
              <h2 className="text-lg font-semibold mb-3">
                {isAr ? "خطوات Sprint (١٠ خطوات)" : "Sprint Steps (10 Steps)"}
              </h2>
              <div className="space-y-1.5">
                {data.steps.map((step) => (
                  <div
                    key={step.name}
                    className="flex items-center gap-3 p-2.5 rounded-lg bg-muted/30"
                  >
                    <span className={`w-2 h-2 rounded-full flex-shrink-0 ${
                      step.status === "ran" ? "bg-emerald-500" :
                      step.status === "blocked" ? "bg-red-500" : "bg-amber-400"
                    }`} />
                    <p className="text-sm flex-1">{step.name.replace(/_/g, " ")}</p>
                    <Badge variant={step.status === "ran" ? "default" : "secondary"} className="text-xs">
                      {step.status}
                    </Badge>
                  </div>
                ))}
              </div>
            </section>

            {/* CTA Block */}
            <Card className="p-8 text-center bg-gradient-to-br from-primary/5 to-primary/10 border-primary/20">
              <h2 className="text-xl font-bold mb-2">
                {isAr ? "جاهز تشغّل هذا على بيانات شركتك؟" : "Ready to run this on your company data?"}
              </h2>
              <p className="text-muted-foreground text-sm mb-6">
                {isAr
                  ? "٧ أيام · Proof Pack PDF ثنائي اللغة · Company Brain v1 · ٤٩٩ ر.س فقط"
                  : "7 days · Bilingual PDF Proof Pack · Company Brain v1 · Only 499 SAR"}
              </p>
              <div className="flex flex-wrap gap-3 justify-center">
                <Button asChild size="lg" className="font-semibold">
                  <Link href={`/${locale}/offer/lead-intelligence-sprint`}>
                    {isAr ? "ابدأ Sprint الآن — ٤٩٩ ر.س" : "Start Sprint Now — 499 SAR"}
                  </Link>
                </Button>
                <Button asChild variant="outline" size="lg">
                  <Link href={`/${locale}/dealix-diagnostic`}>
                    {isAr ? "تشخيص مجاني أولاً" : "Free Diagnostic First"}
                  </Link>
                </Button>
              </div>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
}
