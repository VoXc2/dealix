"use client";

import Link from "next/link";
import { useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { RevenueWarRoomTable } from "@/components/gtm/RevenueWarRoomTable";
import api from "@/lib/api";

const ADMIN_KEY =
  typeof window !== "undefined"
    ? process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY || ""
    : "";

type Summary = {
  today?: { top_targets_count?: number; follow_ups_due?: number };
  revenue?: Record<string, number>;
  anti_waste_guard?: { blocked_sample?: boolean };
};

type SocialPayload = {
  post?: { week?: number; day?: number; title_ar?: string };
  linkedin_draft?: string;
  policy_ar?: string;
};

type MeetingBrief = {
  company?: string;
  discovery_questions_ar?: string[];
  outreach_draft_ar?: string;
  objection_hints?: { id?: string; response_draft_ar?: string }[];
  demo_path?: string;
};

type P0Row = { company?: string; next_action?: string; priority?: string };

export function FounderCommandCenter() {
  const locale = useLocale();
  const t = useTranslations("founderCommand");
  const isAr = locale === "ar";
  const [err, setErr] = useState("");
  const [summary, setSummary] = useState<Summary | null>(null);
  const [pendingApprovals, setPendingApprovals] = useState(0);
  const [social, setSocial] = useState<SocialPayload | null>(null);
  const [p0, setP0] = useState<P0Row[]>([]);
  const [poolTotal, setPoolTotal] = useState(0);
  const [selectedLeadId, setSelectedLeadId] = useState<string | null>(null);
  const [brief, setBrief] = useState<MeetingBrief | null>(null);
  const [importing, setImporting] = useState(false);
  const [bizRed, setBizRed] = useState(0);

  const loadMeta = useCallback(async () => {
    if (!ADMIN_KEY) {
      setErr(t("missingAdminKey"));
      return;
    }
    setErr("");
    try {
      const [sumRes, apprRes, socRes, p0Res, poolRes, bizRes] = await Promise.all([
        api.getWarRoomSummary(ADMIN_KEY),
        api.getApprovalsPending(),
        api.getMarketingSocialToday(ADMIN_KEY),
        api.getTargetingP0Today(ADMIN_KEY, 10),
        api.getTargetingPool(ADMIN_KEY),
        api.getBusinessNowSnapshot(),
      ]);
      setSummary(sumRes.data as Summary);
      const pending = (apprRes.data as { items?: unknown[] })?.items ?? apprRes.data;
      setPendingApprovals(Array.isArray(pending) ? pending.length : 0);
      setSocial(socRes.data as SocialPayload);
      const p0data = p0Res.data as { items?: P0Row[] };
      setP0(p0data.items ?? []);
      setPoolTotal((poolRes.data as { total?: number }).total ?? 0);
      const snap = bizRes.data as {
        pillars?: Record<string, { status?: string }>;
        overall_verdict?: string;
      };
      const pillarMap = snap.pillars ?? {};
      const warnCount = Object.values(pillarMap).filter(
        (p) => p?.status === "red" || p?.status === "amber",
      ).length;
      setBizRed(warnCount || (snap.overall_verdict === "NO_GO" ? 1 : 0));
    } catch {
      setErr(t("loadFailed"));
    }
  }, [t]);

  useEffect(() => {
    loadMeta();
  }, [loadMeta]);

  useEffect(() => {
    if (!selectedLeadId || !ADMIN_KEY) {
      setBrief(null);
      return;
    }
    api
      .getLeadMeetingBrief(ADMIN_KEY, selectedLeadId, locale)
      .then((r) => setBrief(r.data as MeetingBrief))
      .catch(() => setBrief(null));
  }, [selectedLeadId, locale]);

  const importCsv = async () => {
    if (!ADMIN_KEY) return;
    setImporting(true);
    try {
      await api.importWarRoomTargets(ADMIN_KEY, { use_default_csv: true });
      await loadMeta();
    } catch {
      setErr(t("importFailed"));
    } finally {
      setImporting(false);
    }
  };

  const copySocial = async () => {
    const text = social?.linkedin_draft || "";
    if (text) await navigator.clipboard.writeText(text);
  };

  return (
    <div className="space-y-8" dir={isAr ? "rtl" : "ltr"}>
      <p className="text-sm text-muted-foreground">{t("subtitle")}</p>
      {err && <p className="text-destructive text-sm">{err}</p>}

      <Card className="p-4 border-primary/20 bg-muted/20">
        <h2 className="font-semibold text-sm mb-2">{t("morningCommand")}</h2>
        <pre className="text-xs bg-background p-2 rounded border overflow-x-auto" dir="ltr">
          bash scripts/run_founder_commercial_day.sh
        </pre>
      </Card>

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
        <Card className="p-3">
          <p className="text-xs text-muted-foreground">{t("approvals")}</p>
          <p className="text-2xl font-semibold">{pendingApprovals}</p>
          <Link href={`/${locale}/approvals`} className="text-xs text-primary">
            {t("openApprovals")}
          </Link>
        </Card>
        <Card className="p-3">
          <p className="text-xs text-muted-foreground">{t("targetsToday")}</p>
          <p className="text-2xl font-semibold">
            {summary?.today?.top_targets_count ?? 0}/10
          </p>
        </Card>
        <Card className="p-3">
          <p className="text-xs text-muted-foreground">{t("targetPool")}</p>
          <p className="text-2xl font-semibold">{poolTotal}</p>
        </Card>
        <Card className="p-3">
          <p className="text-xs text-muted-foreground">{t("paid")}</p>
          <p className="text-2xl font-semibold">{summary?.revenue?.paid ?? 0}</p>
        </Card>
        <Card className="p-3">
          <p className="text-xs text-muted-foreground">Business NOW</p>
          <p className="text-2xl font-semibold">{bizRed}</p>
          <Link href={`/${locale}/business-now`} className="text-xs text-primary">
            {t("openBizNow")}
          </Link>
        </Card>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card className="p-4 space-y-3">
          <h2 className="font-semibold">{t("socialToday")}</h2>
          {social?.post?.title_ar && (
            <p className="text-sm font-medium">{social.post.title_ar}</p>
          )}
          <p className="text-xs text-muted-foreground whitespace-pre-wrap max-h-32 overflow-y-auto">
            {social?.linkedin_draft || t("noSocial")}
          </p>
          <div className="flex gap-2">
            <Button size="sm" variant="outline" onClick={copySocial}>
              {t("copyDraft")}
            </Button>
            <Link href={`/${locale}/ops/marketing`}>
              <Button size="sm" variant="secondary">
                {t("openMarketing")}
              </Button>
            </Link>
          </div>
        </Card>

        <Card className="p-4 space-y-3">
          <h2 className="font-semibold">{t("p0Today")}</h2>
          <ul className="text-sm space-y-1 max-h-40 overflow-y-auto">
            {p0.map((row, i) => (
              <li key={`${row.company}-${i}`}>
                <span className="font-medium">{row.company}</span>
                <span className="text-muted-foreground text-xs block">
                  {row.next_action}
                </span>
              </li>
            ))}
          </ul>
          <Button size="sm" variant="outline" onClick={importCsv} disabled={importing}>
            {t("importAgencies")}
          </Button>
        </Card>
      </div>

      {selectedLeadId && brief && (
        <Card className="p-4 border-primary/30">
          <h2 className="font-semibold mb-2">
            {t("meetingBrief")}: {brief.company}
          </h2>
          <ul className="text-sm list-disc ms-5 space-y-1">
            {(brief.discovery_questions_ar ?? []).map((q) => (
              <li key={q}>{q}</li>
            ))}
          </ul>
          {brief.objection_hints && brief.objection_hints.length > 0 && (
            <div className="mt-3">
              <p className="text-xs font-medium text-muted-foreground">{t("objections")}</p>
              {brief.objection_hints.map((o) => (
                <p key={o.id} className="text-sm mt-1 whitespace-pre-wrap">
                  {o.response_draft_ar}
                </p>
              ))}
            </div>
          )}
          {brief.demo_path && (
            <Link href={brief.demo_path} className="text-sm text-primary mt-2 inline-block">
              {t("openDemo")}
            </Link>
          )}
        </Card>
      )}

      <Card className="p-4">
        <h2 className="font-semibold mb-4">{t("warRoomTitle")}</h2>
        <RevenueWarRoomTable
          onSelectLead={setSelectedLeadId}
          selectedLeadId={selectedLeadId}
        />
      </Card>
    </div>
  );
}
