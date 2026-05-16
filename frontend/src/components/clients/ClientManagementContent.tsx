"use client";

import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { useTranslations, useLocale } from "next-intl";
import { motion } from "framer-motion";
import { Search, Plus, MoreHorizontal } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { cn, formatCurrency, getStatusColor } from "@/lib/utils";
import { api } from "@/lib/api";
import { founderLeadToClient } from "@/lib/api-normalize";
import type { Client } from "@/types";

export function ClientManagementContent() {
  const t = useTranslations("clients");
  const locale = useLocale();
  const isAr = locale === "ar";
  const [search, setSearch] = useState("");

  const leadsQuery = useQuery({
    queryKey: ["clients", "founder-leads"],
    queryFn: async () => (await api.getLeads()).data,
  });

  const clients: Client[] = useMemo(() => {
    if (!leadsQuery.data || typeof leadsQuery.data !== "object") {
      return [];
    }
    const root = leadsQuery.data as Record<string, unknown>;
    const leads = root.leads;
    if (!Array.isArray(leads)) return [];
    return leads.map((row, i) =>
      founderLeadToClient(row as Record<string, unknown>, i),
    );
  }, [leadsQuery.data]);

  const filtered = clients.filter(
    (c) =>
      c.company.toLowerCase().includes(search.toLowerCase()) ||
      c.contactName.toLowerCase().includes(search.toLowerCase()),
  );

  return (
    <div>
      {leadsQuery.isError && (
        <div
          role="alert"
          className="mb-4 rounded-xl border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm"
        >
          <p>
            {isAr
              ? "تعذر تحميل العملاء من صندوق الـ leads."
              : "Could not load clients from the lead inbox."}
          </p>
          <Button
            type="button"
            variant="outline"
            size="sm"
            className="mt-2"
            onClick={() => leadsQuery.refetch()}
          >
            {isAr ? "إعادة المحاولة" : "Retry"}
          </Button>
        </div>
      )}

      <div className="flex items-center gap-3 mb-6">
        <div className="relative flex-1 max-w-sm">
          <Search
            className={cn(
              "absolute top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground",
              isAr ? "right-3" : "left-3",
            )}
          />
          <Input
            placeholder={isAr ? "بحث عن عميل..." : "Search clients..."}
            className={cn(isAr ? "pr-9" : "pl-9")}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <Button variant="gold" size="sm" type="button">
          <Plus className="w-4 h-4 me-1.5" />
          {t("addClient")}
        </Button>
      </div>

      {leadsQuery.isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div
              key={i}
              className="h-56 rounded-2xl bg-muted/50 animate-pulse border border-border"
            />
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <p className="text-sm text-muted-foreground text-center py-16">
          {isAr
            ? "لا يوجد عملاء بعد. عند وصول طلبات عبر النموذج العام ستظهر هنا."
            : "No clients yet. Inquiries from the public form will appear here."}
        </p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {filtered.map((client, i) => (
            <motion.div
              key={client.id}
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.06 }}
              className="rounded-2xl border border-border bg-card p-5 hover:border-gold-500/30 hover:shadow-md transition-all group"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-gold-500/20 to-emerald-500/20 border border-gold-500/20 flex items-center justify-center text-base font-bold text-gold-400">
                    {client.company[0] ?? "—"}
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-foreground">
                      {client.company}
                    </h3>
                    <p className="text-xs text-muted-foreground mt-0.5">
                      {client.contactName}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Badge
                    variant="outline"
                    className={cn("text-[10px]", getStatusColor(client.status))}
                  >
                    {client.status === "active"
                      ? isAr
                        ? "نشط"
                        : "Active"
                      : client.status === "inactive"
                        ? isAr
                          ? "غير نشط"
                          : "Inactive"
                        : client.status === "churned"
                          ? isAr
                            ? "منسحب"
                            : "Churned"
                          : isAr
                            ? "محتمل"
                            : "Prospect"}
                  </Badge>
                  <button
                    type="button"
                    aria-label={isAr ? "خيارات" : "Options"}
                    className="opacity-0 group-hover:opacity-100 transition-opacity text-muted-foreground hover:text-foreground"
                  >
                    <MoreHorizontal className="w-4 h-4" />
                  </button>
                </div>
              </div>

              <div className="mb-1">
                <p className="text-xs text-muted-foreground">{client.industry}</p>
              </div>

              <div className="mb-3">
                <div className="flex items-center justify-between text-xs mb-1">
                  <span className="text-muted-foreground">
                    {isAr ? "درجة الذكاء الاصطناعي" : "AI Score"}
                  </span>
                  <span className="font-semibold text-gold-400">
                    {client.aiScore}/100
                  </span>
                </div>
                <Progress value={client.aiScore} className="h-1.5" />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="p-2.5 rounded-xl bg-muted/50">
                  <p className="text-xs text-muted-foreground">
                    {isAr ? "الصفقات" : "Deals"}
                  </p>
                  <p className="text-base font-bold text-foreground">
                    {client.totalDeals}
                  </p>
                </div>
                <div className="p-2.5 rounded-xl bg-muted/50">
                  <p className="text-xs text-muted-foreground">
                    {isAr ? "الميزانية المذكورة" : "Stated budget"}
                  </p>
                  <p className="text-sm font-bold text-gold-400 truncate">
                    {formatCurrency(client.totalRevenue)}
                  </p>
                </div>
              </div>

              {client.tags.length > 0 && (
                <div className="flex flex-wrap gap-1 mt-3">
                  {client.tags.map((tag) => (
                    <span
                      key={tag}
                      className="text-[10px] px-2 py-0.5 rounded-full bg-muted text-muted-foreground"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
}
