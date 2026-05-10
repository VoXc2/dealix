"use client";

import { useMemo } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useTranslations, useLocale } from "next-intl";
import { motion, AnimatePresence } from "framer-motion";
import { Check, X, AlertTriangle, Clock, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { cn, getRiskColor, formatRelativeTime } from "@/lib/utils";
import { toast } from "sonner";
import { api } from "@/lib/api";
import {
  backendApprovalToUi,
  extractApprovalRows,
} from "@/lib/api-normalize";
import { useAuth } from "@/lib/hooks/useAuth";
import type { ApprovalRequest, RiskLevel } from "@/types";

const riskIcons: Record<RiskLevel, React.ReactNode> = {
  high: <AlertTriangle className="w-3.5 h-3.5" />,
  medium: <Shield className="w-3.5 h-3.5" />,
  low: <Clock className="w-3.5 h-3.5" />,
};

function ApprovalCard({ request, onApprove, onReject, actionsDisabled }: {
  request: ApprovalRequest;
  onApprove: (id: string) => void;
  onReject: (id: string) => void;
  actionsDisabled?: boolean;
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
      {/* Risk stripe */}
      <div className={cn(
        "h-1",
        request.riskLevel === "high" ? "bg-gradient-to-r from-red-500 to-red-400" :
        request.riskLevel === "medium" ? "bg-gradient-to-r from-gold-500 to-gold-400" :
        "bg-gradient-to-r from-emerald-500 to-emerald-400"
      )} />

      <div className="p-5">
        {/* Header */}
        <div className="flex items-start justify-between gap-3 mb-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-muted flex items-center justify-center text-base">
              {agentIconMap[request.agentType] ?? "⚙️"}
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

        {/* Description */}
        <p className="text-sm text-muted-foreground mb-4 leading-relaxed">
          {request.description}
        </p>

        {/* Target & Impact */}
        <div className="grid grid-cols-1 gap-2 mb-4 p-3 rounded-xl bg-muted/40">
          <div className="flex items-center justify-between text-xs">
            <span className="text-muted-foreground">{isAr ? "الهدف:" : "Target:"}</span>
            <span className="font-medium text-foreground">{request.target}</span>
          </div>
          {request.estimatedImpact && (
            <div className="flex items-center justify-between text-xs">
              <span className="text-muted-foreground">{isAr ? "التأثير المتوقع:" : "Estimated Impact:"}</span>
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

        {/* Actions */}
        {request.status === "pending" && (
          <div className="flex gap-3">
            <Button
              variant="emerald"
              size="sm"
              className="flex-1"
              disabled={actionsDisabled}
              onClick={() => onApprove(request.id)}
            >
              <Check className="w-3.5 h-3.5 me-1.5" />
              {t("approve")}
            </Button>
            <Button
              variant="outline"
              size="sm"
              className="flex-1 text-destructive border-destructive/30 hover:bg-destructive/10"
              disabled={actionsDisabled}
              onClick={() => onReject(request.id)}
            >
              <X className="w-3.5 h-3.5 me-1.5" />
              {t("reject")}
            </Button>
          </div>
        )}

        {request.status !== "pending" && (
          <div className={cn(
            "flex items-center justify-between text-xs p-2 rounded-lg",
            request.status === "approved" ? "bg-emerald-500/10 text-emerald-400" : "bg-red-500/10 text-red-400"
          )}>
            {request.status === "approved" ? <Check className="w-3.5 h-3.5" /> : <X className="w-3.5 h-3.5" />}
            <span className="font-medium">
              {request.status === "approved" ? t("approved") : t("rejected")}{" "}
              {isAr ? "بواسطة" : "by"}{" "}
              {request.reviewedBy ?? (isAr ? "غير معروف" : "Unknown")}
            </span>
            <span className="text-muted-foreground">
              {request.reviewedAt && formatRelativeTime(request.reviewedAt, locale)}
            </span>
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
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const who = user?.email?.trim() || (isAr ? "لوحة_التحكم" : "dashboard_user");

  const pendingQuery = useQuery({
    queryKey: ["approvals", "pending"],
    queryFn: async () => (await api.getApprovals()).data,
  });

  const historyQuery = useQuery({
    queryKey: ["approvals", "history"],
    queryFn: async () => (await api.getApprovalsHistory(100)).data,
  });

  const pending = useMemo(() => {
    return extractApprovalRows(pendingQuery.data)
      .map(backendApprovalToUi)
      .filter((a) => a.status === "pending");
  }, [pendingQuery.data]);

  const reviewed = useMemo(() => {
    return extractApprovalRows(historyQuery.data)
      .map(backendApprovalToUi)
      .filter((a) => a.status !== "pending");
  }, [historyQuery.data]);

  const approveMut = useMutation({
    mutationFn: (id: string) => api.approveApproval(id, who),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["approvals"] });
      toast.success(isAr ? "تمت الموافقة بنجاح" : "Approved successfully");
    },
    onError: () => {
      toast.error(isAr ? "فشلت الموافقة" : "Approval failed");
    },
  });

  const rejectMut = useMutation({
    mutationFn: (id: string) =>
      api.rejectApproval(id, who, isAr ? "مرفوض من لوحة التحكم" : "Rejected from dashboard"),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["approvals"] });
      toast.success(isAr ? "تم الرفض" : "Rejected");
    },
    onError: () => {
      toast.error(isAr ? "فشل الرفض" : "Reject failed");
    },
  });

  const handleApprove = (id: string) => approveMut.mutate(id);
  const handleReject = (id: string) => rejectMut.mutate(id);

  const loading = pendingQuery.isLoading || historyQuery.isLoading;
  const hasError = pendingQuery.isError || historyQuery.isError;

  return (
    <div>
      {hasError && (
        <div
          role="alert"
          className="mb-4 rounded-xl border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm"
        >
          <p>
            {isAr
              ? "تعذر تحميل طلبات الموافقة. تحقق من الـ API."
              : "Could not load approvals. Check the API."}
          </p>
          <div className="mt-2 flex gap-2">
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => {
                pendingQuery.refetch();
                historyQuery.refetch();
              }}
            >
              {isAr ? "إعادة المحاولة" : "Retry"}
            </Button>
          </div>
        </div>
      )}

      {/* Summary */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        {[
          { label: isAr ? "قيد الانتظار" : "Pending", value: pending.length, color: "text-gold-400", bg: "bg-gold-400/10" },
          {
            label: isAr ? "موافق عليه" : "Approved",
            value: reviewed.filter((a) => a.status === "approved").length,
            color: "text-emerald-400",
            bg: "bg-emerald-400/10",
          },
          {
            label: isAr ? "مرفوض / منتهي" : "Rejected / closed",
            value: reviewed.filter((a) => a.status !== "approved").length,
            color: "text-red-400",
            bg: "bg-red-400/10",
          },
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
        <TabsList className="mb-6">
          <TabsTrigger value="pending">
            {isAr ? "قيد الانتظار" : "Pending"} ({pending.length})
          </TabsTrigger>
          <TabsTrigger value="reviewed">
            {isAr ? "تمت المراجعة" : "Reviewed"} ({reviewed.length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="pending">
          <AnimatePresence>
            {loading ? (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                {Array.from({ length: 4 }).map((_, i) => (
                  <div
                    key={i}
                    className="h-48 rounded-2xl bg-muted/50 animate-pulse border border-border"
                  />
                ))}
              </div>
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
                    actionsDisabled={approveMut.isPending || rejectMut.isPending}
                  />
                ))}
              </div>
            )}
          </AnimatePresence>
        </TabsContent>

        <TabsContent value="reviewed">
          {loading ? (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {Array.from({ length: 4 }).map((_, i) => (
                <div
                  key={i}
                  className="h-48 rounded-2xl bg-muted/50 animate-pulse border border-border"
                />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {reviewed.length === 0 ? (
                <p className="text-sm text-muted-foreground col-span-full text-center py-12">
                  {isAr ? "لا يوجد سجل مراجعة بعد." : "No review history yet."}
                </p>
              ) : (
                reviewed.map((approval) => (
                  <ApprovalCard
                    key={approval.id}
                    request={approval}
                    onApprove={handleApprove}
                    onReject={handleReject}
                    actionsDisabled={approveMut.isPending || rejectMut.isPending}
                  />
                ))
              )}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}
