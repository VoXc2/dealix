"use client";

import { useCallback, useState } from "react";
import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { useTranslations } from "next-intl";

interface VerticalResult {
  recommended_vertical?: string;
  playbook?: { pain_ar?: string; message_angle_ar?: string; buyer?: string };
}

interface CommercialStrategyToolsProps {
  verticalKeys?: string[];
  onVerticalResult?: (result: VerticalResult) => void;
}

export function CommercialStrategyTools({
  verticalKeys = [],
  onVerticalResult,
}: CommercialStrategyToolsProps) {
  const t = useTranslations("businessNow.commercialStrategy.tools");

  const [industry, setIndustry] = useState("clinics");
  const [city, setCity] = useState("Riyadh");
  const [budget, setBudget] = useState("2500");
  const [goal, setGoal] = useState("pipeline");
  const [verticalLoading, setVerticalLoading] = useState(false);
  const [verticalResult, setVerticalResult] = useState<VerticalResult | null>(null);
  const [planResult, setPlanResult] = useState<Record<string, unknown> | null>(null);
  const [simulateResult, setSimulateResult] = useState<Record<string, unknown> | null>(null);
  const [gtm10, setGtm10] = useState<Record<string, unknown> | null>(null);
  const [salesScript, setSalesScript] = useState<Record<string, unknown> | null>(null);
  const [proofDemo, setProofDemo] = useState<Record<string, unknown> | null>(null);
  const [anti, setAnti] = useState<Record<string, unknown> | null>(null);
  const [antiLoading, setAntiLoading] = useState(false);
  const [accordionLoading, setAccordionLoading] = useState<string | null>(null);

  const runVertical = useCallback(
    async (ind?: string) => {
      setVerticalLoading(true);
      try {
        const res = await api.postBusinessVerticalRecommend({
          industry: ind ?? industry,
          city,
          goal,
        });
        const data = res.data as VerticalResult;
        setVerticalResult(data);
        onVerticalResult?.(data);
      } finally {
        setVerticalLoading(false);
      }
    },
    [industry, city, goal, onVerticalResult],
  );

  const runPlan = async () => {
    const res = await api.postBusinessRecommendPlan({
      company_size: "sme",
      monthly_budget_sar: Number(budget) || 2500,
      goal,
    });
    setPlanResult(res.data as Record<string, unknown>);
  };

  const runSimulate = async () => {
    const res = await api.postCommercialStrategySimulate({
      industry,
      city,
      company_size: "sme",
      monthly_budget_sar: Number(budget) || 2500,
      goal,
    });
    setSimulateResult(res.data as Record<string, unknown>);
  };

  const loadGtm10 = async () => {
    if (gtm10) return;
    setAccordionLoading("gtm10");
    try {
      const res = await api.getBusinessGtmFirst10();
      setGtm10(res.data as Record<string, unknown>);
    } finally {
      setAccordionLoading(null);
    }
  };

  const loadSalesScript = async () => {
    if (salesScript) return;
    setAccordionLoading("script");
    try {
      const res = await api.getBusinessSalesScript();
      setSalesScript(res.data as Record<string, unknown>);
    } finally {
      setAccordionLoading(null);
    }
  };

  const loadProofDemo = async () => {
    if (proofDemo) return;
    setAccordionLoading("proof");
    try {
      const res = await api.getBusinessProofPackDemo();
      setProofDemo(res.data as Record<string, unknown>);
    } finally {
      setAccordionLoading(null);
    }
  };

  const runAntiWaste = async () => {
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

  const listSection = (title: string, items: unknown) => (
    <motion.div className="text-xs space-y-1">
      <p className="font-medium text-foreground">{title}</p>
      {Array.isArray(items) &&
        items.map((item) => (
          <p key={String(item)} className="text-muted-foreground">
            • {String(item)}
          </p>
        ))}
    </motion.div>
  );

  return (
    <div className="space-y-4 rounded-xl border border-border/60 p-4 bg-muted/20">
      <h3 className="text-sm font-semibold">{t("title")}</h3>

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <label className="text-xs space-y-1">
          {t("industryLabel")}
          <input
            className="w-full rounded-md border border-border bg-background px-2 py-1.5 text-sm"
            value={industry}
            onChange={(e) => setIndustry(e.target.value)}
          />
        </label>
        <label className="text-xs space-y-1">
          {t("cityLabel")}
          <input
            className="w-full rounded-md border border-border bg-background px-2 py-1.5 text-sm"
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />
        </label>
        <label className="text-xs space-y-1">
          {t("budgetLabel")}
          <input
            type="number"
            className="w-full rounded-md border border-border bg-background px-2 py-1.5 text-sm"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
          />
        </label>
        <label className="text-xs space-y-1">
          {t("goalLabel")}
          <input
            className="w-full rounded-md border border-border bg-background px-2 py-1.5 text-sm"
            value={goal}
            onChange={(e) => setGoal(e.target.value)}
          />
        </label>
      </div>

      {verticalKeys.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {verticalKeys.map((key) => (
            <Button
              key={key}
              type="button"
              variant="secondary"
              size="sm"
              disabled={verticalLoading}
              onClick={() => void runVertical(key)}
            >
              {key}
            </Button>
          ))}
        </div>
      )}

      <div className="flex flex-wrap gap-2">
        <Button type="button" size="sm" variant="outline" disabled={verticalLoading} onClick={() => void runVertical()}>
          {verticalLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : t("verticalBtn")}
        </Button>
        <Button type="button" size="sm" variant="outline" onClick={() => void runPlan()}>
          {t("planBtn")}
        </Button>
        <Button type="button" size="sm" variant="outline" onClick={() => void runSimulate()}>
          {t("simulateBtn")}
        </Button>
        <Button type="button" size="sm" variant="outline" disabled={antiLoading} onClick={() => void runAntiWaste()}>
          {antiLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : t("antiWasteBtn")}
        </Button>
      </div>

      {verticalResult?.playbook && (
        <Card>
          <CardContent className="pt-4 text-sm space-y-1">
            <Badge variant="outline">{verticalResult.recommended_vertical}</Badge>
            <p>{verticalResult.playbook.message_angle_ar}</p>
            <p className="text-muted-foreground text-xs">{verticalResult.playbook.pain_ar}</p>
          </CardContent>
        </Card>
      )}

      {planResult && (
        <Card>
          <CardContent className="pt-4 text-xs">
            <pre className="whitespace-pre-wrap overflow-x-auto max-h-40">
              {JSON.stringify(planResult, null, 2)}
            </pre>
          </CardContent>
        </Card>
      )}

      {simulateResult && (
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm">{t("simulateResult")}</CardTitle>
          </CardHeader>
          <CardContent className="text-xs">
            <pre className="whitespace-pre-wrap overflow-x-auto max-h-48">
              {JSON.stringify(simulateResult, null, 2)}
            </pre>
          </CardContent>
        </Card>
      )}

      {anti && (
        <p className="text-xs text-muted-foreground">
          {t("antiResult")}: {String((anti as { verdict?: string }).verdict ?? JSON.stringify(anti))}
        </p>
      )}

      <motion.div layout className="grid gap-3 md:grid-cols-3">
        <Card>
          <CardHeader className="pb-2 flex flex-row items-center justify-between">
            <CardTitle className="text-sm">{t("gtm10Title")}</CardTitle>
            <Button type="button" size="sm" variant="ghost" onClick={() => void loadGtm10()}>
              {accordionLoading === "gtm10" ? <Loader2 className="w-3 h-3 animate-spin" /> : t("load")}
            </Button>
          </CardHeader>
          {gtm10 && (
            <CardContent className="space-y-2 text-xs">
              {listSection(t("who"), gtm10.who)}
              {listSection(t("how"), gtm10.how_to_find)}
              {listSection(t("success"), gtm10.success_criteria)}
            </CardContent>
          )}
        </Card>
        <Card>
          <CardHeader className="pb-2 flex flex-row items-center justify-between">
            <CardTitle className="text-sm">{t("scriptTitle")}</CardTitle>
            <Button type="button" size="sm" variant="ghost" onClick={() => void loadSalesScript()}>
              {accordionLoading === "script" ? <Loader2 className="w-3 h-3 animate-spin" /> : t("load")}
            </Button>
          </CardHeader>
          {salesScript && (
            <CardContent className="space-y-2 text-xs">
              {listSection(t("discovery"), salesScript.discovery_questions)}
              <p className="text-muted-foreground">{String(salesScript.demo_story_ar ?? "")}</p>
            </CardContent>
          )}
        </Card>
        <Card>
          <CardHeader className="pb-2 flex flex-row items-center justify-between">
            <CardTitle className="text-sm">{t("proofTitle")}</CardTitle>
            <Button type="button" size="sm" variant="ghost" onClick={() => void loadProofDemo()}>
              {accordionLoading === "proof" ? <Loader2 className="w-3 h-3 animate-spin" /> : t("load")}
            </Button>
          </CardHeader>
          {proofDemo && (
            <CardContent className="text-xs max-h-40 overflow-auto">
              <pre className="whitespace-pre-wrap">{JSON.stringify(proofDemo, null, 2)}</pre>
            </CardContent>
          )}
        </Card>
      </motion.div>
    </div>
  );
}
