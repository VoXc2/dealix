"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { useLocale } from "next-intl";
import { motion } from "framer-motion";
import { RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn, formatRelativeTime } from "@/lib/utils";
import { toast } from "sonner";
import { api } from "@/lib/api";

interface OrchStatus {
  automations: string[];
  high_risk_actions: string[];
  agents: Record<string, number>;
  task_summary: Record<string, number>;
}

interface EvidenceEvent {
  event_id: string;
  event_type: string;
  entity_type: string;
  entity_id: string;
  summary_en?: string;
  summary_ar?: string;
  created_at: string;
}

export function FounderCommandCenter() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const T = (ar: string, en: string) => (isAr ? ar : en);

  const [status, setStatus] = useState<OrchStatus | null>(null);
  const [pendingApprovals, setPendingApprovals] = useState(0);
  const [evidence, setEvidence] = useState<EvidenceEvent[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [statusRes, approvalsRes, evidenceRes] = await Promise.all([
        api.getOrchestratorStatus(),
        api.getApprovalsPending(),
        api.getEvidence({ limit: 12 }),
      ]);
      setStatus(statusRes.data as OrchStatus);
      const aData = approvalsRes.data as { approvals?: unknown[] };
      setPendingApprovals(Array.isArray(aData.approvals) ? aData.approvals.length : 0);
      const eData = evidenceRes.data as { events?: EvidenceEvent[] };
      setEvidence(Array.isArray(eData.events) ? eData.events : []);
    } catch {
      toast.error(T("تعذّر تحميل اللوحة", "Could not load the command center"));
    } finally {
      setLoading(false);
    }
  }, [isAr]);

  useEffect(() => {
    void load();
  }, [load]);

  const tasks = status?.task_summary || {};
  const stats = [
    {
      label: T("موافقات معلّقة", "Pending approvals"),
      value: pendingApprovals,
      color: "text-gold-400",
      bg: "bg-gold-400/10",
    },
    {
      label: T("بانتظار الموافقة", "Awaiting approval"),
      value: tasks["awaiting_approval"] || 0,
      color: "text-amber-400",
      bg: "bg-amber-400/10",
    },
    {
      label: T("مهام قيد التنفيذ", "Tasks pending"),
      value: tasks["pending"] || 0,
      color: "text-blue-400",
      bg: "bg-blue-400/10",
    },
    {
      label: T("الوكلاء", "Agents"),
      value: status?.agents?.total || 0,
      color: "text-emerald-400",
      bg: "bg-emerald-400/10",
    },
  ];

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <p className="text-sm text-muted-foreground">
          {T("ملخّص العمليات اليومي للمؤسس.", "Daily operations snapshot for the founder.")}
        </p>
        <Button variant="outline" size="sm" onClick={() => void load()} disabled={loading}>
          <RefreshCw className={cn("w-4 h-4 me-1", loading && "animate-spin")} />
          {T("تحديث", "Refresh")}
        </Button>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {stats.map((s, i) => (
          <motion.div
            key={s.label}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            className={cn("rounded-2xl border border-border p-4", s.bg)}
          >
            <p className={cn("text-3xl font-bold", s.color)}>{s.value}</p>
            <p className="text-xs text-muted-foreground mt-1">{s.label}</p>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="rounded-2xl border border-border bg-card p-5">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-semibold">{T("أحدث الأدلة", "Latest evidence")}</h3>
            <Link
              href={`/${locale}/ops/evidence`}
              className="text-xs text-gold-400 hover:underline"
            >
              {T("عرض السجل", "View ledger")}
            </Link>
          </div>
          {evidence.length === 0 ? (
            <p className="text-xs text-muted-foreground">{T("لا أحداث", "No events")}</p>
          ) : (
            <ul className="space-y-2">
              {evidence.map((e) => (
                <li key={e.event_id} className="text-xs flex justify-between gap-2">
                  <span className="truncate">
                    <Badge variant="outline" className="text-[9px] me-1">
                      {e.event_type}
                    </Badge>
                    {(isAr ? e.summary_ar : e.summary_en) || e.entity_id}
                  </span>
                  <span className="text-muted-foreground whitespace-nowrap">
                    {formatRelativeTime(e.created_at, locale)}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="rounded-2xl border border-border bg-card p-5">
          <h3 className="text-sm font-semibold mb-3">
            {T("الإجراءات عالية المخاطر", "High-risk actions")}
          </h3>
          <p className="text-xs text-muted-foreground mb-2">
            {T(
              "هذه الإجراءات تمرّ دائماً عبر موافقتك.",
              "These actions always route through your approval.",
            )}
          </p>
          <div className="flex flex-wrap gap-1.5">
            {(status?.high_risk_actions || []).map((a) => (
              <Badge key={a} variant="outline" className="text-[10px]">
                {a}
              </Badge>
            ))}
          </div>
          <Link
            href={`/${locale}/approvals`}
            className="inline-block mt-4 text-xs text-gold-400 hover:underline"
          >
            {T("افتح مركز الموافقات", "Open the Approval Center")}
          </Link>
        </div>
      </div>
    </div>
  );
}
