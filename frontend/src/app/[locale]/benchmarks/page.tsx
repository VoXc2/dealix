"use client";

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { toast } from "sonner";

type Benchmark = {
  sector: string;
  metric: string;
  customer_value: number | null;
  p50: number | null;
  p75: number | null;
  p90: number | null;
  unit: string;
};

const API_BASE =
  (typeof window !== "undefined" && (window as any).__DEALIX_API_BASE__) ||
  process.env.NEXT_PUBLIC_API_BASE ||
  "";

function authHeader(): Record<string, string> {
  const t = typeof window !== "undefined" ? localStorage.getItem("dealix_access_token") : null;
  return t ? { Authorization: `Bearer ${t}` } : {};
}

export default function BenchmarksPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [rows, setRows] = useState<Benchmark[]>([]);
  const [source, setSource] = useState<string>("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/api/v1/benchmarks/sector`, {
      headers: { accept: "application/json", ...authHeader() },
    })
      .then(async (r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then((d) => {
        setRows(d.rows || []);
        setSource(d.source || "");
      })
      .catch((err) => toast.error(err.message))
      .finally(() => setLoading(false));
  }, []);

  const t = (ar: string, en: string) => (isAr ? ar : en);

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      <header>
        <h1 className="text-3xl font-bold">{t("معايير قطاعك", "Sector benchmarks")}</h1>
        <p className="text-sm text-muted-foreground">
          {t("مصدر البيانات:", "Source:")} <code>{source || "fallback"}</code>
        </p>
      </header>

      {loading ? (
        <p>{t("جاري التحميل…", "Loading…")}</p>
      ) : rows.length === 0 ? (
        <p className="text-muted-foreground">
          {t(
            "لم تتوفر بيانات كافية لمقارنة قطاعك بعد.",
            "Not enough sector data to compare yet."
          )}
        </p>
      ) : (
        <div className="overflow-x-auto bg-card border border-border rounded-xl">
          <table className="w-full text-sm">
            <thead className="text-muted-foreground text-left bg-muted">
              <tr>
                <th className="p-2">{t("القطاع", "Sector")}</th>
                <th className="p-2">{t("المقياس", "Metric")}</th>
                <th className="p-2">{t("قيمتك", "You")}</th>
                <th className="p-2">P50</th>
                <th className="p-2">P75</th>
                <th className="p-2">P90</th>
                <th className="p-2">{t("الوحدة", "Unit")}</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r, i) => (
                <tr key={i} className="border-t border-border">
                  <td className="p-2">{r.sector}</td>
                  <td className="p-2">{r.metric}</td>
                  <td className="p-2 font-medium">
                    {r.customer_value != null ? r.customer_value : "—"}
                  </td>
                  <td className="p-2">{r.p50 ?? "—"}</td>
                  <td className="p-2">{r.p75 ?? "—"}</td>
                  <td className="p-2">{r.p90 ?? "—"}</td>
                  <td className="p-2">{r.unit}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
