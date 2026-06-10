"use client";

import { useState } from "react";
import { useLocale } from "next-intl";
import { Button } from "@/components/ui/button";
import { OpsMarketingSocial } from "@/components/gtm/OpsMarketingSocial";
import { OpsMarketingContent } from "@/components/gtm/OpsMarketingContent";

export function OpsMarketingHub() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [tab, setTab] = useState<"today" | "factory">("today");

  return (
    <div className="space-y-4" dir={isAr ? "rtl" : "ltr"}>
      <div className="flex gap-2 flex-wrap">
        <Button
          size="sm"
          variant={tab === "today" ? "default" : "outline"}
          onClick={() => setTab("today")}
        >
          {isAr ? "اليوم" : "Today"}
        </Button>
        <Button
          size="sm"
          variant={tab === "factory" ? "default" : "outline"}
          onClick={() => setTab("factory")}
        >
          {isAr ? "المصنع" : "Factory"}
        </Button>
      </div>
      {tab === "today" ? <OpsMarketingSocial /> : <OpsMarketingContent />}
    </div>
  );
}
