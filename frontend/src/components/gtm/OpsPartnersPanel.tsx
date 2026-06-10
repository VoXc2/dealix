"use client";

import { useLocale } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";

const ADMIN_KEY =
  typeof window !== "undefined"
    ? process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY || ""
    : "";

type LeadRow = {
  lead_id: string;
  target: string;
  segment: string;
  status: string;
  lead_score: number;
};

export function OpsPartnersPanel() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [rows, setRows] = useState<LeadRow[]>([]);
  const [importing, setImporting] = useState(false);
  const [msg, setMsg] = useState("");

  const load = useCallback(async () => {
    if (!ADMIN_KEY) return;
    const res = await api.getWarRoom(ADMIN_KEY, { status_in: "partner_candidate" });
    const items = (res.data as { items: LeadRow[] }).items ?? [];
    const partnerish = items.filter(
      (r) =>
        r.segment?.includes("partner") ||
        r.status === "referral_requested",
    );
    if (partnerish.length) {
      setRows(partnerish);
      return;
    }
    const all = await api.getWarRoom(ADMIN_KEY, {});
    const filtered = ((all.data as { items: LeadRow[] }).items ?? []).filter((r) =>
      (r.segment || "").includes("partner"),
    );
    setRows(filtered);
  }, []);

  useEffect(() => {
    load().catch(() => setMsg(isAr ? "تعذّر التحميل" : "Load failed"));
  }, [load, isAr]);

  const importPipeline = async () => {
    if (!ADMIN_KEY) return;
    setImporting(true);
    setMsg("");
    try {
      const res = await api.importWarRoomTargets(ADMIN_KEY, { use_default_csv: true });
      const d = res.data as { imported?: number; skipped_duplicates?: number };
      setMsg(
        isAr
          ? `تم استيراد ${d.imported ?? 0} (تخطي ${d.skipped_duplicates ?? 0})`
          : `Imported ${d.imported ?? 0} (skipped ${d.skipped_duplicates ?? 0})`,
      );
      await load();
    } catch {
      setMsg(isAr ? "فشل الاستيراد" : "Import failed");
    } finally {
      setImporting(false);
    }
  };

  return (
    <div className="space-y-6" dir={isAr ? "rtl" : "ltr"}>
      <p className="text-sm text-muted-foreground">
        {isAr
          ? "شركاء وإحالات — pilot واحد أولاً. راجع PARTNER_PILOT_PIPELINE.yaml في المستودع."
          : "Partners & referrals — one pilot first. See PARTNER_PILOT_PIPELINE.yaml."}
      </p>
      <Button onClick={importPipeline} disabled={importing}>
        {isAr ? "استيراد أهداف CSV إلى War Room" : "Import CSV targets to War Room"}
      </Button>
      {msg && <p className="text-sm">{msg}</p>}
      <div className="space-y-2">
        {rows.map((r) => (
          <Card key={r.lead_id} className="p-3 text-sm">
            <p className="font-medium">{r.target}</p>
            <p className="text-muted-foreground">
              {r.segment} · {r.status} · score {r.lead_score}
            </p>
          </Card>
        ))}
        {rows.length === 0 && (
          <p className="text-muted-foreground text-sm">
            {isAr ? "لا شركاء مسجلون بعد — استخدم /partners أو الاستيراد." : "No partner leads yet."}
          </p>
        )}
      </div>
    </div>
  );
}
