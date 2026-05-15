"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { api } from "@/lib/api";

export default function CustomerPortalPage() {
  const t = useTranslations("customerPortal");
  const [handle, setHandle] = useState("Slot-A");
  const [data, setData] = useState<unknown>(null);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const res = await api.getCustomerPortal(handle.trim() || "Slot-A");
      setData(res.data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <div className="flex flex-wrap gap-3 items-end mb-6">
        <div className="flex flex-col gap-1">
          <label className="text-xs text-muted-foreground">{t("handleLabel")}</label>
          <Input value={handle} onChange={(e) => setHandle(e.target.value)} className="w-64" />
        </div>
        <Button onClick={() => void load()} disabled={loading}>
          {t("load")}
        </Button>
      </div>

      {!!data && typeof data === "object" && "promise_ar" in data && (
        <div className="mb-4 rounded-xl border border-border p-4 bg-muted/20">
          <h3 className="text-sm font-semibold mb-2">{t("promiseTitle")}</h3>
          <p className="text-sm leading-relaxed">{(data as { promise_ar: string }).promise_ar}</p>
        </div>
      )}

      {data ? (
        <pre className="text-xs bg-muted/40 rounded-xl p-4 overflow-auto max-h-[560px]">
          {JSON.stringify(data, null, 2)}
        </pre>
      ) : (
        <p className="text-sm text-muted-foreground">…</p>
      )}
    </AppLayout>
  );
}
