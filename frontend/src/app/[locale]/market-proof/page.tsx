"use client";

import { useCallback, useEffect, useState } from "react";
import { useTranslations } from "next-intl";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";

type Json = Record<string, unknown>;

export default function MarketProofPage() {
  const t = useTranslations("marketProof");
  const tc = useTranslations("common");
  const [status, setStatus] = useState<Json | null>(null);
  const [sector, setSector] = useState<Json | null>(null);
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [st, se] = await Promise.all([
        api.getProofToMarketStatus(),
        api.getProofToMarketSectorLearning(),
      ]);
      setStatus(st.data as Json);
      setSector(se.data as Json);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <p className="text-sm text-muted-foreground mb-6">{t("sendNote")}</p>

      <div className="mb-6">
        <Button onClick={() => void load()} disabled={loading}>
          {t("refresh")}
        </Button>
      </div>

      <section className="mb-10">
        <h2 className="text-lg font-semibold mb-3">{t("statusTitle")}</h2>
        {status ? (
          <pre className="text-xs bg-muted/40 rounded-xl p-4 overflow-auto max-h-[320px]">
            {JSON.stringify(status, null, 2)}
          </pre>
        ) : (
          <p className="text-sm text-muted-foreground">{tc("loading")}</p>
        )}
      </section>

      <section>
        <h2 className="text-lg font-semibold mb-3">{t("sectorTitle")}</h2>
        {sector ? (
          <pre className="text-xs bg-muted/40 rounded-xl p-4 overflow-auto max-h-[320px]">
            {JSON.stringify(sector, null, 2)}
          </pre>
        ) : (
          <p className="text-sm text-muted-foreground">{tc("loading")}</p>
        )}
      </section>
    </AppLayout>
  );
}
