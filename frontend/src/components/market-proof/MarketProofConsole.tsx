"use client";

import { useState } from "react";
import { useTranslations, useLocale } from "next-intl";
import { ClipboardCheck, MessageSquare } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { DEFAULT_CUSTOMER_ID } from "@/lib/commercial";
import { CelBadge } from "@/components/commercial/CelBadge";
import { GateStatusGrid } from "@/components/commercial/GateStatusGrid";
import {
  EvidenceTimeline,
  type EvidenceEvent,
} from "@/components/commercial/EvidenceTimeline";

export function MarketProofConsole() {
  const t = useTranslations("marketProof");
  const locale = useLocale();
  const isAr = locale === "ar";

  const [customerId, setCustomerId] = useState(DEFAULT_CUSTOMER_ID);
  const [subjectId, setSubjectId] = useState("contact_demo");
  const [founderConfirmed, setFounderConfirmed] = useState(false);
  const [classification, setClassification] = useState<
    "replied_interested" | "silent" | "not_interested"
  >("replied_interested");
  const [busy, setBusy] = useState(false);

  const [events, setEvents] = useState<EvidenceEvent[]>([]);
  const [sentCount, setSentCount] = useState(0);
  const [classifiedCount, setClassifiedCount] = useState(0);
  const [usedInMeeting, setUsedInMeeting] = useState(false);
  const [lastCel, setLastCel] = useState<string | null>(null);

  const errMsg = (e: unknown) => {
    const err = e as { response?: { status?: number }; message?: string };
    if (err?.response?.status === 422) return t("illegalTransition");
    return err?.message ?? t("error");
  };

  const recordSend = async () => {
    if (!founderConfirmed) {
      toast.error(t("founderConfirmRequired"));
      return;
    }
    setBusy(true);
    try {
      const res = await api.postEvidenceEvent({
        customer_id: customerId,
        subject_type: "contact",
        subject_id: subjectId,
        next_state: "sent",
        founder_confirmed: true,
        actor: "market_proof_console",
      });
      const data = res.data as { cel?: string };
      setLastCel(data.cel ?? "CEL4");
      setEvents((ev) => [...ev, { state: "sent", at: new Date().toLocaleString(locale) }]);
      setSentCount((c) => c + 1);
      toast.success(t("sendRecorded"));
    } catch (e) {
      toast.error(errMsg(e));
    } finally {
      setBusy(false);
    }
  };

  const recordClassification = async () => {
    setBusy(true);
    try {
      const res = await api.postEvidenceEvent({
        customer_id: customerId,
        subject_type: "contact",
        subject_id: subjectId,
        next_state: classification,
        actor: "market_proof_console",
      });
      const data = res.data as { cel?: string };
      setLastCel(data.cel ?? lastCel);
      setEvents((ev) => [
        ...ev,
        { state: classification, at: new Date().toLocaleString(locale) },
      ]);
      setClassifiedCount((c) => c + 1);
      if (classification === "replied_interested") setUsedInMeeting(false);
      toast.success(t("replyRecorded"));
    } catch (e) {
      toast.error(errMsg(e));
    } finally {
      setBusy(false);
    }
  };

  // G1: 5 sends + >=1 classified reply. G2: any CEL5 (used_in_meeting).
  const g1Passed = sentCount >= 5 && classifiedCount >= 1;
  const g2Passed = usedInMeeting;

  return (
    <div className="space-y-6">
      <div className="rounded-lg border border-emerald-500/30 bg-emerald-500/10 p-3 text-xs text-emerald-300">
        {t("noAutoSendNotice")}
      </div>

      <Card>
        <CardContent className="pt-6 grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="space-y-1.5">
            <Label htmlFor="mp-customer">{t("customerLabel")}</Label>
            <Input
              id="mp-customer"
              value={customerId}
              onChange={(e) => setCustomerId(e.target.value)}
            />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="mp-subject">{t("subjectLabel")}</Label>
            <Input
              id="mp-subject"
              value={subjectId}
              onChange={(e) => setSubjectId(e.target.value)}
            />
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Record send */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">{t("warmListTitle")}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <label className="flex items-start gap-2 rounded-lg border border-border p-3 text-sm cursor-pointer">
              <input
                type="checkbox"
                checked={founderConfirmed}
                onChange={(e) => setFounderConfirmed(e.target.checked)}
                className="mt-0.5 accent-gold-500"
              />
              <span>{t("founderConfirm")}</span>
            </label>
            <Button
              onClick={recordSend}
              disabled={busy || !founderConfirmed}
            >
              <ClipboardCheck className="w-4 h-4 me-1.5" />
              {t("recordSend")}
            </Button>
            {lastCel && (
              <div className="flex items-center gap-2">
                <CelBadge level={lastCel} />
              </div>
            )}
          </CardContent>
        </Card>

        {/* Classify reply */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">{t("classifyTitle")}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Select
              value={classification}
              onValueChange={(v) =>
                setClassification(
                  v as "replied_interested" | "silent" | "not_interested",
                )
              }
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="replied_interested">
                  {t("classifyInterested")}
                </SelectItem>
                <SelectItem value="silent">{t("classifySilent")}</SelectItem>
                <SelectItem value="not_interested">
                  {t("classifyNotInterested")}
                </SelectItem>
              </SelectContent>
            </Select>
            <Button onClick={recordClassification} disabled={busy}>
              <MessageSquare className="w-4 h-4 me-1.5" />
              {t("classify")}
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Gate progress */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">{t("progressTitle")}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="rounded-xl border border-border p-4">
              <p className="text-xs text-muted-foreground">
                {isAr ? "إرسالات مسجّلة" : "Sends recorded"}
              </p>
              <p className="text-2xl font-bold text-gold-400">{sentCount} / 5</p>
            </div>
            <div className="rounded-xl border border-border p-4">
              <p className="text-xs text-muted-foreground">
                {isAr ? "ردود مصنّفة" : "Replies classified"}
              </p>
              <p className="text-2xl font-bold text-gold-400">
                {classifiedCount}
              </p>
            </div>
          </div>
          <GateStatusGrid passedGates={[...(g1Passed ? ["G1"] : []), ...(g2Passed ? ["G2"] : [])]} />
        </CardContent>
      </Card>

      {/* Timeline */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">
            {isAr ? "سجل الأدلة" : "Evidence log"}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <EvidenceTimeline events={events} />
        </CardContent>
      </Card>
    </div>
  );
}
