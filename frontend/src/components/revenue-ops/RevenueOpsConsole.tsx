"use client";

import { useState } from "react";
import { useTranslations, useLocale } from "next-intl";
import { motion } from "framer-motion";
import { Stethoscope, Upload, Gauge, FileCheck, Send, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { DEFAULT_CUSTOMER_ID } from "@/lib/commercial";

const READINESS_SIGNALS = [
  "crm_in_use",
  "clean_account_list",
  "named_owner",
  "defined_offer",
  "warm_contacts",
];

interface FollowUpDraft {
  draft_id?: string;
  channel?: string;
  subject_ar?: string;
  subject_en?: string;
  body_ar?: string;
  body_en?: string;
  [k: string]: unknown;
}

function GovernanceBlock({ decision }: { decision: unknown }) {
  const t = useTranslations("revenueOps");
  if (!decision) return null;
  return (
    <div className="mt-3">
      <p className="text-xs font-medium text-muted-foreground mb-1">
        {t("governanceDecision")}
      </p>
      <pre className="text-[11px] bg-muted/40 rounded-lg p-3 overflow-auto max-h-48">
        {JSON.stringify(decision, null, 2)}
      </pre>
    </div>
  );
}

export function RevenueOpsConsole() {
  const t = useTranslations("revenueOps");
  const locale = useLocale();
  const isAr = locale === "ar";

  const [customerId, setCustomerId] = useState(DEFAULT_CUSTOMER_ID);
  const [accountId, setAccountId] = useState("acct_demo");
  const [notes, setNotes] = useState("");
  const [busy, setBusy] = useState(false);

  const [diagnosticId, setDiagnosticId] = useState<string | null>(null);
  const [diagnostic, setDiagnostic] = useState<Record<string, unknown> | null>(null);
  const [diagnosticGov, setDiagnosticGov] = useState<unknown>(null);

  const [csvText, setCsvText] = useState("");
  const [upload, setUpload] = useState<Record<string, unknown> | null>(null);

  const [signals, setSignals] = useState<Record<string, boolean>>({});
  const [readiness, setReadiness] = useState<Record<string, unknown> | null>(null);

  const [passport, setPassport] = useState<Record<string, unknown> | null>(null);

  const [drafts, setDrafts] = useState<FollowUpDraft[]>([]);
  const [routed, setRouted] = useState<Record<string, boolean>>({});

  const errMsg = (e: unknown) =>
    e instanceof Error ? e.message : t("error");

  const createDiagnostic = async () => {
    setBusy(true);
    try {
      const res = await api.postRevenueOpsDiagnostic({
        customer_id: customerId,
        account_id: accountId,
        notes: notes || undefined,
        actor: "ops_console",
      });
      const data = res.data as {
        diagnostic?: Record<string, unknown>;
        governance_decision?: unknown;
      };
      setDiagnostic(data.diagnostic ?? null);
      setDiagnosticGov(data.governance_decision ?? null);
      setDiagnosticId(
        data.diagnostic?.diagnostic_id
          ? String(data.diagnostic.diagnostic_id)
          : null,
      );
      toast.success(t("diagnosticCreated"));
    } catch (e) {
      toast.error(errMsg(e));
    } finally {
      setBusy(false);
    }
  };

  const uploadCsv = async () => {
    setBusy(true);
    try {
      const res = await api.postRevenueOpsUpload({
        customer_id: customerId,
        csv_text: csvText,
      });
      setUpload((res.data as { upload?: Record<string, unknown> }).upload ?? null);
      toast.success(t("uploaded"));
    } catch (e) {
      toast.error(errMsg(e));
    } finally {
      setBusy(false);
    }
  };

  const scoreReadiness = async () => {
    setBusy(true);
    try {
      const res = await api.postRevenueOpsScore({
        customer_id: customerId,
        signals,
      });
      setReadiness(
        (res.data as { readiness?: Record<string, unknown> }).readiness ?? null,
      );
      toast.success(t("scored"));
    } catch (e) {
      toast.error(errMsg(e));
    } finally {
      setBusy(false);
    }
  };

  const loadPassport = async () => {
    if (!diagnosticId) return;
    setBusy(true);
    try {
      const selected = Object.keys(signals).filter((k) => signals[k]);
      const res = await api.getRevenueOpsDecisionPassport(
        diagnosticId,
        customerId,
        selected,
      );
      setPassport(
        (res.data as { decision_passport?: Record<string, unknown> })
          .decision_passport ?? null,
      );
    } catch (e) {
      toast.error(errMsg(e));
    } finally {
      setBusy(false);
    }
  };

  const generateDrafts = async () => {
    if (!diagnosticId) return;
    setBusy(true);
    try {
      const res = await api.postRevenueOpsFollowUpDrafts(diagnosticId, {
        customer_id: customerId,
      });
      const list = (res.data as { drafts?: FollowUpDraft[] }).drafts ?? [];
      setDrafts(list);
      setRouted({});
      toast.success(t("draftsGenerated"));
    } catch (e) {
      toast.error(errMsg(e));
    } finally {
      setBusy(false);
    }
  };

  const sendDraftToApproval = async (draft: FollowUpDraft, idx: number) => {
    setBusy(true);
    try {
      await api.postApproval({
        customer_id: customerId,
        action_type: "revenue_ops_follow_up",
        object_type: "follow_up_draft",
        object_id: draft.draft_id ?? `${diagnosticId}_draft_${idx}`,
        channel: draft.channel ?? "email",
        summary_ar: draft.subject_ar ?? "مسودة متابعة",
        summary_en: draft.subject_en ?? "Follow-up draft",
        payload: draft,
        requested_by: "ops_console",
      });
      setRouted((r) => ({ ...r, [idx]: true }));
      toast.success(t("sentToApproval"));
    } catch (e) {
      toast.error(errMsg(e));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* shared customer fields */}
      <Card>
        <CardContent className="pt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="space-y-1.5">
            <Label htmlFor="ro-customer">{t("customerLabel")}</Label>
            <Input
              id="ro-customer"
              value={customerId}
              onChange={(e) => setCustomerId(e.target.value)}
            />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="ro-account">{t("accountLabel")}</Label>
            <Input
              id="ro-account"
              value={accountId}
              onChange={(e) => setAccountId(e.target.value)}
            />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="ro-notes">{t("notesLabel")}</Label>
            <Input
              id="ro-notes"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
            />
          </div>
        </CardContent>
      </Card>

      <Tabs defaultValue="diagnostic">
        <TabsList className="mb-6 flex flex-wrap h-auto gap-1">
          <TabsTrigger value="diagnostic">
            <Stethoscope className="w-3.5 h-3.5 me-1.5" />
            {t("tabDiagnostic")}
          </TabsTrigger>
          <TabsTrigger value="upload">
            <Upload className="w-3.5 h-3.5 me-1.5" />
            {t("tabUpload")}
          </TabsTrigger>
          <TabsTrigger value="score">
            <Gauge className="w-3.5 h-3.5 me-1.5" />
            {t("tabScore")}
          </TabsTrigger>
          <TabsTrigger value="passport">
            <FileCheck className="w-3.5 h-3.5 me-1.5" />
            {t("tabPassport")}
          </TabsTrigger>
          <TabsTrigger value="drafts">
            <Send className="w-3.5 h-3.5 me-1.5" />
            {t("tabDrafts")}
          </TabsTrigger>
        </TabsList>

        {/* Diagnostic */}
        <TabsContent value="diagnostic">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">{t("tabDiagnostic")}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button onClick={createDiagnostic} disabled={busy}>
                <Plus className="w-4 h-4 me-1.5" />
                {t("createDiagnostic")}
              </Button>
              {diagnosticId && (
                <Badge
                  variant="outline"
                  className="ms-2 border-emerald-500/30 bg-emerald-500/10 text-emerald-400"
                >
                  {diagnosticId}
                </Badge>
              )}
              {diagnostic && (
                <pre className="text-[11px] bg-muted/40 rounded-lg p-3 overflow-auto max-h-64">
                  {JSON.stringify(diagnostic, null, 2)}
                </pre>
              )}
              <GovernanceBlock decision={diagnosticGov} />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Upload */}
        <TabsContent value="upload">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">{t("tabUpload")}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-1.5">
                <Label htmlFor="ro-csv">{t("csvLabel")}</Label>
                <textarea
                  id="ro-csv"
                  value={csvText}
                  onChange={(e) => setCsvText(e.target.value)}
                  placeholder={t("csvPlaceholder")}
                  rows={6}
                  className="flex w-full rounded-xl border border-input bg-background px-4 py-2 text-sm font-mono ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
                />
              </div>
              <Button onClick={uploadCsv} disabled={busy || !csvText.trim()}>
                <Upload className="w-4 h-4 me-1.5" />
                {t("uploadCsv")}
              </Button>
              {upload && (
                <pre className="text-[11px] bg-muted/40 rounded-lg p-3 overflow-auto max-h-64">
                  {JSON.stringify(upload, null, 2)}
                </pre>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Score */}
        <TabsContent value="score">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">{t("tabScore")}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-sm text-muted-foreground">
                {t("signalsLabel")}
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {READINESS_SIGNALS.map((sig) => (
                  <label
                    key={sig}
                    className="flex items-center gap-2 rounded-lg border border-border p-3 text-sm cursor-pointer hover:bg-muted/40"
                  >
                    <input
                      type="checkbox"
                      checked={Boolean(signals[sig])}
                      onChange={(e) =>
                        setSignals((s) => ({ ...s, [sig]: e.target.checked }))
                      }
                      className="accent-gold-500"
                    />
                    <span className="font-mono text-xs">{sig}</span>
                  </label>
                ))}
              </div>
              <Button onClick={scoreReadiness} disabled={busy}>
                <Gauge className="w-4 h-4 me-1.5" />
                {t("scoreReadiness")}
              </Button>
              {readiness && (
                <div className="rounded-lg border border-border p-4">
                  <p className="text-sm text-muted-foreground">{t("score")}</p>
                  <p className="text-3xl font-bold text-gold-400">
                    {String(readiness.score ?? "—")}
                  </p>
                  <pre className="text-[11px] bg-muted/40 rounded-lg p-3 mt-3 overflow-auto max-h-48">
                    {JSON.stringify(readiness, null, 2)}
                  </pre>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Passport */}
        <TabsContent value="passport">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">{t("tabPassport")}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {!diagnosticId ? (
                <p className="text-sm text-muted-foreground">
                  {t("needDiagnostic")}
                </p>
              ) : (
                <>
                  <Button onClick={loadPassport} disabled={busy}>
                    <FileCheck className="w-4 h-4 me-1.5" />
                    {t("loadPassport")}
                  </Button>
                  {passport && (
                    <pre className="text-[11px] bg-muted/40 rounded-lg p-3 overflow-auto max-h-80">
                      {JSON.stringify(passport, null, 2)}
                    </pre>
                  )}
                </>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Drafts */}
        <TabsContent value="drafts">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">{t("tabDrafts")}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {!diagnosticId ? (
                <p className="text-sm text-muted-foreground">
                  {t("needDiagnostic")}
                </p>
              ) : (
                <>
                  <Button onClick={generateDrafts} disabled={busy}>
                    <Plus className="w-4 h-4 me-1.5" />
                    {t("generateDrafts")}
                  </Button>
                  <div className="rounded-lg border border-gold-500/30 bg-gold-500/10 p-3 text-xs text-gold-300">
                    {t("draftsNotice")}
                  </div>
                  <div className="space-y-3">
                    {drafts.map((draft, idx) => (
                      <motion.div
                        key={draft.draft_id ?? idx}
                        initial={{ opacity: 0, y: 8 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="rounded-xl border border-border p-4 bg-card"
                      >
                        <p className="text-sm font-semibold text-foreground">
                          {isAr
                            ? draft.subject_ar ?? draft.subject_en
                            : draft.subject_en ?? draft.subject_ar}
                        </p>
                        <p className="text-xs text-muted-foreground mt-1 whitespace-pre-wrap">
                          {isAr
                            ? draft.body_ar ?? draft.body_en
                            : draft.body_en ?? draft.body_ar}
                        </p>
                        <div className="mt-3">
                          <Button
                            size="sm"
                            variant="outline"
                            disabled={busy || routed[idx]}
                            onClick={() => sendDraftToApproval(draft, idx)}
                          >
                            <Send className="w-3.5 h-3.5 me-1.5" />
                            {routed[idx]
                              ? t("sentToApproval")
                              : t("sendToApproval")}
                          </Button>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
