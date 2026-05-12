"use client";

/**
 * First-login product tour using driver.js.
 *
 * Walks new users through: dashboard → onboarding → billing → support.
 * Persists completion in localStorage so the tour fires once per user.
 *
 * To trigger manually for QA: localStorage.removeItem('dealix_tour_done').
 */

import { useEffect } from "react";
import { useLocale, useTranslations } from "next-intl";
// driver.js is the only new dep; it's lightweight (~9KB gzip).
// If not installed yet (CI shipping packages later), this dynamically
// imports and silently no-ops when the module isn't found.

const STORAGE_KEY = "dealix_tour_done";

export function Tour(): JSX.Element | null {
  const locale = useLocale();
  const isAr = locale === "ar";

  useEffect(() => {
    if (typeof window === "undefined") return;
    if (window.localStorage.getItem(STORAGE_KEY)) return;
    let cancelled = false;
    (async () => {
      let driverPkg: any = null;
      try {
        driverPkg = await import("driver.js");
        await import("driver.js/dist/driver.css" as any).catch(() => null);
      } catch {
        // driver.js isn't installed yet; silently skip.
        return;
      }
      if (cancelled || !driverPkg) return;
      const drv = driverPkg.driver({
        showProgress: true,
        animate: true,
        allowClose: true,
        nextBtnText: isAr ? "التالي" : "Next",
        prevBtnText: isAr ? "السابق" : "Back",
        doneBtnText: isAr ? "تم" : "Done",
        steps: [
          {
            element: '[data-tour="dashboard"]',
            popover: {
              title: isAr ? "اللوحة الرئيسية" : "Dashboard",
              description: isAr
                ? "هنا تتابع KPIs لـ Leads و Deals و الفرص اليومية."
                : "Track lead, deal, and opportunity KPIs.",
            },
          },
          {
            element: '[data-tour="billing"]',
            popover: {
              title: isAr ? "الفواتير" : "Billing",
              description: isAr
                ? "اطلع على باقتك، فواتيرك، وفرص الترقية."
                : "Plan, invoices, upgrade options.",
            },
          },
          {
            element: '[data-tour="audit"]',
            popover: {
              title: isAr ? "سجل التدقيق" : "Audit log",
              description: isAr
                ? "صدّر CSV لكل إجراء جرى على بياناتك."
                : "Export a CSV of every action against your data.",
            },
          },
          {
            element: '[data-tour="support"]',
            popover: {
              title: isAr ? "الدعم" : "Support",
              description: isAr
                ? "افتح تذكرة وسيتواصل الفريق خلال يوم عمل."
                : "Open a ticket — we reply within one business day.",
            },
          },
        ],
      });
      drv.drive();
      const onDestroy = () => {
        window.localStorage.setItem(STORAGE_KEY, new Date().toISOString());
        drv.destroy();
      };
      drv.on("destroyed", onDestroy);
    })();
    return () => {
      cancelled = true;
    };
  }, [isAr]);

  return null;
}
