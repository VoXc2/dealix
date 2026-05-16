"use client";

import { useCallback, useEffect, useState } from "react";
import { useTranslations, useLocale } from "next-intl";
import { motion } from "framer-motion";
import { Clock, CheckCircle2, ShieldCheck } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { api } from "@/lib/api";
import {
  HEADLINE_OFFER_IDS,
  type ServiceOffering,
} from "@/lib/commercial";
import { PriceRange } from "@/components/commercial/PriceRange";

function OfferingCard({
  offering,
  index,
  headline,
}: {
  offering: ServiceOffering;
  index: number;
  headline?: boolean;
}) {
  const t = useTranslations("servicesCatalog");
  const locale = useLocale();
  const isAr = locale === "ar";

  const name = isAr ? offering.name_ar : offering.name_en;
  const kpi = isAr ? offering.kpi_commitment_ar : offering.kpi_commitment_en;
  const refund = isAr ? offering.refund_policy_ar : offering.refund_policy_en;

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.06 }}
    >
      <Card className={headline ? "border-gold-500/30" : ""}>
        <CardHeader>
          <div className="flex items-start justify-between gap-3">
            <CardTitle className="text-base leading-snug">{name}</CardTitle>
            <PriceRange offering={offering} />
          </div>
          {offering.is_estimate && (
            <Badge
              variant="outline"
              className="mt-1 w-fit text-[10px] border-orange-500/30 bg-orange-500/10 text-orange-400"
            >
              {t("estimate")}
            </Badge>
          )}
        </CardHeader>
        <CardContent className="space-y-3">
          {offering.duration_days != null && (
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <Clock className="w-3.5 h-3.5" />
              <span>
                {t("duration")}: {offering.duration_days} {t("days")}
              </span>
            </div>
          )}

          {offering.deliverables.length > 0 && (
            <div>
              <p className="text-xs font-medium text-foreground mb-1.5">
                {t("deliverables")}
              </p>
              <ul className="space-y-1">
                {offering.deliverables.map((d, i) => (
                  <li
                    key={i}
                    className="flex items-start gap-1.5 text-xs text-muted-foreground"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 mt-0.5 flex-shrink-0" />
                    <span>{d}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {kpi && (
            <div>
              <p className="text-xs font-medium text-foreground">
                {t("kpiCommitment")}
              </p>
              <p className="text-xs text-muted-foreground">{kpi}</p>
            </div>
          )}

          {refund && (
            <div>
              <p className="text-xs font-medium text-foreground">
                {t("refundPolicy")}
              </p>
              <p className="text-xs text-muted-foreground">{refund}</p>
            </div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}

export function ServiceCatalog() {
  const t = useTranslations("servicesCatalog");
  const [offerings, setOfferings] = useState<ServiceOffering[]>([]);
  const [hardGates, setHardGates] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getServices();
      const data = res.data as {
        offerings?: ServiceOffering[];
        hard_gates?: string[];
      };
      setOfferings(Array.isArray(data.offerings) ? data.offerings : []);
      setHardGates(Array.isArray(data.hard_gates) ? data.hard_gates : []);
    } catch {
      setError(t("loadError"));
    } finally {
      setLoading(false);
    }
  }, [t]);

  useEffect(() => {
    void load();
  }, [load]);

  const headline = HEADLINE_OFFER_IDS.map((id) =>
    offerings.find((o) => o.id === id),
  ).filter((o): o is ServiceOffering => Boolean(o));

  const rest = offerings.filter((o) => !HEADLINE_OFFER_IDS.includes(o.id));

  if (loading) {
    return <p className="text-sm text-muted-foreground">…</p>;
  }

  if (error) {
    return <p className="text-sm text-destructive">{error}</p>;
  }

  if (offerings.length === 0) {
    return <p className="text-sm text-muted-foreground">{t("empty")}</p>;
  }

  return (
    <div className="space-y-8">
      {headline.length > 0 && (
        <section>
          <h2 className="text-sm font-semibold text-foreground mb-3">
            {t("headlineTitle")}
          </h2>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            {headline.map((o, i) => (
              <OfferingCard key={o.id} offering={o} index={i} headline />
            ))}
          </div>
        </section>
      )}

      {rest.length > 0 && (
        <section>
          <Separator className="mb-6" />
          <h2 className="text-sm font-semibold text-foreground mb-3">
            {t("moreTitle")}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {rest.map((o, i) => (
              <OfferingCard key={o.id} offering={o} index={i} />
            ))}
          </div>
        </section>
      )}

      {hardGates.length > 0 && (
        <section className="rounded-xl border border-border bg-muted/30 p-4">
          <h3 className="text-sm font-semibold text-foreground flex items-center gap-2 mb-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            {t("hardGatesTitle")}
          </h3>
          <ul className="space-y-1">
            {hardGates.map((g, i) => (
              <li key={i} className="text-xs text-muted-foreground">
                · {g}
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
