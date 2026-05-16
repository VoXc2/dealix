"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useTranslations } from "next-intl";
import { RefreshCw } from "lucide-react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { api } from "@/lib/api";

interface BlockedItem {
  contact_id: string;
  from_state: string;
  to_state: string;
  reason: string;
}

interface Snapshot {
  level_counts: Record<string, number>;
  current_state_by_contact: Record<string, string>;
  blocked_items: BlockedItem[];
  contacts_with_confirmed_revenue: number;
  revenue_confirmed: boolean;
}

const EMPTY: Snapshot = {
  level_counts: { L4: 0, L5: 0, L6: 0, L7: 0 },
  current_state_by_contact: {},
  blocked_items: [],
  contacts_with_confirmed_revenue: 0,
  revenue_confirmed: false,
};

export default function BoardDecisionPage() {
  const t = useTranslations("boardDecision");
  const [snap, setSnap] = useState<Snapshot>(EMPTY);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getMarketProofSnapshot();
      setSnap({ ...EMPTY, ...(res.data as Snapshot) });
    } catch (e) {
      setError(e instanceof Error ? e.message : "load_failed");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const lc = snap.level_counts;

  const decisions = useMemo(() => {
    const out: string[] = [];
    if ((lc.L4 ?? 0) > 0) out.push(`${lc.L4} contact(s) at L4 — prioritise turning replies into meetings.`);
    if ((lc.L5 ?? 0) > 0) out.push(`${lc.L5} contact(s) at L5 — push for a scope or intro request.`);
    if ((lc.L6 ?? 0) > 0) out.push(`${lc.L6} contact(s) at L6 — issue invoices to close revenue.`);
    if (snap.blocked_items.length > 0)
      out.push(`${snap.blocked_items.length} blocked item(s) — clear governance gates before they age.`);
    if (out.length === 0) out.push("No active pipeline — fund first-market-proof outreach.");
    return out;
  }, [lc, snap.blocked_items.length]);

  const bhk = [
    { key: "build", color: "border-emerald-500/30 bg-emerald-500/5", label: "build", body: "buildBody" },
    { key: "hold", color: "border-gold-500/30 bg-gold-500/5", label: "hold", body: "holdBody" },
    { key: "kill", color: "border-destructive/30 bg-destructive/5", label: "kill", body: "killBody" },
  ] as const;

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <div className="flex items-center justify-between gap-3 mb-6">
        <Button variant="outline" size="sm" onClick={() => void load()} disabled={loading}>
          <RefreshCw className={cn("w-4 h-4 me-1", loading && "animate-spin")} />
          {t("refresh")}
        </Button>
        {error && <p className="text-xs text-destructive">{error}</p>}
      </div>

      <section className="mb-8">
        <h2 className="text-lg font-semibold mb-3">{t("revenueTitle")}</h2>
        <div className="rounded-2xl border border-border bg-card p-4">
          <p className="text-3xl font-bold text-emerald-400">
            {snap.contacts_with_confirmed_revenue}
          </p>
          <p className="text-sm text-muted-foreground mt-1">{t("revenueConfirmed")}</p>
          <p className="text-xs text-muted-foreground mt-2">{t("revenueNote")}</p>
        </div>
      </section>

      <section className="mb-8">
        <h2 className="text-lg font-semibold mb-3">{t("pipelineTitle")}</h2>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {(["L4", "L5", "L6", "L7"] as const).map((lvl) => (
            <div key={lvl} className="rounded-2xl border border-border bg-card p-4">
              <p className="text-2xl font-bold">{lc[lvl] ?? 0}</p>
              <p className="text-sm text-muted-foreground mt-1">{lvl}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mb-8">
        <h2 className="text-lg font-semibold mb-3">{t("decisionsTitle")}</h2>
        <ul className="space-y-2">
          {decisions.map((d, i) => (
            <li key={i} className="rounded-xl border border-border bg-card p-3 text-sm">
              {d}
            </li>
          ))}
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-lg font-semibold mb-3">{t("risksTitle")}</h2>
        {snap.blocked_items.length === 0 ? (
          <p className="text-sm text-muted-foreground">{t("noRisks")}</p>
        ) : (
          <ul className="space-y-2">
            {snap.blocked_items.map((b, i) => (
              <li key={i} className="rounded-xl border border-destructive/30 bg-destructive/5 p-3">
                <p className="text-sm font-medium">
                  {b.contact_id} · {b.from_state} → {b.to_state}
                </p>
                <p className="text-xs text-muted-foreground mt-1">{b.reason}</p>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section>
        <h2 className="text-lg font-semibold mb-3">{t("bhkTitle")}</h2>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {bhk.map((b) => (
            <div key={b.key} className={cn("rounded-2xl border p-4", b.color)}>
              <p className="text-sm font-bold mb-1">{t(b.label)}</p>
              <p className="text-xs text-muted-foreground leading-relaxed">{t(b.body)}</p>
            </div>
          ))}
        </div>
      </section>
    </AppLayout>
  );
}
