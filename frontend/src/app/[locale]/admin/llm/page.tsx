"use client";

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { toast } from "sonner";

const API_BASE =
  (typeof window !== "undefined" && (window as any).__DEALIX_API_BASE__) ||
  process.env.NEXT_PUBLIC_API_BASE ||
  "";

function authHeader(): Record<string, string> {
  const t = typeof window !== "undefined" ? localStorage.getItem("dealix_access_token") : null;
  return t ? { Authorization: `Bearer ${t}` } : {};
}

function tenantIdFromStorage(): string | null {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem("dealix_user");
  if (!raw) return null;
  try {
    return JSON.parse(raw).tenant_id ?? null;
  } catch {
    return null;
  }
}

export default function LlmUsageAdminPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const t = (ar: string, en: string) => (isAr ? ar : en);
  const [usage, setUsage] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const tid = tenantIdFromStorage();

  useEffect(() => {
    if (!tid) {
      setLoading(false);
      return;
    }
    fetch(`${API_BASE}/api/v1/customers/${tid}/llm/usage`, {
      headers: { accept: "application/json", ...authHeader() },
    })
      .then(async (r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(setUsage)
      .catch((e: any) => toast.error(e.message))
      .finally(() => setLoading(false));
  }, [tid]);

  if (loading) return <div className="p-8">{t("جاري التحميل…", "Loading…")}</div>;
  if (!usage) return <div className="p-8">{t("لا بيانات", "No data")}</div>;

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">{t("استخدام النماذج", "LLM usage")}</h1>
      <section className="grid grid-cols-1 md:grid-cols-4 gap-3">
        <div className="bg-card border border-border rounded-xl p-3">
          <div className="text-muted-foreground text-xs">{t("الإنفاق اليوم", "Today")}</div>
          <div className="text-2xl font-bold">${usage.spent_today_usd}</div>
        </div>
        <div className="bg-card border border-border rounded-xl p-3">
          <div className="text-muted-foreground text-xs">{t("النافذة", "Window")}</div>
          <div className="text-2xl font-bold">${usage.total_usd_window}</div>
        </div>
        <div className="bg-card border border-border rounded-xl p-3">
          <div className="text-muted-foreground text-xs">{t("سقف الطلب", "Per-request cap")}</div>
          <div className="text-2xl font-bold">${usage.per_request_cap_usd}</div>
        </div>
        <div className="bg-card border border-border rounded-xl p-3">
          <div className="text-muted-foreground text-xs">{t("سقف اليوم", "Day cap")}</div>
          <div className="text-2xl font-bold">${usage.tenant_day_cap_usd}</div>
        </div>
      </section>
      <section>
        <h2 className="font-semibold mb-2">{t("التفصيل بالنموذج", "By model")}</h2>
        {(usage.by_model || []).length === 0 ? (
          <p className="text-muted-foreground text-sm">{t("لا استخدام في النافذة.", "No usage in window.")}</p>
        ) : (
          <table className="w-full text-sm bg-card border border-border rounded-xl">
            <thead className="bg-muted text-muted-foreground text-left">
              <tr>
                <th className="p-2">{t("المزود", "Provider")}</th>
                <th className="p-2">{t("النموذج", "Model")}</th>
                <th className="p-2">{t("الطلبات", "Calls")}</th>
                <th className="p-2">{t("التوكنات", "Tokens")}</th>
                <th className="p-2">{t("التكلفة", "Cost (USD)")}</th>
              </tr>
            </thead>
            <tbody>
              {usage.by_model.map((r: any, i: number) => (
                <tr key={i} className="border-t border-border">
                  <td className="p-2">{r.provider}</td>
                  <td className="p-2">{r.model}</td>
                  <td className="p-2">{r.calls}</td>
                  <td className="p-2">{r.tokens.toLocaleString()}</td>
                  <td className="p-2">${r.cost_usd}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
}
