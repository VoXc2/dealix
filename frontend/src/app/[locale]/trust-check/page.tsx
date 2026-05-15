"use client";

import { useCallback, useEffect, useState } from "react";
import { useTranslations } from "next-intl";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";

export default function TrustCheckPage() {
  const t = useTranslations("trustCheck");
  const [levels, setLevels] = useState<unknown>(null);
  const [anti, setAnti] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(false);

  const loadEvidence = useCallback(async () => {
    const res = await api.getEvidenceLevels();
    setLevels(res.data);
  }, []);

  useEffect(() => {
    void loadEvidence();
  }, [loadEvidence]);

  const runAnti = async () => {
    setLoading(true);
    try {
      const res = await api.postRevenueOsAntiWasteCheck({
        has_decision_passport: false,
        action_external: true,
        upsell_attempt: false,
        proof_event_count: 0,
        evidence_level_for_public: 0,
        public_marketing_attempt: false,
      });
      setAnti(res.data as Record<string, unknown>);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <p className="text-sm text-muted-foreground mb-6">{t("hint")}</p>

      <section className="mb-10">
        <h2 className="text-lg font-semibold mb-3">{t("evidenceTitle")}</h2>
        {levels ? (
          <pre className="text-xs bg-muted/40 rounded-xl p-4 overflow-auto max-h-[360px]">
            {JSON.stringify(levels, null, 2)}
          </pre>
        ) : (
          <p className="text-sm text-muted-foreground">…</p>
        )}
      </section>

      <section>
        <h2 className="text-lg font-semibold mb-3">{t("antiTitle")}</h2>
        <Button onClick={() => void runAnti()} disabled={loading}>
          {t("runCheck")}
        </Button>
        {anti && (
          <div className="mt-4 rounded-xl border border-border p-4 bg-muted/20">
            <p className="text-sm font-medium mb-2">
              {anti.ok ? t("pass") : t("blocked")}
            </p>
            <pre className="text-xs overflow-auto max-h-[280px]">{JSON.stringify(anti, null, 2)}</pre>
          </div>
        )}
      </section>
    </AppLayout>
  );
}
