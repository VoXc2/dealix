"use client";

import { useCallback, useEffect, useState } from "react";
import { useTranslations } from "next-intl";
import { RefreshCw } from "lucide-react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { api } from "@/lib/api";

interface LedgerRecord {
  from_state: string;
  to_state: string;
  from_level: string | null;
  to_level: string | null;
  evidence_ref: string | null;
  revenue_counted: boolean;
  recorded_at: string;
}

export default function EvidenceLedgerPage() {
  const t = useTranslations("evidenceLedger");
  const [ledger, setLedger] = useState<Record<string, LedgerRecord[]>>({});
  const [levels, setLevels] = useState<unknown>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [lRes, evRes] = await Promise.all([
        api.getMarketProofLedger(),
        api.getEvidenceLevels().catch(() => ({ data: null })),
      ]);
      setLedger((lRes.data as { ledger?: Record<string, LedgerRecord[]> }).ledger ?? {});
      setLevels(evRes.data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "load_failed");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const contacts = Object.entries(ledger);

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <div className="flex items-center justify-between gap-3 mb-6">
        <Button variant="outline" size="sm" onClick={() => void load()} disabled={loading}>
          <RefreshCw className={cn("w-4 h-4 me-1", loading && "animate-spin")} />
          {t("refresh")}
        </Button>
        {error && <p className="text-xs text-destructive">{error}</p>}
      </div>

      <section className="mb-10">
        <h2 className="text-lg font-semibold mb-3">{t("ledgerTitle")}</h2>
        {loading ? (
          <p className="text-sm text-muted-foreground">…</p>
        ) : contacts.length === 0 ? (
          <p className="text-sm text-muted-foreground">{t("noLedger")}</p>
        ) : (
          <div className="space-y-5">
            {contacts.map(([cid, recs]) => (
              <div key={cid} className="rounded-2xl border border-border bg-card p-4">
                <p className="text-sm font-semibold mb-3">{cid}</p>
                <ol className="space-y-2">
                  {recs.map((r, i) => (
                    <li
                      key={i}
                      className="flex flex-wrap items-center gap-2 text-xs border-s-2 border-border ps-3"
                    >
                      <span className="font-mono">
                        {r.from_state} → {r.to_state}
                      </span>
                      {r.to_level && (
                        <Badge
                          variant="outline"
                          className={cn(r.revenue_counted && "text-emerald-400 border-emerald-400/40")}
                        >
                          {r.to_level}
                        </Badge>
                      )}
                      <span className="text-muted-foreground">
                        {r.evidence_ref ? `${t("evidenceRef")}: ${r.evidence_ref}` : t("noEvidenceRef")}
                      </span>
                      <span className="text-muted-foreground ms-auto">
                        {new Date(r.recorded_at).toLocaleString()}
                      </span>
                    </li>
                  ))}
                </ol>
              </div>
            ))}
          </div>
        )}
      </section>

      <section>
        <h2 className="text-lg font-semibold mb-3">{t("levelsTitle")}</h2>
        {levels ? (
          <pre className="text-xs bg-muted/40 rounded-xl p-4 overflow-auto max-h-[360px]">
            {JSON.stringify(levels, null, 2)}
          </pre>
        ) : (
          <p className="text-sm text-muted-foreground">—</p>
        )}
      </section>
    </AppLayout>
  );
}
