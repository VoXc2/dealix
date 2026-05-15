"use client";

import { useCallback, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const DEMO_KEY = process.env.NEXT_PUBLIC_DEMO_API_KEY || "";

type SprintToolsPanelProps = {
  locale: string;
};

export default function SprintToolsPanel({ locale }: SprintToolsPanelProps) {
  const enabled = process.env.NEXT_PUBLIC_SHOW_OPERATIONAL_TOOLS === "1";
  const [log, setLog] = useState<string>("");
  const isAr = locale === "ar";

  const headers = useCallback(() => {
    const h: Record<string, string> = { "Content-Type": "application/json" };
    if (DEMO_KEY) h["X-API-Key"] = DEMO_KEY;
    return h;
  }, []);

  const runSample = useCallback(
    async (path: string, body: unknown) => {
      setLog(isAr ? "جاري التشغيل…" : "Running…");
      try {
        const res = await fetch(`${API_BASE}${path}`, {
          method: "POST",
          headers: headers(),
          body: JSON.stringify(body),
        });
        const json = await res.json();
        setLog(JSON.stringify(json, null, 2).slice(0, 4000));
      } catch (e) {
        setLog(String(e));
      }
    },
    [headers, isAr],
  );

  if (!enabled) return null;

  return (
    <div className="mt-10 rounded-lg border border-dashed border-border bg-muted/30 p-5 text-start" dir={isAr ? "rtl" : "ltr"}>
      <p className="text-sm font-semibold text-foreground">
        {isAr ? "أدوات تشغيل تجريبية (مفعّلة عبر البيئة)" : "Operational tools (env-gated)"}
      </p>
      <p className="mt-1 text-xs text-muted-foreground">
        NEXT_PUBLIC_SHOW_OPERATIONAL_TOOLS=1 — {isAr ? "لا إرسال خارجي؛ تقارير فقط." : "No external send; reports only."}
      </p>
      <div className="mt-4 flex flex-wrap gap-2">
        <button
          type="button"
          className="rounded-md bg-secondary px-3 py-1.5 text-xs font-medium text-secondary-foreground"
          onClick={() =>
            runSample("/api/v1/commercial/engagements/lead-intelligence-sprint", {
              accounts: [{ company_name: "Demo", sector: "tech", city: "Riyadh" }],
            })
          }
        >
          Lead Intelligence
        </button>
        <button
          type="button"
          className="rounded-md bg-secondary px-3 py-1.5 text-xs font-medium text-secondary-foreground"
          onClick={() =>
            runSample("/api/v1/commercial/engagements/support-desk-sprint", {
              messages: ["أريد استرداد المبلغ"],
            })
          }
        >
          Support Desk
        </button>
        <button
          type="button"
          className="rounded-md bg-secondary px-3 py-1.5 text-xs font-medium text-secondary-foreground"
          onClick={() =>
            runSample("/api/v1/revenue-data/csv-preview", {
              csv_text: "company_name,sector,city\nX,saas,Jeddah\n",
            })
          }
        >
          CSV preview
        </button>
      </div>
      {log ? (
        <pre className="mt-4 max-h-64 overflow-auto rounded bg-background p-3 text-xs text-foreground">{log}</pre>
      ) : null}
    </div>
  );
}
