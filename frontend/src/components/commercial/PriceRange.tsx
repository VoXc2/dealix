"use client";

import { useLocale } from "next-intl";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { ServiceOffering } from "@/lib/commercial";

function fmt(n: number, locale: string): string {
  return new Intl.NumberFormat(locale === "ar" ? "ar-SA" : "en-US").format(n);
}

interface PriceRangeProps {
  offering: Pick<
    ServiceOffering,
    "price_mode" | "price_sar" | "price_sar_min" | "price_sar_max" | "price_unit"
  >;
  className?: string;
}

/**
 * Renders an offering's price honouring the pricing doctrine:
 *  - `range`            -> "4,999 - 25,000 SAR"
 *  - `recommended_draft`-> a localized "quoted per scope" pill (never a number)
 *  - `fixed`            -> the single confirmed number
 * A `recommended_draft` offering NEVER renders a fabricated single number.
 */
export function PriceRange({ offering, className }: PriceRangeProps) {
  const locale = useLocale();
  const isAr = locale === "ar";
  const sar = isAr ? "ريال" : "SAR";

  const unitSuffix =
    offering.price_unit === "per_month"
      ? isAr
        ? " / شهرياً"
        : " / month"
      : "";

  if (offering.price_mode === "recommended_draft") {
    return (
      <Badge
        variant="outline"
        className={cn(
          "border-violet-500/30 bg-violet-500/10 text-violet-400 text-xs",
          className,
        )}
      >
        {isAr ? "يُسعّر حسب النطاق" : "Quoted per scope"}
      </Badge>
    );
  }

  if (
    offering.price_mode === "range" &&
    offering.price_sar_min != null &&
    offering.price_sar_max != null
  ) {
    return (
      <span className={cn("text-sm font-semibold text-foreground", className)}>
        {fmt(offering.price_sar_min, locale)} – {fmt(offering.price_sar_max, locale)}{" "}
        {sar}
        {unitSuffix}
      </span>
    );
  }

  if (offering.price_mode === "fixed" && offering.price_sar != null) {
    return (
      <span className={cn("text-sm font-semibold text-foreground", className)}>
        {fmt(offering.price_sar, locale)} {sar}
        {unitSuffix}
      </span>
    );
  }

  // Fallback: never fabricate a number.
  return (
    <Badge
      variant="outline"
      className={cn(
        "border-violet-500/30 bg-violet-500/10 text-violet-400 text-xs",
        className,
      )}
    >
      {isAr ? "يُسعّر حسب النطاق" : "Quoted per scope"}
    </Badge>
  );
}
