"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { AppLayout } from "@/components/layout/AppLayout";
import { api } from "@/lib/api";

interface PortalData {
  promise_ar?: string;
  promise_en?: string;
  sprint_status?: string;
  proof_score?: number;
  proof_tier?: string;
  retainer_eligible?: boolean;
  top_decisions?: string[];
  proof_pack_ready?: boolean;
  engagement_id?: string;
  [key: string]: unknown;
}

export default function CustomerPortalPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [handle, setHandle] = useState("Slot-A");
  const [data, setData] = useState<PortalData | null>(null);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const res = await api.getCustomerPortal(handle.trim() || "Slot-A");
      setData(res.data as PortalData);
    } catch {
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  const proofPackUrl = data?.engagement_id
    ? `${process.env.NEXT_PUBLIC_API_URL ?? "https://api.dealix.me"}/api/v1/sprint/render/pdf`
    : null;

  return (
    <AppLayout
      title={isAr ? "بوابة العميل" : "Customer Portal"}
      subtitle={isAr ? "Sprint Status · Proof Pack · قرارات الإيراد" : "Sprint Status · Proof Pack · Revenue Decisions"}
    >
      {/* Handle Lookup */}
      <div className="flex flex-wrap gap-3 items-end mb-8">
        <div className="flex flex-col gap-1">
          <label className="text-xs text-muted-foreground">
            {isAr ? "معرّف الحساب (Customer Handle)" : "Customer Handle"}
          </label>
          <Input
            value={handle}
            onChange={(e) => setHandle(e.target.value)}
            placeholder="Slot-A"
            className="w-64"
            onKeyDown={(e) => e.key === "Enter" && void load()}
          />
        </div>
        <Button onClick={() => void load()} disabled={loading}>
          {loading ? (isAr ? "جاري التحميل..." : "Loading...") : (isAr ? "تحميل" : "Load")}
        </Button>
      </div>

      {!data && !loading && (
        <Card className="p-8 text-center text-muted-foreground">
          <p className="text-4xl mb-3">📊</p>
          <p>{isAr ? "أدخل معرّف حسابك لعرض بيانات Sprint" : "Enter your customer handle to view Sprint data"}</p>
        </Card>
      )}

      {data && (
        <div className="space-y-6" dir={isAr ? "rtl" : "ltr"}>
          {/* Promise / Status Banner */}
          {(data.promise_ar || data.promise_en) && (
            <Card className="p-5 border-primary/20 bg-primary/5">
              <h3 className="text-sm font-semibold mb-2 text-primary">
                {isAr ? "الوعد التجاري" : "Commercial Promise"}
              </h3>
              <p className="text-sm leading-relaxed">
                {isAr ? data.promise_ar : (data.promise_en ?? data.promise_ar)}
              </p>
            </Card>
          )}

          {/* Sprint Status Card */}
          <Card className="p-6">
            <h3 className="font-semibold mb-4">
              {isAr ? "حالة Sprint" : "Sprint Status"}
            </h3>
            <div className="flex flex-wrap gap-4">
              {data.sprint_status && (
                <div>
                  <p className="text-xs text-muted-foreground mb-1">{isAr ? "الحالة" : "Status"}</p>
                  <Badge variant={data.sprint_status === "completed" ? "default" : "secondary"}>
                    {data.sprint_status}
                  </Badge>
                </div>
              )}
              {data.proof_score !== undefined && (
                <div>
                  <p className="text-xs text-muted-foreground mb-1">{isAr ? "درجة الإثبات" : "Proof Score"}</p>
                  <span className="text-2xl font-bold">{data.proof_score}</span>
                  <span className="text-muted-foreground text-sm">/100</span>
                </div>
              )}
              {data.proof_tier && (
                <div>
                  <p className="text-xs text-muted-foreground mb-1">{isAr ? "المستوى" : "Tier"}</p>
                  <Badge variant="outline">{data.proof_tier}</Badge>
                </div>
              )}
              {data.retainer_eligible !== undefined && (
                <div>
                  <p className="text-xs text-muted-foreground mb-1">{isAr ? "مؤهّل للـ Retainer" : "Retainer Eligible"}</p>
                  <Badge variant={data.retainer_eligible ? "default" : "secondary"}>
                    {data.retainer_eligible ? "✓" : "—"}
                  </Badge>
                </div>
              )}
            </div>
          </Card>

          {/* Top 3 Decisions */}
          {Array.isArray(data.top_decisions) && data.top_decisions.length > 0 && (
            <Card className="p-6">
              <h3 className="font-semibold mb-4">
                {isAr ? "أعلى ٣ قرارات موصى بها" : "Top 3 Recommended Decisions"}
              </h3>
              <div className="space-y-3">
                {data.top_decisions.slice(0, 3).map((decision, i) => (
                  <div key={i} className="flex gap-3 p-3 rounded-lg bg-muted/30">
                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-primary/10 text-primary text-xs font-bold flex items-center justify-center">
                      {i + 1}
                    </span>
                    <p className="text-sm">{decision}</p>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Proof Pack Download */}
          <Card className="p-6 border-emerald-500/20 bg-emerald-50/30 dark:bg-emerald-950/20">
            <div className="flex items-center justify-between flex-wrap gap-4">
              <div>
                <h3 className="font-semibold text-emerald-800 dark:text-emerald-300">
                  {isAr ? "Proof Pack PDF" : "Proof Pack PDF"}
                </h3>
                <p className="text-sm text-muted-foreground mt-1">
                  {isAr
                    ? "تقرير ثنائي اللغة بنتائج Sprint + قرارات الإيراد"
                    : "Bilingual Sprint results + revenue decisions report"}
                </p>
              </div>
              <div className="flex gap-2">
                {proofPackUrl && (
                  <form
                    method="post"
                    action={proofPackUrl}
                    target="_blank"
                  >
                    <input type="hidden" name="customer_handle" value={handle} />
                    <input type="hidden" name="engagement_id" value={String(data.engagement_id ?? "proof_pack")} />
                    <Button type="submit" size="sm" className="bg-emerald-600 hover:bg-emerald-700">
                      {isAr ? "تحميل PDF ↓" : "Download PDF ↓"}
                    </Button>
                  </form>
                )}
                <Button asChild variant="outline" size="sm">
                  <Link href={`/${locale}/proof-pack`}>
                    {isAr ? "عرض الملخص" : "View Summary"}
                  </Link>
                </Button>
              </div>
            </div>
          </Card>

          {/* Upgrade CTA */}
          {data.retainer_eligible && (
            <Card className="p-6 text-center bg-gradient-to-br from-primary/5 to-primary/10 border-primary/20">
              <p className="font-bold text-lg mb-2">
                {isAr ? "🎉 أنت مؤهّل للـ Retainer الشهري!" : "🎉 You're eligible for monthly Retainer!"}
              </p>
              <p className="text-sm text-muted-foreground mb-4">
                {isAr
                  ? "استمر في تحسين إيراداتك مع Dealix Managed Ops — ٢,٩٩٩ - ٤,٩٩٩ ر.س/شهر"
                  : "Continue improving revenue with Dealix Managed Ops — 2,999-4,999 SAR/month"}
              </p>
              <Button asChild>
                <Link href={`/${locale}/offer`}>
                  {isAr ? "عرض خيارات الـ Retainer" : "View Retainer Options"}
                </Link>
              </Button>
            </Card>
          )}

          {/* Raw Data (collapsed) */}
          <details className="text-xs">
            <summary className="cursor-pointer text-muted-foreground hover:text-foreground">
              {isAr ? "عرض البيانات الخام" : "View raw data"}
            </summary>
            <pre className="mt-2 bg-muted/40 rounded-xl p-4 overflow-auto max-h-64">
              {JSON.stringify(data, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </AppLayout>
  );
}
