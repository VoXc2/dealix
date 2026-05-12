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

function tenantIdFromStorage(): string {
  if (typeof window === "undefined") return "";
  const raw = localStorage.getItem("dealix_user");
  if (!raw) return "";
  try {
    return JSON.parse(raw).tenant_id ?? "";
  } catch {
    return "";
  }
}

export default function TrialExpiredPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const t = (ar: string, en: string) => (isAr ? ar : en);
  const [loading, setLoading] = useState<string | null>(null);
  const tenantId = typeof window !== "undefined" ? tenantIdFromStorage() : "";

  useEffect(() => {
    // Fire one-time Loops + Knock event so the founder sees the conversion attempt.
    fetch(`${API_BASE}/api/v1/trial/upgrade-clicked`, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...authHeader() },
      body: JSON.stringify({ tenant_id: tenantId }),
    }).catch(() => {});
  }, [tenantId]);

  async function checkout(gateway: "stripe" | "moyasar") {
    setLoading(gateway);
    try {
      const path =
        gateway === "stripe"
          ? "/api/v1/billing/checkout/stripe"
          : "/api/v1/pricing/checkout";
      const r = await fetch(`${API_BASE}${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...authHeader() },
        body: JSON.stringify({
          tenant_id: tenantId,
          plan: "growth",
          amount_cents: 49900 * 12, // SAR 499 × 12 months
          currency: gateway === "stripe" ? "usd" : "sar",
          email: "",
          success_url: window.location.origin + "/checkout/ok",
          cancel_url: window.location.origin + "/trial-expired",
          mode: "subscription",
        }),
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const data = await r.json();
      const url = data.checkout_url || data.session?.url || data.url;
      if (url) window.location.assign(url);
      else toast.error(t("لا يوجد رابط دفع", "No checkout URL"));
    } catch (e: any) {
      toast.error(e.message);
    } finally {
      setLoading(null);
    }
  }

  return (
    <main className="min-h-screen flex items-center justify-center p-8 bg-gradient-to-br from-emerald-50 to-teal-50">
      <div className="max-w-xl bg-white border border-border rounded-2xl p-8 shadow-sm text-center">
        <div className="text-6xl mb-4">⏱️</div>
        <h1 className="text-3xl font-bold mb-2">
          {t("انتهت فترة التجربة", "Your trial has ended")}
        </h1>
        <p className="text-muted-foreground mb-6">
          {t(
            "تابع رحلتك مع Dealix بخطة Growth — وكلاء AI، فواتير ZATCA، WhatsApp، وامتثال PDPL مدمج.",
            "Keep the momentum on the Growth plan — AI agents, ZATCA invoicing, WhatsApp, and built-in PDPL compliance."
          )}
        </p>
        <div className="text-3xl font-bold text-emerald-700 mb-1">SAR 499 / seat / mo</div>
        <p className="text-sm text-muted-foreground mb-6">
          {t("اشتراك سنوي يوفّر 17%", "Annual billing saves 17%")}
        </p>

        <div className="flex flex-col gap-2">
          <button
            onClick={() => checkout("moyasar")}
            disabled={loading !== null}
            className="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 disabled:bg-emerald-300 text-white rounded-lg font-medium"
          >
            {loading === "moyasar"
              ? t("جاري التحويل…", "Redirecting…")
              : t("ادفع بالريال (Moyasar + Mada + Tabby)", "Pay in SAR (Moyasar + Mada + Tabby)")}
          </button>
          <button
            onClick={() => checkout("stripe")}
            disabled={loading !== null}
            className="px-6 py-3 bg-slate-800 hover:bg-slate-900 disabled:bg-slate-500 text-white rounded-lg font-medium"
          >
            {loading === "stripe"
              ? t("جاري التحويل…", "Redirecting…")
              : t("ادفع بالعملة الدولية (Stripe)", "Pay internationally (Stripe)")}
          </button>
          <a
            href="mailto:sales@ai-company.sa"
            className="px-6 py-3 border border-border rounded-lg text-sm hover:bg-muted"
          >
            {t("تواصل مع المبيعات", "Talk to sales")}
          </a>
        </div>

        <p className="text-xs text-muted-foreground mt-6">
          {t(
            "بياناتك محفوظة. ستستعيد الوصول الكامل خلال دقيقة من الدفع.",
            "Your data is preserved. Full access restored within a minute of payment."
          )}
        </p>
      </div>
    </main>
  );
}
