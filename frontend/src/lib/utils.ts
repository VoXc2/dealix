import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(amount: number, currency = "SAR"): string {
  return new Intl.NumberFormat("ar-SA", {
    style: "currency",
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

export function formatNumber(value: number): string {
  return new Intl.NumberFormat("ar-SA").format(value);
}

export function formatPercentage(value: number): string {
  return new Intl.NumberFormat("ar-SA", {
    style: "percent",
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  }).format(value / 100);
}

export function formatRelativeTime(dateStr: string): string {
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return "الآن";
  if (diffMins < 60) return `منذ ${diffMins} دقيقة`;
  if (diffHours < 24) return `منذ ${diffHours} ساعة`;
  return `منذ ${diffDays} يوم`;
}

export function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    active: "text-green-500",
    completed: "text-blue-500",
    pending: "text-yellow-500",
    failed: "text-red-500",
    discovery: "text-purple-500",
    qualified: "text-green-500",
    proposal: "text-blue-500",
    negotiation: "text-orange-500",
    closed_won: "text-green-600",
    closed_lost: "text-red-600",
  };
  return colors[status] || "text-gray-500";
}

export function getRiskColor(level: string): string {
  const colors: Record<string, string> = {
    low: "text-green-500",
    medium: "text-yellow-500",
    high: "text-orange-500",
    critical: "text-red-500",
  };
  return colors[level] || "text-gray-500";
}
