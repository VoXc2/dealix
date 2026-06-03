"use client";

import Link from "next/link";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import api from "@/lib/api";
import { ValuePlanPanel, type ValuePlanPayload } from "@/components/gtm/ValuePlanPanel";
import { OpsExpansionStatusCard } from "@/components/gtm/OpsExpansionStatusCard";

const ADMIN_KEY =
  typeof window !== "undefined"
    ? process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY || ""
    : "";

const OPS_ROUTES = [
  { key: "opsFounder", href: "/ops/founder", descAr: "صباح واحد + تركيز اليوم", descEn: "Morning command + daily focus" },
  { key: "opsWarRoom", href: "/ops/war-room", descAr: "١٠ أهداف P0 دوّارة", descEn: "10 rotating P0 targets" },
  { key: "opsMarketing", href: "/ops/marketing", descAr: "مسودة سوشال + موافقة", descEn: "Social draft + approval" },
  { key: "opsSales", href: "/ops/sales", descAr: "خط المبيعات", descEn: "Sales pipeline" },
  { key: "approvals", href: "/ops/approvals", descAr: "مركز الموافقات", descEn: "Approval center" },
  { key: "opsEvidence", href: "/ops/evidence", descAr: "سجل الأدلة", descEn: "Evidence ledger" },
  { key: "opsPartners", href: "/ops/partners", descAr: "شركاء", descEn: "Partners" },
  { key: "opsSupport", href: "/ops/support", descAr: "دعم", descEn: "Support" },
] as const;

type HealthKpi = { key: string; value: number | null; computed: boolean };

export function OpsHubHealthCards() {
  const locale = useLocale();
  const t = useTranslations("nav");
  const tHub = useTranslations("opsHub");
  const isAr = locale === "ar";
  const [healthOk, setHealthOk] = useState<boolean | null>(null);
  const [kpis, setKpis] = useState<HealthKpi[]>([]);
  const [bridge7d, setBridge7d] = useState<number | null>(null);
  const [valuePlan, setValuePlan] = useState<ValuePlanPayload | null>(null);

  useEffect(() => {
    if (!ADMIN_KEY) {
      setHealthOk(null);
      setValuePlan(null);
      return;
    }
    api.getFounderValuePlan(ADMIN_KEY, 5).then((r) => setValuePlan(r.data as ValuePlanPayload)).catch(() => setValuePlan(null));
    api
      .getFullOpsHealth(ADMIN_KEY)
      .then((r) => {
        const data = r.data as {
          kpis?: HealthKpi[];
          bridge_events_total?: number;
          operational?: { bridge_events_7d?: number };
        };
        setKpis((data.kpis ?? []).slice(0, 4));
        setBridge7d(
          data.operational?.bridge_events_7d ??
            (typeof data.bridge_events_total === "number" ? data.bridge_events_total : null),
        );
        setHealthOk(true);
      })
      .catch(() => setHealthOk(false));
  }, []);

  return (
    <div className="space-y-6" dir={isAr ? "rtl" : "ltr"}>
      <Card className="p-4 border-primary/20">
        <p className="text-sm text-muted-foreground mb-2">
          {isAr ? "أمر الصباح:" : "Morning command:"}
        </p>
        <pre className="text-xs bg-muted/50 p-2 rounded overflow-x-auto" dir="ltr">
          bash scripts/run_founder_commercial_day.sh
        </pre>
        <p className="text-xs text-muted-foreground mt-2" dir="ltr">
          bash scripts/verify_dealix_commercial_go_live.sh
        </p>
      </Card>

      {valuePlan && <ValuePlanPanel valuePlan={valuePlan} variant="compact" />}

      {ADMIN_KEY && <OpsExpansionStatusCard />}

      {ADMIN_KEY && (
        <Card className="p-4">
          <div className="flex flex-wrap items-center gap-2 mb-3">
            <h2 className="font-semibold text-sm">{isAr ? "صحة التشغيل" : "Ops health"}</h2>
            {healthOk === true && (
              <Badge variant="outline" className="text-emerald-600">
                {tHub("healthLive")}
              </Badge>
            )}
            {healthOk === false && <Badge variant="destructive">{tHub("healthFailed")}</Badge>}
            {bridge7d != null && (
              <span className="text-xs text-muted-foreground">
                {tHub("bridge7d")}: {bridge7d}
              </span>
            )}
          </div>
          {kpis.length > 0 && (
            <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-4">
              {kpis.map((k) => (
                <div key={k.key} className="text-xs border rounded p-2">
                  <p className="text-muted-foreground truncate">{k.key}</p>
                  <p className="font-medium">
                    {k.computed && k.value != null ? k.value : "—"}
                  </p>
                </div>
              ))}
            </div>
          )}
        </Card>
      )}

      {!ADMIN_KEY && <p className="text-sm text-amber-600">{tHub("missingAdminKey")}</p>}

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {OPS_ROUTES.map((route) => (
          <Link key={route.href} href={`/${locale}${route.href}`}>
            <Card className="p-4 h-full hover:border-primary/40 transition-colors">
              <h2 className="font-semibold">{t(route.key)}</h2>
              <p className="text-sm text-muted-foreground mt-1">
                {isAr ? route.descAr : route.descEn}
              </p>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
