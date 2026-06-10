"use client";

import { useState } from "react";
import { FileText, Plus, Search, Filter, CheckCircle, Clock, AlertCircle, Edit3, Trash2 } from "lucide-react";
import { useLocale } from "next-intl";
import { cn, formatRelativeTime } from "@/lib/utils";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";

interface ContentItem {
  id: string;
  title: string;
  platform: string;
  status: "draft" | "scheduled" | "published" | "failed";
  scheduledFor?: string;
  createdAt: string;
}

const mockContent: ContentItem[] = [
  { id: "1", title: "Why Saudi Businesses Need AI RevOps", platform: "LinkedIn", status: "published", scheduledFor: "2026-06-01", createdAt: "2026-05-28" },
  { id: "2", title: "Dealix vs Traditional CRM: ROI Analysis", platform: "Blog", status: "scheduled", scheduledFor: "2026-06-03", createdAt: "2026-05-27" },
  { id: "3", title: "Customer Success: AI Transformation", platform: "Case Study", status: "draft", createdAt: "2026-05-26" },
  { id: "4", title: "ZATCA Compliance Made Easy", platform: "Twitter", status: "draft", createdAt: "2026-05-25" },
  { id: "5", title: "The Future of Revenue Operations", platform: "LinkedIn", status: "failed", createdAt: "2026-05-24" },
];

const statusConfig: Record<string, { label: string; labelAr: string; color: string; icon: React.ElementType }> = {
  published: { label: "Published", labelAr: "منشور", color: "bg-emerald-500/10 text-emerald-500 border-emerald-500/20", icon: CheckCircle },
  scheduled: { label: "Scheduled", labelAr: "مجدول", color: "bg-blue-500/10 text-blue-500 border-blue-500/20", icon: Clock },
  draft: { label: "Draft", labelAr: "مسودة", color: "bg-muted text-muted-foreground border-border", icon: FileText },
  failed: { label: "Failed", labelAr: "فشل", color: "bg-red-500/10 text-red-500 border-red-500/20", icon: AlertCircle },
};

export default function ContentQueuePage() {
  const [search, setSearch] = useState("");
  const locale = useLocale();
  const isRTL = locale === "ar";

  const filtered = mockContent.filter((c) =>
    c.title.toLowerCase().includes(search.toLowerCase()),
  );

  return (
    <AppLayout
      title={isRTL ? "قائمة المحتوى" : "Content Queue"}
      subtitle={isRTL ? "إدارة وجدولة المحتوى التسويقي" : "Manage and schedule marketing content"}
    >
      <Card>
        <CardHeader>
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <CardTitle className="text-lg font-bold flex items-center gap-2">
              <FileText className="w-5 h-5 text-gold-500" />
              {isRTL ? "جميع المحتوى" : "All Content"}
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
                {isRTL ? "لا يوجد محتوى" : "No content found"}
              </p>
            </div>
          ) : (
            <div className="space-y-2">
              {filtered.map((item) => {
                const config = statusConfig[item.status];
                const Icon = config.icon;
                return (
                  <div
                    key={item.id}
                    className="flex items-center gap-4 rounded-xl border border-border p-4 hover:bg-accent/30 transition-colors group"
                  >
                    <div className={cn("flex h-10 w-10 items-center justify-center rounded-lg", config.color)}>
                      <Icon className="w-5 h-5" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-semibold text-foreground truncate">{item.title}</p>
                      <div className="flex items-center gap-2 mt-0.5">
                        <span className="text-xs text-muted-foreground">{item.platform}</span>
                        <span className="text-muted-foreground">·</span>
                        <span className="text-xs text-muted-foreground">
                          {formatRelativeTime(item.createdAt, locale)}
                        </span>
                      </div>
                    </div>
                    <Badge variant="outline" className={cn("text-xs", config.color)}>
                      {isRTL ? config.labelAr : config.label}
                    </Badge>
                    <div className="hidden group-hover:flex items-center gap-1">
                      <Button variant="ghost" size="sm">
                        <Edit3 className="w-3.5 h-3.5" />
                      </Button>
                      <Button variant="ghost" size="sm">
                        <Trash2 className="w-3.5 h-3.5 text-red-500" />
                      </Button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </CardContent>
      </Card>
    </AppLayout>
  );
}
