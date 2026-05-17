"use client";

import { useCallback, useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { cn } from "@/lib/utils";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { KnowledgeManager } from "@/components/ops/KnowledgeManager";

interface Ticket {
  ticket_id: string;
  subject: string;
  message_redacted: string;
  category: string;
  status: string;
  risk_level: string;
  suggested_reply: string;
  escalation_needed: boolean;
}

const RISK_COLOR: Record<string, string> = {
  high: "text-red-400",
  medium: "text-amber-400",
  low: "text-emerald-400",
};

function TicketCard({ ticket, onAction }: { ticket: Ticket; onAction: () => void }) {
  const locale = useLocale();
  const isAr = locale === "ar";
  const T = (ar: string, en: string) => (isAr ? ar : en);

  async function run(fn: () => Promise<unknown>, ok: string) {
    try {
      await fn();
      toast.success(ok);
      onAction();
    } catch {
      toast.error(T("فشل الإجراء", "Action failed"));
    }
  }

  return (
    <div className="rounded-xl border border-border bg-card p-4">
      <div className="flex items-start justify-between gap-3 mb-2">
        <div className="min-w-0">
          <p className="text-sm font-semibold truncate">
            {ticket.subject || ticket.ticket_id}
          </p>
          <p className="text-xs text-muted-foreground line-clamp-2 mt-0.5">
            {ticket.message_redacted}
          </p>
        </div>
        <span className={cn("text-xs font-medium", RISK_COLOR[ticket.risk_level])}>
          {ticket.risk_level}
        </span>
      </div>

      <div className="flex flex-wrap items-center gap-1.5 mb-3">
        <Badge variant="outline" className="text-[10px]">
          {ticket.category}
        </Badge>
        <Badge variant="outline" className="text-[10px]">
          {ticket.status}
        </Badge>
        {ticket.escalation_needed && (
          <Badge variant="outline" className="text-[10px] text-red-400">
            {T("مُصعّد", "escalated")}
          </Badge>
        )}
      </div>

      {ticket.suggested_reply && (
        <div className="rounded-lg bg-muted/40 p-2 mb-3">
          <p className="text-[10px] text-muted-foreground mb-0.5">
            {T("الرد المقترح (مسودة)", "Suggested reply (draft)")}
          </p>
          <p className="text-xs">{ticket.suggested_reply}</p>
        </div>
      )}

      <div className="flex flex-wrap gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() =>
            void run(
              () => api.draftSupportResponse(ticket.ticket_id),
              T("تم إعداد المسودة", "Draft prepared"),
            )
          }
        >
          {T("صياغة رد", "Draft reply")}
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() =>
            void run(
              () => api.escalateSupportTicket(ticket.ticket_id, "manual"),
              T("تم التصعيد", "Escalated"),
            )
          }
        >
          {T("تصعيد", "Escalate")}
        </Button>
        <Button
          variant="outline"
          size="sm"
          onClick={() =>
            void run(
              () => api.resolveSupportTicket(ticket.ticket_id),
              T("تم الحل", "Resolved"),
            )
          }
        >
          {T("حل", "Resolve")}
        </Button>
        <Button
          variant="emerald"
          size="sm"
          onClick={() =>
            void run(
              () => api.sendSupportReply(ticket.ticket_id),
              T("أُرسل للموافقة", "Sent for approval"),
            )
          }
        >
          {T("إرسال الرد (يحتاج موافقة)", "Send reply (needs approval)")}
        </Button>
      </div>
    </div>
  );
}

export function SupportConsole() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const T = (ar: string, en: string) => (isAr ? ar : en);

  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.getSupportTickets();
      setTickets((res.data as { tickets?: Ticket[] }).tickets || []);
    } catch {
      toast.error(T("تعذّر تحميل التذاكر", "Could not load tickets"));
    } finally {
      setLoading(false);
    }
  }, [isAr]);

  useEffect(() => {
    void load();
  }, [load]);

  return (
    <Tabs defaultValue="tickets">
      <TabsList className="mb-6">
        <TabsTrigger value="tickets">{T("التذاكر", "Tickets")}</TabsTrigger>
        <TabsTrigger value="knowledge">{T("قاعدة المعرفة", "Knowledge base")}</TabsTrigger>
      </TabsList>

      <TabsContent value="tickets">
        <div className="flex items-center justify-between mb-4">
          <p className="text-sm text-muted-foreground">
            {T(
              "الردود تُرسَل دائماً بعد موافقتك — الدعم لا يرسل تلقائياً.",
              "Replies are always sent after your approval — support never auto-sends.",
            )}
          </p>
          <Button variant="outline" size="sm" onClick={() => void load()} disabled={loading}>
            <RefreshCw className={cn("w-4 h-4 me-1", loading && "animate-spin")} />
            {T("تحديث", "Refresh")}
          </Button>
        </div>
        {loading ? (
          <p className="text-sm text-muted-foreground">{T("جاري التحميل…", "Loading…")}</p>
        ) : tickets.length === 0 ? (
          <p className="text-sm text-muted-foreground">{T("لا تذاكر", "No tickets")}</p>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {tickets.map((t) => (
              <TicketCard key={t.ticket_id} ticket={t} onAction={() => void load()} />
            ))}
          </div>
        )}
      </TabsContent>

      <TabsContent value="knowledge">
        <KnowledgeManager />
      </TabsContent>
    </Tabs>
  );
}
