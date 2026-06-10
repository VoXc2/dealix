"use client";

import { useState } from "react";
import { FileText, Plus, Search, Eye, Edit3, Trash2, Star, Download, ExternalLink } from "lucide-react";
import { useLocale } from "next-intl";
import { cn, formatRelativeTime } from "@/lib/utils";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";

interface CaseStudy {
  id: string;
  title: string;
  company: string;
  industry: string;
  status: "draft" | "published" | "archived";
  featured: boolean;
  createdAt: string;
}

const mockStudies: CaseStudy[] = [
  { id: "1", title: "How TechCo Boosted Revenue 300% with AI", company: "TechCo", industry: "Technology", status: "published", featured: true, createdAt: "2026-05-20" },
  { id: "2", title: "RetailChain: AI-Powered Customer Segmentation", company: "RetailChain", industry: "Retail", status: "draft", featured: false, createdAt: "2026-05-18" },
  { id: "3", title: "FinServ Achieves ZATCA Compliance in 2 Weeks", company: "FinServ", industry: "Finance", status: "published", featured: true, createdAt: "2026-05-15" },
  { id: "4", title: "HealthPlus: Streamlining Patient Acquisition", company: "HealthPlus", industry: "Healthcare", status: "draft", featured: false, createdAt: "2026-05-10" },
];

const statusConfig: Record<string, { label: string; labelAr: string; color: string }> = {
  published: { label: "Published", labelAr: "منشور", color: "bg-emerald-500/10 text-emerald-500 border-emerald-500/20" },
  draft: { label: "Draft", labelAr: "مسودة", color: "bg-muted text-muted-foreground border-border" },
  archived: { label: "Archived", labelAr: "مؤرشف", color: "bg-muted text-muted-foreground border-border" },
};

export default function CaseStudiesPage() {
  const [search, setSearch] = useState("");
  const locale = useLocale();
  const isRTL = locale === "ar";

  const filtered = mockStudies.filter((s) =>
    s.title.toLowerCase().includes(search.toLowerCase()) ||
    s.company.toLowerCase().includes(search.toLowerCase()),
  );

  return (
    <AppLayout
      title={isRTL ? "دراسات الحالة" : "Case Studies"}
      subtitle={isRTL ? "إدارة دراسات الحالة التسويقية" : "Manage marketing case studies"}
    >
      <Card>
        <CardHeader>
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <CardTitle className="text-lg font-bold flex items-center gap-2">
              <FileText className="w-5 h-5 text-gold-500" />
              {isRTL ? "جميع دراسات الحالة" : "All Case Studies"}
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
              <Button>
                <Plus className="w-4 h-4 mr-1" />
                {isRTL ? "جديد" : "New"}
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {filtered.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <FileText className="w-12 h-12 text-muted-foreground/30 mb-3" />
              <p className="text-sm text-muted-foreground">
                {isRTL ? "لا توجد دراسات حالة" : "No case studies found"}
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {filtered.map((study) => {
                const config = statusConfig[study.status];
                return (
                  <Card key={study.id} className="hover:border-gold-500/30 transition-colors group">
                    <CardContent className="p-5">
                      <div className="flex items-start justify-between mb-2">
                        <Badge variant="outline" className={cn("text-xs", config.color)}>
                          {isRTL ? config.labelAr : config.label}
                        </Badge>
                        {study.featured && (
                          <Star className="w-4 h-4 text-gold-500 fill-gold-500" />
                        )}
                      </div>
                      <h3 className="text-sm font-semibold text-foreground mb-1 line-clamp-2">
                        {study.title}
                      </h3>
                      <p className="text-xs text-muted-foreground mb-3">
                        {study.company} · {study.industry}
                      </p>
                      <div className="flex items-center justify-between">
                        <span className="text-[10px] text-muted-foreground">
                          {formatRelativeTime(study.createdAt, locale)}
                        </span>
                        <div className="hidden group-hover:flex items-center gap-1">
                          <Button variant="ghost" size="sm"><Eye className="w-3.5 h-3.5" /></Button>
                          <Button variant="ghost" size="sm"><Edit3 className="w-3.5 h-3.5" /></Button>
                          <Button variant="ghost" size="sm"><Download className="w-3.5 h-3.5" /></Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          )}
        </CardContent>
      </Card>
    </AppLayout>
  );
}
