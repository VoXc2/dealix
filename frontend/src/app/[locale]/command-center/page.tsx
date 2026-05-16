"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useTranslations } from "next-intl";
import { motion } from "framer-motion";
import { RefreshCw, AlertTriangle, ShieldAlert } from "lucide-react";
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

export default function CommandCenterPage() {
  const t = useTranslations("commandCenter");
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
  const contactCount = Object.keys(snap.current_state_by_contact).length;

  const actions = useMemo(() => {
    const out: string[] = [];
    if (contactCount === 0) out.push(t("actionFirstFive"));
    if ((lc.L4 ?? 0) > 0 && (lc.L5 ?? 0) === 0) out.push(t("actionToMeeting"));
    if ((lc.L5 ?? 0) > 0 && (lc.L6 ?? 0) === 0) out.push(t("actionToScope"));
    if ((lc.L6 ?? 0) > 0 && (lc.L7 ?? 0) === 0) out.push(t("actionToInvoice"));
    if (snap.blocked_items.length > 0)
      out.push(t("actionResolveBlocked", { count: snap.blocked_items.length }));
    if (out.length === 0) out.push(t("actionHoldSteady"));
    return out.slice(0, 3);
  }, [contactCount, lc, snap.blocked_items.length, t]);

  const cards = [
    { key: "l4", value: lc.L4 ?? 0, color: "text-sky-400", bg: "bg-sky-400/10" },
    { key: "l5", value: lc.L5 ?? 0, color: "text-gold-400", bg: "bg-gold-400/10" },
    { key: "l6", value: lc.L6 ?? 0, color: "text-violet-400", bg: "bg-violet-400/10" },
    { key: "l7", value: lc.L7 ?? 0, color: "text-emerald-400", bg: "bg-emerald-400/10" },
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
        <h2 className="text-lg font-semibold mb-3">{t("levelCountsTitle")}</h2>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {cards.map((c, i) => (
            <motion.div
              key={c.key}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06 }}
              className={cn("rounded-2xl border border-border p-4", c.bg)}
            >
              <p className={cn("text-3xl font-bold", c.color)}>{c.value}</p>
              <p className="text-sm text-muted-foreground mt-1">{t(c.key)}</p>
            </motion.div>
          ))}
        </div>
      </section>

      <section className="mb-8">
        <div
          className={cn(
            "rounded-2xl border p-4",
            snap.revenue_confirmed
              ? "border-emerald-500/30 bg-emerald-500/10"
              : "border-border bg-muted/20",
          )}
        >
          <p className="text-sm font-semibold mb-1">
            {snap.revenue_confirmed
              ? `${t("revenueConfirmed")} — ${snap.contacts_with_confirmed_revenue} ${t("contactsConfirmed")}`
              : t("revenueConfirmed")}
          </p>
          {!snap.revenue_confirmed && (
            <p className="text-xs text-muted-foreground">{t("revenuePending")}</p>
          )}
        </div>
      </section>

      <section className="mb-8">
        <h2 className="text-lg font-semibold mb-3">{t("nextActionsTitle")}</h2>
        <ol className="space-y-2">
          {actions.map((a, i) => (
            <li
              key={i}
              className="flex items-start gap-3 rounded-xl border border-border bg-card p-3"
            >
              <span className="flex-shrink-0 w-6 h-6 rounded-lg bg-gold-400/15 text-gold-400 text-sm font-bold flex items-center justify-center">
                {i + 1}
              </span>
              <span className="text-sm">{a}</span>
            </li>
          ))}
        </ol>
      </section>

      <section className="mb-8">
        <h2 className="text-lg font-semibold mb-3 flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-gold-400" />
          {t("blockedTitle")}
        </h2>
        {snap.blocked_items.length === 0 ? (
          <p className="text-sm text-muted-foreground">{t("noBlocked")}</p>
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
        <div className="rounded-2xl border border-gold-500/30 bg-gold-500/5 p-4">
          <h3 className="text-sm font-semibold mb-1 flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-gold-400" />
            {t("noBuildTitle")}
          </h3>
          <p className="text-xs text-muted-foreground leading-relaxed">{t("noBuildBody")}</p>
        </div>
      </section>
    </AppLayout>
  );
}
