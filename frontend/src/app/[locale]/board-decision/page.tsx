"use client";

import { useCallback, useEffect, useState } from "react";
import { useTranslations } from "next-intl";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

type Json = Record<string, unknown>;
type RiskRow = { code: string; mitigation_decision: string };
type ClassifiedRow = { investment: string; bucket: string | null };

export default function BoardDecisionPage() {
  const t = useTranslations("boardDecision");
  const tc = useTranslations("common");

  const [overview, setOverview] = useState<Json | null>(null);
  const [risks, setRisks] = useState<RiskRow[]>([]);
  const [investments, setInvestments] = useState("");
  const [classified, setClassified] = useState<ClassifiedRow[]>([]);
  const [checkedSections, setCheckedSections] = useState<Set<string>>(new Set());
  const [memo, setMemo] = useState<Json | null>(null);
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    const [ov, rk] = await Promise.all([
      api.getBoardDecisionOverview(),
      api.getBoardDecisionRisks(),
    ]);
    setOverview(ov.data as Json);
    setRisks(((rk.data as Json).risk_register as RiskRow[]) ?? []);
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const memoSections = (overview?.memo_sections as string[]) ?? [];

  const toggleSection = (key: string) => {
    setCheckedSections((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });
  };

  const classify = async () => {
    setLoading(true);
    try {
      const res = await api.getBoardDecisionCapitalAllocation(investments.trim());
      setClassified(((res.data as Json).classified as ClassifiedRow[]) ?? []);
    } finally {
      setLoading(false);
    }
  };

  const checkMemo = async () => {
    setLoading(true);
    try {
      const res = await api.postBoardDecisionMemo([...checkedSections]);
      setMemo(res.data as Json);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <p className="text-sm text-muted-foreground mb-6">{t("readOnlyNote")}</p>

      <section className="mb-10">
        <h2 className="text-lg font-semibold mb-3">{t("overviewTitle")}</h2>
        {overview ? (
          <div className="grid gap-3 sm:grid-cols-3">
            {(["memo_section_count", "risk_count"] as const).map((k) => (
              <div
                key={k}
                className="rounded-xl border border-border bg-muted/20 p-4"
              >
                <p className="text-xl font-semibold">{String(overview[k] ?? 0)}</p>
                <p className="mt-1 text-xs text-muted-foreground">{k}</p>
              </div>
            ))}
            <div className="rounded-xl border border-border bg-muted/20 p-4">
              <p className="text-sm font-medium">
                {((overview.capital_buckets as string[]) ?? []).join(" · ")}
              </p>
              <p className="mt-1 text-xs text-muted-foreground">capital_buckets</p>
            </div>
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">{tc("loading")}</p>
        )}
      </section>

      <section className="mb-10">
        <h2 className="text-lg font-semibold mb-3">{t("risksTitle")}</h2>
        <div className="overflow-x-auto rounded-xl border border-border">
          <table className="w-full text-sm">
            <thead className="bg-muted/40 text-muted-foreground">
              <tr>
                <th className="px-4 py-2 text-start">{t("riskCode")}</th>
                <th className="px-4 py-2 text-start">{t("mitigation")}</th>
              </tr>
            </thead>
            <tbody>
              {risks.map((r) => (
                <tr key={r.code} className="border-t border-border">
                  <td className="px-4 py-2 font-medium">{r.code}</td>
                  <td className="px-4 py-2 text-muted-foreground">
                    {r.mitigation_decision}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="mb-10">
        <h2 className="text-lg font-semibold mb-3">{t("capitalTitle")}</h2>
        <p className="text-sm text-muted-foreground mb-3">{t("capitalHint")}</p>
        <div className="flex flex-wrap items-center gap-3">
          <Input
            value={investments}
            onChange={(e) => setInvestments(e.target.value)}
            placeholder="proof_pack_generator, scraping_engine"
            className="max-w-md"
          />
          <Button onClick={() => void classify()} disabled={loading}>
            {t("classify")}
          </Button>
        </div>
        {classified.length > 0 && (
          <ul className="mt-4 space-y-1 text-sm">
            {classified.map((c) => (
              <li key={c.investment} className="flex gap-2">
                <span className="font-medium">{c.investment}</span>
                <span className="text-gold-400">
                  → {c.bucket ?? tc("noData")}
                </span>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section>
        <h2 className="text-lg font-semibold mb-3">{t("memoTitle")}</h2>
        <p className="text-sm text-muted-foreground mb-3">{t("memoHint")}</p>
        <div className="grid gap-2 sm:grid-cols-2">
          {memoSections.map((s) => (
            <label key={s} className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={checkedSections.has(s)}
                onChange={() => toggleSection(s)}
              />
              {s}
            </label>
          ))}
        </div>
        <Button
          className="mt-4"
          onClick={() => void checkMemo()}
          disabled={loading}
        >
          {t("checkMemo")}
        </Button>
        {memo && (
          <div className="mt-4 rounded-xl border border-border bg-muted/20 p-4 text-sm">
            {memo.complete ? (
              <p className="text-emerald-500">{t("complete")}</p>
            ) : (
              <div>
                <p className="font-medium">{t("incomplete")}</p>
                <p className="mt-1 text-muted-foreground">
                  {((memo.missing_sections as string[]) ?? []).join(", ")}
                </p>
              </div>
            )}
          </div>
        )}
      </section>
    </AppLayout>
  );
}
