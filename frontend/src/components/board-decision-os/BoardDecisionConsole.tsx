"use client";

import { useState } from "react";
import { useTranslations, useLocale } from "next-intl";
import { motion } from "framer-motion";
import { Star, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { DEFAULT_CUSTOMER_ID, type GateKey } from "@/lib/commercial";
import { GateStatusGrid, type GateState } from "@/components/commercial/GateStatusGrid";
import { CelBadge } from "@/components/commercial/CelBadge";

interface BoardOverview {
  north_star?: { metric?: string; count?: number; definition?: string };
  gates?: Partial<Record<GateKey, GateState>>;
  gates_passed?: string[];
  cel_summary?: {
    engagements?: number;
    by_cel?: Record<string, number>;
    by_state?: Record<string, number>;
  };
  governance_decision?: unknown;
}

export function BoardDecisionConsole() {
  const t = useTranslations("boardDecisionOs");
  const locale = useLocale();
  const isAr = locale === "ar";

  const [customerId, setCustomerId] = useState(DEFAULT_CUSTOMER_ID);
  const [busy, setBusy] = useState(false);
  const [overview, setOverview] = useState<BoardOverview | null>(null);

  const load = async () => {
    setBusy(true);
    try {
      const res = await api.getBoardDecisionOverview(customerId, false);
      setOverview(res.data as BoardOverview);
    } catch {
      toast.error(t("loadError"));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardContent className="pt-6 flex flex-wrap items-end gap-4">
          <div className="space-y-1.5 flex-1 min-w-[200px]">
            <Label htmlFor="bd-customer">{t("customerLabel")}</Label>
            <Input
              id="bd-customer"
              value={customerId}
              onChange={(e) => setCustomerId(e.target.value)}
            />
          </div>
          <Button onClick={load} disabled={busy}>
            <RefreshCw className={busy ? "w-4 h-4 me-1.5 animate-spin" : "w-4 h-4 me-1.5"} />
            {t("load")}
          </Button>
        </CardContent>
      </Card>

      {!overview ? (
        <p className="text-sm text-muted-foreground text-center py-12">
          {t("empty")}
        </p>
      ) : (
        <>
          {/* North Star */}
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
            <Card>
              <CardHeader>
                <CardTitle className="text-base flex items-center gap-2">
                  <Star className="w-4 h-4 text-gold-400" />
                  {t("northStarTitle")}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-5xl font-bold text-gold-400">
                  {overview.north_star?.count ?? 0}
                </p>
                <p className="text-sm text-foreground mt-2">
                  {overview.north_star?.metric ?? "—"}
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  {overview.north_star?.definition ?? ""}
                </p>
              </CardContent>
            </Card>
          </motion.div>

          {/* Gates */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base">{t("gatesTitle")}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <GateStatusGrid
                gates={overview.gates}
                passedGates={overview.gates_passed}
              />
              {overview.gates_passed && overview.gates_passed.length > 0 && (
                <p className="text-xs text-muted-foreground">
                  {t("gatesPassed")}: {overview.gates_passed.join(", ")}
                </p>
              )}
            </CardContent>
          </Card>

          {/* CEL summary */}
          <Card>
            <CardHeader>
              <CardTitle className="text-base">{t("celSummaryTitle")}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="rounded-xl border border-border p-4">
                <p className="text-xs text-muted-foreground">
                  {t("engagements")}
                </p>
                <p className="text-2xl font-bold text-foreground">
                  {overview.cel_summary?.engagements ?? 0}
                </p>
              </div>
              {overview.cel_summary?.by_cel && (
                <div>
                  <p className="text-xs font-medium text-muted-foreground mb-2">
                    {t("byCel")}
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(overview.cel_summary.by_cel).map(
                      ([cel, n]) => (
                        <div
                          key={cel}
                          className="flex items-center gap-1.5"
                        >
                          <CelBadge level={cel} showLabel={false} />
                          <span className="text-sm font-semibold text-foreground">
                            {n}
                          </span>
                        </div>
                      ),
                    )}
                  </div>
                </div>
              )}
              {overview.cel_summary?.by_state && (
                <div>
                  <p className="text-xs font-medium text-muted-foreground mb-2">
                    {t("byState")}
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(overview.cel_summary.by_state).map(
                      ([state, n]) => (
                        <Badge key={state} variant="outline" className="text-[10px]">
                          <span className="font-mono">{state}</span>
                          <span className="ms-1.5 font-semibold">{n}</span>
                        </Badge>
                      ),
                    )}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {overview.governance_decision != null && (
            <Card>
              <CardHeader>
                <CardTitle className="text-base">
                  {isAr ? "قرار الحوكمة" : "Governance decision"}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <pre className="text-[11px] bg-muted/40 rounded-lg p-3 overflow-auto max-h-64">
                  {JSON.stringify(overview.governance_decision, null, 2)}
                </pre>
              </CardContent>
            </Card>
          )}
        </>
      )}
    </div>
  );
}
