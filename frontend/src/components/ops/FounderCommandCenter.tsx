"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { useTranslations, useLocale } from "next-intl";
import { motion } from "framer-motion";
import {
  Inbox,
  AlertTriangle,
  CreditCard,
  CheckSquare,
  FileCheck,
  Boxes,
  RefreshCw,
  Shield,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn, formatRelativeTime } from "@/lib/utils";
import { toast } from "sonner";
import { api } from "@/lib/api";

type Row = Record<string, unknown>;

interface Section {
  count?: number;
  total?: number;
  items?: Row[];
  note?: string;
}

interface FounderData {
  generated_at?: string;
  leads_waiting_24h_plus?: Section;
  friction_last_7d?: Section;
  renewals_due_next_7d?: Section;
  pending_approvals?: Section;
  recent_proof_events?: Section;
  capital_assets_this_week?: Section;
  governance_decision?: string;
  is_estimate?: boolean;
}

const s = (v: unknown): string => (v === undefined || v === null ? "" : String(v));

function SectionCard({
  icon,
  label,
  count,
  accent,
  note,
  delay,
  children,
}: {
  icon: React.ReactNode;
  label: string;
  count: number;
  accent: string;
  note?: string;
  delay: number;
  children?: React.ReactNode;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay }}
      className="rounded-2xl border border-border bg-card overflow-hidden flex flex-col"
    >
      <div className={cn("h-1", accent)} />
      <div className="p-5 flex flex-col flex-1">
        <div className="flex items-center justify-between gap-3 mb-3">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-muted flex items-center justify-center text-muted-foreground">
              {icon}
            </div>
            <h4 className="text-sm font-semibold text-foreground leading-tight">{label}</h4>
          </div>
          <span className="text-3xl font-bold text-foreground">{count}</span>
        </div>
        <div className="flex-1">{children}</div>
        {note && <p className="text-[10px] text-muted-foreground mt-3">{note}</p>}
      </div>
    </motion.div>
  );
}

function ItemList({
  rows,
  empty,
  render,
}: {
  rows: Row[];
  empty: string;
  render: (row: Row) => { primary: string; secondary?: string; time?: string };
}) {
  const locale = useLocale();
  if (rows.length === 0) {
    return <p className="text-xs text-muted-foreground">{empty}</p>;
  }
  return (
    <ul className="space-y-2">
      {rows.slice(0, 6).map((row, i) => {
        const r = render(row);
        return (
          <li key={i} className="rounded-lg border border-border bg-muted/30 p-2.5">
            <div className="flex items-center justify-between gap-2">
              <span className="text-xs font-medium text-foreground truncate">{r.primary}</span>
              {r.time && (
                <span className="text-[10px] text-muted-foreground flex-shrink-0">
                  {formatRelativeTime(r.time, locale)}
                </span>
              )}
            </div>
            {r.secondary && (
              <p className="text-[11px] text-muted-foreground truncate mt-0.5">{r.secondary}</p>
            )}
          </li>
        );
      })}
    </ul>
  );
}

export function FounderCommandCenter() {
  const t = useTranslations("opsFounder");
  const locale = useLocale();
  const isAr = locale === "ar";
  const [data, setData] = useState<FounderData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.getFounderDashboard();
      setData(res.data as FounderData);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "load_failed";
      setError(msg);
      toast.error(isAr ? "تعذر تحميل لوحة المؤسس" : "Could not load founder dashboard");
    } finally {
      setLoading(false);
    }
  }, [isAr]);

  useEffect(() => {
    void load();
  }, [load]);

  if (loading && !data) {
    return <p className="text-muted-foreground text-sm">{t("loading")}</p>;
  }

  const leads = data?.leads_waiting_24h_plus ?? {};
  const friction = data?.friction_last_7d ?? {};
  const renewals = data?.renewals_due_next_7d ?? {};
  const approvals = data?.pending_approvals ?? {};
  const proof = data?.recent_proof_events ?? {};
  const capital = data?.capital_assets_this_week ?? {};

  const emptyLabel = t("noItems");

  return (
    <div>
      <div className="flex flex-wrap items-center justify-between gap-3 mb-6">
        <div className="flex flex-wrap items-center gap-2">
          <Button variant="outline" size="sm" onClick={() => void load()} disabled={loading}>
            <RefreshCw className={cn("w-4 h-4 me-1", loading && "animate-spin")} />
            {t("refresh")}
          </Button>
          {data?.governance_decision && (
            <Badge variant="outline" className="flex items-center gap-1 text-[10px]">
              <Shield className="w-3 h-3" />
              {t("governance")}: {data.governance_decision}
            </Badge>
          )}
          {data?.is_estimate && (
            <Badge
              variant="outline"
              className="text-[10px] text-gold-400 border-gold-400/30 bg-gold-400/10"
            >
              {t("estimate")}
            </Badge>
          )}
        </div>
        {data?.generated_at && (
          <p className="text-xs text-muted-foreground">
            {t("generatedAt")}: {formatRelativeTime(data.generated_at, locale)}
          </p>
        )}
      </div>

      {error && (
        <div className="rounded-xl border border-destructive/30 bg-destructive/10 p-3 mb-6">
          <p className="text-xs text-destructive">
            {isAr ? "تعذّر الوصول إلى الخادم — تأكد من تشغيل الواجهة الخلفية." : "Could not reach the API — make sure the backend is running."}
          </p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        <SectionCard
          icon={<Inbox className="w-5 h-5" />}
          label={t("leadsWaiting")}
          count={leads.count ?? 0}
          accent="bg-gradient-to-r from-gold-500 to-gold-400"
          note={leads.note}
          delay={0}
        >
          <ItemList
            rows={leads.items ?? []}
            empty={emptyLabel}
            render={(r) => ({
              primary: s(r.name) || s(r.company) || s(r.id) || "—",
              secondary: [s(r.company), s(r.sector)].filter(Boolean).join(" · "),
              time: s(r.created_at) || undefined,
            })}
          />
        </SectionCard>

        <SectionCard
          icon={<AlertTriangle className="w-5 h-5" />}
          label={t("friction")}
          count={friction.total ?? friction.count ?? 0}
          accent="bg-gradient-to-r from-red-500 to-red-400"
          note={friction.note}
          delay={0.05}
        >
          <ItemList
            rows={friction.items ?? []}
            empty={t("frictionEmpty")}
            render={(r) => ({
              primary: s(r.category) || s(r.type) || s(r.label) || "—",
              secondary: s(r.detail) || s(r.note) || undefined,
              time: s(r.created_at) || undefined,
            })}
          />
        </SectionCard>

        <SectionCard
          icon={<CreditCard className="w-5 h-5" />}
          label={t("renewals")}
          count={renewals.count ?? 0}
          accent="bg-gradient-to-r from-emerald-500 to-emerald-400"
          note={renewals.note}
          delay={0.1}
        >
          <ItemList
            rows={renewals.items ?? []}
            empty={emptyLabel}
            render={(r) => ({
              primary: s(r.customer_id) || "—",
              secondary: [s(r.plan), r.amount_sar ? `${s(r.amount_sar)} ${isAr ? "ر.س" : "SAR"}` : ""]
                .filter(Boolean)
                .join(" · "),
              time: s(r.next_attempt_at) || undefined,
            })}
          />
        </SectionCard>

        <SectionCard
          icon={<CheckSquare className="w-5 h-5" />}
          label={t("approvals")}
          count={approvals.count ?? 0}
          accent="bg-gradient-to-r from-blue-500 to-blue-400"
          note={approvals.note}
          delay={0.15}
        >
          <ItemList
            rows={approvals.items ?? []}
            empty={emptyLabel}
            render={(r) => ({
              primary:
                s(r.summary_ar) || s(r.summary_en) || s(r.action_type) || s(r.approval_id) || s(r.id) || "—",
              secondary: [s(r.object_type), s(r.risk_level)].filter(Boolean).join(" · "),
              time: s(r.created_at) || undefined,
            })}
          />
        </SectionCard>

        <SectionCard
          icon={<FileCheck className="w-5 h-5" />}
          label={t("proofEvents")}
          count={proof.count ?? 0}
          accent="bg-gradient-to-r from-purple-500 to-purple-400"
          note={proof.note}
          delay={0.2}
        >
          <ItemList
            rows={proof.items ?? []}
            empty={emptyLabel}
            render={(r) => ({
              primary: s(r.event_type) || s(r.id) || "—",
              secondary: s(r.customer_handle) || undefined,
              time: s(r.created_at) || undefined,
            })}
          />
        </SectionCard>

        <SectionCard
          icon={<Boxes className="w-5 h-5" />}
          label={t("capitalAssets")}
          count={capital.count ?? 0}
          accent="bg-gradient-to-r from-teal-500 to-teal-400"
          note={capital.note}
          delay={0.25}
        >
          <ItemList
            rows={capital.items ?? []}
            empty={emptyLabel}
            render={(r) => ({
              primary: s(r.asset_type) || s(r.asset_id) || "—",
              secondary: [s(r.owner), s(r.engagement_id)].filter(Boolean).join(" · "),
              time: s(r.created_at) || undefined,
            })}
          />
        </SectionCard>
      </div>

      <div className="mt-6 flex flex-wrap gap-2">
        <Button variant="ghost" size="sm" asChild>
          <Link href={`/${locale}/approvals`}>{isAr ? "مركز الموافقات" : "Approval center"}</Link>
        </Button>
        <Button variant="ghost" size="sm" asChild>
          <Link href={`/${locale}/pipeline`}>{isAr ? "خط الصفقات" : "Pipeline"}</Link>
        </Button>
        <Button variant="ghost" size="sm" asChild>
          <Link href={`/${locale}/trust-check`}>{isAr ? "فحص منع الهدر" : "Anti-waste check"}</Link>
        </Button>
      </div>
    </div>
  );
}
