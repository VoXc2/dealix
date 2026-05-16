"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import { FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { DEFAULT_CUSTOMER_ID } from "@/lib/commercial";

export function ProofPackGenerator() {
  const t = useTranslations("proofPack");

  const [customerId, setCustomerId] = useState(DEFAULT_CUSTOMER_ID);
  const [diagnosticId, setDiagnosticId] = useState("");
  const [signalsText, setSignalsText] = useState("");
  const [busy, setBusy] = useState(false);

  const [passport, setPassport] = useState<Record<string, unknown> | null>(null);
  const [governance, setGovernance] = useState<unknown>(null);

  const build = async () => {
    if (!diagnosticId.trim()) return;
    setBusy(true);
    try {
      const signals = signalsText
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean);
      const res = await api.getRevenueOpsDecisionPassport(
        diagnosticId.trim(),
        customerId,
        signals,
      );
      const data = res.data as {
        decision_passport?: Record<string, unknown>;
        governance_decision?: unknown;
      };
      setPassport(data.decision_passport ?? null);
      setGovernance(data.governance_decision ?? null);
    } catch {
      toast.error(t("error"));
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="rounded-lg border border-border bg-muted/30 p-3 text-xs text-muted-foreground">
        {t("readOnlyNotice")}
      </div>

      <Card>
        <CardContent className="pt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="space-y-1.5">
            <Label htmlFor="pp-customer">{t("customerLabel")}</Label>
            <Input
              id="pp-customer"
              value={customerId}
              onChange={(e) => setCustomerId(e.target.value)}
            />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="pp-diagnostic">{t("diagnosticLabel")}</Label>
            <Input
              id="pp-diagnostic"
              value={diagnosticId}
              onChange={(e) => setDiagnosticId(e.target.value)}
            />
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="pp-signals">{t("signalsLabel")}</Label>
            <Input
              id="pp-signals"
              value={signalsText}
              onChange={(e) => setSignalsText(e.target.value)}
            />
          </div>
        </CardContent>
      </Card>

      <Button onClick={build} disabled={busy || !diagnosticId.trim()}>
        <FileText className="w-4 h-4 me-1.5" />
        {t("generate")}
      </Button>

      {!passport ? (
        <p className="text-sm text-muted-foreground text-center py-12">
          {t("empty")}
        </p>
      ) : (
        <>
          <Card>
            <CardHeader>
              <CardTitle className="text-base">{t("previewTitle")}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <p className="text-xs font-medium text-muted-foreground mb-1">
                  {t("decisionPassport")}
                </p>
                <pre className="text-[11px] bg-muted/40 rounded-lg p-3 overflow-auto max-h-96">
                  {JSON.stringify(passport, null, 2)}
                </pre>
              </div>
              {governance != null && (
                <div>
                  <p className="text-xs font-medium text-muted-foreground mb-1">
                    {t("governanceDecision")}
                  </p>
                  <pre className="text-[11px] bg-muted/40 rounded-lg p-3 overflow-auto max-h-64">
                    {JSON.stringify(governance, null, 2)}
                  </pre>
                </div>
              )}
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}
