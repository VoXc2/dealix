"use client";

import { useState } from "react";
import { useTranslations, useLocale } from "next-intl";
import { motion, AnimatePresence } from "framer-motion";
import { Check, X, AlertTriangle, Clock, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { cn, getRiskColor, formatRelativeTime } from "@/lib/utils";
import { toast } from "sonner";
import type { ApprovalRequest, RiskLevel } from "@/types";

const mockApprovals: ApprovalRequest[] = [
  {
    id: "ap1",
    agentType: "outreach",
    action: "إرسال 50 رسالة تسويقية للشركات الناشئة في رياض",
    description: "يريد وكيل التواصل إرسال حملة بريد إلكتروني مستهدفة لـ 50 شركة ناشئة محددة في منطقة الرياض، استناداً إلى إشارات التمويل الأخيرة.",
    riskLevel: "high",
    status: "pending",
    requestedAt: new Date(Date.now() - 10 * 60000).toISOString(),
    target: "50 شركة ناشئة - الرياض",
    estimatedImpact: "متوسط معدل الرد المتوقع: 18%",
  },
  {
    id: "ap2",
    agentType: "compliance",
    action: "تعديل شروط العقد لتضمين بند PDPL الجديد",
    description: "وكيل الامتثال يقترح إضافة بند حماية البيانات وفق لوائح PDPL السعودية الجديدة لعام 2024 في جميع عقود العملاء.",
    riskLevel: "medium",
    status: "pending",
    requestedAt: new Date(Date.now() - 25 * 60000).toISOString(),
    target: "قوالب العقود - الإصدار 3.2",
    estimatedImpact: "تحسين الامتثال القانوني",
  },
  {
    id: "ap3",
    agentType: "scoring",
    action: "رفع أولوية 12 عميلاً إلى مستوى VIP",
    description: "بناءً على تحليل سلوك الشراء وإشارات التوسع الأخيرة، يقترح وكيل التقييم ترقية 12 حساباً إلى مستوى VIP.",
    riskLevel: "low",
    status: "pending",
    requestedAt: new Date(Date.now() - 40 * 60000).toISOString(),
    target: "12 حساب - درجة AI > 85",
    estimatedImpact: "إيرادات متوقعة إضافية: 2.4M ريال",
  },
  {
    id: "ap4",
    agentType: "outreach",
    action: "جدولة مكالمات متابعة مع عملاء المرحلة C",
    description: "تلقائي: تحديد 8 مواعيد اجتماعات مع عملاء لم يستجيبوا خلال 14 يوماً.",
    riskLevel: "low",
    status: "approved",
    requestedAt: new Date(Date.now() - 3 * 3600000).toISOString(),
    reviewedAt: new Date(Date.now() - 2 * 3600000).toISOString(),
    reviewedBy: "أحمد الحربي",
    target: "8 عملاء - المرحلة C",
  },
  {
    id: "ap5",
    agentType: "intelligence",
    action: "الوصول إلى بيانات LinkedIn للتحقق من التغييرات الوظيفية",
    description: "طلب صلاحية للوصول إلى بيانات LinkedIn للتحقق من تغييرات الوظيفة لدى جهات الاتصال الرئيسية.",
    riskLevel: "high",
    status: "rejected",
    requestedAt: new Date(Date.now() - 5 * 3600000).toISOString(),
    reviewedAt: new Date(Date.now() - 4 * 3600000).toISOString(),
    reviewedBy: "سارة القحطاني",
    target: "150 جهة اتصال",
  },
];

const riskIcons: Record<RiskLevel, React.ReactNode> = {
  high: <AlertTriangle className="w-3.5 h-3.5" />,
  medium: <Shield className="w-3.5 h-3.5" />,
  low: <Clock className="w-3.5 h-3.5" />,
};

function ApprovalCard({ request, onApprove, onReject }: {
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
              onClick={() => onApprove(request.id)}
            >
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
          <div className={cn(
            "flex items-center justify-between text-xs p-2 rounded-lg",
            request.status === "approved" ? "bg-emerald-500/10 text-emerald-400" : "bg-red-500/10 text-red-400"
          )}>
            {request.status === "approved" ? <Check className="w-3.5 h-3.5" /> : <X className="w-3.5 h-3.5" />}
            <span className="font-medium">
              {request.status === "approved" ? t("approved") : t("rejected")} {isAr ? "بواسطة" : "by"} {request.reviewedBy}
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
  const [approvals, setApprovals] = useState(mockApprovals);

  const handleApprove = (id: string) => {
    setApprovals((prev) =>
      prev.map((a) => a.id === id ? { ...a, status: "approved" as const, reviewedAt: new Date().toISOString(), reviewedBy: isAr ? "أنت" : "You" } : a)
    );
    toast.success(isAr ? "تمت الموافقة بنجاح" : "Approved successfully");
  };

  const handleReject = (id: string) => {
    setApprovals((prev) =>
      prev.map((a) => a.id === id ? { ...a, status: "rejected" as const, reviewedAt: new Date().toISOString(), reviewedBy: isAr ? "أنت" : "You" } : a)
    );
    toast.error(isAr ? "تم الرفض" : "Rejected");
  };

  const pending = approvals.filter((a) => a.status === "pending");
  const reviewed = approvals.filter((a) => a.status !== "pending");

  return (
    <div>
      {/* Summary */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        {[
          { label: isAr ? "قيد الانتظار" : "Pending", value: pending.length, color: "text-gold-400", bg: "bg-gold-400/10" },
          { label: isAr ? "موافق عليه" : "Approved", value: approvals.filter((a) => a.status === "approved").length, color: "text-emerald-400", bg: "bg-emerald-400/10" },
          { label: isAr ? "مرفوض" : "Rejected", value: approvals.filter((a) => a.status === "rejected").length, color: "text-red-400", bg: "bg-red-400/10" },
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
            {pending.length === 0 ? (
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
            {reviewed.map((approval) => (
              <ApprovalCard
                key={approval.id}
                request={approval}
                onApprove={handleApprove}
                onReject={handleReject}
              />
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
