"use client";

/**
 * Profile / preferences — locale, Hijri toggle, billing-portal link.
 * Preferences are persisted in localStorage (server-side persistence is
 * future work via a `/api/v1/users/me/preferences` endpoint).
 */

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { toast } from "sonner";

export default function ProfilePage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const t = (ar: string, en: string) => (isAr ? ar : en);
  const [hijriDefault, setHijriDefault] = useState(true);
  const [autoUpgrade, setAutoUpgrade] = useState(false);

  useEffect(() => {
    setHijriDefault(localStorage.getItem("dealix_hijri_default") !== "false");
    setAutoUpgrade(localStorage.getItem("dealix_auto_upgrade") === "true");
  }, []);

  function save() {
    localStorage.setItem("dealix_hijri_default", String(hijriDefault));
    localStorage.setItem("dealix_auto_upgrade", String(autoUpgrade));
    toast.success(t("تم الحفظ", "Saved"));
  }

  return (
    <div className="p-8 max-w-2xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">{t("التفضيلات", "Preferences")}</h1>
      <div className="bg-card border border-border rounded-xl p-6 space-y-4">
        <label className="flex items-center gap-3 text-sm">
          <input type="checkbox" checked={hijriDefault} onChange={(e) => setHijriDefault(e.target.checked)} />
          <span>
            {t("عرض التواريخ بالهجري + الميلادي بشكل افتراضي", "Show dates dual-calendar (Hijri + Gregorian) by default")}
          </span>
        </label>
        <label className="flex items-center gap-3 text-sm">
          <input type="checkbox" checked={autoUpgrade} onChange={(e) => setAutoUpgrade(e.target.checked)} />
          <span>{t("اقترح ترقية الباقة عند تجاوز الحد", "Suggest plan upgrades when limits are crossed")}</span>
        </label>
        <button onClick={save} className="bg-emerald-500 text-white rounded-lg px-4 py-2">
          {t("احفظ", "Save")}
        </button>
      </div>

      <div className="bg-card border border-border rounded-xl p-6">
        <h2 className="font-semibold">{t("بوابة الفواتير", "Billing portal")}</h2>
        <p className="text-sm text-muted-foreground my-2">
          {t(
            "لإدارة وسائل الدفع وفواتيركم السابقة، توجه لصفحة الفواتير.",
            "To manage payment methods and prior invoices, head to the billing page."
          )}
        </p>
        <a href={`/${locale}/billing`} className="text-emerald-500 underline text-sm">
          {t("اذهب للفواتير →", "Go to billing →")}
        </a>
      </div>
    </div>
  );
}
