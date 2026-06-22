import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(
  value: number,
  currency: "SAR" | "USD" = "SAR",
  locale: string = "ar-SA"
): string {
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
}

export function formatNumber(value: number, locale: string = "ar-SA"): string {
  return new Intl.NumberFormat(locale).format(value);
}

export function formatPercentage(value: number): string {
  return `${value > 0 ? "+" : ""}${value.toFixed(1)}%`;
}

export function formatRelativeTime(dateStr: string, locale: string = "ar"): string {
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMins / 60);
  const diffDays = Math.floor(diffHours / 24);

  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: "auto" });

  if (diffMins < 60) return rtf.format(-diffMins, "minute");
  if (diffHours < 24) return rtf.format(-diffHours, "hour");
  return rtf.format(-diffDays, "day");
}

export function getRiskColor(level: "high" | "medium" | "low"): string {
  const colors = {
    high: "text-red-400 bg-red-400/10 border-red-400/20",
    medium: "text-gold-400 bg-gold-400/10 border-gold-400/20",
    low: "text-emerald-400 bg-emerald-400/10 border-emerald-400/20",
  };
  return colors[level];
}

export function getAgentTypeIcon(type: string): string {
  const icons: Record<string, string> = {
    outreach: "📤",
    scoring: "📊",
    compliance: "🛡️",
    intelligence: "🔍",
    orchestrator: "⚙️",
  };
  return icons[type] ?? "🤖";
}

export function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    running: "text-blue-400 bg-blue-400/10",
    completed: "text-emerald-400 bg-emerald-400/10",
    pending: "text-gold-400 bg-gold-400/10",
    failed: "text-red-400 bg-red-400/10",
    active: "text-emerald-400 bg-emerald-400/10",
    inactive: "text-gray-400 bg-gray-400/10",
    prospect: "text-blue-400 bg-blue-400/10",
  };
  return colors[status] ?? "text-gray-400 bg-gray-400/10";
}
