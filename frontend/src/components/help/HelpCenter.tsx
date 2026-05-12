"use client";

/**
 * Slide-out help drawer. Searches the docs / SDK examples and
 * surfaces the support form + status link in one place.
 */

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";

type SearchHit = { id: string; type: string; text: string };

const API_BASE =
  (typeof window !== "undefined" && (window as any).__DEALIX_API_BASE__) ||
  process.env.NEXT_PUBLIC_API_BASE ||
  "";

function authHeader(): Record<string, string> {
  const t = typeof window !== "undefined" ? localStorage.getItem("dealix_access_token") : null;
  return t ? { Authorization: `Bearer ${t}` } : {};
}

export function HelpCenter(): JSX.Element {
  const locale = useLocale();
  const isAr = locale === "ar";
  const t = (ar: string, en: string) => (isAr ? ar : en);
  const [open, setOpen] = useState(false);
  const [q, setQ] = useState("");
  const [hits, setHits] = useState<SearchHit[]>([]);
  const [loading, setLoading] = useState(false);

  async function search(query: string) {
    if (!query.trim()) {
      setHits([]);
      return;
    }
    setLoading(true);
    try {
      const r = await fetch(
        `${API_BASE}/api/v1/search?q=${encodeURIComponent(query)}&kind=docs`,
        { headers: { accept: "application/json", ...authHeader() } }
      );
      const data = await r.json();
      setHits(data.hits || []);
    } catch {
      setHits([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    const id = setTimeout(() => search(q), 250);
    return () => clearTimeout(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [q]);

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="text-sm px-3 py-1 rounded hover:bg-muted"
        aria-label={t("المساعدة", "Help")}
      >
        {t("المساعدة", "Help")}
      </button>
      {open && (
        <div
          role="dialog"
          className="fixed inset-0 z-50 bg-black/40 flex"
          onClick={() => setOpen(false)}
        >
          <div
            className="ml-auto w-full max-w-md h-full bg-card border-l border-border p-6 overflow-y-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <header className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">{t("مركز المساعدة", "Help center")}</h2>
              <button onClick={() => setOpen(false)} className="text-muted-foreground">
                ✕
              </button>
            </header>
            <input
              type="search"
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder={t("ابحث في الوثائق…", "Search docs…")}
              className="w-full bg-background border border-border rounded-lg px-3 py-2 text-sm mb-3"
            />
            {loading && <p className="text-xs text-muted-foreground">{t("جاري…", "Searching…")}</p>}
            <ul className="space-y-2 text-sm">
              {hits.map((h) => (
                <li key={h.id} className="bg-muted/40 rounded p-2">
                  <div className="font-medium">{h.text}</div>
                  <div className="text-xs text-muted-foreground">{h.type}</div>
                </li>
              ))}
            </ul>
            <hr className="my-4 border-border" />
            <div className="space-y-2 text-sm">
              <a className="text-emerald-500 underline block" href={`/${locale}/support`}>
                {t("افتح تذكرة دعم", "Open a support ticket")}
              </a>
              <a className="text-emerald-500 underline block" href={`/${locale}/status`}>
                {t("لوحة الحالة", "Status board")}
              </a>
              <a
                className="text-emerald-500 underline block"
                href="https://docs.dealix.sa"
                target="_blank"
                rel="noreferrer"
              >
                {t("توثيق API كامل", "Full API docs")}
              </a>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
