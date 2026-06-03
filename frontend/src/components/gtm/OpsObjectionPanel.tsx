"use client";

import { useLocale } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { getAdminApiKey, isOpsConfigured, opsMissingKeyMessage } from "@/lib/opsAdmin";

type Objection = {
  id?: string;
  labels_ar?: string[];
  classify?: string;
  response_draft_ar?: string;
  content_asset_slug?: string;
};

export function OpsObjectionPanel() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [items, setItems] = useState<Objection[]>([]);
  const [err, setErr] = useState("");
  const [copiedId, setCopiedId] = useState("");

  const load = useCallback(async () => {
    if (!isOpsConfigured()) {
      setErr(opsMissingKeyMessage(isAr));
      return;
    }
    setErr("");
    try {
      const res = await api.getSalesObjections(getAdminApiKey());
      const data = res.data as { objections?: Objection[] };
      setItems(data.objections ?? []);
    } catch {
      setErr(isAr ? "تعذّر تحميل الاعتراضات." : "Failed to load objections.");
    }
  }, [isAr]);

  useEffect(() => {
    load();
  }, [load]);

  const copy = async (ob: Objection) => {
    const text = ob.response_draft_ar || "";
    if (!text) return;
    await navigator.clipboard.writeText(text);
    setCopiedId(ob.id || "");
    setTimeout(() => setCopiedId(""), 2000);
  };

  return (
    <Card className="p-4 space-y-4" dir={isAr ? "rtl" : "ltr"}>
      <div className="flex justify-between items-start gap-2">
        <div>
          <h2 className="font-semibold">{isAr ? "محرك الاعتراضات" : "Objection engine"}</h2>
          <p className="text-xs text-muted-foreground mt-1">
            {isAr
              ? "من objection_engine_registry.yaml — انسخ الرد بعد التخصيص."
              : "From objection_engine_registry.yaml — copy after tailoring."}
          </p>
        </div>
        <Button variant="ghost" size="sm" onClick={load}>
          {isAr ? "تحديث" : "Refresh"}
        </Button>
      </div>
      {err && <p className="text-sm text-destructive">{err}</p>}
      <ul className="space-y-3">
        {items.map((ob) => (
          <li key={ob.id} className="border rounded-md p-3 text-sm">
            <p className="font-medium">{ob.id}</p>
            <p className="text-xs text-muted-foreground">
              {(ob.labels_ar || []).slice(0, 2).join(" · ")} · {ob.classify}
            </p>
            <p className="mt-2 whitespace-pre-wrap">{ob.response_draft_ar}</p>
            <Button variant="outline" size="sm" className="mt-2" onClick={() => copy(ob)}>
              {copiedId === ob.id
                ? isAr
                  ? "نُسخ"
                  : "Copied"
                : isAr
                  ? "نسخ الرد"
                  : "Copy response"}
            </Button>
          </li>
        ))}
      </ul>
    </Card>
  );
}
