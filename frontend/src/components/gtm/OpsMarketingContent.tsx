"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { getAdminApiKey, isOpsConfigured, opsMissingKeyMessage } from "@/lib/opsAdmin";

type CalendarItem = {
  id: string;
  scheduled_date: string;
  channel: string;
  title_ar: string;
  status: string;
  utm_campaign?: string;
};

type Stats = {
  calendar_total?: number;
  calendar_approved_or_published?: number;
  utm_links_total?: number;
};

export function OpsMarketingContent() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const adminKey = getAdminApiKey();
  const [items, setItems] = useState<CalendarItem[]>([]);
  const [stats, setStats] = useState<Stats>({});
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);
  const [lastUtm, setLastUtm] = useState("");

  const load = useCallback(() => {
    if (!isOpsConfigured()) {
      setErr(opsMissingKeyMessage(isAr));
      return;
    }
    api
      .getMarketingCalendar(adminKey)
      .then((r) => {
        const data = r.data as { items?: CalendarItem[]; stats?: Stats };
        setItems(data.items ?? []);
        setStats(data.stats ?? {});
        setErr("");
      })
      .catch(() => setErr(isAr ? "تعذّر تحميل التقويم." : "Calendar load failed."));
  }, [adminKey, isAr]);

  useEffect(() => {
    load();
  }, [load]);

  const applyWeekly = () => {
    if (!adminKey) return;
    setBusy(true);
    api
      .applyMarketingWeeklyPack(adminKey, { queue_approvals: true })
      .then(() => load())
      .catch(() => setErr(isAr ? "فشل تطبيق الحزمة الأسبوعية." : "Weekly pack apply failed."))
      .finally(() => setBusy(false));
  };

  const copyPublishKit = (slotId: string) => {
    if (!adminKey) return;
    setBusy(true);
    api
      .getMarketingPublishKit(adminKey, slotId)
      .then(async (r) => {
        const d = r.data as {
          post_text_ar?: string;
          utm_url?: string;
          disclosure_ar?: string;
        };
        const text = [d.post_text_ar, d.disclosure_ar, d.utm_url].filter(Boolean).join("\n\n");
        await navigator.clipboard.writeText(text);
      })
      .catch(() => setErr(isAr ? "فشل نسخ حزمة النشر." : "Publish kit copy failed."))
      .finally(() => setBusy(false));
  };

  const markApproved = (slotId: string) => {
    if (!adminKey) return;
    setBusy(true);
    api
      .patchMarketingCalendar(adminKey, slotId, { status: "approved" })
      .then(() => load())
      .catch(() => setErr(isAr ? "فشل تحديث الحالة." : "Status update failed."))
      .finally(() => setBusy(false));
  };

  const buildSampleUtm = () => {
    if (!adminKey) return;
    setBusy(true);
    api
      .buildMarketingUtm(adminKey, {
        utm_campaign: "founder_ops_dashboard",
        utm_medium: "social",
        utm_source: "dealix",
      })
      .then((r) => {
        const url = (r.data as { full_url?: string }).full_url ?? "";
        setLastUtm(url);
        load();
      })
      .catch(() => setErr(isAr ? "فشل بناء UTM." : "UTM build failed."))
      .finally(() => setBusy(false));
  };

  return (
    <div className="space-y-4" dir={isAr ? "rtl" : "ltr"}>
      <p className="text-sm text-muted-foreground">
        {isAr
          ? "مصنع التسويق المحكوم — مسودات وتقويم وUTM فقط؛ لا نشر خارجي تلقائي."
          : "Governed marketing factory — drafts, calendar, UTM; no autonomous external publish."}
      </p>
      {err && <p className="text-destructive text-sm">{err}</p>}

      <div className="flex flex-wrap gap-2 items-center">
        <Button type="button" disabled={busy || !adminKey} onClick={applyWeekly}>
          {isAr ? "تطبيق الحزمة الأسبوعية + موافقات" : "Apply weekly pack + approvals"}
        </Button>
        <Button type="button" variant="outline" disabled={busy || !adminKey} onClick={buildSampleUtm}>
          {isAr ? "بناء رابط UTM نموذجي" : "Build sample UTM link"}
        </Button>
        <Link href={`/${locale}/approvals`} className="text-sm text-primary underline">
          {isAr ? "مركز الموافقات" : "Approvals"}
        </Link>
      </div>

      <Card className="p-3 text-xs text-muted-foreground">
        {isAr
          ? "إفصاح الأفلييت/الشراكة إلزامي قبل النشر: «إعلان · شراكة مع Dealix» — لا وعود إيراد أو أتمتة كاملة بلا حوكمة."
          : "Affiliate disclosure required before publish; no revenue guarantees or ungoverned full automation claims."}
      </Card>

      {lastUtm && (
        <Card className="p-3 text-xs break-all">
          <p className="text-muted-foreground mb-1">UTM</p>
          <a href={lastUtm} className="text-primary underline" target="_blank" rel="noreferrer">
            {lastUtm}
          </a>
        </Card>
      )}

      <div className="grid gap-3 sm:grid-cols-3">
        <Card className="p-3">
          <p className="text-xs text-muted-foreground">{isAr ? "خانات التقويم" : "Calendar slots"}</p>
          <p className="text-xl font-semibold">{stats.calendar_total ?? 0}</p>
        </Card>
        <Card className="p-3">
          <p className="text-xs text-muted-foreground">{isAr ? "جاهز/منشور" : "Ready/published"}</p>
          <p className="text-xl font-semibold">{stats.calendar_approved_or_published ?? 0}</p>
        </Card>
        <Card className="p-3">
          <p className="text-xs text-muted-foreground">{isAr ? "روابط UTM" : "UTM links"}</p>
          <p className="text-xl font-semibold">{stats.utm_links_total ?? 0}</p>
        </Card>
      </div>

      <div className="space-y-2">
        {items.map((slot) => (
          <Card key={slot.id} className="p-3">
            <div className="flex justify-between gap-2 text-sm">
              <span className="font-medium">{slot.title_ar}</span>
              <span className="text-muted-foreground">{slot.status}</span>
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              {slot.scheduled_date} · {slot.channel}
              {slot.utm_campaign ? ` · ${slot.utm_campaign}` : ""}
            </p>
            <div className="flex flex-wrap gap-2 mt-2">
              <Button
                type="button"
                size="sm"
                variant="secondary"
                disabled={busy || !adminKey}
                onClick={() => copyPublishKit(slot.id)}
              >
                {isAr ? "نسخ للنشر" : "Copy for publish"}
              </Button>
              <Button
                type="button"
                size="sm"
                variant="outline"
                disabled={busy || !adminKey}
                onClick={() => markApproved(slot.id)}
              >
                {isAr ? "معتمد" : "Mark approved"}
              </Button>
            </div>
          </Card>
        ))}
        {items.length === 0 && !err && (
          <p className="text-sm text-muted-foreground">
            {isAr ? "لا خانات بعد — طبّق الحزمة الأسبوعية." : "No slots yet — apply the weekly pack."}
          </p>
        )}
      </div>
    </div>
  );
}
