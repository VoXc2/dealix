"use client";

import { useState } from "react";
import { Handshake, Users, DollarSign, TrendingUp, ArrowRight, ExternalLink } from "lucide-react";
import { useLocale } from "next-intl";
import Link from "next/link";
import { cn, formatCurrency, formatNumber } from "@/lib/utils";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { usePartners, type PartnerData } from "@/lib/hooks/usePartners";

export default function PartnerDashboardPage() {
  const locale = useLocale();
  const isRTL = locale === "ar";
  const { data: partners, isLoading } = usePartners();

  const stats = [
    { icon: Users, label: "Total Partners", labelAr: "إجمالي الشركاء", value: partners?.length ?? 0, format: "number" as const },
    { icon: TrendingUp, label: "Active Partners", labelAr: "الشركاء النشطون", value: partners?.filter((p) => p.status === "active").length ?? 0, format: "number" as const },
    { icon: DollarSign, label: "Total Commission", labelAr: "إجمالي العمولات", value: partners?.reduce((s, p) => s + p.totalCommission, 0) ?? 0, format: "currency" as const },
    { icon: Handshake, label: "Total Referrals", labelAr: "إجمالي الإحالات", value: partners?.reduce((s, p) => s + p.totalReferrals, 0) ?? 0, format: "number" as const },
  ];

  return (
    <AppLayout
      title={isRTL ? "لوحة الشركاء" : "Partner Dashboard"}
      subtitle={isRTL ? "إدارة الشركاء والإحالات والعمولات" : "Manage partners, referrals, and commissions"}
    >
      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {stats.map((stat, idx) => (
          <Card key={idx}>
            <CardContent className="p-5">
              <div className="flex items-center justify-between mb-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gold-500/10">
                  <stat.icon className="w-5 h-5 text-gold-500" />
                </div>
              </div>
              <p className="text-2xl font-bold text-foreground tabular-nums mb-1">
                {stat.format === "currency" ? formatCurrency(stat.value as number, locale) : formatNumber(stat.value as number)}
              </p>
              <p className="text-sm text-muted-foreground">
                {isRTL ? stat.labelAr : stat.label}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Quick actions */}
      <div className="flex items-center gap-3 mb-6">
        <Link href={`/${locale}/partners/register`}>
          <Button variant="default">
            <Handshake className="w-4 h-4 mr-1" />
            {isRTL ? "تسجيل شريك جديد" : "Register Partner"}
          </Button>
        </Link>
        <Link href={`/${locale}/partners/commissions`}>
          <Button variant="outline">
            <DollarSign className="w-4 h-4 mr-1" />
            {isRTL ? "العمولات" : "Commissions"}
          </Button>
        </Link>
      </div>

      {/* Partners list */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg font-bold">
            {isRTL ? "قائمة الشركاء" : "Partner List"}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex items-center justify-center py-8 text-sm text-muted-foreground">
              {isRTL ? "جاري التحميل..." : "Loading..."}
            </div>
          ) : partners && partners.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left py-3 px-4 font-medium text-muted-foreground">{isRTL ? "الشركة" : "Company"}</th>
                    <th className="text-left py-3 px-4 font-medium text-muted-foreground">{isRTL ? "المستوى" : "Tier"}</th>
                    <th className="text-left py-3 px-4 font-medium text-muted-foreground">{isRTL ? "الحالة" : "Status"}</th>
                    <th className="text-right py-3 px-4 font-medium text-muted-foreground">{isRTL ? "الإحالات" : "Referrals"}</th>
                    <th className="text-right py-3 px-4 font-medium text-muted-foreground">{isRTL ? "العمولات" : "Commission"}</th>
                  </tr>
                </thead>
                <tbody>
                  {partners.map((partner) => (
                    <tr key={partner.id} className="border-b border-border/50 hover:bg-accent/30 transition-colors">
                      <td className="py-3 px-4 font-medium text-foreground">{partner.company}</td>
                      <td className="py-3 px-4">
                        <Badge
                          variant="outline"
                          className={cn(
                            partner.tier === "platinum" && "bg-purple-500/10 text-purple-500 border-purple-500/20",
                            partner.tier === "gold" && "bg-gold-500/10 text-gold-500 border-gold-500/20",
                            partner.tier === "silver" && "bg-blue-500/10 text-blue-500 border-blue-500/20",
                            partner.tier === "bronze" && "bg-amber-500/10 text-amber-500 border-amber-500/20",
                          )}
                        >
                          {partner.tier}
                        </Badge>
                      </td>
                      <td className="py-3 px-4">
                        <Badge
                          variant="outline"
                          className={cn(
                            partner.status === "active" ? "bg-emerald-500/10 text-emerald-500" : "bg-muted text-muted-foreground",
                          )}
                        >
                          {partner.status}
                        </Badge>
                      </td>
                      <td className="py-3 px-4 text-right tabular-nums">{partner.totalReferrals}</td>
                      <td className="py-3 px-4 text-right tabular-nums">{formatCurrency(partner.totalCommission, locale)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <Handshake className="w-12 h-12 text-muted-foreground/30 mb-3" />
              <p className="text-sm text-muted-foreground mb-4">
                {isRTL ? "لا يوجد شركاء بعد" : "No partners yet"}
              </p>
              <Link href={`/${locale}/partners/register`}>
                <Button size="sm">
                  {isRTL ? "تسجيل أول شريك" : "Register First Partner"}
                </Button>
              </Link>
            </div>
          )}
        </CardContent>
      </Card>
    </AppLayout>
  );
}
