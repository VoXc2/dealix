"use client";

import { useLocale } from "next-intl";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { CelLevel } from "@/lib/commercial";

const CEL_STYLES: Record<CelLevel, string> = {
  CEL2: "border-border bg-muted text-muted-foreground",
  CEL4: "border-blue-500/30 bg-blue-500/10 text-blue-400",
  CEL5: "border-gold-500/30 bg-gold-500/10 text-gold-400",
  CEL6: "border-violet-500/30 bg-violet-500/10 text-violet-400",
  CEL7_candidate: "border-orange-500/30 bg-orange-500/10 text-orange-400",
  CEL7_confirmed: "border-emerald-500/30 bg-emerald-500/10 text-emerald-400",
};

const CEL_LABEL_AR: Record<CelLevel, string> = {
  CEL2: "مُجهّز",
  CEL4: "مُرسَل",
  CEL5: "استُخدم في اجتماع",
  CEL6: "طلب جذب",
  CEL7_candidate: "فاتورة صادرة",
  CEL7_confirmed: "إيراد مؤكد",
};

const CEL_LABEL_EN: Record<CelLevel, string> = {
  CEL2: "Prepared",
  CEL4: "Sent",
  CEL5: "Used in meeting",
  CEL6: "Pull requested",
  CEL7_candidate: "Invoice issued",
  CEL7_confirmed: "Revenue confirmed",
};

interface CelBadgeProps {
  level?: CelLevel | string | null;
  showLabel?: boolean;
  className?: string;
}

export function CelBadge({ level, showLabel = true, className }: CelBadgeProps) {
  const locale = useLocale();
  const isAr = locale === "ar";

  if (!level || !(level in CEL_STYLES)) {
    return (
      <Badge variant="outline" className={cn("text-[10px]", className)}>
        {isAr ? "لا مستوى" : "No level"}
      </Badge>
    );
  }

  const cel = level as CelLevel;
  return (
    <Badge
      variant="outline"
      className={cn("text-[10px] font-semibold", CEL_STYLES[cel], className)}
    >
      <span className="font-mono">{cel.replace("_", " ")}</span>
      {showLabel && (
        <span className="ms-1.5 font-normal">
          {isAr ? CEL_LABEL_AR[cel] : CEL_LABEL_EN[cel]}
        </span>
      )}
    </Badge>
  );
}
