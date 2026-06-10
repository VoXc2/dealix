"use client";

import { useState } from "react";
import { FileText, Download, Search, Filter, ArrowUpRight } from "lucide-react";
import { useLocale } from "next-intl";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { cn, formatCurrency, formatRelativeTime } from "@/lib/utils";
import { useInvoices, type InvoiceData } from "@/lib/hooks/usePayments";

const statusConfig: Record<string, { label: string; labelAr: string; color: string }> = {
  paid: { label: "Paid", labelAr: "مدفوعة", color: "bg-emerald-500/10 text-emerald-500 border-emerald-500/20" },
  sent: { label: "Sent", labelAr: "مرسلة", color: "bg-blue-500/10 text-blue-500 border-blue-500/20" },
  draft: { label: "Draft", labelAr: "مسودة", color: "bg-muted text-muted-foreground border-border" },
  overdue: { label: "Overdue", labelAr: "متأخرة", color: "bg-red-500/10 text-red-500 border-red-500/20" },
  cancelled: { label: "Cancelled", labelAr: "ملغية", color: "bg-muted text-muted-foreground border-border" },
};

export default function InvoicesPage() {
  const [search, setSearch] = useState("");
  const locale = useLocale();
  const isRTL = locale === "ar";
  const { data, isLoading } = useInvoices({ limit: 50 });

  const invoices = data?.data ?? [];
  const filtered = invoices.filter(
    (inv) =>
      inv.number.toLowerCase().includes(search.toLowerCase()) ||
      inv.items.some((i) => i.description.toLowerCase().includes(search.toLowerCase())),
  );

  return (
    <AppLayout
      title={isRTL ? "الفواتير" : "Invoices"}
      subtitle={isRTL ? "سجل الفواتير والمدفوعات" : "Invoice and payment history"}
    >
      <Card>
        <CardHeader>
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <CardTitle className="text-lg font-bold flex items-center gap-2">
              <FileText className="w-5 h-5 text-gold-500" />
              {isRTL ? "جميع الفواتير" : "All Invoices"}
            </CardTitle>
            <div className="flex items-center gap-2 w-full sm:w-auto">
              <div className="relative flex-1 sm:w-64">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <Input
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder={isRTL ? "بحث..." : "Search..."}
                  className="pl-9"
                  dir={isRTL ? "rtl" : "ltr"}
                />
              </div>
              <Button variant="outline" size="icon">
                <Filter className="w-4 h-4" />
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
              <FileText className="w-12 h-12 text-muted-foreground/30 mb-3" />
              <p className="text-sm text-muted-foreground">
                {isRTL ? "لا توجد فواتير" : "No invoices found"}
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border">
                    <th className="text-left py-3 px-4 font-medium text-muted-foreground">
                      {isRTL ? "الرقم" : "Number"}
                    </th>
                    <th className="text-left py-3 px-4 font-medium text-muted-foreground">
                      {isRTL ? "المبلغ" : "Amount"}
                    </th>
                    <th className="text-left py-3 px-4 font-medium text-muted-foreground">
                      {isRTL ? "الحالة" : "Status"}
                    </th>
                    <th className="text-left py-3 px-4 font-medium text-muted-foreground">
                      {isRTL ? "تاريخ الإصدار" : "Issued"}
                    </th>
                    <th className="text-left py-3 px-4 font-medium text-muted-foreground">
                      {isRTL ? "تاريخ الاستحقاق" : "Due"}
                    </th>
                    <th className="text-right py-3 px-4 font-medium text-muted-foreground">
                      {isRTL ? "إجراءات" : "Actions"}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((inv) => {
                    const config = statusConfig[inv.status] || statusConfig.draft;
                    return (
                      <tr
                        key={inv.id}
                        className="border-b border-border/50 hover:bg-accent/30 transition-colors"
                      >
                        <td className="py-3 px-4 font-medium text-foreground">
                          {inv.number}
                        </td>
                        <td className="py-3 px-4 tabular-nums">
                          {formatCurrency(inv.amount, locale)}
                        </td>
                        <td className="py-3 px-4">
                          <Badge variant="outline" className={cn("text-xs", config.color)}>
                            {isRTL ? config.labelAr : config.label}
                          </Badge>
                        </td>
                        <td className="py-3 px-4 text-muted-foreground">
                          {formatRelativeTime(inv.issuedAt, locale)}
                        </td>
                        <td className="py-3 px-4 text-muted-foreground">
                          {formatRelativeTime(inv.dueDate, locale)}
                        </td>
                        <td className="py-3 px-4 text-right">
                          <div className="flex items-center justify-end gap-1">
                            <Button variant="ghost" size="sm">
                              <Download className="w-3.5 h-3.5" />
                            </Button>
                            <Button variant="ghost" size="sm">
                              <ArrowUpRight className="w-3.5 h-3.5" />
                            </Button>
                          </div>
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
