"use client";

import { useLocale } from "next-intl";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import { CelBadge } from "./CelBadge";
import { STATE_TO_CEL, type CommercialState } from "@/lib/commercial";

const STATE_LABEL_AR: Record<CommercialState, string> = {
  prepared_not_sent: "مُجهّز — لم يُرسل",
  sent: "أُرسل",
  replied_interested: "رد مهتم",
  meeting_booked: "اجتماع محجوز",
  used_in_meeting: "استُخدم في اجتماع",
  scope_requested: "طلب نطاق",
  pilot_intro_requested: "طلب تجربة / تعريف",
  invoice_sent: "فاتورة صادرة",
  invoice_paid: "فاتورة مدفوعة",
  silent: "صمت",
  not_interested: "غير مهتم",
};

const STATE_LABEL_EN: Record<CommercialState, string> = {
  prepared_not_sent: "Prepared — not sent",
  sent: "Sent",
  replied_interested: "Replied — interested",
  meeting_booked: "Meeting booked",
  used_in_meeting: "Used in meeting",
  scope_requested: "Scope requested",
  pilot_intro_requested: "Pilot / intro requested",
  invoice_sent: "Invoice sent",
  invoice_paid: "Invoice paid",
  silent: "Silent",
  not_interested: "Not interested",
};

export interface EvidenceEvent {
  state: CommercialState | string;
  label_ar?: string;
  label_en?: string;
  at?: string;
  note?: string;
}

interface EvidenceTimelineProps {
  events: EvidenceEvent[];
  emptyText?: string;
}

export function EvidenceTimeline({ events, emptyText }: EvidenceTimelineProps) {
  const locale = useLocale();
  const isAr = locale === "ar";

  if (!events.length) {
    return (
      <p className="text-sm text-muted-foreground py-6 text-center">
        {emptyText ?? (isAr ? "لا أحداث بعد" : "No events yet")}
      </p>
    );
  }

  return (
    <ol className="relative space-y-4 ps-5">
      <span className="absolute top-1 bottom-1 start-[5px] w-px bg-border" />
      {events.map((ev, i) => {
        const st = ev.state as CommercialState;
        const cel = STATE_TO_CEL[st] ?? null;
        const label =
          (isAr ? ev.label_ar : ev.label_en) ??
          (st in STATE_LABEL_EN
            ? isAr
              ? STATE_LABEL_AR[st]
              : STATE_LABEL_EN[st]
            : String(ev.state));
        return (
          <motion.li
            key={`${ev.state}-${i}`}
            initial={{ opacity: 0, x: isAr ? 8 : -8 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.05 }}
            className="relative"
          >
            <span
              className={cn(
                "absolute -start-5 top-1 w-3 h-3 rounded-full border-2 border-background",
                cel === "CEL7_confirmed"
                  ? "bg-emerald-400"
                  : cel
                    ? "bg-gold-400"
                    : "bg-muted-foreground",
              )}
            />
            <div className="flex flex-wrap items-center gap-2">
              <p className="text-sm font-medium text-foreground">{label}</p>
              {cel && <CelBadge level={cel} showLabel={false} />}
            </div>
            {ev.at && (
              <p className="text-[11px] text-muted-foreground mt-0.5">{ev.at}</p>
            )}
            {ev.note && (
              <p className="text-xs text-muted-foreground mt-0.5">{ev.note}</p>
            )}
          </motion.li>
        );
      })}
    </ol>
  );
}
