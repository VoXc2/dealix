"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import api from "@/lib/api";
import { getAdminApiKey, isOpsConfigured, opsMissingKeyMessage } from "@/lib/opsAdmin";
import { toast } from "sonner";

type WarRow = {
  lead_id: string;
  target: string;
  segment: string;
  pain_hypothesis: string;
  offer: string;
  proof_asset: string;
  next_action: string;
  next_action_due: string | null;
  status: string;
  lead_score: number;
};

type Summary = {
  today?: { top_targets_count?: number; follow_ups_due?: number };
  revenue?: Record<string, number>;
  anti_waste_guard?: { blocked_sample?: boolean };
};

type TargetTodayRow = {
  company?: string;
  segment?: string;
  channel?: string;
  next_action?: string;
  outreach_draft_ar?: string;
};

type MeetingBrief = {
  company?: string;
  discovery_questions_ar?: string[];
  outreach_draft_ar?: string;
};

const STATUS_OPTIONS = [
  "not_contacted",
  "message_drafted",
  "approved_to_send",
  "sent_manual",
  "replied",
  "proof_pack_sent",
  "meeting_booked",
  "scope_requested",
  "invoice_sent",
  "paid",
  "delivery_started",
  "proof_pack_delivered",
  "upsell_candidate",
  "referral_requested",
  "closed_lost",
] as const;

type FilterMode = "top10" | "follow" | "due" | "all";

type Props = {
  onSelectLead?: (leadId: string | null) => void;
  selectedLeadId?: string | null;
  hideHeader?: boolean;
};

export function RevenueWarRoomTable({ onSelectLead, selectedLeadId, hideHeader }: Props) {
  const router = useRouter();
  const locale = useLocale();
  const t = useTranslations("warRoom");
  const isAr = locale === "ar";
  const [rows, setRows] = useState<WarRow[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [filter, setFilter] = useState<FilterMode>("top10");
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(false);
  const [importing, setImporting] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editDraft, setEditDraft] = useState<Partial<WarRow>>({});
  const [targetingToday, setTargetingToday] = useState<TargetTodayRow[]>([]);
  const [csvOpen, setCsvOpen] = useState(false);
  const [csvText, setCsvText] = useState("");
  const [briefLeadId, setBriefLeadId] = useState<string | null>(null);
  const [brief, setBrief] = useState<MeetingBrief | null>(null);
  const [actionMsg, setActionMsg] = useState("");

  const adminKey = getAdminApiKey();

  const load = useCallback(async () => {
    if (!isOpsConfigured()) {
      setErr(opsMissingKeyMessage(locale === "ar"));
      return;
    }
    const key = adminKey || "";
    setLoading(true);
    setErr("");
    try {
      const params =
        filter === "top10"
          ? { top_n: 10 }
          : filter === "follow"
            ? { needs_follow_up: true }
            : filter === "due"
              ? { due_today: true }
              : {};
      const [listRes, sumRes, tgtRes] = await Promise.all([
        api.getWarRoom(key, params),
        api.getWarRoomSummary(key),
        api.getTargetingToday(key, 5),
      ]);
      setRows((listRes.data as { items: WarRow[] }).items ?? []);
      setSummary(sumRes.data as Summary);
      const tgtItems = (tgtRes.data as { targets?: { items?: TargetTodayRow[] } })?.targets
        ?.items;
      setTargetingToday(tgtItems ?? []);
    } catch {
      setErr(t("loadFailed"));
    } finally {
      setLoading(false);
    }
  }, [filter, t, adminKey, locale]);

  useEffect(() => {
    load();
  }, [load]);

  const patchLead = async (leadId: string, body: Record<string, unknown>) => {
    if (!isOpsConfigured()) return;
    await api.patchWarRoom(adminKey || "", leadId, body);
    await load();
  };

  const patchStatus = async (leadId: string, status: string) => {
    try {
      await patchLead(leadId, {
        war_room_status: status,
        payment_proof_logged: status === "paid",
      });
    } catch {
      setErr(t("patchFailed"));
    }
  };

  const approveSend = async (leadId: string) => {
    try {
      await patchLead(leadId, { war_room_status: "approved_to_send" });
      router.push(`/${locale}/approvals`);
    } catch {
      setErr(t("patchFailed"));
    }
  };

  const generateDraft = async (leadId: string) => {
    if (!isOpsConfigured()) return;
    try {
      await api.postWarRoomGenerateOutreach(adminKey || "", leadId);
      await load();
    } catch {
      setErr(t("draftFailed"));
    }
  };

  const generateClientPack = async (row: WarRow) => {
    if (!isOpsConfigured()) return;
    try {
      const res = await api.postClientPackGenerate(adminKey || "", {
        company: row.target,
        lead_id: row.lead_id,
        write_disk: true,
      });
      const dir = (res.data as { paths?: { directory?: string } }).paths?.directory;
      toast.success(dir ? `${t("clientPackDone")} → ${dir}` : t("clientPackDone"));
    } catch {
      setErr(t("clientPackFailed"));
    }
  };

  const importCsv = async () => {
    if (!isOpsConfigured()) return;
    setImporting(true);
    try {
      const res = await api.importWarRoomTargets(adminKey || "", { use_default_csv: true });
      const imported = (res.data as { imported?: number })?.imported ?? 0;
      toast.success(
        isAr ? `تم استيراد ${imported} هدفاً` : `Imported ${imported} targets`,
      );
      await load();
    } catch {
      setErr(t("importFailed"));
      toast.error(t("importFailed"));
    } finally {
      setImporting(false);
    }
  };

  const importCsvText = async () => {
    if (!isOpsConfigured() || !csvText.trim()) return;
    setImporting(true);
    setErr("");
    try {
      const res = await api.postTargetingImport(adminKey || "", { csv_text: csvText.trim() });
      const n = (res.data as { imported_rows?: number })?.imported_rows ?? 0;
      toast.success(isAr ? `تم كتابة ${n} صفاً` : `Wrote ${n} rows`);
      setCsvText("");
      setCsvOpen(false);
      await load();
    } catch {
      setErr(t("importFailed"));
      toast.error(t("importFailed"));
    } finally {
      setImporting(false);
    }
  };

  const loadMeetingBrief = async (leadId: string) => {
    if (!isOpsConfigured()) return;
    setBriefLeadId(leadId);
    setActionMsg("");
    try {
      const r = await api.getLeadMeetingBrief(adminKey || "", leadId, locale);
      setBrief(r.data as MeetingBrief);
    } catch {
      setBrief(null);
      setErr(t("loadFailed"));
    }
  };

  const createInvoiceDraft = async (leadId: string) => {
    if (!isOpsConfigured()) return;
    setActionMsg("");
    try {
      await api.invoiceDraftAutopilot(adminKey || "", { lead_id: leadId, tier: "starter" });
      setActionMsg(t("invoiceDraftOk"));
      toast.success(t("invoiceDraftOk"));
    } catch {
      setActionMsg(t("invoiceDraftBlocked"));
      toast.error(t("invoiceDraftBlocked"));
    }
  };

  const startEdit = (row: WarRow) => {
    setEditingId(row.lead_id);
    setEditDraft({ ...row });
  };

  const saveEdit = async () => {
    if (!editingId) return;
    try {
      await patchLead(editingId, {
        segment: editDraft.segment,
        pain_hypothesis: editDraft.pain_hypothesis,
        offer_id: editDraft.offer,
        proof_asset: editDraft.proof_asset,
        next_action: editDraft.next_action,
        next_action_due: editDraft.next_action_due,
      });
      setEditingId(null);
    } catch {
      setErr(t("patchFailed"));
    }
  };

  return (
    <div className="space-y-6" dir={isAr ? "rtl" : "ltr"}>
      {!hideHeader && (
        <p className="text-sm text-muted-foreground">{t("subtitle")}</p>
      )}

      {err && <p className="text-destructive text-sm">{err}</p>}
      {actionMsg && <p className="text-sm text-primary">{actionMsg}</p>}

      {targetingToday.length > 0 && (
        <Card className="p-4 border-primary/20">
          <h3 className="font-semibold text-sm mb-3">{t("todayTargetTitle")}</h3>
          <ul className="space-y-3 text-sm">
            {targetingToday.map((row, i) => (
              <li key={`${row.company}-${i}`} className="border-b pb-2 last:border-0">
                <p className="font-medium">{row.company || "—"}</p>
                <p className="text-xs text-muted-foreground">
                  {row.segment}
                  {row.channel ? ` · ${t("todayTargetChannel")}: ${row.channel}` : ""}
                </p>
                <p className="text-xs mt-1">{row.next_action}</p>
                {row.outreach_draft_ar && (
                  <pre className="text-xs mt-2 p-2 bg-muted/50 rounded whitespace-pre-wrap">
                    {row.outreach_draft_ar}
                  </pre>
                )}
              </li>
            ))}
          </ul>
        </Card>
      )}

      {summary && (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          <Card className="p-3">
            <p className="text-xs text-muted-foreground">{t("todayTouches")}</p>
            <p className="text-xl font-semibold">
              {summary.today?.top_targets_count ?? 0} / 10
            </p>
          </Card>
          <Card className="p-3">
            <p className="text-xs text-muted-foreground">{t("followUps")}</p>
            <p className="text-xl font-semibold">
              {summary.today?.follow_ups_due ?? 0}
            </p>
          </Card>
          <Card className="p-3">
            <p className="text-xs text-muted-foreground">{t("paid")}</p>
            <p className="text-xl font-semibold">{summary.revenue?.paid ?? 0}</p>
          </Card>
          <Card className="p-3 border-amber-500/30">
            <p className="text-xs text-muted-foreground">{t("risks")}</p>
            <p className="text-xs mt-1">
              {summary.anti_waste_guard?.blocked_sample
                ? t("antiWasteActive")
                : t("guardsOk")}
            </p>
          </Card>
        </div>
      )}

      <div className="flex flex-wrap gap-2">
        {(["top10", "follow", "due", "all"] as const).map((f) => (
          <Button
            key={f}
            size="sm"
            variant={filter === f ? "default" : "outline"}
            onClick={() => setFilter(f)}
          >
            {t(`filter.${f}`)}
          </Button>
        ))}
        <Button size="sm" variant="secondary" onClick={() => load()} disabled={loading}>
          {t("refresh")}
        </Button>
        <Button size="sm" variant="outline" onClick={importCsv} disabled={importing || loading}>
          {t("importCsv")}
        </Button>
        <Button
          size="sm"
          variant="ghost"
          onClick={() => setCsvOpen((v) => !v)}
          disabled={loading}
        >
          {t("importCsvToggle")}
        </Button>
        <Link href={`/${locale}/approvals`} className="text-sm text-primary self-center">
          {t("approvalsLink")}
        </Link>
      </div>

      {csvOpen && (
        <Card className="p-4 space-y-2">
          <p className="text-sm font-medium">{t("importCsvText")}</p>
          <textarea
            className="w-full min-h-[120px] text-xs border rounded p-2 font-mono"
            placeholder={t("importCsvPlaceholder")}
            value={csvText}
            onChange={(e) => setCsvText(e.target.value)}
          />
          <Button size="sm" onClick={importCsvText} disabled={importing || !csvText.trim()}>
            {t("importCsvSubmit")}
          </Button>
        </Card>
      )}

      {brief && briefLeadId && (
        <Card className="p-4 border-primary/20">
          <h3 className="font-semibold text-sm mb-2">{t("briefTitle")}</h3>
          <p className="text-sm font-medium">{brief.company}</p>
          {brief.outreach_draft_ar && (
            <pre className="text-xs mt-2 p-2 bg-muted/50 rounded whitespace-pre-wrap">
              {brief.outreach_draft_ar}
            </pre>
          )}
          {brief.discovery_questions_ar && (
            <ul className="text-xs mt-2 list-disc ps-4">
              {brief.discovery_questions_ar.map((q) => (
                <li key={q}>{q}</li>
              ))}
            </ul>
          )}
        </Card>
      )}

      <div className="overflow-x-auto rounded-lg border">
        <table className="w-full text-sm">
          <thead className="bg-muted/50">
            <tr>
              <th className="p-2 text-start w-8" />
              <th className="p-2 text-start">{t("col.target")}</th>
              <th className="p-2 text-start">{t("col.segment")}</th>
              <th className="p-2 text-start">{t("col.pain")}</th>
              <th className="p-2 text-start">{t("col.offer")}</th>
              <th className="p-2 text-start">{t("col.proof")}</th>
              <th className="p-2 text-start">{t("col.next")}</th>
              <th className="p-2 text-start">{t("col.status")}</th>
              <th className="p-2 text-start">{t("col.actions")}</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => {
              const isSelected = selectedLeadId === row.lead_id;
              const isEditing = editingId === row.lead_id;
              return (
                <tr
                  key={row.lead_id}
                  className={`border-t align-top ${isSelected ? "bg-muted/40" : ""}`}
                >
                  <td className="p-2">
                    <input
                      type="radio"
                      name="war-room-select"
                      checked={isSelected}
                      onChange={() => onSelectLead?.(row.lead_id)}
                    />
                  </td>
                  <td className="p-2">
                    <div className="font-medium">{row.target}</div>
                    <Badge variant="outline" className="mt-1 text-xs">
                      {row.lead_score}
                    </Badge>
                  </td>
                  {isEditing ? (
                    <>
                      <td className="p-2">
                        <input
                          className="w-full text-xs border rounded px-1"
                          value={editDraft.segment ?? ""}
                          onChange={(e) =>
                            setEditDraft((d) => ({ ...d, segment: e.target.value }))
                          }
                        />
                      </td>
                      <td className="p-2">
                        <input
                          className="w-full text-xs border rounded px-1"
                          value={editDraft.pain_hypothesis ?? ""}
                          onChange={(e) =>
                            setEditDraft((d) => ({
                              ...d,
                              pain_hypothesis: e.target.value,
                            }))
                          }
                        />
                      </td>
                      <td className="p-2">
                        <input
                          className="w-full text-xs border rounded px-1"
                          value={editDraft.offer ?? ""}
                          onChange={(e) =>
                            setEditDraft((d) => ({ ...d, offer: e.target.value }))
                          }
                        />
                      </td>
                      <td className="p-2">
                        <input
                          className="w-full text-xs border rounded px-1"
                          value={editDraft.proof_asset ?? ""}
                          onChange={(e) =>
                            setEditDraft((d) => ({ ...d, proof_asset: e.target.value }))
                          }
                        />
                      </td>
                      <td className="p-2">
                        <input
                          className="w-full text-xs border rounded px-1 mb-1"
                          value={editDraft.next_action ?? ""}
                          onChange={(e) =>
                            setEditDraft((d) => ({ ...d, next_action: e.target.value }))
                          }
                        />
                        <input
                          type="date"
                          className="w-full text-xs border rounded px-1"
                          value={(editDraft.next_action_due ?? "").slice(0, 10)}
                          onChange={(e) =>
                            setEditDraft((d) => ({
                              ...d,
                              next_action_due: e.target.value,
                            }))
                          }
                        />
                      </td>
                    </>
                  ) : (
                    <>
                      <td className="p-2">{row.segment || "—"}</td>
                      <td className="p-2 max-w-[10rem] truncate" title={row.pain_hypothesis}>
                        {row.pain_hypothesis || "—"}
                      </td>
                      <td className="p-2 text-xs">{row.offer || "—"}</td>
                      <td className="p-2 text-xs">{row.proof_asset || "—"}</td>
                      <td className="p-2 text-xs">
                        {row.next_action || "—"}
                        {row.next_action_due && (
                          <span className="text-muted-foreground block">
                            {row.next_action_due.slice(0, 10)}
                          </span>
                        )}
                      </td>
                    </>
                  )}
                  <td className="p-2">
                    <select
                      className="text-xs border rounded px-1 py-1 max-w-[9rem] bg-background"
                      value={row.status}
                      onChange={(e) => patchStatus(row.lead_id, e.target.value)}
                    >
                      {STATUS_OPTIONS.map((s) => (
                        <option key={s} value={s}>
                          {t(`status.${s}`)}
                        </option>
                      ))}
                    </select>
                  </td>
                  <td className="p-2">
                    <div className="flex flex-col gap-1">
                      {isEditing ? (
                        <>
                          <Button size="sm" variant="default" onClick={saveEdit}>
                            {t("save")}
                          </Button>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => setEditingId(null)}
                          >
                            {t("cancel")}
                          </Button>
                        </>
                      ) : (
                        <>
                          <Button size="sm" variant="outline" onClick={() => startEdit(row)}>
                            {t("edit")}
                          </Button>
                          <Button
                            size="sm"
                            variant="secondary"
                            onClick={() => generateDraft(row.lead_id)}
                          >
                            {t("genDraft")}
                          </Button>
                          <Button
                            size="sm"
                            variant="secondary"
                            onClick={() => generateClientPack(row)}
                          >
                            {t("clientPack")}
                          </Button>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => approveSend(row.lead_id)}
                          >
                            {t("approveSend")}
                          </Button>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => loadMeetingBrief(row.lead_id)}
                          >
                            {t("meetingBrief")}
                          </Button>
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => createInvoiceDraft(row.lead_id)}
                          >
                            {t("invoiceDraft")}
                          </Button>
                        </>
                      )}
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {rows.length === 0 && !loading && (
          <p className="p-4 text-center text-muted-foreground text-sm">{t("empty")}</p>
        )}
      </div>
    </div>
  );
}
