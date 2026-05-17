"use client";

import { useParams, useSearchParams } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const COPY = {
  en: {
    dir: "ltr" as const,
    title: "Partner Dashboard",
    enterId: "Enter your partner ID",
    load: "Load",
    notFound: "Partner not found.",
    status: "Status",
    tier: "Tier",
    score: "Score",
    link: "Your referral link",
    noLink: "No referral link yet — issued after approval.",
    earned: "Earned",
    pending: "Pending",
    paid: "Paid",
    clawedBack: "Clawed back",
    referrals: "Referrals",
    company: "Company",
    refStatus: "Status",
    commissions: "Commissions",
    amount: "Amount (SAR)",
    none: "Nothing here yet.",
  },
  ar: {
    dir: "rtl" as const,
    title: "لوحة الشريك",
    enterId: "أدخل معرّف الشريك الخاص بك",
    load: "عرض",
    notFound: "الشريك غير موجود.",
    status: "الحالة",
    tier: "المستوى",
    score: "التقييم",
    link: "رابط الإحالة الخاص بك",
    noLink: "لا يوجد رابط إحالة بعد — يُصدر بعد القبول.",
    earned: "المكتسب",
    pending: "قيد الانتظار",
    paid: "المدفوع",
    clawedBack: "المُسترد",
    referrals: "الإحالات",
    company: "الشركة",
    refStatus: "الحالة",
    commissions: "العمولات",
    amount: "المبلغ (ريال)",
    none: "لا يوجد شيء بعد.",
  },
};

interface Dashboard {
  partner: { display_name: string; status: string; tier: string; score: number };
  links: { code: string }[];
  referrals: {
    affiliate_referral_id: string;
    lead_company: string;
    status: string;
  }[];
  commissions: {
    commission_id: string;
    commission_sar: number;
    status: string;
  }[];
  totals_sar: {
    earned: number;
    pending: number;
    paid: number;
    clawed_back: number;
  };
}

export default function PartnerDashboardPage() {
  const params = useParams();
  const search = useSearchParams();
  const locale = params?.locale === "ar" ? "ar" : "en";
  const t = COPY[locale];

  const [partnerId, setPartnerId] = useState(search?.get("id") || "");
  const [data, setData] = useState<Dashboard | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const load = useCallback(async (id: string) => {
    if (!id.trim()) return;
    setLoading(true);
    setError("");
    setData(null);
    try {
      const res = await fetch(
        `${API_BASE}/api/v1/affiliates/partners/${encodeURIComponent(
          id.trim(),
        )}/dashboard`,
      );
      if (res.status === 404) throw new Error("notfound");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setData((await res.json()) as Dashboard);
    } catch (e) {
      setError(e instanceof Error && e.message === "notfound" ? "" : String(e));
      if (e instanceof Error && e.message === "notfound") setError("notfound");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const id = search?.get("id");
    if (id) void load(id);
  }, [search, load]);

  const stat =
    "rounded-xl border border-border bg-muted/40 p-4 text-center";

  return (
    <div className="min-h-screen bg-background grid-pattern">
      <div className="mx-auto max-w-3xl px-6 py-16" dir={t.dir}>
        <h1 className="text-3xl font-bold tracking-tight text-foreground">
          {t.title}
        </h1>

        <div className="mt-6 flex gap-2">
          <input
            className="w-full rounded-lg border border-border bg-background px-3 py-2 text-sm"
            placeholder={t.enterId}
            value={partnerId}
            onChange={(e) => setPartnerId(e.target.value)}
          />
          <button
            type="button"
            onClick={() => void load(partnerId)}
            disabled={loading}
            className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-primary-foreground disabled:opacity-50"
          >
            {t.load}
          </button>
        </div>

        {error === "notfound" && (
          <p className="mt-4 text-sm text-red-500">{t.notFound}</p>
        )}
        {error && error !== "notfound" && (
          <p className="mt-4 text-sm text-red-500">{error}</p>
        )}

        {data && (
          <div className="mt-8 space-y-8">
            <div>
              <h2 className="text-lg font-semibold text-foreground">
                {data.partner.display_name}
              </h2>
              <p className="text-sm text-muted-foreground">
                {t.status}: {data.partner.status} · {t.tier}:{" "}
                {data.partner.tier || "—"} · {t.score}: {data.partner.score}
              </p>
            </div>

            <div>
              <h3 className="text-sm font-semibold text-foreground">
                {t.link}
              </h3>
              {data.links[0] ? (
                <code className="mt-1 block rounded bg-muted px-2 py-1 text-sm">
                  https://dealix.me/partners/go?code={data.links[0].code}
                </code>
              ) : (
                <p className="text-sm text-muted-foreground">{t.noLink}</p>
              )}
            </div>

            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
              <div className={stat}>
                <p className="text-xs text-muted-foreground">{t.earned}</p>
                <p className="text-lg font-semibold">
                  {data.totals_sar.earned}
                </p>
              </div>
              <div className={stat}>
                <p className="text-xs text-muted-foreground">{t.pending}</p>
                <p className="text-lg font-semibold">
                  {data.totals_sar.pending}
                </p>
              </div>
              <div className={stat}>
                <p className="text-xs text-muted-foreground">{t.paid}</p>
                <p className="text-lg font-semibold">{data.totals_sar.paid}</p>
              </div>
              <div className={stat}>
                <p className="text-xs text-muted-foreground">
                  {t.clawedBack}
                </p>
                <p className="text-lg font-semibold">
                  {data.totals_sar.clawed_back}
                </p>
              </div>
            </div>

            <div>
              <h3 className="mb-2 text-sm font-semibold text-foreground">
                {t.referrals}
              </h3>
              {data.referrals.length ? (
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-muted-foreground">
                      <th className="py-1 text-start">{t.company}</th>
                      <th className="py-1 text-start">{t.refStatus}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.referrals.map((r) => (
                      <tr
                        key={r.affiliate_referral_id}
                        className="border-t border-border"
                      >
                        <td className="py-1">{r.lead_company}</td>
                        <td className="py-1">{r.status}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <p className="text-sm text-muted-foreground">{t.none}</p>
              )}
            </div>

            <div>
              <h3 className="mb-2 text-sm font-semibold text-foreground">
                {t.commissions}
              </h3>
              {data.commissions.length ? (
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-muted-foreground">
                      <th className="py-1 text-start">{t.amount}</th>
                      <th className="py-1 text-start">{t.refStatus}</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.commissions.map((c) => (
                      <tr
                        key={c.commission_id}
                        className="border-t border-border"
                      >
                        <td className="py-1">{c.commission_sar}</td>
                        <td className="py-1">{c.status}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <p className="text-sm text-muted-foreground">{t.none}</p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
