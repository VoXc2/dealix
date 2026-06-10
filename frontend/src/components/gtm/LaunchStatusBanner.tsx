"use client";
import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";
import { usePublicLaunchStatus } from "@/lib/usePublicLaunchStatus";

export function LaunchStatusBanner() {
  const isAr = useLocale() === "ar";
  const { status, loading, moyasarLive } = usePublicLaunchStatus();
  if (loading && !status) return null;
  if (!status) return null;
  const ok = status.healthcheck_ok !== false;
  return (
    <Card className={`p-3 text-xs ${ok ? "border-[var(--dealix-deep-green)]/30" : "border-amber-500/40"}`}>
      <p className="font-medium">{ok ? (isAr ? "المنصة جاهزة" : "Platform ready") : (isAr ? "جاري التفعيل" : "Activating")}</p>
      {!moyasarLive && <p className="text-muted-foreground mt-1">{isAr ? "إطلاق ناعم — الدفع الإلكتروني لاحقاً." : "Soft launch — online checkout later."}</p>}
    </Card>
  );
}
