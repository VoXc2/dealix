"use client";

import Link from "next/link";
import { useLocale, useTranslations } from "next-intl";
import { Card } from "@/components/ui/card";

const LINKS = [
  { hrefKey: "founder", path: "/ops/founder" },
  { hrefKey: "warRoom", path: "/ops/war-room" },
  { hrefKey: "diagnostic", path: "/dealix-diagnostic" },
  { hrefKey: "riskScore", path: "/risk-score" },
  { hrefKey: "businessNow", path: "/business-now" },
] as const;

export function CommercialValueMapStrip() {
  const t = useTranslations("businessNow.valueMap");
  const locale = useLocale();

  return (
    <Card className="p-4 border-emerald-500/25 bg-emerald-500/5">
      <h2 className="text-lg font-semibold mb-1">{t("title")}</h2>
      <p className="text-sm text-muted-foreground mb-3">{t("subtitle")}</p>
      <div className="flex flex-wrap gap-3 text-sm">
        {LINKS.map((item) => (
          <Link
            key={item.path}
            href={`/${locale}${item.path}`}
            className="text-primary underline"
          >
            {t(`links.${item.hrefKey}`)}
          </Link>
        ))}
      </div>
      <p className="text-xs text-muted-foreground mt-3 font-mono">{t("docHint")}</p>
    </Card>
  );
}
