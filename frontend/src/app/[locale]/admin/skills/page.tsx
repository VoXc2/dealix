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

type Skill = {
  id: string;
  path: string;
  description: string;
  inputs: string[];
  output_shape: string;
};

export default function SkillsCatalogPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const t = (ar: string, en: string) => (isAr ? ar : en);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    fetch(`${API_BASE}/api/v1/skills`, {
      headers: { accept: "application/json", ...authHeader() },
    })
      .then((r) => r.json())
      .then((d) => setSkills(d.skills || []))
      .catch((e: any) => toast.error(e.message))
      .finally(() => setLoading(false));
  }, []);

  const filtered = skills.filter(
    (s) =>
      !filter ||
      s.id.toLowerCase().includes(filter.toLowerCase()) ||
      s.description.toLowerCase().includes(filter.toLowerCase())
  );

  if (loading) return <div className="p-8">{t("جاري التحميل…", "Loading…")}</div>;

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-6">
      <header>
        <h1 className="text-3xl font-bold">{t("مكتبة المهارات", "Skills catalogue")}</h1>
        <p className="text-muted-foreground mt-2">
          {t(
            "كل مهارة تنشر كأداة MCP ويستعملها صانع الوكلاء.",
            "Every skill is exposed as an MCP tool and reusable by the agent builder."
          )}
        </p>
      </header>
      <input
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        placeholder={t("بحث…", "Search…")}
        className="w-full px-3 py-2 border border-border rounded-lg bg-card"
      />
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {filtered.map((s) => (
          <article
            key={s.id}
            className="border border-border bg-card rounded-xl p-4 space-y-2"
          >
            <header className="flex justify-between items-baseline">
              <h2 className="font-bold text-lg">{s.id}</h2>
              <code className="text-xs text-muted-foreground">{s.path}</code>
            </header>
            <p className="text-sm">{s.description}</p>
            <div className="flex flex-wrap gap-1">
              {s.inputs.map((i) => (
                <span
                  key={i}
                  className="text-xs px-2 py-0.5 rounded-full bg-muted text-muted-foreground"
                >
                  {i}
                </span>
              ))}
            </div>
            <code className="block text-xs text-muted-foreground break-all">
              → {s.output_shape}
            </code>
          </article>
        ))}
      </div>
      {filtered.length === 0 && (
        <p className="text-muted-foreground text-center py-8">
          {t("لا نتائج.", "No results.")}
        </p>
      )}
    </div>
  );
}
