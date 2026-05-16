"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useTranslations } from "next-intl";
import { Info, ListChecks } from "lucide-react";
import { AppLayout } from "@/components/layout/AppLayout";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { api } from "@/lib/api";

interface StateMachine {
  states: string[];
  state_to_level: Record<string, string>;
  allowed_transitions: Record<string, string[]>;
}

interface LedgerRecord {
  to_state: string;
  to_level: string | null;
  recorded_at: string;
}

const selectClass =
  "w-full rounded-lg border border-border bg-card px-3 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-gold-400";

function errText(e: unknown): string {
  if (
    typeof e === "object" &&
    e !== null &&
    "response" in e &&
    typeof (e as { response?: unknown }).response === "object"
  ) {
    const detail = (e as { response?: { data?: { detail?: unknown } } }).response?.data?.detail;
    if (typeof detail === "string") return detail;
    if (detail) return JSON.stringify(detail);
  }
  return e instanceof Error ? e.message : "error";
}

export default function MarketProofPage() {
  const t = useTranslations("marketProof");
  const [sm, setSm] = useState<StateMachine | null>(null);
  const [ledger, setLedger] = useState<Record<string, LedgerRecord[]>>({});
  const [loading, setLoading] = useState(true);

  const [contactId, setContactId] = useState("");
  const [fromState, setFromState] = useState("prepared_not_sent");
  const [toState, setToState] = useState("sent");
  const [founderConfirmed, setFounderConfirmed] = useState(false);
  const [paymentConfirmed, setPaymentConfirmed] = useState(false);
  const [scopeNote, setScopeNote] = useState("");
  const [evidenceRef, setEvidenceRef] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [sRes, lRes] = await Promise.all([
        api.getMarketProofStages(),
        api.getMarketProofLedger(),
      ]);
      setSm(sRes.data as StateMachine);
      setLedger((lRes.data as { ledger?: Record<string, LedgerRecord[]> }).ledger ?? {});
    } catch {
      toast.error("load_failed");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const toOptions = useMemo(() => {
    if (sm?.allowed_transitions?.[fromState]?.length) {
      return sm.allowed_transitions[fromState];
    }
    return sm?.states ?? [];
  }, [sm, fromState]);

  useEffect(() => {
    if (toOptions.length && !toOptions.includes(toState)) {
      setToState(toOptions[0]);
    }
  }, [toOptions, toState]);

  const showScope = toState === "scope_requested" || toState === "pilot_intro_requested";
  const showPayment = toState === "invoice_paid";

  const submit = async () => {
    if (!contactId.trim()) {
      toast.error(t("contactId"));
      return;
    }
    setSubmitting(true);
    try {
      await api.postMarketProofEvent({
        contact_id: contactId.trim(),
        from_state: fromState,
        to_state: toState,
        founder_confirmed: founderConfirmed,
        payment_confirmed: paymentConfirmed,
        scope_or_intro_request: showScope && scopeNote.trim() ? scopeNote.trim() : null,
        evidence_ref: evidenceRef.trim() || null,
      });
      toast.success(t("recorded"));
      setScopeNote("");
      setEvidenceRef("");
      setFounderConfirmed(false);
      setPaymentConfirmed(false);
      await load();
    } catch (e) {
      toast.error(`${t("rejected")}: ${errText(e)}`);
    } finally {
      setSubmitting(false);
    }
  };

  const contacts = Object.entries(ledger);

  return (
    <AppLayout title={t("title")} subtitle={t("subtitle")}>
      <div className="rounded-xl border border-sky-500/30 bg-sky-500/5 p-3 mb-6 flex items-start gap-2">
        <Info className="w-4 h-4 text-sky-400 flex-shrink-0 mt-0.5" />
        <p className="text-xs text-muted-foreground">{t("noSendNotice")}</p>
      </div>

      <section className="mb-8">
        <h2 className="text-lg font-semibold mb-3 flex items-center gap-2">
          <ListChecks className="w-4 h-4 text-gold-400" />
          {t("contactsTitle")}
        </h2>
        {loading ? (
          <p className="text-sm text-muted-foreground">…</p>
        ) : contacts.length === 0 ? (
          <p className="text-sm text-muted-foreground">{t("noContacts")}</p>
        ) : (
          <ul className="space-y-2">
            {contacts.map(([cid, recs]) => {
              const last = recs[recs.length - 1];
              return (
                <li
                  key={cid}
                  className="flex items-center justify-between rounded-xl border border-border bg-card p-3"
                >
                  <span className="text-sm font-medium">{cid}</span>
                  <span className="flex items-center gap-2 text-xs">
                    <span className="text-muted-foreground">{t("currentState")}:</span>
                    <span className="font-mono">{last?.to_state ?? "—"}</span>
                    {last?.to_level && <Badge variant="outline">{last.to_level}</Badge>}
                  </span>
                </li>
              );
            })}
          </ul>
        )}
      </section>

      <section>
        <h2 className="text-lg font-semibold mb-3">{t("recordTitle")}</h2>
        <div className="rounded-2xl border border-border bg-card p-5 space-y-4 max-w-xl">
          <div>
            <label className="text-xs text-muted-foreground mb-1 block">{t("contactId")}</label>
            <Input value={contactId} onChange={(e) => setContactId(e.target.value)} />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">{t("fromState")}</label>
              <select
                className={selectClass}
                value={fromState}
                onChange={(e) => setFromState(e.target.value)}
              >
                {(sm?.states ?? []).map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">{t("toState")}</label>
              <select
                className={selectClass}
                value={toState}
                onChange={(e) => setToState(e.target.value)}
              >
                {toOptions.map((s) => (
                  <option key={s} value={s}>
                    {s}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {toState === "sent" && (
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={founderConfirmed}
                onChange={(e) => setFounderConfirmed(e.target.checked)}
              />
              {t("founderConfirmed")}
            </label>
          )}

          {showScope && (
            <div>
              <label className="text-xs text-muted-foreground mb-1 block">
                {t("scopeOrIntro")}
              </label>
              <Input value={scopeNote} onChange={(e) => setScopeNote(e.target.value)} />
            </div>
          )}

          {showPayment && (
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={paymentConfirmed}
                onChange={(e) => setPaymentConfirmed(e.target.checked)}
              />
              {t("paymentConfirmed")}
            </label>
          )}

          <div>
            <label className="text-xs text-muted-foreground mb-1 block">{t("evidenceRef")}</label>
            <Input value={evidenceRef} onChange={(e) => setEvidenceRef(e.target.value)} />
          </div>

          <Button onClick={() => void submit()} disabled={submitting}>
            {t("record")}
          </Button>
        </div>
      </section>
    </AppLayout>
  );
}
