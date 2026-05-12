"use client";

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";

const API_BASE =
  (typeof window !== "undefined" && (window as any).__DEALIX_API_BASE__) ||
  process.env.NEXT_PUBLIC_API_BASE ||
  "";

export default function StatusPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const t = (ar: string, en: string) => (isAr ? ar : en);
  const [status, setStatus] = useState<any | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${API_BASE}/api/v1/status`, { headers: { accept: "application/json" } })
      .then(async (r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(setStatus)
      .catch((e: any) => setErr(e.message));
  }, []);

  if (err) {
    return (
      <div className="p-8 max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-2">{t("الحالة", "Status")}</h1>
        <div className="bg-card border border-rose-500/40 rounded-xl p-6 text-rose-500">{err}</div>
      </div>
    );
  }
  if (!status) return <div className="p-8">{t("جاري التحميل…", "Loading…")}</div>;

  const overall = String(status.status || "unknown").toLowerCase();
  const pillColor =
    overall === "ok" ? "text-emerald-500 bg-emerald-500/10" : overall === "degraded" ? "text-amber-500 bg-amber-500/10" : "text-rose-500 bg-rose-500/10";

  return (
    <div className="p-8 max-w-3xl mx-auto space-y-6">
      <header className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">{t("الحالة", "Status")}</h1>
        <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${pillColor}`}>{overall}</span>
      </header>
      <p className="text-sm text-muted-foreground">
        env=<code>{status.env}</code> · version=<code>{status.version}</code> · git=<code>{(status.git_sha || "").slice(0, 8)}</code>
      </p>
      <ul className="grid gap-3">
        {Object.entries(status.checks || {}).map(([k, v]: [string, any]) => {
          const s = String(v?.status || "unknown");
          const c = s === "ok" ? "text-emerald-500" : s === "fail" ? "text-rose-500" : "text-amber-500";
          return (
            <li key={k} className="bg-card border border-border rounded-xl p-3 flex justify-between">
              <span className="font-medium">{k}</span>
              <span className={c}>{s}</span>
            </li>
          );
        })}
      </ul>
      <p className="text-xs text-muted-foreground">
        SLA: <a href="/docs/sla.md" className="underline">docs/sla.md</a> · {t("الثقة:", "Trust:")}{" "}
        <a href="/trust" className="underline">trust pack</a>
      </p>
    </div>
  );
}
