"use client";

import { useCallback, useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn, formatRelativeTime } from "@/lib/utils";
import { toast } from "sonner";
import { api } from "@/lib/api";

interface EvidenceEvent {
  event_id: string;
  event_type: string;
  entity_type: string;
  entity_id: string;
  actor: string;
  action: string;
  summary_en?: string;
  summary_ar?: string;
  is_estimate: boolean;
  source?: string;
  created_at: string;
}

export function EvidenceLedger() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const T = (ar: string, en: string) => (isAr ? ar : en);

  const [events, setEvents] = useState<EvidenceEvent[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.getEvidence({ limit: 100 });
      const data = res.data as { events?: EvidenceEvent[] };
      setEvents(Array.isArray(data.events) ? data.events : []);
    } catch {
      toast.error(T("تعذّر تحميل السجل", "Could not load the ledger"));
    } finally {
      setLoading(false);
    }
  }, [isAr]);

  useEffect(() => {
    void load();
  }, [load]);

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-muted-foreground">
          {T("سجل أحداث الأدلة — للقراءة فقط، يُكتب فقط من داخل النظام.",
            "Evidence event ledger — read-only, append-only.")}
        </p>
        <Button variant="outline" size="sm" onClick={() => void load()} disabled={loading}>
          <RefreshCw className={cn("w-4 h-4 me-1", loading && "animate-spin")} />
          {T("تحديث", "Refresh")}
        </Button>
      </div>

      {loading ? (
        <p className="text-sm text-muted-foreground">{T("جاري التحميل…", "Loading…")}</p>
      ) : events.length === 0 ? (
        <p className="text-sm text-muted-foreground">{T("لا أحداث بعد", "No events yet")}</p>
      ) : (
        <div className="space-y-2">
          {events.map((e) => (
            <div
              key={e.event_id}
              className="rounded-xl border border-border bg-card p-3 flex items-start justify-between gap-3"
            >
              <div className="min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <Badge variant="outline" className="text-[10px]">
                    {e.event_type}
                  </Badge>
                  <span className="text-xs text-muted-foreground">
                    {e.entity_type} · {e.entity_id}
                  </span>
                  {e.is_estimate && (
                    <Badge variant="outline" className="text-[10px] text-amber-400">
                      estimate
                    </Badge>
                  )}
                </div>
                <p className="text-sm mt-1 truncate">
                  {(isAr ? e.summary_ar : e.summary_en) || e.action}
                </p>
                <p className="text-[11px] text-muted-foreground mt-0.5">
                  {e.actor}
                  {e.source ? ` · ${e.source}` : ""}
                </p>
              </div>
              <span className="text-[11px] text-muted-foreground whitespace-nowrap">
                {formatRelativeTime(e.created_at, locale)}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
