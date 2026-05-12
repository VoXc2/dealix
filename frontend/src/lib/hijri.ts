/**
 * Hijri (Umm Al-Qura) date helpers for the dashboard.
 *
 * Browser locale `ar-SA-u-ca-islamic-umalqura` produces a correct
 * Umm Al-Qura-based Hijri date. We expose two helpers and one React
 * hook-friendly memoisable function so every date in the UI can show
 * dual-calendar without each component re-implementing the conversion.
 */

export interface HijriParts {
  day: number;
  month: number;
  year: number;
  monthNameAr: string;
}

const _AR_MONTHS = [
  "محرم",
  "صفر",
  "ربيع الأول",
  "ربيع الآخر",
  "جمادى الأولى",
  "جمادى الآخرة",
  "رجب",
  "شعبان",
  "رمضان",
  "شوال",
  "ذو القعدة",
  "ذو الحجة",
];

export function hijriFromGregorian(input: Date | string): HijriParts {
  const d = typeof input === "string" ? new Date(input) : input;
  const fmt = new Intl.DateTimeFormat("ar-SA-u-ca-islamic-umalqura", {
    day: "numeric",
    month: "numeric",
    year: "numeric",
    numberingSystem: "latn",
  }).formatToParts(d);
  const day = Number(fmt.find((p) => p.type === "day")?.value ?? 1);
  const month = Number(fmt.find((p) => p.type === "month")?.value ?? 1);
  const year = Number(fmt.find((p) => p.type === "year")?.value ?? 1446);
  return {
    day,
    month,
    year,
    monthNameAr: _AR_MONTHS[Math.max(0, Math.min(11, month - 1))],
  };
}

export function formatHijriShort(input: Date | string): string {
  const h = hijriFromGregorian(input);
  return `${h.day}/${h.month}/${h.year}هـ`;
}

export function formatHijriLong(input: Date | string): string {
  const h = hijriFromGregorian(input);
  return `${h.day} ${h.monthNameAr} ${h.year}هـ`;
}

export function dualCalendar(input: Date | string, locale: string = "ar"): string {
  const d = typeof input === "string" ? new Date(input) : input;
  const greg = new Intl.DateTimeFormat(locale === "ar" ? "ar-SA" : "en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  }).format(d);
  return `${greg} · ${formatHijriShort(d)}`;
}
