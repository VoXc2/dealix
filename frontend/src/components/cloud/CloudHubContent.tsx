"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { useLocale, useTranslations } from "next-intl";
import { motion } from "framer-motion";
import {
  LayoutDashboard,
  Database,
  Shield,
  Bot,
  GitBranch,
  Users,
  BarChart3,
  Building2,
  CheckSquare,
  Loader2,
  Link2,
  Activity,
  Target,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface CloudModule {
  id: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
  healthPath?: string;
}

const modules: CloudModule[] = [
  { id: "warRoom", href: "/ops/war-room", icon: Target },
  { id: "workspace", href: "/clients", icon: Users },
  { id: "dashboard", href: "/dashboard", icon: LayoutDashboard },
  { id: "scorecards", href: "/analytics", icon: BarChart3 },
  { id: "pipeline", href: "/pipeline", icon: GitBranch, healthPath: "/api/v1/revenue-os/catalog" },
  { id: "governance", href: "/approvals", icon: CheckSquare },
  { id: "agents", href: "/agents", icon: Bot },
  { id: "proof", href: "/trust-check", icon: Shield },
  { id: "portal", href: "/customer-portal", icon: Building2 },
];

type ModuleHealth = "live" | "offline" | "checking";

export function CloudHubContent() {
  const t = useTranslations("cloud");
  const locale = useLocale();
  const [catalogLoading, setCatalogLoading] = useState(true);
  const [catalogError, setCatalogError] = useState<string | null>(null);
  const [sourceCount, setSourceCount] = useState<number | null>(null);
  const [evidenceLevels, setEvidenceLevels] = useState<string[]>([]);
  const [goldenChain, setGoldenChain] = useState<unknown>(null);
  const [kpiSnapshot, setKpiSnapshot] = useState<Record<string, unknown> | null>(null);
  const [moduleHealth, setModuleHealth] = useState<Record<string, ModuleHealth>>({});
  const [anti, setAnti] = useState<Record<string, unknown> | null>(null);
  const [antiLoading, setAntiLoading] = useState(false);

  const checkModuleHealth = useCallback(async () => {
    const next: Record<string, ModuleHealth> = {};
    for (const mod of modules) {
      next[mod.id] = "checking";
    }
    setModuleHealth({ ...next });

    const apiUp = await fetch(`${API_BASE}/health`)
      .then((r) => r.ok)
      .catch(() => false);

    const resolved: Record<string, ModuleHealth> = {};
    for (const mod of modules) {
      if (!apiUp) {
        resolved[mod.id] = "offline";
        continue;
      }
      if (mod.healthPath) {
        const ok = await fetch(`${API_BASE}${mod.healthPath}`)
          .then((r) => r.ok)
          .catch(() => false);
        resolved[mod.id] = ok ? "live" : "offline";
      } else {
        resolved[mod.id] = "live";
      }
    }
    setModuleHealth(resolved);
  }, []);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      setCatalogLoading(true);
      setCatalogError(null);
      try {
        const [catRes, evRes, chainRes, kpiRes] = await Promise.all([
          api.getRevenueOsCatalog(),
          api.getEvidenceLevels(),
          api.getDecisionPassportGoldenChain(),
          fetch(`${API_BASE}/api/v1/transformation/kpi-snapshot`),
        ]);
        const catalog = catRes.data;
        const sources =
          catalog?.source_registry?.sources ??
          catalog?.sources ??
          (Array.isArray(catalog?.source_registry) ? catalog.source_registry : []);
        if (!cancelled) setSourceCount(Array.isArray(sources) ? sources.length : null);

        const ev = evRes.data;
        const levels = ev?.levels ?? ev?.evidence_levels ?? [];
        if (!cancelled && Array.isArray(levels)) {
          setEvidenceLevels(
            levels.map((l: { id?: string; level?: string }) => String(l.id ?? l.level ?? l)),
          );
        }
        if (!cancelled) setGoldenChain(chainRes.data);

        if (kpiRes.ok && !cancelled) {
          setKpiSnapshot((await kpiRes.json()) as Record<string, unknown>);
        }
      } catch (e) {
        if (!cancelled) {
          setCatalogError(e instanceof Error ? e.message : "fetch_failed");
        }
      } finally {
        if (!cancelled) setCatalogLoading(false);
      }
    }
    void load();
    void checkModuleHealth();
    return () => {
      cancelled = true;
    };
  }, [checkModuleHealth]);

  const runAnti = async () => {
    setAntiLoading(true);
    try {
      const res = await api.postRevenueOsAntiWasteCheck({
        has_decision_passport: false,
        action_external: true,
        upsell_attempt: false,
        proof_event_count: 0,
        evidence_level_for_public: 0,
        public_marketing_attempt: false,
      });
      setAnti(res.data as Record<string, unknown>);
    } finally {
      setAntiLoading(false);
    }
  };

  const healthBadge = (id: string) => {
    const h = moduleHealth[id] ?? "checking";
    if (h === "checking") return <Badge variant="outline">{t("moduleChecking")}</Badge>;
    if (h === "live") return <Badge className="bg-emerald-600/20 text-emerald-500">{t("moduleLive")}</Badge>;
    return <Badge variant="destructive">{t("moduleOffline")}</Badge>;
  };

  return (
    <div className="space-y-8">
      <div className="space-y-2">
        <h1 className="text-2xl font-display font-bold text-foreground">{t("title")}</h1>
        <p className="text-muted-foreground text-sm max-w-2xl">{t("subtitle")}</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {modules.map((mod) => {
          const Icon = mod.icon;
          const href = `/${locale}${mod.href}`;
          return (
            <Link key={mod.id} href={href}>
              <Card className="h-full hover:border-gold-500/40 transition-colors cursor-pointer">
                <CardHeader className="pb-2">
                  <div className="flex items-center justify-between gap-2">
                    <div className="flex items-center gap-2 min-w-0">
                      <Icon className="w-5 h-5 text-gold-500 shrink-0" />
                      <CardTitle className="text-base truncate">{t(`modules.${mod.id}`)}</CardTitle>
                    </div>
                    {healthBadge(mod.id)}
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-xs text-muted-foreground">{t(`modulesDesc.${mod.id}`)}</p>
                </CardContent>
              </Card>
            </Link>
          );
        })}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Link2 className="w-5 h-5 text-gold-500" />
              {t("goldenChainTitle")}
            </CardTitle>
          </CardHeader>
          <CardContent>
            {goldenChain ? (
              <pre className="text-xs bg-muted/40 rounded-xl p-4 overflow-auto max-h-[280px]">
                {JSON.stringify(goldenChain, null, 2)}
              </pre>
            ) : (
              <p className="text-sm text-muted-foreground">{t("loading")}</p>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Shield className="w-5 h-5 text-gold-500" />
              {t("antiWasteTitle")}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="text-xs text-muted-foreground">{t("antiWasteHint")}</p>
            <Button size="sm" onClick={() => void runAnti()} disabled={antiLoading}>
              {antiLoading ? t("loading") : t("runAntiWaste")}
            </Button>
            {anti && (
              <p className="text-sm font-medium">{anti.ok ? t("antiPass") : t("antiBlocked")}</p>
            )}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Activity className="w-5 h-5 text-gold-500" />
            {t("kpiSnapshotTitle")}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {kpiSnapshot ? (
            <div className="space-y-2 text-sm">
              <p>
                {t("commercialPending", {
                  count: (kpiSnapshot.commercial_registry as { pending_count?: number })
                    ?.pending_count ?? 0,
                })}
              </p>
              <pre className="text-xs bg-muted/40 rounded-xl p-4 overflow-auto max-h-[200px]">
                {JSON.stringify(kpiSnapshot.snapshots, null, 2)}
              </pre>
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">{t("kpiSnapshotOffline")}</p>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Database className="w-5 h-5 text-gold-500" />
            {t("revenueOsTitle")}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {catalogLoading && (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Loader2 className="w-4 h-4 animate-spin" />
              {t("loading")}
            </div>
          )}
          {catalogError && <p className="text-sm text-amber-600">{t("catalogOffline")}</p>}
          {!catalogLoading && !catalogError && (
            <div className="flex flex-wrap gap-2">
              {sourceCount !== null && (
                <Badge variant="outline">{t("sourceCount", { count: sourceCount })}</Badge>
              )}
              {evidenceLevels.length > 0 && (
                <Badge variant="outline">
                  {t("evidenceLevels", { levels: evidenceLevels.join(", ") })}
                </Badge>
              )}
            </div>
          )}
          <Button variant="outline" size="sm" asChild>
            <a
              href={`${API_BASE}/api/v1/revenue-os/catalog`}
              target="_blank"
              rel="noopener noreferrer"
            >
              {t("openCatalogApi")}
            </a>
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
