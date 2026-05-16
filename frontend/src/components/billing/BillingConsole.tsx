"use client";

import { useState } from "react";
import { useTranslations, useLocale } from "next-intl";
import { motion } from "framer-motion";
import { Receipt, CheckCircle2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { DEFAULT_CUSTOMER_ID } from "@/lib/commercial";
import { CelBadge } from "@/components/commercial/CelBadge";

interface InvoiceItem {
  id: string;
  cel: string;
  at: string;
}

export function BillingConsole() {
  const t = useTranslations("billing");
  const locale = useLocale();

  const [customerId, setCustomerId] = useState(DEFAULT_CUSTOMER_ID);
  const [subjectId, setSubjectId] = useState("invoice_demo");
  const [busy, setBusy] = useState(false);

  const [candidates, setCandidates] = useState<InvoiceItem[]>([]);
  const [confirmed, setConfirmed] = useState<InvoiceItem[]>([]);

  const errMsg = (e: unknown) => {
    const err = e as { message?: string };
    return err?.message ?? t("error");
  };

  const recordInvoiceSent = async () => {
    setBusy(true);
    try {
      const res = await api.postEvidenceEvent({
        customer_id: customerId,
        subject_type: "invoice",
        subject_id: subjectId,
        next_state: "invoice_sent",
        actor: "billing_console",
      });
      const data = res.data as { cel?: string };
      setCandidates((c) => [
        {
          id: subjectId,
          cel: data.cel ?? "CEL7_candidate",
          at: new Date().toLocaleString(locale),
        },
        ...c.filter((i) => i.id !== subjectId),
      ]);
      toast.success(t("invoiceSentDone"));
    } catch (e) {
      toast.error(errMsg(e));
    } finally {
      setBusy(false);
    }
  };

  const markPaid = async (id: string) => {
    setBusy(true);
    try {
      const res = await api.postEvidenceEvent({
        customer_id: customerId,
        subject_type: "invoice",
        subject_id: id,
        next_state: "invoice_paid",
        invoice_paid: true,
        actor: "billing_console",
      });
      const data = res.data as { cel?: string };
      setCandidates((c) => c.filter((i) => i.id !== id));
      setConfirmed((c) => [
        {
          id,
          cel: data.cel ?? "CEL7_confirmed",
          at: new Date().toLocaleString(locale),
        },
        ...c.filter((i) => i.id !== id),
      ]);
      toast.success(t("paidDone"));
    } catch (e) {
      toast.error(errMsg(e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="rounded-lg border border-emerald-500/30 bg-emerald-500/10 p-3 text-xs text-emerald-300">
        {t("noAutoSendNotice")}
      </div>

      <Card>
        <CardContent className="pt-6 grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="space-y-1.5">
            <Label htmlFor="bl-customer">{t("customerLabel")}</Label>
            <Input
              id="bl-customer"
              value={customerId}
              onChange={(e) => setCustomerId(e.target.value)}
            />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="bl-subject">{t("subjectLabel")}</Label>
            <Input
              id="bl-subject"
              value={subjectId}
              onChange={(e) => setSubjectId(e.target.value)}
            />
          </div>
        </CardContent>
      </Card>

      <Button onClick={recordInvoiceSent} disabled={busy}>
        <Receipt className="w-4 h-4 me-1.5" />
        {t("recordInvoiceSent")}
      </Button>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Candidates */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">{t("candidateTitle")}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {candidates.length === 0 ? (
              <p className="text-sm text-muted-foreground">{t("empty")}</p>
            ) : (
              candidates.map((item) => (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="rounded-xl border border-orange-500/30 bg-orange-500/5 p-4"
                >
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <p className="text-sm font-semibold text-foreground">
                        {item.id}
                      </p>
                      <p className="text-[11px] text-muted-foreground">
                        {item.at}
                      </p>
                    </div>
                    <CelBadge level={item.cel} />
                  </div>
                  <Button
                    size="sm"
                    variant="emerald"
                    className="mt-3"
                    disabled={busy}
                    onClick={() => markPaid(item.id)}
                  >
                    <CheckCircle2 className="w-3.5 h-3.5 me-1.5" />
                    {t("markPaid")}
                  </Button>
                </motion.div>
              ))
            )}
          </CardContent>
        </Card>

        {/* Confirmed */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">{t("confirmedTitle")}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {confirmed.length === 0 ? (
              <p className="text-sm text-muted-foreground">{t("empty")}</p>
            ) : (
              confirmed.map((item) => (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="rounded-xl border border-emerald-500/30 bg-emerald-500/5 p-4"
                >
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <p className="text-sm font-semibold text-foreground">
                        {item.id}
                      </p>
                      <p className="text-[11px] text-muted-foreground">
                        {item.at}
                      </p>
                    </div>
                    <CelBadge level={item.cel} />
                  </div>
                </motion.div>
              ))
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
