import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatRelativeTime(timestamp: string, locale: string): string {
  const now = Date.now();
  const then = new Date(timestamp).getTime();
  const diffMs = now - then;
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHr = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHr / 24);

  const isAr = locale === "ar";

  if (diffSec < 60) {
    return isAr ? "الآن" : "just now";
  }
  if (diffMin < 60) {
    return isAr ? `منذ ${diffMin} د` : `${diffMin}m ago`;
  }
  if (diffHr < 24) {
    return isAr ? `منذ ${diffHr} س` : `${diffHr}h ago`;
  }
  if (diffDay < 7) {
    return isAr ? `منذ ${diffDay} ي` : `${diffDay}d ago`;
  }

  return new Date(timestamp).toLocaleDateString(locale === "ar" ? "ar-SA" : "en-US", {
    month: "short",
    day: "numeric",
  });
}

const statusColorMap: Record<string, string> = {
  completed: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
  running: "bg-blue-500/10 text-blue-400 border-blue-500/20",
  pending: "bg-amber-500/10 text-amber-400 border-amber-500/20",
  failed: "bg-red-500/10 text-red-400 border-red-500/20",
};

export function getStatusColor(status: string): string {
  return statusColorMap[status] ?? "bg-muted text-muted-foreground border-border";
}

export function formatCurrency(amount: number, locale: string = "ar"): string {
  return new Intl.NumberFormat(locale === "ar" ? "ar-SA" : "en-SA", {
    style: "currency",
    currency: "SAR",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

export function formatNumber(value: number, locale: string = "ar"): string {
  return new Intl.NumberFormat(locale === "ar" ? "ar-SA" : "en-US").format(value);
}

export function formatPercentage(value: number): string {
  return `${value.toFixed(1)}%`;
}

const riskColorMap: Record<string, string> = {
  high: "bg-red-500/10 text-red-400 border-red-500/20",
  medium: "bg-amber-500/10 text-amber-400 border-amber-500/20",
  low: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
};

export function getRiskColor(risk: string): string {
  return riskColorMap[risk] ?? "bg-muted text-muted-foreground border-border";
}
