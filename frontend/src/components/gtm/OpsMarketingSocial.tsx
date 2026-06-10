"use client";

import { useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { getAdminApiKey, isOpsConfigured, opsMissingKeyMessage } from "@/lib/opsAdmin";

type SocialPayload = {
  post?: {
    week?: number;
    day?: number;
    title_ar?: string;
    body_ar?: string;
    cta_ar?: string;
    status?: string;
    soaen_checklist_ar?: string[];
  };
  linkedin_draft?: string;
  policy_ar?: string;
};

export function OpsMarketingSocial() {
  const locale = useLocale();
  const t = useTranslations("marketingOps");
  const isAr = locale === "ar";
  const [data, setData] = useState<SocialPayload | null>(null);
  const [err, setErr] = useState("");
  const [copied, setCopied] = useState(false);
  const [queued, setQueued] = useState(false);

  const adminKey = getAdminApiKey();

  const load = useCallback(async () => {
    if (!isOpsConfigured()) {
      setErr(opsMissingKeyMessage(isAr));
      return;
    }
    setErr("");
    try {
      const res = await api.getMarketingSocialToday(adminKey || "");
      setData(res.data as SocialPayload);
    } catch {
      setErr(t("loadFailed"));
    }
  }, [t, isAr, adminKey]);

  useEffect(() => {
    load();
  }, [load]);

  const copyDraft = async () => {
    const text = data?.linkedin_draft || "";
    if (!text) return;
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const queueApproval = async () => {
    if (!isOpsConfigured()) return;
    setErr("");
    try {
      await api.postMarketingQueueApproval(adminKey || "");
      setQueued(true);
      setTimeout(() => setQueued(false), 3000);
    } catch {
      setErr(isAr ? "تعذّر إرسال للموافقة." : "Failed to queue for approval.");
    }
  };

  const mark = async (status: "approved" | "published") => {
    const p = data?.post;
    if (!p || p.week == null || p.day == null || !isOpsConfigured()) return;
    try {
      await api.postMarketingSocialMark(adminKey || "", {
        week: p.week,
        day: p.day,
        status,
      });
      await load();
    } catch {
      setErr(t("markFailed"));
    }
  };

  const post = data?.post;

  return (
    <div className="space-y-6" dir={isAr ? "rtl" : "ltr"}>
      <p className="text-sm text-muted-foreground">{t("subtitle")}</p>
      {err && <p className="text-destructive text-sm">{err}</p>}

      {post && (
        <Card className="p-5 space-y-4">
          <div className="flex justify-between items-start gap-2">
            <h2 className="font-semibold text-lg">{post.title_ar}</h2>
            <span className="text-xs text-muted-foreground">{post.status}</span>
          </div>
          <p className="text-sm whitespace-pre-wrap">{post.body_ar}</p>
          <p className="text-sm font-medium text-primary">{post.cta_ar}</p>
          {post.soaen_checklist_ar && (
            <ul className="text-xs list-disc mr-5 space-y-1 text-muted-foreground">
              {post.soaen_checklist_ar.map((line) => (
                <li key={line}>{line}</li>
              ))}
            </ul>
          )}
        </Card>
      )}

      <div className="flex flex-wrap gap-2">
        <Button onClick={copyDraft} disabled={!data?.linkedin_draft}>
          {copied ? t("copied") : t("copyLinkedIn")}
        </Button>
        <Button variant="outline" onClick={queueApproval} disabled={!adminKey}>
          {queued
            ? isAr
              ? "في قائمة الموافقات"
              : "Queued"
            : isAr
              ? "إرسال للموافقة"
              : "Queue for approval"}
        </Button>
        <Button variant="outline" onClick={() => mark("approved")}>
          {t("markApproved")}
        </Button>
        <Button variant="secondary" onClick={() => mark("published")}>
          {t("markPublished")}
        </Button>
        <Button variant="ghost" onClick={load}>
          {t("refresh")}
        </Button>
      </div>

      {data?.policy_ar && (
        <p className="text-xs text-muted-foreground">{data.policy_ar}</p>
      )}
    </div>
  );
}
