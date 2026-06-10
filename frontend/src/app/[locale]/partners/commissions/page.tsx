"use client";

import { useState } from "react";
import { DollarSign, Filter, Download, CheckCircle, Clock, AlertTriangle } from "lucide-react";
import { useLocale } from "next-intl";
import { cn, formatCurrency, formatRelativeTime } from "@/lib/utils";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { usePartners, usePartnerCommissions, type PartnerCommission } from "@/lib/hooks/usePartners";

const statusConfig: Record<string, { label: string; labelAr: string; color: string; icon: React.ElementType }> = {
  paid: { label: "Paid", labelAr: "مدفوعة", color: "bg-emerald-500/10 text-emerald-500 border-emerald-500/20", icon: CheckCircle },
  approved: { label: "Approved", labelAr: "معتمدة", color: "bg-blue-500/10 text-blue-500 border-blue-500/20", icon: CheckCircle },
  pending: { label: "Pending", labelAr: "معلقة", color: "bg-amber-500/10 text-amber-500 border-amber-500/20", icon: Clock },
};

export default function CommissionsPage() {
  const [search, setSearch] = useState("");
  const [selectedPartner, setSelectedPartner] = useState<string | null>(null);
  const locale = useLocale();
  const isRTL = locale === "ar";

  const { data: partners } = usePartners();
  const { data: commissions, isLoading } = usePartnerCommissions(selectedPartner);

  const allCommissions = commissions ?? [];

  const filtered = allCommissions.filter((c) => {
    if (!search) return true;
    return c.id.toLowerCase().includes(search.toLowerCase());
  });

  const totalPending = allCommissions.filter((c) => c.status === "pending").reduce((s, c) => s + c.amount, 0);
  const totalPaid = allCommissions.filter((c) => c.status === "paid").reduce((s, c) => s + c.amount, 0);

  return (
    <AppLayout
      title={isRTL ? "العمولات" : "Commissions"}
      subtitle={isRTL ? "تتبع العمولات والمدفوعات" : "Track commissions and payments"}
    >
      {/* Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <Card>
          <CardContent className="p-5">
            <p className="text-xs text-muted-foreground mb-1">
              {isRTL ? "إجمالي العمولات" : "Total Commissions"}
            </p>
            <p className="text-2xl font-bold text-foreground">
              {formatCurrency(totalPending + totalPaid, locale)}
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-5">
            <p className="text-xs text-muted-foreground mb-1">
              {isRTL ? "المدفوعة" : "Paid"}
            </p>
            <p className="text-2xl font-bold text-emerald-500">
              {formatCurrency(totalPaid, locale)}
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-5">
            <p className="text-xs text-muted-foreground mb-1">
              {isRTL ? "المعلقة" : "Pending"}
            </p>
            <p className="text-2xl font-bold text-amber-500">
              {formatCurrency(totalPending, locale)}
            </p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <CardTitle className="text-lg font-bold flex items-center gap-2">
              <DollarSign className="w-5 h-5 text-gold-500" />
              {isRTL ? "سجل العمولات" : "Commission History"}
            </CardTitle>
            <div className="flex items-center gap-2 w-full sm:w-auto">
              {parties && parties.length > 0 && (
                <select
                  value={selectedPartner ?? ""}
                  onChange={(e) => setSelectedPartner(e.target.value || null)}
                  className="rounded-lg border border-border bg-background px-3 py-1.5 text-sm"
                >
                  <option value="">
                    {isRTL ? "جميع الشركاء" : "All Partners"}
                  </option>
                  {parties.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.company}
                    </option>
                  ))}
                </select>
              )}
              <Button variant="outline" size="sm">
                <Download className="w-3.5 h-3.5 mr-1" />
                {isRTL ? "تصدير" : "Export"}
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex items-center justify-center py-12 text-sm text-muted-foreground">
              {isRTL ? "جاري التحميل..." : "Loading..."}
            </div>
          ) : filtered.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <DollarSign className="w-12 h-12 text-muted-foreground/30 mb-3" />
              <p className="text-sm text-muted-foreground">
                {isRTL ? "لا توجد عمولات" : "No commissions found"}
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left py-3 px-4 font-medium text-muted-foreground">ID</th>
                    <th className="text-right py-3 px-4 font-medium text-muted-foreground">{isRTL ? "المبلغ" : "Amount"}</th>
                    <th className="text-left py-3 px-4 font-medium text-muted-foreground">{isRTL ? "الحالة" : "Status"}</th>
                    <th className="text-left py-3 px-4 font-medium text-muted-foreground">{isRTL ? "التاريخ" : "Date"}</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((comm) => {
                    const config = statusConfig[comm.status] || statusConfig.pending;
                    const Icon = config.icon;
                    return (
                      <tr key={comm.id} className="border-b border-border/50 hover:bg-accent/30 transition-colors">
                        <td className="py-3 px-4 font-mono text-xs text-foreground">
                          {comm.id.slice(0, 8)}...
                        </td>
                        <td className="py-3 px-4 text-right tabular-nums font-semibold text-foreground">
                          {formatCurrency(comm.amount, locale)}
                        </td>
                        <td className="py-3 px-4">
                          <Badge variant="outline" className={cn("text-xs", config.color)}>
                            <Icon className="w-3 h-3 mr-1" />
                            {isRTL ? config.labelAr : config.label}
                          </Badge>
                        </td>
                        <td className="py-3 px-4 text-muted-foreground">
                          {formatRelativeTime(comm.earnedAt, locale)}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>
    </AppLayout>
  );
}
