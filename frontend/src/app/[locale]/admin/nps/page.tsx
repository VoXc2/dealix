"use client";

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { toast } from "sonner";

type Response = { response: number | string; distinct_id: string; timestamp: string };

const API_BASE =
  (typeof window !== "undefined" && (window as any).__DEALIX_API_BASE__) ||
  process.env.NEXT_PUBLIC_API_BASE ||
  "";

function authHeader(): Record<string, string> {
  const t = typeof window !== "undefined" ? localStorage.getItem("dealix_access_token") : null;
  return t ? { Authorization: `Bearer ${t}` } : {};
}

function scoreBucket(s: number): "promoter" | "passive" | "detractor" {
  if (s >= 9) return "promoter";
  if (s >= 7) return "passive";
  return "detractor";
}

export default function NpsAdminPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [items, setItems] = useState<Response[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/api/v1/admin/nps/responses`, {
      headers: { accept: "application/json", ...authHeader() },
    })
      .then(async (r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((d) => setItems(d.items || []))
      .catch((err) => toast.error(err.message))
      .finally(() => setLoading(false));
  }, []);

  const t = (ar: string, en: string) => (isAr ? ar : en);
  const numeric = items
    .map((it) => Number(it.response))
    .filter((n) => !Number.isNaN(n) && n >= 0 && n <= 10);
  const promoters = numeric.filter((n) => n >= 9).length;
  const detractors = numeric.filter((n) => n <= 6).length;
  const nps = numeric.length
    ? Math.round(((promoters - detractors) / numeric.length) * 100)
    : null;

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">{t("درجة NPS", "NPS")}</h1>
      <section className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-card border border-border rounded-xl p-4">
          <div className="text-muted-foreground text-sm">{t("الردود", "Responses")}</div>
          <div className="text-3xl font-bold">{numeric.length}</div>
        </div>
        <div className="bg-card border border-border rounded-xl p-4">
          <div className="text-muted-foreground text-sm">NPS</div>
          <div className="text-3xl font-bold">{nps ?? "—"}</div>
        </div>
        <div className="bg-card border border-border rounded-xl p-4">
          <div className="text-muted-foreground text-sm">{t("مروّجون", "Promoters")}</div>
          <div className="text-3xl font-bold text-emerald-500">{promoters}</div>
        </div>
        <div className="bg-card border border-border rounded-xl p-4">
          <div className="text-muted-foreground text-sm">{t("منتقدون", "Detractors")}</div>
          <div className="text-3xl font-bold text-rose-500">{detractors}</div>
        </div>
      </section>

      {loading ? (
        <p>{t("جاري التحميل…", "Loading…")}</p>
      ) : (
        <table className="w-full text-sm bg-card border border-border rounded-xl">
          <thead className="text-muted-foreground text-left bg-muted">
            <tr>
              <th className="p-2">{t("التاريخ", "When")}</th>
              <th className="p-2">{t("الدرجة", "Score")}</th>
              <th className="p-2">{t("الفئة", "Bucket")}</th>
              <th className="p-2">{t("المعرّف", "ID")}</th>
            </tr>
          </thead>
          <tbody>
            {items.map((r, i) => {
              const score = Number(r.response);
              const bucket = Number.isNaN(score) ? "—" : scoreBucket(score);
              return (
                <tr key={i} className="border-t border-border">
                  <td className="p-2">{new Date(r.timestamp).toLocaleString(isAr ? "ar-SA" : "en-US")}</td>
                  <td className="p-2 font-medium">{String(r.response)}</td>
                  <td className="p-2 capitalize">{bucket}</td>
                  <td className="p-2 font-mono">{r.distinct_id}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}
    </div>
  );
}
