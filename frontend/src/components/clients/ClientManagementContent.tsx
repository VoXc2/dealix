"use client";

import { useState } from "react";
import { useTranslations, useLocale } from "next-intl";
import { motion } from "framer-motion";
import { Search, Plus, MoreHorizontal } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { cn, formatCurrency, getStatusColor } from "@/lib/utils";
import type { Client } from "@/types";

const mockClientsAr: Client[] = [
  {
    id: "c1",
    company: "أرامكو السعودية",
    contactName: "فهد العبدالله",
    contactEmail: "fahad@aramco.com",
    status: "active",
    industry: "النفط والطاقة",
    totalDeals: 8,
    totalRevenue: 12500000,
    lastActivity: new Date(Date.now() - 2 * 3600000).toISOString(),
    aiScore: 94,
    tags: ["enterprise", "oil-gas"],
  },
  {
    id: "c2",
    company: "البنك الأهلي السعودي",
    contactName: "نورة السلطان",
    contactEmail: "noura@ncb.com.sa",
    status: "active",
    industry: "الخدمات المصرفية",
    totalDeals: 5,
    totalRevenue: 8200000,
    lastActivity: new Date(Date.now() - 5 * 3600000).toISOString(),
    aiScore: 87,
    tags: ["banking", "fintech"],
  },
  {
    id: "c3",
    company: "STC",
    contactName: "عبدالرحمن الزهراني",
    contactEmail: "ar@stc.com.sa",
    status: "active",
    industry: "الاتصالات",
    totalDeals: 6,
    totalRevenue: 9800000,
    lastActivity: new Date(Date.now() - 30 * 60000).toISOString(),
    aiScore: 91,
    tags: ["telecom", "enterprise"],
  },
  {
    id: "c4",
    company: "SABIC",
    contactName: "منى القحطاني",
    contactEmail: "mona@sabic.com",
    status: "prospect",
    industry: "البتروكيماويات",
    totalDeals: 2,
    totalRevenue: 3100000,
    lastActivity: new Date(Date.now() - 2 * 24 * 3600000).toISOString(),
    aiScore: 76,
    tags: ["petrochemical"],
  },
  {
    id: "c5",
    company: "وزارة التجارة",
    contactName: "خالد الغامدي",
    contactEmail: "khalid@commerce.gov.sa",
    status: "active",
    industry: "حكومي",
    totalDeals: 3,
    totalRevenue: 6700000,
    lastActivity: new Date(Date.now() - 45 * 60000).toISOString(),
    aiScore: 88,
    tags: ["government"],
  },
  {
    id: "c6",
    company: "مجموعة الفيصل",
    contactName: "سلطان الفيصل",
    contactEmail: "sultan@alfaisal.com",
    status: "inactive",
    industry: "التجزئة والاستثمار",
    totalDeals: 1,
    totalRevenue: 1200000,
    lastActivity: new Date(Date.now() - 7 * 24 * 3600000).toISOString(),
    aiScore: 58,
    tags: ["retail"],
  },
];

const mockClientsEn: Client[] = [
  {
    id: "c1",
    company: "Saudi Aramco",
    contactName: "Fahad Al-Abdullah",
    contactEmail: "fahad@aramco.com",
    status: "active",
    industry: "Oil & Energy",
    totalDeals: 8,
    totalRevenue: 12500000,
    lastActivity: new Date(Date.now() - 2 * 3600000).toISOString(),
    aiScore: 94,
    tags: ["enterprise", "oil-gas"],
  },
  {
    id: "c2",
    company: "Saudi National Bank",
    contactName: "Noura Al-Sultan",
    contactEmail: "noura@ncb.com.sa",
    status: "active",
    industry: "Banking",
    totalDeals: 5,
    totalRevenue: 8200000,
    lastActivity: new Date(Date.now() - 5 * 3600000).toISOString(),
    aiScore: 87,
    tags: ["banking", "fintech"],
  },
  {
    id: "c3",
    company: "STC",
    contactName: "Abdulrahman Al-Zahrani",
    contactEmail: "ar@stc.com.sa",
    status: "active",
    industry: "Telecom",
    totalDeals: 6,
    totalRevenue: 9800000,
    lastActivity: new Date(Date.now() - 30 * 60000).toISOString(),
    aiScore: 91,
    tags: ["telecom", "enterprise"],
  },
  {
    id: "c4",
    company: "SABIC",
    contactName: "Mona Al-Qahtani",
    contactEmail: "mona@sabic.com",
    status: "prospect",
    industry: "Petrochemicals",
    totalDeals: 2,
    totalRevenue: 3100000,
    lastActivity: new Date(Date.now() - 2 * 24 * 3600000).toISOString(),
    aiScore: 76,
    tags: ["petrochemical"],
  },
  {
    id: "c5",
    company: "Ministry of Commerce",
    contactName: "Khalid Al-Ghamdi",
    contactEmail: "khalid@commerce.gov.sa",
    status: "active",
    industry: "Government",
    totalDeals: 3,
    totalRevenue: 6700000,
    lastActivity: new Date(Date.now() - 45 * 60000).toISOString(),
    aiScore: 88,
    tags: ["government"],
  },
  {
    id: "c6",
    company: "Al-Faisal Group",
    contactName: "Sultan Al-Faisal",
    contactEmail: "sultan@alfaisal.com",
    status: "inactive",
    industry: "Retail & Investment",
    totalDeals: 1,
    totalRevenue: 1200000,
    lastActivity: new Date(Date.now() - 7 * 24 * 3600000).toISOString(),
    aiScore: 58,
    tags: ["retail"],
  },
];

export function ClientManagementContent() {
  const t = useTranslations("clients");
  const locale = useLocale();
  const isAr = locale === "ar";
  const [search, setSearch] = useState("");
  const clients = isAr ? mockClientsAr : mockClientsEn;

  const filtered = clients.filter(
    (c) =>
      c.company.toLowerCase().includes(search.toLowerCase()) ||
      c.contactName.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      {/* Toolbar */}
      <div className="flex items-center gap-3 mb-6">
        <div className="relative flex-1 max-w-sm">
          <Search className={cn("absolute top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground", isAr ? "right-3" : "left-3")} />
          <Input
            placeholder={isAr ? "بحث عن عميل..." : "Search clients..."}
            className={cn(isAr ? "pr-9" : "pl-9")}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <Button variant="gold" size="sm">
          <Plus className="w-4 h-4 me-1.5" />
          {t("addClient")}
        </Button>
      </div>

      {/* Client grid */}
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
                  {client.company[0]}
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-foreground">{client.company}</h3>
                  <p className="text-xs text-muted-foreground mt-0.5">{client.contactName}</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Badge
                  variant="outline"
                  className={cn("text-[10px]", getStatusColor(client.status))}
                >
                  {client.status === "active" ? (isAr ? "نشط" : "Active") :
                   client.status === "inactive" ? (isAr ? "غير نشط" : "Inactive") :
                   isAr ? "محتمل" : "Prospect"}
                </Badge>
                <button className="opacity-0 group-hover:opacity-100 transition-opacity text-muted-foreground hover:text-foreground">
                  <MoreHorizontal className="w-4 h-4" />
                </button>
              </div>
            </div>

            <div className="mb-1">
              <p className="text-xs text-muted-foreground">{client.industry}</p>
            </div>

            {/* AI Score */}
            <div className="mb-3">
              <div className="flex items-center justify-between text-xs mb-1">
                <span className="text-muted-foreground">{isAr ? "درجة الذكاء الاصطناعي" : "AI Score"}</span>
                <span className="font-semibold text-gold-400">{client.aiScore}/100</span>
              </div>
              <Progress value={client.aiScore} className="h-1.5" />
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 gap-3">
              <div className="p-2.5 rounded-xl bg-muted/50">
                <p className="text-xs text-muted-foreground">{isAr ? "الصفقات" : "Deals"}</p>
                <p className="text-base font-bold text-foreground">{client.totalDeals}</p>
              </div>
              <div className="p-2.5 rounded-xl bg-muted/50">
                <p className="text-xs text-muted-foreground">{isAr ? "الإيرادات" : "Revenue"}</p>
                <p className="text-sm font-bold text-gold-400 truncate">{formatCurrency(client.totalRevenue)}</p>
              </div>
            </div>

            {/* Tags */}
            {client.tags.length > 0 && (
              <div className="flex flex-wrap gap-1 mt-3">
                {client.tags.map((tag) => (
                  <span key={tag} className="text-[10px] px-2 py-0.5 rounded-full bg-muted text-muted-foreground">
                    {tag}
                  </span>
                ))}
              </div>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  );
}
