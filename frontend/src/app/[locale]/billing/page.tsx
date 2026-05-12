"use client";

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";

type Subscription = {
  tenant_id: string;
  name: string;
  plan: string;
  status: string;
  currency: string;
  max_users: number;
  max_leads_per_month: number;
  renewal_at: string;
  features: Record<string, any>;
  billing_provider: string;
};

type Invoice = {
  id: string;
  action: string;
  status: string;
  amount_sar?: number;
  amount_usd?: number;
  provider: string;
  issued_at: string;
};

const API_BASE =
  (typeof window !== "undefined" && (window as any).__DEALIX_API_BASE__) ||
  process.env.NEXT_PUBLIC_API_BASE ||
  "";

async function getJSON<T>(path: string): Promise<T> {
  const token =
    typeof window !== "undefined"
      ? localStorage.getItem("dealix_access_token")
      : null;
  const r = await fetch(`${API_BASE}${path}`, {
    headers: {
      accept: "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  });
  if (!r.ok) {
    const detail = await r.json().catch(() => ({}));
    throw new Error(detail?.detail || `request_failed_${r.status}`);
  }
  return (await r.json()) as T;
}

function getTenantIdFromToken(): string | null {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem("dealix_user");
  if (!raw) return null;
  try {
    return JSON.parse(raw).tenant_id || null;
  } catch {
    return null;
  }
}

export default function BillingPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [sub, setSub] = useState<Subscription | null>(null);
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const tenantId = getTenantIdFromToken();
    if (!tenantId) {
      setLoading(false);
      return;
    }
    Promise.all([
      getJSON<Subscription>(`/api/v1/customers/${tenantId}/subscription`),
      getJSON<{ invoices: Invoice[] }>(`/api/v1/customers/${tenantId}/invoices`),
    ])
      .then(([s, i]) => {
        setSub(s);
        setInvoices(i.invoices || []);
      })
      .catch((err) => toast.error(err.message))
      .finally(() => setLoading(false));
  }, []);

  const t = (ar: string, en: string) => (isAr ? ar : en);

  if (loading) {
    return (
      <div className="p-8 text-muted-foreground">
        {t("جاري التحميل…", "Loading…")}
      </div>
    );
  }
  if (!sub) {
    return (
      <div className="p-8">
        {t(
          "لم نتمكن من جلب بيانات الاشتراك — تسجل دخول مع حساب مرتبط بمستأجر.",
          "Could not load subscription — log in with a tenant-bound account."
        )}
      </div>
    );
  }

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold">{t("الفواتير والاشتراك", "Billing & subscription")}</h1>

      <section className="bg-card border border-border rounded-xl p-6">
        <h2 className="text-xl font-semibold mb-4">
          {t("اشتراكك الحالي", "Current subscription")}
        </h2>
        <dl className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <dt className="text-muted-foreground">{t("الباقة", "Plan")}</dt>
            <dd className="text-lg font-medium capitalize">{sub.plan}</dd>
          </div>
          <div>
            <dt className="text-muted-foreground">{t("الحالة", "Status")}</dt>
            <dd className="text-lg font-medium capitalize">{sub.status}</dd>
          </div>
          <div>
            <dt className="text-muted-foreground">{t("العملة", "Currency")}</dt>
            <dd className="text-lg font-medium">{sub.currency}</dd>
          </div>
          <div>
            <dt className="text-muted-foreground">{t("التجديد", "Renewal")}</dt>
            <dd className="text-lg font-medium">
              {new Date(sub.renewal_at).toLocaleDateString(isAr ? "ar-SA" : "en-US")}
            </dd>
          </div>
          <div>
            <dt className="text-muted-foreground">{t("الحد الأقصى للمستخدمين", "Max users")}</dt>
            <dd className="text-lg font-medium">{sub.max_users}</dd>
          </div>
          <div>
            <dt className="text-muted-foreground">{t("Leads/شهر", "Leads/month")}</dt>
            <dd className="text-lg font-medium">{sub.max_leads_per_month}</dd>
          </div>
          <div>
            <dt className="text-muted-foreground">{t("مزود الدفع", "Provider")}</dt>
            <dd className="text-lg font-medium capitalize">{sub.billing_provider}</dd>
          </div>
        </dl>
        <div className="mt-6 flex gap-3">
          <Button variant="default">{t("ترقية", "Upgrade")}</Button>
          <Button variant="outline">{t("تواصل مع المبيعات", "Contact sales")}</Button>
        </div>
      </section>

      <section className="bg-card border border-border rounded-xl p-6">
        <h2 className="text-xl font-semibold mb-4">{t("سجل الفواتير", "Invoice history")}</h2>
        {invoices.length === 0 ? (
          <p className="text-muted-foreground">
            {t("لا توجد فواتير بعد.", "No invoices yet.")}
          </p>
        ) : (
          <table className="w-full text-sm">
            <thead className="text-muted-foreground text-left">
              <tr>
                <th className="py-2">{t("المعرّف", "ID")}</th>
                <th className="py-2">{t("المبلغ", "Amount")}</th>
                <th className="py-2">{t("المزوّد", "Provider")}</th>
                <th className="py-2">{t("الحالة", "Status")}</th>
                <th className="py-2">{t("التاريخ", "Issued")}</th>
              </tr>
            </thead>
            <tbody>
              {invoices.map((inv) => (
                <tr key={inv.id} className="border-t border-border">
                  <td className="py-2 font-mono">{inv.id}</td>
                  <td className="py-2">
                    {inv.amount_sar
                      ? `${inv.amount_sar} SAR`
                      : inv.amount_usd
                      ? `${inv.amount_usd} USD`
                      : "—"}
                  </td>
                  <td className="py-2 capitalize">{inv.provider}</td>
                  <td className="py-2 capitalize">{inv.status}</td>
                  <td className="py-2">
                    {new Date(inv.issued_at).toLocaleDateString(isAr ? "ar-SA" : "en-US")}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
}
