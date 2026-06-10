"use client";

import { useLocale } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { ValuePlanPanel, type ValuePlanPayload } from "@/components/gtm/ValuePlanPanel";
import { getAdminApiKey, isOpsConfigured, opsMissingKeyMessage } from "@/lib/opsAdmin";

const EVENT_TYPES = [
  "message_sent_manual",
  "reply_received",
  "demo_booked",
  "scope_requested",
  "invoice_sent",
  "payment_received",
  "proof_pack_delivered",
] as const;

type EvRow = {
  event_type: string;
  summary: string;
  created_at?: string;
  entity_type?: string;
  entity_id?: string;
};

export function OpsEvidenceLedger() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const adminKey = getAdminApiKey();
  const [items, setItems] = useState<EvRow[]>([]);
  const [valuePlan, setValuePlan] = useState<ValuePlanPayload | null>(null);
  const [err, setErr] = useState("");
  const [company, setCompany] = useState("");
  const [eventType, setEventType] = useState<string>("message_sent_manual");
  const [notes, setNotes] = useState("");
  const [appendMsg, setAppendMsg] = useState("");

  const load = useCallback(() => {
    if (!isOpsConfigured()) {
      setErr(opsMissingKeyMessage(isAr));
      return;
    }
    setErr("");
    Promise.all([
      api.getEvidenceLedger(adminKey, 60),
      api.getFounderValuePlan(adminKey, 3),
    ])
      .then(([ev, vp]) => {
        setItems((ev.data as { items?: EvRow[] }).items ?? []);
        setValuePlan(vp.data as ValuePlanPayload);
      })
      .catch(() => setErr(isAr ? "تعذّر تحميل الأدلة." : "Evidence load failed."));
  }, [adminKey, isAr]);

  useEffect(() => {
    load();
  }, [load]);

  const appendRow = () => {
    if (!company.trim()) {
      setAppendMsg(isAr ? "أدخل اسم الشركة." : "Enter company name.");
      return;
    }
    api
      .postFounderEvidenceCsvAppend(adminKey, {
        event_type: eventType,
        company: company.trim(),
        notes: notes.trim(),
      })
      .then(() => {
        setAppendMsg(isAr ? "تم التسجيل في CSV." : "Logged to CSV.");
        setCompany("");
        setNotes("");
        load();
      })
      .catch(() => setAppendMsg(isAr ? "فشل التسجيل." : "Append failed."));
  };

  return (
    <div className="space-y-6" dir={isAr ? "rtl" : "ltr"}>
      {valuePlan && <ValuePlanPanel valuePlan={valuePlan} variant="compact" />}

      <Card className="p-4 border-primary/30">
        <h2 className="font-semibold text-sm mb-3">
          {isAr ? "تسجيل حدث (CSV)" : "Log event (CSV)"}
        </h2>
        <p className="text-xs text-muted-foreground mb-3">
          {isAr
            ? "بعد لمسة يدوية موافَق عليها — لا إرسال تلقائي."
            : "After approved manual touch — no auto-send."}
        </p>
        {valuePlan?.first_paid_diagnostic?.verdict && (
          <p className="text-xs font-mono mb-2 text-amber-700 dark:text-amber-400">
            {isAr ? "أول Diagnostic مدفوع:" : "First paid diagnostic:"}{" "}
            {valuePlan.first_paid_diagnostic.verdict}
          </p>
        )}
        <div className="grid gap-3 sm:grid-cols-2">
          <label className="text-xs">
            {isAr ? "الشركة" : "Company"}
            <input
              className="mt-1 w-full rounded border border-input bg-background px-2 py-1 text-sm"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
            />
          </label>
          <label className="text-xs">
            {isAr ? "نوع الحدث" : "Event type"}
            <select
              className="mt-1 w-full rounded border border-input bg-background px-2 py-1 text-sm"
              value={eventType}
              onChange={(e) => setEventType(e.target.value)}
            >
              {EVENT_TYPES.map((et) => (
                <option key={et} value={et}>
                  {et}
                </option>
              ))}
            </select>
          </label>
        </div>
        <label className="text-xs block mt-3">
          {isAr ? "ملاحظات" : "Notes"}
          <input
            className="mt-1 w-full rounded border border-input bg-background px-2 py-1 text-sm"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
        </label>
        <Button type="button" size="sm" className="mt-3" onClick={appendRow}>
          {isAr ? "سجّل" : "Log"}
        </Button>
        {appendMsg && <p className="text-xs mt-2 text-muted-foreground">{appendMsg}</p>}
      </Card>

      <p className="text-sm text-muted-foreground">
        {isAr ? "أحداث الأدلة الأخيرة — مسار التصريف." : "Recent evidence events — GTM trail."}
      </p>
      {err && <p className="text-destructive text-sm">{err}</p>}
      <div className="space-y-2 max-h-[50vh] overflow-auto">
        {items.map((ev, i) => (
          <Card key={`${ev.event_type}-${i}`} className="p-3 text-sm">
            <p className="font-mono text-xs text-primary">{ev.event_type}</p>
            <p className="mt-1">{ev.summary}</p>
            <p className="text-xs text-muted-foreground mt-1">
              {ev.entity_type}:{ev.entity_id} · {ev.created_at}
            </p>
          </Card>
        ))}
      </div>
    </div>
  );
}
