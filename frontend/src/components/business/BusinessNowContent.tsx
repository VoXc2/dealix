"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { useLocale, useTranslations, type TranslationValues } from "next-intl";
import { motion } from "framer-motion";
import {
  Briefcase,
  Truck,
  Box,
  Shield,
  Wallet,
  Users,
  Server,
  Megaphone,
  RefreshCw,
  Loader2,
  ChevronRight,
  ExternalLink,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { CommercialStrategyTools } from "@/components/business/CommercialStrategyTools";
import { CommercialValueMapStrip } from "@/components/gtm/CommercialValueMapStrip";
import { ValuePlanPanel, type ValuePlanPayload } from "@/components/gtm/ValuePlanPanel";
import { getAdminApiKey, isOpsConfigured } from "@/lib/opsAdmin";

type PillarKey =
  | "commercial"
  | "gtm"
  | "delivery"
  | "product"
  | "compliance"
  | "finance"
  | "team"
  | "platform";

const pillarIcons: Record<PillarKey, React.ComponentType<{ className?: string }>> = {
  commercial: Briefcase,
  gtm: Megaphone,
  delivery: Truck,
  product: Box,
  compliance: Shield,
  finance: Wallet,
  team: Users,
  platform: Server,
};

const pillarLinks: Record<PillarKey, string> = {
  commercial: "/pipeline",
  gtm: "/trust-check",
  delivery: "/clients",
  product: "/cloud",
  compliance: "/trust-check",
  finance: "/analytics",
  team: "/settings",
  platform: "/cloud",
};

interface Snapshot {
  generated_at?: string;
  pillars?: Record<string, Record<string, unknown>>;
  today_actions?: Array<{ priority: number; action_ar: string; href?: string }>;
}

interface KpiSnapshot {
  weekly_ops?: { last_checklist_run_iso?: string };
  snapshots?: Record<string, unknown>;
  commercial_registry?: { pending_count?: number; pending_keys?: string[] };
}

interface OperatorSignals {
  leads_waiting_24h_plus?: { count?: number };
  friction_last_7d?: { total?: number };
  pending_approvals?: { count?: number };
}

interface CommercialStrategy {
  focus?: {
    primary_offer_id?: string | null;
    secondary_offer_id?: string;
    stage?: string;
    rationale_ar?: string;
  };
  offers_playbook?: Array<Record<string, unknown>>;
  weekly_motions?: Array<{ day?: string; action_ar?: string; href?: string }>;
  guardrails_ar?: string[];
  positioning?: { differentiators?: string[] };
  expansion?: {
    upsell_matrix?: Array<{
      proof_signal?: string;
      recommended_offer?: string;
      label_ar?: string;
    }>;
  };
  verticals_priority?: Array<{ key?: string; pain_ar?: string; message_angle_ar?: string }>;
  quality_scores_demo?: {
    revenue_quality?: { score?: number; band?: string };
    client_quality?: { score?: number; band?: string };
    is_estimate?: boolean;
  };
  next_best_actions?: Array<{
    priority?: number;
    action_ar?: string;
    href?: string;
    api_hint?: string;
  }>;
  ops_client_pack?: {
    primary_offer_pitch_ar?: string;
    suggested_price_sar_range?: number[];
    conversation_opener_en?: string;
    discovery_question_en?: string;
    demo_steps?: string[];
    closing_line_ar?: string;
    runbook_doc?: string;
    sales_kit_deck?: string;
  };
  integration_truth_summary?: {
    overall_status?: string;
    counts?: { green?: number; yellow?: number; red?: number };
    founder_rule_ar?: string;
    doc_matrix?: string;
    verify_script?: string;
    ladder?: Array<{ id?: string; label_ar?: string; status?: string; founder_says_ar?: string }>;
    integrations?: Array<{ id?: string; label_ar?: string; status?: string; founder_says_ar?: string }>;
  };
}

function pillarStatus(key: PillarKey, snap: Snapshot): "ok" | "warn" | "risk" {
  const p = snap.pillars?.[key];
  if (!p) return "warn";
  if (key === "commercial" && (p.commercial_kpi_pending as number) > 0) return "warn";
  if (key === "platform") {
    if (p.transformation_verdict === "FAIL") return "risk";
    if (p.enterprise_control_plane_verdict === "FAIL") return "risk";
    if (p.transformation_verdict === "SKIP") return "warn";
  }
  if (key === "product" && (p.phase2_pending_count as number) > 10) return "warn";
  if (key === "compliance" && p.pdpl_module_present === false) return "warn";
  if (key === "delivery") {
    const sprints = (p.pilot_sprints as Array<{ status?: string }>) || [];
    if (sprints.length > 0 && sprints.every((s) => s.status === "template_ready")) return "warn";
  }
  return "ok";
}

function pillarFacts(key: PillarKey, p: Record<string, unknown> | undefined, t: (k: string, v?: TranslationValues) => string) {
  if (!p) return null;
  switch (key) {
    case "commercial":
      return (
        <>
          <p>{t("offersCount", { count: ((p.offers as unknown[]) || []).length })}</p>
          <p>{t("kpiPending", { count: (p.commercial_kpi_pending as number) ?? 0 })}</p>
        </>
      );
    case "gtm":
      return (
        <>
          <p className="truncate">{String(p.leads_endpoint || "—")}</p>
          <p>{t("gtmAntiWaste")}</p>
        </>
      );
    case "delivery":
      return <p>{t("pilotsCount", { count: ((p.pilot_sprints as unknown[]) || []).length })}</p>;
    case "product":
      return <p>{t("phase2Pending", { count: (p.phase2_pending_count as number) ?? 0 })}</p>;
    case "compliance":
      return (
        <>
          <p>{String(p.overall_posture || "—")}</p>
          <p className="truncate">{String(p.gtm_bundle_cmd || "")}</p>
        </>
      );
    case "finance": {
      const keys = Object.keys((p.platform_snapshots as Record<string, unknown>) || {});
      return (
        <>
          <p>{t("financeSnapshots", { count: keys.length })}</p>
          <p>{String(p.moyasar_mode || "—")}</p>
        </>
      );
    }
    case "team":
      return <p>{t("hiringOpen", { count: (p.hiring_open_count as number) ?? 0 })}</p>;
    case "platform":
      return (
        <>
          <p>{t("transformationVerdict", { v: String(p.transformation_verdict ?? "—") })}</p>
          <p>{t("enterpriseCpVerdict", { v: String(p.enterprise_control_plane_verdict ?? "—") })}</p>
        </>
      );
    default:
      return null;
  }
}

const QUICK_LINKS = [
  { href: "/cloud", labelKey: "linkCloud" as const },
  { href: "/approvals", labelKey: "linkApprovals" as const },
  { href: "/trust-check", labelKey: "linkTrust" as const },
  { href: "/pipeline", labelKey: "linkPipeline" as const },
];

export function BusinessNowContent() {
  const t = useTranslations("businessNow");
  const tc = useTranslations("businessNow.commercialStrategy");
  const locale = useLocale();
  const [snap, setSnap] = useState<Snapshot | null>(null);
  const [kpi, setKpi] = useState<KpiSnapshot | null>(null);
  const [strategy, setStrategy] = useState<CommercialStrategy | null>(null);
  const [operator, setOperator] = useState<OperatorSignals | null>(null);
  const [valuePlan, setValuePlan] = useState<ValuePlanPayload | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const pillars: PillarKey[] = [
    "commercial",
    "gtm",
    "delivery",
    "product",
    "compliance",
    "finance",
    "team",
    "platform",
  ];

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [snapRes, kpiRes, stratRes] = await Promise.all([
        api.getBusinessNowSnapshot(),
        api.getTransformationKpiSnapshot(),
        api.getCommercialStrategy(),
      ]);
      setSnap(snapRes.data as Snapshot);
      setKpi(kpiRes.data as KpiSnapshot);
      setStrategy(stratRes.data as CommercialStrategy);

      const adminKey = getAdminApiKey() || process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY;
      if (adminKey) {
        try {
          const opRes = await api.getBusinessNowOperatorSignals(adminKey);
          setOperator(opRes.data as OperatorSignals);
        } catch {
          setOperator(null);
        }
        if (isOpsConfigured()) {
          try {
            const vpRes = await api.getFounderCommercialValueMap(adminKey, 5);
            const body = vpRes.data as { value_plan?: ValuePlanPayload };
            setValuePlan(body.value_plan ?? null);
          } catch {
            setValuePlan(null);
          }
        }
      } else {
        setOperator(null);
        setValuePlan(null);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "fetch_failed");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  const statusBadge = (s: "ok" | "warn" | "risk") => {
    if (s === "ok") return <Badge className="bg-emerald-600/20 text-emerald-500">{t("statusOk")}</Badge>;
    if (s === "risk") return <Badge variant="destructive">{t("statusRisk")}</Badge>;
    return <Badge className="bg-amber-600/20 text-amber-600">{t("statusWarn")}</Badge>;
  };

  const docHref =
    "https://github.com/dealix-me/dealix/blob/main/docs/business/DEALIX_BUSINESS_NOW_AR.md";
  const strategyDocHref =
    "https://github.com/dealix-me/dealix/blob/main/docs/business/DEALIX_COMMERCIAL_STRATEGY_AR.md";

  const focusOffer = strategy?.offers_playbook?.find(
    (o) => o.service_id === strategy?.focus?.primary_offer_id,
  );

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-8">
      <motion.div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-xs text-muted-foreground">
            {snap?.generated_at
              ? t("generatedAt", { at: new Date(snap.generated_at).toLocaleString(locale) })
              : "—"}
          </p>
          {snap?.pillars?.platform?.cache_generated_at ? (
            <p className="text-xs text-muted-foreground mt-1">
              {t("cacheAt", {
                at: new Date(String(snap.pillars.platform.cache_generated_at)).toLocaleString(locale),
              })}
            </p>
          ) : null}
        </div>
        <Button variant="outline" size="sm" onClick={() => void load()} disabled={loading}>
          {loading ? (
            <Loader2 className="w-4 h-4 animate-spin me-2" />
          ) : (
            <RefreshCw className="w-4 h-4 me-2" />
          )}
          {t("refresh")}
        </Button>
      </motion.div>

      <div className="flex flex-wrap gap-2">
        {QUICK_LINKS.map((link) => (
          <Button key={link.href} asChild variant="outline" size="sm">
            <Link href={`/${locale}${link.href}`}>{t(link.labelKey)}</Link>
          </Button>
        ))}
        <Button asChild variant="ghost" size="sm">
          <a href={docHref} target="_blank" rel="noopener noreferrer">
            {t("linkDoc")}
            <ExternalLink className="w-3 h-3 ms-1 inline" />
          </a>
        </Button>
      </div>

      {error && <p className="text-sm text-amber-600">{t("loadError")}</p>}

      {snap && (
        <>
          <section>
            <h2 className="text-lg font-semibold mb-4">{t("todayTitle")}</h2>
            <div className="space-y-2">
              {(snap.today_actions || []).map((a) => (
                <Card key={a.priority} className="border-border/60">
                  <CardContent className="py-3 flex items-center justify-between gap-3">
                    <span className="text-sm">
                      <span className="text-gold-500 font-mono me-2">P{a.priority}</span>
                      {a.action_ar}
                    </span>
                    {a.href && a.href.startsWith("/") && (
                      <Link href={`/${locale}${a.href}`}>
                        <ChevronRight className="w-4 h-4 text-muted-foreground" />
                      </Link>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {valuePlan && (
            <section id="value-plan" className="scroll-mt-20">
              <h2 className="text-lg font-semibold mb-4">
                {locale === "ar" ? "خطة القيمة (تشغيل)" : "Value plan (ops)"}
              </h2>
              <ValuePlanPanel valuePlan={valuePlan} />
              <div className="flex flex-wrap gap-2 mt-3">
                <Button asChild size="sm" variant="outline">
                  <Link href={`/${locale}/ops/founder`}>
                    {locale === "ar" ? "مركز المؤسس" : "Founder ops"}
                  </Link>
                </Button>
                <Button asChild size="sm" variant="ghost">
                  <Link href={`/${locale}/ops/war-room`}>
                    {locale === "ar" ? "غرفة الإيراد" : "War Room"}
                  </Link>
                </Button>
              </div>
            </section>
          )}

          {strategy && (
            <section id="strategy" className="space-y-4 scroll-mt-20">
              <h2 className="text-lg font-semibold">{tc("title")}</h2>
              <Card className="border-amber-600/30 bg-amber-600/5">
                <CardContent className="py-3 text-xs space-y-1">
                  {(strategy.guardrails_ar || []).map((g) => (
                    <p key={g}>• {g}</p>
                  ))}
                </CardContent>
              </Card>
              <Card className="border-gold-500/40 bg-gradient-to-br from-gold-500/10 to-transparent">
                <CardHeader className="pb-2">
                  <CardTitle className="text-base">{tc("focusTitle")}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2 text-sm">
                  <Badge variant="outline">{String(strategy.focus?.stage ?? "—")}</Badge>
                  <p>{String(strategy.focus?.rationale_ar ?? "")}</p>
                  {focusOffer && (
                    <p className="font-medium">
                      {String(focusOffer.name_ar)} —{" "}
                      {focusOffer.price_sar != null ? `${focusOffer.price_sar} SAR` : ""}
                    </p>
                  )}
                  <Button asChild size="sm" variant="outline">
                    <Link href={`/${locale}/pipeline`}>{tc("focusCta")}</Link>
                  </Button>
                </CardContent>
              </Card>

              {strategy.quality_scores_demo?.is_estimate && (
                <div className="grid gap-3 sm:grid-cols-2">
                  <Card>
                    <CardContent className="pt-4 text-sm">
                      <p className="text-muted-foreground text-xs">{tc("qualityEstimate")}</p>
                      <p>
                        {tc("revenueQuality")}: {strategy.quality_scores_demo.revenue_quality?.score}{" "}
                        ({strategy.quality_scores_demo.revenue_quality?.band})
                      </p>
                      <p>
                        {tc("clientQuality")}: {strategy.quality_scores_demo.client_quality?.score}{" "}
                        ({strategy.quality_scores_demo.client_quality?.band})
                      </p>
                    </CardContent>
                  </Card>
                </div>
              )}

              {strategy.integration_truth_summary && (
                <Card className="border-border/80">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base flex items-center gap-2">
                      {tc("integrationTruthTitle")}
                      <Badge
                        variant={
                          strategy.integration_truth_summary.overall_status === "green"
                            ? "default"
                            : strategy.integration_truth_summary.overall_status === "red"
                              ? "destructive"
                              : "secondary"
                        }
                      >
                        {strategy.integration_truth_summary.overall_status}
                      </Badge>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="text-sm space-y-2">
                    <p className="text-xs text-muted-foreground">
                      {tc("integrationTruthCounts", {
                        green: strategy.integration_truth_summary.counts?.green ?? 0,
                        yellow: strategy.integration_truth_summary.counts?.yellow ?? 0,
                        red: strategy.integration_truth_summary.counts?.red ?? 0,
                      })}
                    </p>
                    <p className="text-xs">{strategy.integration_truth_summary.founder_rule_ar}</p>
                    <ul className="text-xs space-y-1 max-h-40 overflow-y-auto">
                      {[
                        ...(strategy.integration_truth_summary.ladder || []).slice(0, 4),
                        ...(strategy.integration_truth_summary.integrations || []),
                      ].map((row) => (
                        <li key={row.id} className="flex justify-between gap-2">
                          <span>{row.label_ar}</span>
                          <span
                            className={
                              row.status === "green"
                                ? "text-emerald-600"
                                : row.status === "red"
                                  ? "text-destructive"
                                  : "text-amber-600"
                            }
                          >
                            {row.status}
                          </span>
                        </li>
                      ))}
                    </ul>
                    <p className="text-xs text-muted-foreground">
                      {tc("integrationTruthVerify")}: {strategy.integration_truth_summary.verify_script}
                    </p>
                  </CardContent>
                </Card>
              )}

              {strategy.ops_client_pack && (
                <Card className="border-border/80">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-base">{tc("opsPackTitle")}</CardTitle>
                  </CardHeader>
                  <CardContent className="text-sm space-y-3">
                    <p className="font-medium">{strategy.ops_client_pack.primary_offer_pitch_ar}</p>
                    <p className="text-xs text-muted-foreground">
                      {tc("opsPackPrice", {
                        low: strategy.ops_client_pack.suggested_price_sar_range?.[0] ?? 0,
                        high: strategy.ops_client_pack.suggested_price_sar_range?.[1] ?? 0,
                      })}
                    </p>
                    <p className="text-xs italic text-muted-foreground">
                      {strategy.ops_client_pack.conversation_opener_en}
                    </p>
                    <p className="text-xs">
                      <span className="font-medium">{tc("opsDiscovery")}: </span>
                      {strategy.ops_client_pack.discovery_question_en}
                    </p>
                    <ul className="text-xs list-disc ps-4 space-y-1">
                      {(strategy.ops_client_pack.demo_steps || []).map((s) => (
                        <li key={s}>{s}</li>
                      ))}
                    </ul>
                    <p className="text-xs text-gold-600/90">{strategy.ops_client_pack.closing_line_ar}</p>
                    <p className="text-xs text-muted-foreground">
                      {tc("opsPackFiles")}: {strategy.ops_client_pack.runbook_doc} ·{" "}
                      {strategy.ops_client_pack.sales_kit_deck}
                    </p>
                  </CardContent>
                </Card>
              )}

              <CommercialStrategyTools
                verticalKeys={(strategy.verticals_priority || [])
                  .map((v) => String(v.key))
                  .filter(Boolean)}
              />

              {(strategy.next_best_actions || []).length > 0 && (
                <motion.div>
                  <h3 className="text-sm font-medium mb-2">{tc("nextActionsTitle")}</h3>
                  <ul className="text-sm space-y-1">
                    {(strategy.next_best_actions || []).map((a) => (
                      <li key={a.priority} className="flex justify-between gap-2">
                        <span>
                          P{a.priority}: {a.action_ar}
                        </span>
                        {a.href && (
                          <Link href={`/${locale}${a.href}`} className="text-gold-500 text-xs">
                            {tc("open")}
                          </Link>
                        )}
                      </li>
                    ))}
                  </ul>
                </motion.div>
              )}

              <div className="grid gap-3 lg:grid-cols-2">
                <div>
                  <h3 className="text-sm font-medium mb-2">{tc("differentiatorsTitle")}</h3>
                  <ul className="text-sm space-y-1 text-muted-foreground list-disc ps-5">
                    {(strategy.positioning?.differentiators || []).slice(0, 3).map((d) => (
                      <li key={d}>{d}</li>
                    ))}
                  </ul>
                </div>
                <motion.div>
                  <h3 className="text-sm font-medium mb-2">{tc("verticalsTitle")}</h3>
                  <div className="flex flex-wrap gap-2">
                    {(strategy.verticals_priority || []).map((v) => (
                      <Badge key={String(v.key)} variant="secondary">
                        {String(v.key)}
                      </Badge>
                    ))}
                  </div>
                </motion.div>
              </div>
              <motion.div>
                <h3 className="text-sm font-medium mb-2">{tc("motionsTitle")}</h3>
                <ul className="space-y-1 text-sm">
                  {(strategy.weekly_motions || []).map((m) => (
                    <li key={String(m.day)} className="flex justify-between gap-2">
                      <span>{m.action_ar}</span>
                      {m.href && (
                        <Link
                          href={`/${locale}${m.href}`}
                          className="text-gold-500 text-xs shrink-0"
                        >
                          {tc("open")}
                        </Link>
                      )}
                    </li>
                  ))}
                </ul>
              </motion.div>
              <div>
                <h3 className="text-sm font-medium mb-2">{tc("playbookTitle")}</h3>
                <div className="overflow-x-auto rounded-xl border border-border">
                  <table className="w-full text-sm">
                    <thead className="bg-muted/40">
                      <tr>
                        <th className="text-start p-3">{t("colOffer")}</th>
                        <th className="text-start p-3 hidden md:table-cell">{tc("colSuccess")}</th>
                        <th className="text-start p-3 hidden lg:table-cell">{tc("colNext")}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(strategy.offers_playbook || []).map((o) => (
                        <tr key={String(o.service_id)} className="border-t border-border/60">
                          <td className="p-3">
                            {String(o.name_ar)}
                            <span className="text-xs text-muted-foreground block">
                              {o.price_sar != null ? `${o.price_sar} SAR` : ""}
                            </span>
                          </td>
                          <td className="p-3 hidden md:table-cell text-xs text-muted-foreground">
                            {String(o.success_metric_ar || "—")}
                          </td>
                          <td className="p-3 hidden lg:table-cell text-xs font-mono">
                            {String(o.next_offer || "—")}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
              <div>
                <h3 className="text-sm font-medium mb-2">{tc("upsellTitle")}</h3>
                <motion.div className="overflow-x-auto rounded-xl border border-border">
                  <table className="w-full text-xs">
                    <thead className="bg-muted/40">
                      <tr>
                        <th className="text-start p-2">{tc("colSignal")}</th>
                        <th className="text-start p-2">{tc("colUpsell")}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(strategy.expansion?.upsell_matrix || []).map((row) => (
                        <tr key={String(row.proof_signal)} className="border-t border-border/60">
                          <td className="p-2" title={String(row.proof_signal)}>
                            {String(row.label_ar || row.proof_signal)}
                          </td>
                          <td className="p-2">{String(row.recommended_offer)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </motion.div>
              </div>
              <Button asChild variant="ghost" size="sm">
                <a href={strategyDocHref} target="_blank" rel="noopener noreferrer">
                  {tc("fullDoc")}
                  <ExternalLink className="w-3 h-3 ms-1 inline" />
                </a>
              </Button>
            </section>
          )}

          {operator && (
            <section>
              <h2 className="text-lg font-semibold mb-4">{t("operatorTitle")}</h2>
              <div className="grid gap-3 sm:grid-cols-3">
                <Card>
                  <CardContent className="pt-4">
                    <p className="text-2xl font-semibold">{operator.leads_waiting_24h_plus?.count ?? 0}</p>
                    <p className="text-xs text-muted-foreground">{t("operatorLeads")}</p>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="pt-4">
                    <p className="text-2xl font-semibold">{operator.pending_approvals?.count ?? 0}</p>
                    <p className="text-xs text-muted-foreground">{t("operatorApprovals")}</p>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="pt-4">
                    <p className="text-2xl font-semibold">{operator.friction_last_7d?.total ?? 0}</p>
                    <p className="text-xs text-muted-foreground">{t("operatorFriction")}</p>
                  </CardContent>
                </Card>
              </div>
            </section>
          )}

          <section className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {pillars.map((key) => {
              const Icon = pillarIcons[key];
              const st = pillarStatus(key, snap);
              const p = snap.pillars?.[key];
              return (
                <Link key={key} href={`/${locale}${pillarLinks[key]}`}>
                  <Card className="h-full hover:border-gold-500/40 transition-colors">
                    <CardHeader className="pb-2">
                      <motion.div className="flex items-center justify-between">
                        <Icon className="w-5 h-5 text-gold-500" />
                        {statusBadge(st)}
                      </motion.div>
                      <CardTitle className="text-base">{t(`pillars.${key}`)}</CardTitle>
                    </CardHeader>
                    <CardContent className="text-xs text-muted-foreground space-y-1">
                      {pillarFacts(key, p, t)}
                    </CardContent>
                  </Card>
                </Link>
              );
            })}
          </section>

          {kpi && (
            <section>
              <h2 className="text-lg font-semibold mb-4">{t("kpiTitle")}</h2>
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                <Card>
                  <CardContent className="pt-4">
                    <p className="text-sm font-medium">{t("kpiChecklist")}</p>
                    <p className="text-lg mt-1">
                      {kpi.weekly_ops?.last_checklist_run_iso ?? "—"}
                    </p>
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="pt-4">
                    <p className="text-sm font-medium">{t("kpiCommercialPending")}</p>
                    <p className="text-lg mt-1">{kpi.commercial_registry?.pending_count ?? 0}</p>
                    {(kpi.commercial_registry?.pending_keys || []).slice(0, 3).map((k) => (
                      <p key={k} className="text-xs text-muted-foreground font-mono">
                        {k}
                      </p>
                    ))}
                  </CardContent>
                </Card>
                <Card>
                  <CardContent className="pt-4">
                    <p className="text-sm font-medium">{t("kpiPlatformSignals")}</p>
                    <p className="text-lg mt-1">
                      {Object.keys(kpi.snapshots || {}).length} {t("kpiSignalsUnit")}
                    </p>
                  </CardContent>
                </Card>
              </div>
            </section>
          )}

          <CommercialValueMapStrip />

          <section>
            <h2 className="text-lg font-semibold mb-4">{t("offersTitle")}</h2>
            <motion.div className="overflow-x-auto rounded-xl border border-border">
              <table className="w-full text-sm">
                <thead className="bg-muted/40">
                  <tr>
                    <th className="text-start p-3">{t("colOffer")}</th>
                    <th className="text-start p-3">{t("colPrice")}</th>
                    <th className="text-start p-3 hidden md:table-cell">{t("colIntake")}</th>
                    <th className="text-start p-3 hidden lg:table-cell">{t("colSurface")}</th>
                  </tr>
                </thead>
                <tbody>
                  {((snap.pillars?.commercial?.offers as Array<Record<string, unknown>>) || []).map(
                    (o) => (
                      <tr key={String(o.service_id)} className="border-t border-border/60">
                        <td className="p-3">{String(o.name_ar || o.name_en)}</td>
                        <td className="p-3">
                          {o.price_sar != null ? `${o.price_sar} SAR` : "—"}
                        </td>
                        <td className="p-3 hidden md:table-cell text-xs text-muted-foreground">
                          {String(o.intake_endpoint || "—")}
                        </td>
                        <td className="p-3 hidden lg:table-cell text-xs text-muted-foreground">
                          {String(o.founder_surface || "—")}
                        </td>
                      </tr>
                    ),
                  )}
                </tbody>
              </table>
            </motion.div>
          </section>

          <section>
            <h2 className="text-lg font-semibold mb-4">{t("pilotsTitle")}</h2>
            <div className="grid gap-3 md:grid-cols-3">
              {((snap.pillars?.delivery?.pilot_sprints as Array<Record<string, unknown>>) || []).map(
                (s) => (
                  <Card key={String(s.id)}>
                    <CardContent className="pt-4">
                      <p className="font-medium">{String(s.id)}</p>
                      <Badge variant="outline" className="mt-2">
                        {String(s.status)}
                      </Badge>
                    </CardContent>
                  </Card>
                ),
              )}
            </div>
          </section>

          <section>
            <h2 className="text-lg font-semibold mb-4">{t("phase2Title")}</h2>
            <ul className="space-y-2 text-sm">
              {(
                (snap.pillars?.product?.phase2_items as Array<Record<string, unknown>>) || []
              ).map((item) => (
                <li key={String(item.id)} className="flex items-center gap-2">
                  <Badge variant={item.status === "done" ? "default" : "outline"}>
                    {String(item.status)}
                  </Badge>
                  <span>{String(item.label_ar)}</span>
                </li>
              ))}
            </ul>
          </section>
        </>
      )}
    </motion.div>
  );
}
