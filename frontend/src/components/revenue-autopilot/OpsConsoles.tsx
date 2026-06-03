"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useTranslations } from "next-intl";

import api from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

function useOperatorKey(): string | null {
  return useMemo(() => {
    const fromEnv =
      typeof process !== "undefined"
        ? process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY?.trim()
        : "";
    return fromEnv && fromEnv.length > 0 ? fromEnv : null;
  }, []);
}

function MissingBanner({ locale }: { locale: string }) {
  const tn = useTranslations("opsPages");
  return (
    <Card className="border-yellow-700/70 bg-yellow-950/30">
      <CardHeader>
        <CardTitle>
          {locale === "ar" ? "بحاجة مفتاح تشغيل" : "Requires operator key"}
        </CardTitle>
      </CardHeader>
      <CardContent className="text-sm text-muted-foreground">{tn("missingAdminKey")}</CardContent>
    </Card>
  );
}

export function FounderDashboardPanel({ locale }: { locale: string }) {
  const k = useOperatorKey();
  const tn = useTranslations("opsPages");
  const [data, setData] = useState<Record<string, unknown> | null>(null);
  const [err, setErr] = useState<string>("");

  const load = useCallback(async () => {
    if (!k) return;
    setErr("");
    try {
      const res = await api.getOpsFounderDashboard(k);
      setData(res.data as Record<string, unknown>);
    } catch {
      setErr("dashboard_offline");
    }
  }, [k]);

  useEffect(() => {
    void load();
  }, [load]);

  if (!k) {
    return <MissingBanner locale={locale} />;
  }

  const tiles = (data?.tiles as Record<string, number> | undefined) ?? {};
  const warnings = (data?.no_build_warnings as string[] | undefined) ?? [];

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <CardTitle>{locale === "ar" ? "مركز المؤسّس" : "Founder Command Center"}</CardTitle>
          <p className="text-xs text-muted-foreground">{tn("founderSubtitle")}</p>
        </div>
        <Button variant="outline" size="sm" onClick={() => void load()}>
          {tn("refresh")}
        </Button>
      </CardHeader>
      <CardContent className="space-y-6">
        {err ? (
          <p className="text-sm text-yellow-600">{locale === "ar" ? "تعذر التحميل" : "Offline"}</p>
        ) : null}
        <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-4">
          {Object.entries(tiles).map(([name, count]) => (
            <Card key={name} className="border-border bg-card">
              <CardContent className="pt-6 text-sm font-medium">
                <p className="text-xs uppercase tracking-wide text-muted-foreground">{name}</p>
                <p className="text-2xl">{Number(count ?? 0)}</p>
              </CardContent>
            </Card>
          ))}
        </div>
        {warnings.length ? (
          <Card className="border-destructive/40 bg-destructive/5">
            <CardHeader className="py-4">
              <CardTitle className="text-base">{locale === "ar" ? "تحذيرات" : "No-build warnings"}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2 text-sm">
              {warnings.map((w, i) => (
                <p key={`${w}-${String(i)}`}>{w}</p>
              ))}
            </CardContent>
          </Card>
        ) : null}
        <div className="flex flex-wrap gap-3 text-xs">
          <Link href={`/${locale}/dealix-diagnostic`} className="text-gold-400 underline">
            {locale === "ar" ? "قمع التشخيص" : "Diagnostic funnel"}
          </Link>
          <Link href={`/${locale}/approvals`} className="text-gold-400 underline">
            Approval Center
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}

export function SalesPipelineOps({ locale }: { locale: string }) {
  const k = useOperatorKey();
  const tn = useTranslations("opsPages");
  const [snapshot, setSnapshot] = useState<Record<string, unknown> | null>(null);

  const reload = useCallback(async () => {
    if (!k) return;
    const res = await api.getSalesPipelineAutopilot(k);
    setSnapshot(res.data as Record<string, unknown>);
  }, [k]);

  useEffect(() => {
    void reload();
  }, [reload]);

  if (!k) {
    return <MissingBanner locale={locale} />;
  }

  const stages = (snapshot?.stages as Record<string, number> | undefined) ?? {};

  return (
    <Card>
      <CardHeader className="flex justify-between gap-4">
        <div>
          <CardTitle>{locale === "ar" ? "خط المبيعات" : "Sales pipeline"}</CardTitle>
          <p className="text-xs text-muted-foreground">{tn("salesSubtitle")}</p>
        </div>
        <Button variant="outline" size="sm" onClick={() => void reload()}>
          {tn("refresh")}
        </Button>
      </CardHeader>
      <CardContent className="space-y-3">
        {Object.entries(stages).map(([stage, count]) => (
          <div key={stage} className="space-y-1">
            <div className="flex justify-between text-xs font-medium">
              <span>{stage}</span>
              <span>{Number(count ?? 0)}</span>
            </div>
            <div className="h-2 rounded-full bg-muted">
              <div className="h-2 rounded-full bg-gold-500" style={{ width: `${Math.min(420, Number(count ?? 0) * 28)}px` }} />
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}

export function EvidenceLedgerPanel({ locale }: { locale: string }) {
  const k = useOperatorKey();
  const tn = useTranslations("opsPages");
  const [rows, setRows] = useState<Array<Record<string, unknown>>>([]);

  const reload = useCallback(async () => {
    if (!k) return;
    const res = await api.getEvidenceLedger(k, 50);
    const items = ((res.data as { items?: Array<Record<string, unknown>> })?.items) ?? [];
    setRows(items);
  }, [k]);

  useEffect(() => {
    void reload();
  }, [reload]);

  if (!k) {
    return <MissingBanner locale={locale} />;
  }

  return (
    <Card>
      <CardHeader className="flex justify-between gap-4">
        <div>
          <CardTitle>{locale === "ar" ? "سجل الأدلة" : "Evidence ledger"}</CardTitle>
          <p className="text-xs text-muted-foreground">{tn("evidenceSubtitle")}</p>
        </div>
        <Button variant="outline" size="sm" onClick={() => void reload()}>
          {tn("refresh")}
        </Button>
      </CardHeader>
      <CardContent className="space-y-2 text-xs">
        {rows.map((r) => (
          <Card key={String(r.id)} className="border-white/10 bg-card/70">
            <CardContent className="space-y-1 py-3">
              <div className="flex flex-wrap items-center gap-2">
                <Badge variant="outline">{String(r.event_type)}</Badge>
                <Badge variant="secondary">{String(r.entity_type)}</Badge>
              </div>
              <p className="text-[11px] text-muted-foreground">{String(r.summary)}</p>
            </CardContent>
          </Card>
        ))}
        {!rows.length ? (
          <p>{locale === "ar" ? "لا أحداث بعد" : "Ledger empty"}</p>
        ) : null}
      </CardContent>
    </Card>
  );
}

export function SupportQueuePanel({ locale }: { locale: string }) {
  const k = useOperatorKey();
  const tn = useTranslations("opsPages");
  const [rows, setRows] = useState<Array<Record<string, unknown>>>([]);

  const reload = useCallback(async () => {
    if (!k) return;
    const res = await api.getSupportTicketsAutopilot(k, 40);
    const items = ((res.data as { items?: Array<Record<string, unknown>> })?.items) ?? [];
    setRows(items);
  }, [k]);

  useEffect(() => {
    void reload();
  }, [reload]);

  if (!k) {
    return <MissingBanner locale={locale} />;
  }

  return (
    <Card>
      <CardHeader className="flex justify-between gap-4">
        <div>
          <CardTitle>{locale === "ar" ? "دعم العملاء" : "Customer support"}</CardTitle>
          <p className="text-xs text-muted-foreground">{tn("supportSubtitle")}</p>
        </div>
        <Button variant="outline" size="sm" onClick={() => void reload()}>
          {tn("refresh")}
        </Button>
      </CardHeader>
      <CardContent className="space-y-3 text-xs">
        {rows.map((r) => (
          <Card key={String(r.id)} className="border-white/15 bg-muted/10">
            <CardContent className="space-y-3 py-3">
              <div className="flex flex-wrap gap-2">
                <Badge variant="outline">{String(r.intent)}</Badge>
                <Badge variant={r.risk_level === "high" ? "destructive" : "secondary"}>
                  {String(r.risk_level)}
                </Badge>
              </div>
              <pre className="whitespace-pre-wrap text-[11px] text-muted-foreground">
                {String(r.message)}
              </pre>
              <p className="text-muted-foreground/80">
                {locale === "ar" ? "مسودة مقترحة" : "Suggested draft"}
              </p>
              <pre className="whitespace-pre-wrap rounded-md border bg-background px-3 py-2 text-[11px]">
                {String(r.suggested_response_ar ?? "")}
              </pre>
              <div className="flex gap-2">
                <Button
                  size="sm"
                  variant="outline"
                  onClick={async () => {
                    await api.classifySupportTicket(k, String(r.id));
                    await reload();
                  }}
                >
                  {locale === "ar" ? "تصنيف" : "Classify"}
                </Button>
                <Button
                  size="sm"
                  variant="secondary"
                  onClick={async () => {
                    await api.draftSupportResponse(k, String(r.id));
                    await reload();
                  }}
                >
                  {locale === "ar" ? "مسودة رد" : "Draft reply"}
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </CardContent>
    </Card>
  );
}
