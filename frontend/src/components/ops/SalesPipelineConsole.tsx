"use client";

import { useCallback, useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { toast } from "sonner";
import { api } from "@/lib/api";

interface Task {
  task_id: string;
  agent_id: string;
  action_type: string;
  status: string;
  customer_id: string;
  requires_approval: boolean;
}

const AUTOMATIONS = [
  "on_lead",
  "on_qualified",
  "on_booking",
  "on_scope",
  "on_payment",
  "on_support",
  "on_customer_success",
];

const STATUS_COLORS: Record<string, string> = {
  pending: "text-blue-400",
  awaiting_approval: "text-amber-400",
  approved: "text-emerald-400",
  executing: "text-purple-400",
  succeeded: "text-emerald-400",
  rejected: "text-red-400",
  failed: "text-red-400",
};

export function SalesPipelineConsole() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const T = (ar: string, en: string) => (isAr ? ar : en);

  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.getOrchestratorTasks();
      const data = res.data as { tasks?: Task[] };
      setTasks(Array.isArray(data.tasks) ? data.tasks : []);
    } catch {
      toast.error(T("تعذّر تحميل المهام", "Could not load tasks"));
    } finally {
      setLoading(false);
    }
  }, [isAr]);

  useEffect(() => {
    void load();
  }, [load]);

  async function fire(name: string) {
    try {
      const res = await api.triggerAutomation(name, {
        entity_id: `manual_${Date.now()}`,
      });
      const data = res.data as { requires_approval: boolean };
      toast.success(
        data.requires_approval
          ? T("تم — يحتاج موافقة", "Triggered — approval required")
          : T("تم تشغيل الأتمتة", "Automation triggered"),
      );
      await load();
    } catch {
      toast.error(T("تعذّر التشغيل", "Trigger failed"));
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-muted-foreground">
          {T("مهام محرّك المبيعات والأتمتة.", "Sales engine tasks and automations.")}
        </p>
        <Button variant="outline" size="sm" onClick={() => void load()} disabled={loading}>
          <RefreshCw className={cn("w-4 h-4 me-1", loading && "animate-spin")} />
          {T("تحديث", "Refresh")}
        </Button>
      </div>

      <div className="rounded-2xl border border-border bg-card p-4 mb-6">
        <h3 className="text-sm font-semibold mb-3">{T("تشغيل أتمتة", "Run an automation")}</h3>
        <div className="flex flex-wrap gap-2">
          {AUTOMATIONS.map((a) => (
            <Button key={a} variant="outline" size="sm" onClick={() => void fire(a)}>
              {a}
            </Button>
          ))}
        </div>
        <p className="text-[11px] text-muted-foreground mt-3">
          {T(
            "الإجراءات عالية المخاطر تُسجَّل بانتظار الموافقة ولا تُنفَّذ تلقائياً.",
            "High-risk actions are queued awaiting approval — never auto-executed.",
          )}
        </p>
      </div>

      <h3 className="text-sm font-semibold mb-2">{T("المهام", "Tasks")}</h3>
      {loading ? (
        <p className="text-sm text-muted-foreground">{T("جاري التحميل…", "Loading…")}</p>
      ) : tasks.length === 0 ? (
        <p className="text-sm text-muted-foreground">{T("لا مهام بعد", "No tasks yet")}</p>
      ) : (
        <div className="space-y-2">
          {tasks.map((t) => (
            <div
              key={t.task_id}
              className="rounded-xl border border-border bg-card p-3 flex items-center justify-between gap-3"
            >
              <div className="min-w-0">
                <p className="text-sm font-medium">{t.action_type}</p>
                <p className="text-[11px] text-muted-foreground">
                  {t.agent_id} · {t.customer_id}
                </p>
              </div>
              <div className="flex items-center gap-2">
                {t.requires_approval && (
                  <Badge variant="outline" className="text-[10px] text-amber-400">
                    {T("موافقة", "approval")}
                  </Badge>
                )}
                <span
                  className={cn(
                    "text-xs font-medium",
                    STATUS_COLORS[t.status] || "text-muted-foreground",
                  )}
                >
                  {t.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
