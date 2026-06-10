"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { getAdminApiKey, isOpsConfigured, opsMissingKeyMessage } from "@/lib/opsAdmin";
import { OpsObjectionPanel } from "@/components/gtm/OpsObjectionPanel";

type LeadItem = {
  id: string;
  company: string;
  stage: string;
  lead_score: number;
  war_room_status?: string;
};

export function OpsSalesPipeline() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const adminKey = getAdminApiKey();
  const [stages, setStages] = useState<Record<string, number>>({});
  const [leads, setLeads] = useState<LeadItem[]>([]);
  const [brief, setBrief] = useState<string>("");
  const [err, setErr] = useState("");

  useEffect(() => {
    if (!isOpsConfigured()) {
      setErr(opsMissingKeyMessage(isAr));
      return;
    }
    const key = adminKey || "";
    Promise.all([
      api.getSalesPipelineAutopilot(key),
      api.getOpsLeads(key, 40),
    ])
      .then(([pipeRes, leadsRes]) => {
        setStages((pipeRes.data as { stages?: Record<string, number> }).stages ?? {});
        const items = (leadsRes.data as { items?: LeadItem[] }).items ?? [];
        setLeads(items);
      })
      .catch(() => setErr(isAr ? "تعذّر التحميل." : "Load failed."));
  }, [adminKey, isAr]);

  const advanceStage = async (leadId: string, target: string) => {
    if (!isOpsConfigured()) return;
    try {
      await api.advanceLeadStage(adminKey || "", leadId, { target_stage: target });
      setErr(isAr ? "تم تقديم المرحلة." : "Stage advanced.");
    } catch {
      setErr(isAr ? "فشل تقديم المرحلة." : "Advance failed.");
    }
  };

  const draftInvoice = async (leadId: string, tier: string) => {
    if (!isOpsConfigured()) return;
    try {
      await api.invoiceDraftAutopilot(adminKey || "", { lead_id: leadId, tier });
      setErr(isAr ? "مسودة فاتورة أُنشئت — راجع الموافقات." : "Invoice draft created — check approvals.");
    } catch {
      setErr(isAr ? "فشل إنشاء الفاتورة (تحقق من مرحلة النطاق)." : "Invoice draft blocked (check scope stage).");
    }
  };

  const loadBrief = async (leadId: string) => {
    if (!isOpsConfigured()) return;
    try {
      const res = await api.getLeadMeetingBrief(adminKey || "", leadId, locale);
      const d = res.data as { discovery_questions_ar?: string[]; demo_path?: string };
      setBrief(
        [...(d.discovery_questions_ar ?? []), "", `Demo: ${d.demo_path ?? ""}`].join("\n"),
      );
    } catch {
      setBrief(isAr ? "تعذّر تحميل الموجز." : "Brief failed.");
    }
  };

  return (
    <div className="space-y-6" dir={isAr ? "rtl" : "ltr"}>
      <p className="text-sm text-muted-foreground">
        {isAr
          ? "خط المبيعات + مسودات فاتورة (بعد scope_sent) + موجز اجتماع."
          : "Pipeline + invoice drafts (after scope) + meeting brief."}
      </p>
      {err && <p className="text-sm text-destructive">{err}</p>}
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {Object.entries(stages).map(([stage, count]) => (
          <Card key={stage} className="p-3">
            <p className="text-xs text-muted-foreground">{stage}</p>
            <p className="text-xl font-semibold">{count}</p>
          </Card>
        ))}
      </div>
      <div className="space-y-2 max-h-[40vh] overflow-auto">
        {leads.map((L) => (
          <Card key={L.id} className="p-3 flex flex-wrap gap-2 items-center justify-between">
            <div>
              <p className="font-medium">{L.company || L.id}</p>
              <p className="text-xs text-muted-foreground">
                {L.stage} · {L.war_room_status} · {L.lead_score}
              </p>
            </div>
            <div className="flex gap-1 flex-wrap">
              <Button size="sm" variant="outline" onClick={() => loadBrief(L.id)}>
                {isAr ? "موجز" : "Brief"}
              </Button>
              <Button size="sm" variant="secondary" onClick={() => draftInvoice(L.id, "starter")}>
                {isAr ? "فاتورة" : "Invoice"}
              </Button>
              <Button
                size="sm"
                variant="outline"
                onClick={() => advanceStage(L.id, "meeting_booked")}
              >
                {isAr ? "اجتماع" : "Meeting"}
              </Button>
            </div>
          </Card>
        ))}
      </div>
      {brief && (
        <Card className="p-3 text-sm whitespace-pre-wrap">
          <pre className="text-xs">{brief}</pre>
        </Card>
      )}
      <OpsObjectionPanel />
      <Link href={`/${locale}/ops/war-room`} className="text-sm text-primary hover:underline">
        {isAr ? "غرفة الإيراد" : "War Room"}
      </Link>
    </div>
  );
}
