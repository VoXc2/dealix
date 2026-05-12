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

type Vertical = {
  id: string;
  label_ar: string;
  label_en: string;
  description_en: string;
  agents: string[];
  workflows: string[];
  pricing_default_plan: string;
};

export default function VerticalsPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const t = (ar: string, en: string) => (isAr ? ar : en);
  const [verts, setVerts] = useState<Vertical[]>([]);
  const [applying, setApplying] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/api/v1/verticals`, {
      headers: { accept: "application/json", ...authHeader() },
    })
      .then((r) => r.json())
      .then((d) => setVerts(d.verticals || []))
      .catch((e: any) => toast.error(e.message))
      .finally(() => setLoading(false));
  }, []);

  async function apply(vertical_id: string) {
    setApplying(vertical_id);
    try {
      const r = await fetch(`${API_BASE}/api/v1/verticals/apply`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          accept: "application/json",
          ...authHeader(),
        },
        body: JSON.stringify({ vertical_id }),
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      toast.success(t("تم اختيار القطاع", "Vertical applied"));
    } catch (e: any) {
      toast.error(e.message);
    } finally {
      setApplying(null);
    }
  }

  if (loading) return <div className="p-8">{t("جاري التحميل…", "Loading…")}</div>;

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-6">
      <header>
        <h1 className="text-3xl font-bold">{t("القطاعات", "Industry verticals")}</h1>
        <p className="text-muted-foreground mt-2">
          {t(
            "اختر قطاع لتفعيل الوكلاء والمسارات والتسعير المسبق.",
            "Pick a vertical to pre-configure agents, workflows, and pricing."
          )}
        </p>
      </header>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {verts.map((v) => (
          <article
            key={v.id}
            className="border border-border bg-card rounded-xl p-5 space-y-3"
          >
            <header className="flex justify-between items-baseline">
              <h2 className="font-bold text-lg">
                {isAr ? v.label_ar : v.label_en}
              </h2>
              <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700">
                {v.pricing_default_plan}
              </span>
            </header>
            <p className="text-sm text-muted-foreground">{v.description_en}</p>
            <div>
              <div className="text-xs text-muted-foreground mb-1">
                {t("الوكلاء", "Agents")}
              </div>
              <div className="flex flex-wrap gap-1">
                {v.agents.map((a) => (
                  <code
                    key={a}
                    className="text-xs px-2 py-0.5 rounded bg-muted text-foreground"
                  >
                    {a}
                  </code>
                ))}
              </div>
            </div>
            <div>
              <div className="text-xs text-muted-foreground mb-1">
                {t("المسارات", "Workflows")}
              </div>
              <div className="flex flex-wrap gap-1">
                {v.workflows.map((w) => (
                  <code
                    key={w}
                    className="text-xs px-2 py-0.5 rounded bg-muted text-foreground"
                  >
                    {w}
                  </code>
                ))}
              </div>
            </div>
            <button
              onClick={() => apply(v.id)}
              disabled={applying === v.id}
              className="w-full py-2 mt-2 bg-emerald-600 hover:bg-emerald-700 disabled:bg-emerald-300 text-white rounded-lg text-sm font-medium"
            >
              {applying === v.id
                ? t("جاري التطبيق…", "Applying…")
                : t("تفعيل هذا القطاع", "Apply this vertical")}
            </button>
          </article>
        ))}
      </div>
    </div>
  );
}
