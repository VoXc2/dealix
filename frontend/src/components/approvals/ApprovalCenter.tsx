"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useTranslations, useLocale } from "next-intl";
import { motion, AnimatePresence } from "framer-motion";
import { Check, X, AlertTriangle, Clock, Shield, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { cn, getRiskColor, formatRelativeTime } from "@/lib/utils";
import { toast } from "sonner";
import type { ApprovalRequest, RiskLevel, AgentType, ApprovalStatus } from "@/types";
import { api } from "@/lib/api";

const APPROVAL_WHO = process.env.NEXT_PUBLIC_APPROVAL_ACTOR?.trim() || "sami";

function mapRisk(raw: string | undefined): RiskLevel {
  const r = (raw || "low").toLowerCase();
  if (r === "high" || r === "critical") return "high";
  if (r === "medium") return "medium";
  return "low";
}

function mapAgentType(actionType: string | undefined): AgentType {
  const at = (actionType || "").toLowerCase();
  if (at.includes("email") || at.includes("draft_email") || at.includes("outreach")) return "outreach";
  if (at.includes("linkedin")) return "intelligence";
  if (at.includes("support")) return "scoring";
  if (at.includes("payment") || at.includes("compliance") || at.includes("pdpl")) return "compliance";
  return "orchestrator";
}

function mapStatus(raw: string | undefined): ApprovalStatus {
  const s = (raw || "pending").toLowerCase();
  if (s === "approved") return "approved";
  if (s === "rejected") return "rejected";
  return "pending";
}

function mapApiApproval(raw: Record<string, unknown>): ApprovalRequest {
  const summaryAr = String(raw.summary_ar || "");
  const summaryEn = String(raw.summary_en || "");
  const actionType = String(raw.action_type || "");
  return {
    id: String(raw.approval_id || raw.id || "unknown"),
    agentType: mapAgentType(actionType),
    action: summaryAr || summaryEn || actionType || "—",
    description: `${String(raw.object_type || "object")} · ${String(raw.object_id || "—")}`,
    riskLevel: mapRisk(String(raw.risk_level)),
    status: mapStatus(String(raw.status)),
    requestedAt: String(raw.created_at || new Date().toISOString()),
    reviewedAt: raw.updated_at ? String(raw.updated_at) : undefined,
    reviewedBy: undefined,
    target: String(raw.channel || raw.object_id || "—"),
    estimatedImpact: String(raw.proof_impact || raw.action_mode || ""),
  };
}

const riskIcons: Record<RiskLevel, React.ReactNode> = {
  high: <AlertTriangle className="w-3.5 h-3.5" />,
  medium: <Shield className="w-3.5 h-3.5" />,
  low: <Clock className="w-3.5 h-3.5" />,
};

function ApprovalCard({
  request,
  onApprove,
  onReject,
}: {
  request: ApprovalRequest;
  onApprove: (id: string) => void;
  onReject: (id: string) => void;
}) {
  const t = useTranslations("approvals");
  const locale = useLocale();
  const isAr = locale === "ar";

  const agentIconMap: Record<string, string> = {
    outreach: "📤",
    scoring: "📊",
    compliance: "🛡️",
    intelligence: "🔍",
    orchestrator: "⚙️",
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="rounded-2xl border border-border bg-card overflow-hidden hover:border-border/80 transition-all"
    >
      <div
        className={cn(
          "h-1",
          request.riskLevel === "high"
            ? "bg-gradient-to-r from-red-500 to-red-400"
            : request.riskLevel === "medium"
              ? "bg-gradient-to-r from-gold-500 to-gold-400"
              : "bg-gradient-to-r from-emerald-500 to-emerald-400",
        )}
      />

      <div className="p-5">
        <div className="flex items-start justify-between gap-3 mb-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-muted flex items-center justify-center text-base">
              {agentIconMap[request.agentType]}
            </div>
            <div>
              <p className="text-xs text-muted-foreground capitalize">{request.agentType}</p>
              <h4 className="text-sm font-semibold text-foreground leading-tight mt-0.5">
                {request.action}
              </h4>
            </div>
          </div>
          <Badge
            variant="outline"
            className={cn("flex items-center gap-1 text-[10px] flex-shrink-0", getRiskColor(request.riskLevel))}
          >
            {riskIcons[request.riskLevel]}
            {t(`${request.riskLevel}Risk` as "highRisk")}
          </Badge>
        </div>

        <p className="text-sm text-muted-foreground mb-4 leading-relaxed">{request.description}</p>

        <div className="grid grid-cols-1 gap-2 mb-4 p-3 rounded-xl bg-muted/40">
          <div className="flex items-center justify-between text-xs">
            <span className="text-muted-foreground">{isAr ? "الهدف:" : "Target:"}</span>
            <span className="font-medium text-foreground">{request.target}</span>
          </div>
          {request.estimatedImpact && (
            <div className="flex items-center justify-between text-xs">
              <span className="text-muted-foreground">{isAr ? "الأثر / الوضع:" : "Impact / mode:"}</span>
              <span className="font-medium text-emerald-400">{request.estimatedImpact}</span>
            </div>
          )}
          <div className="flex items-center justify-between text-xs">
            <span className="text-muted-foreground">{isAr ? "وقت الطلب:" : "Requested:"}</span>
            <span className="font-medium text-foreground">
              {formatRelativeTime(request.requestedAt, locale)}
            </span>
          </div>
        </div>

        {request.status === "pending" && (
          <div className="flex gap-3">
            <Button variant="emerald" size="sm" className="flex-1" onClick={() => onApprove(request.id)}>
              <Check className="w-3.5 h-3.5 me-1.5" />
              {t("approve")}
            </Button>
            <Button
              variant="outline"
              size="sm"
              className="flex-1 text-destructive border-destructive/30 hover:bg-destructive/10"
              onClick={() => onReject(request.id)}
            >
              <X className="w-3.5 h-3.5 me-1.5" />
              {t("reject")}
            </Button>
          </div>
        )}

        {request.status !== "pending" && (
          <div
            className={cn(
              "flex items-center justify-between text-xs p-2 rounded-lg",
              request.status === "approved" ? "bg-emerald-500/10 text-emerald-400" : "bg-red-500/10 text-red-400",
            )}
          >
            {request.status === "approved" ? <Check className="w-3.5 h-3.5" /> : <X className="w-3.5 h-3.5" />}
            <span className="font-medium">
              {request.status === "approved" ? t("approved") : t("rejected")}
              {request.reviewedBy ? ` ${isAr ? "بواسطة" : "by"} ${request.reviewedBy}` : ""}
            </span>
            {request.reviewedAt && (
              <span className="text-muted-foreground">{formatRelativeTime(request.reviewedAt, locale)}</span>
            )}
          </div>
        )}
      </div>
    </motion.div>
  );
}

export function ApprovalCenter() {
  const t = useTranslations("approvals");
  const locale = useLocale();
  const isAr = locale === "ar";
  const [pending, setPending] = useState<ApprovalRequest[]>([]);
  const [reviewed, setReviewed] = useState<ApprovalRequest[]>([]);
  const [gmail, setGmail] = useState<Record<string, unknown>[]>([]);
  const [linkedin, setLinkedin] = useState<Record<string, unknown>[]>([]);
  const [policy, setPolicy] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadAll = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [pRes, hRes, gRes, lRes, polRes] = await Promise.all([
        api.getApprovalsPending(),
        api.getApprovalsHistory(80),
        api.getGmailDraftsToday(),
        api.getLinkedInDraftsToday(),
        api.getChannelPolicyStatus(),
      ]);

      const pRows = (pRes.data as { approvals?: unknown[] })?.approvals ?? [];
      setPending(pRows.map((r) => mapApiApproval(r as Record<string, unknown>)));

      const hRows = (hRes.data as { approvals?: unknown[] })?.approvals ?? [];
      setReviewed(
        hRows
          .map((r) => mapApiApproval(r as Record<string, unknown>))
          .filter((a) => a.status !== "pending"),
      );

      const gData = gRes.data as { items?: Record<string, unknown>[]; count?: number };
      setGmail(Array.isArray(gData.items) ? gData.items : []);

      const lData = lRes.data as { items?: Record<string, unknown>[] };
      setLinkedin(Array.isArray(lData.items) ? lData.items : []);

      setPolicy((polRes.data as Record<string, unknown>) || null);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "load_failed";
      setError(msg);
      toast.error(isAr ? "تعذر تحميل البيانات من الخادم" : "Could not load from API");
    } finally {
      setLoading(false);
    }
  }, [isAr]);

  useEffect(() => {
    void loadAll();
  }, [loadAll]);

  const counts = useMemo(
    () => ({
      pending: pending.length,
      approved: reviewed.filter((a) => a.status === "approved").length,
      rejected: reviewed.filter((a) => a.status === "rejected").length,
    }),
    [pending, reviewed],
  );

  const handleApprove = async (id: string) => {
    try {
      await api.postApprovalApprove(id, APPROVAL_WHO);
      toast.success(isAr ? "تمت الموافقة في الخادم" : "Approved on server");
      await loadAll();
    } catch {
      toast.error(isAr ? "فشلت الموافقة" : "Approve failed");
    }
  };

  const handleReject = async (id: string) => {
    const reason = isAr ? "مرفوض من لوحة الموافقات" : "Rejected from approvals UI";
    try {
      await api.postApprovalReject(id, APPROVAL_WHO, reason);
      toast.success(isAr ? "تم الرفض في الخادم" : "Rejected on server");
      await loadAll();
    } catch {
      toast.error(isAr ? "فشل الرفض" : "Reject failed");
    }
  };

  return (
    <div>
      <div className="flex flex-wrap items-center justify-between gap-3 mb-6">
        <div className="flex gap-2">
          <Button variant="outline" size="sm" onClick={() => void loadAll()} disabled={loading}>
            <RefreshCw className={cn("w-4 h-4 me-1", loading && "animate-spin")} />
            {isAr ? "تحديث" : "Refresh"}
          </Button>
          <Button variant="ghost" size="sm" asChild>
            <Link href={`/${locale}/trust-check`}>{isAr ? "فحص منع الهدر" : "Anti-waste check"}</Link>
          </Button>
        </div>
        {error && <p className="text-xs text-destructive">{error}</p>}
      </div>

      <div className="grid grid-cols-3 gap-4 mb-6">
        {[
          { label: isAr ? "قيد الانتظار" : "Pending", value: counts.pending, color: "text-gold-400", bg: "bg-gold-400/10" },
          { label: isAr ? "موافق عليه (سجل)" : "Approved (history)", value: counts.approved, color: "text-emerald-400", bg: "bg-emerald-400/10" },
          { label: isAr ? "مرفوض (سجل)" : "Rejected (history)", value: counts.rejected, color: "text-red-400", bg: "bg-red-400/10" },
        ].map((s, i) => (
          <motion.div
            key={s.label}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.07 }}
            className={cn("rounded-2xl border border-border p-4", s.bg)}
          >
            <p className={cn("text-3xl font-bold", s.color)}>{s.value}</p>
            <p className="text-sm text-muted-foreground mt-1">{s.label}</p>
          </motion.div>
        ))}
      </div>

      <Tabs defaultValue="pending">
        <TabsList className="mb-6 flex flex-wrap h-auto gap-1">
          <TabsTrigger value="pending">
            {isAr ? "قيد الانتظار" : "Pending"} ({pending.length})
          </TabsTrigger>
          <TabsTrigger value="reviewed">
            {isAr ? "السجل" : "History"} ({reviewed.length})
          </TabsTrigger>
          <TabsTrigger value="drafts">{isAr ? "مسودات اليوم" : "Today's drafts"}</TabsTrigger>
          <TabsTrigger value="policy">{isAr ? "بوابة القنوات" : "Channel gates"}</TabsTrigger>
        </TabsList>

        <TabsContent value="pending">
          <AnimatePresence>
            {loading ? (
              <p className="text-muted-foreground text-sm">{isAr ? "جاري التحميل…" : "Loading…"}</p>
            ) : pending.length === 0 ? (
              <div className="text-center py-16 text-muted-foreground">
                <p className="text-4xl mb-3">✅</p>
                <p className="font-medium">{isAr ? "لا توجد موافقات معلقة" : "No pending approvals"}</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                {pending.map((approval) => (
                  <ApprovalCard
                    key={approval.id}
                    request={approval}
                    onApprove={handleApprove}
                    onReject={handleReject}
                  />
                ))}
              </div>
            )}
          </AnimatePresence>
        </TabsContent>

        <TabsContent value="reviewed">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {reviewed.length === 0 ? (
              <p className="text-muted-foreground text-sm">{isAr ? "لا سجل بعد" : "No history yet"}</p>
            ) : (
              reviewed.map((approval) => (
                <ApprovalCard
                  key={`${approval.id}-${approval.status}`}
                  request={approval}
                  onApprove={handleApprove}
                  onReject={handleReject}
                />
              ))
            )}
          </div>
        </TabsContent>

        <TabsContent value="drafts">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div>
              <h3 className="text-sm font-semibold mb-2">Gmail</h3>
              {gmail.length === 0 ? (
                <p className="text-xs text-muted-foreground">{isAr ? "لا مسودات اليوم" : "No Gmail drafts today"}</p>
              ) : (
                <ul className="space-y-2 text-xs">
                  {gmail.map((row) => (
                    <li key={String(row.id)} className="rounded-lg border border-border p-3 bg-muted/30">
                      <p className="font-medium">{String(row.subject || "—")}</p>
                      <p className="text-muted-foreground truncate">{String(row.to_email || "")}</p>
                    </li>
                  ))}
                </ul>
              )}
            </div>
            <div>
              <h3 className="text-sm font-semibold mb-2">LinkedIn</h3>
              {linkedin.length === 0 ? (
                <p className="text-xs text-muted-foreground">{isAr ? "لا مسودات اليوم" : "No LinkedIn drafts today"}</p>
              ) : (
                <ul className="space-y-2 text-xs">
                  {linkedin.map((row) => (
                    <li key={String(row.id)} className="rounded-lg border border-border p-3 bg-muted/30">
                      <p className="font-medium">{String(row.company_name || "—")}</p>
                      <p className="text-muted-foreground line-clamp-3">{String(row.message_ar || "")}</p>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </TabsContent>

        <TabsContent value="policy">
          {policy ? (
            <pre className="text-xs bg-muted/40 rounded-xl p-4 overflow-auto max-h-[420px]">
              {JSON.stringify(policy, null, 2)}
            </pre>
          ) : (
            <p className="text-muted-foreground text-sm">{isAr ? "لا بيانات" : "No data"}</p>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
