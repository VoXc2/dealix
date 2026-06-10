"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Crosshair, Target, TrendingUp, Users, DollarSign, Phone, Mail, MessageCircle, RefreshCw, Filter, Plus } from "lucide-react";
import { useLocale } from "next-intl";
import { cn, formatCurrency, formatRelativeTime } from "@/lib/utils";
import { AppLayout } from "@/components/layout/AppLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

interface WarRoomLead {
  id: string;
  company: string;
  contactName: string;
  value: number;
  stage: string;
  priority: "p0" | "p1" | "p2";
  nextAction: string;
  lastActivity: string;
  score: number;
}

const mockLeads: WarRoomLead[] = [
  { id: "1", company: "Saudi Tech Solutions", contactName: "Ahmed Al-Saud", value: 250000, stage: "Proposal", priority: "p0", nextAction: "Send proposal", lastActivity: "2026-05-28T10:00:00Z", score: 92 },
  { id: "2", company: "AlRajhi Digital", contactName: "Khalid Al-Otaibi", value: 180000, stage: "Negotiation", priority: "p0", nextAction: "Schedule closing call", lastActivity: "2026-05-27T15:30:00Z", score: 88 },
  { id: "3", company: "STC Business", contactName: "Nora Al-Ghamdi", value: 500000, stage: "Pilot", priority: "p1", nextAction: "Review pilot results", lastActivity: "2026-05-26T09:00:00Z", score: 75 },
  { id: "4", company: "Mobily Enterprise", contactName: "Fahad Al-Omar", value: 120000, stage: "Qualified", priority: "p1", nextAction: "Send diagnostic report", lastActivity: "2026-05-25T14:00:00Z", score: 65 },
  { id: "5", company: "SABIC Digital", contactName: "Mohammed Al-Ali", value: 750000, stage: "Lead", priority: "p2", nextAction: "Initial outreach", lastActivity: "2026-05-24T11:00:00Z", score: 45 },
];

const priorityConfig = {
  p0: { label: "P0", labelAr: "عاجل", color: "bg-red-500/10 text-red-500 border-red-500/20" },
  p1: { label: "P1", labelAr: "هام", color: "bg-amber-500/10 text-amber-500 border-amber-500/20" },
  p2: { label: "P2", labelAr: "عادي", color: "bg-blue-500/10 text-blue-500 border-blue-500/20" },
};

export default function WarRoomPage() {
  const [filter, setFilter] = useState<"all" | "p0" | "p1" | "p2">("all");
  const locale = useLocale();
  const isRTL = locale === "ar";

  const filtered = filter === "all" ? mockLeads : mockLeads.filter((l) => l.priority === filter);
  const totalValue = filtered.reduce((s, l) => s + l.value, 0);

  return (
    <AppLayout
      title={isRTL ? "غرفة الحرب" : "War Room"}
      subtitle={isRTL ? "لوحة القيادة المباشرة للصفقات ذات الأولوية" : "Live command center for priority deals"}
    >
      {/* Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4 mb-8">
        <Card>
          <CardContent className="p-5">
            <div className="flex items-center gap-2 mb-2">
              <Target className="w-4 h-4 text-red-500" />
              <span className="text-xs text-muted-foreground">{isRTL ? "الأهداف النشطة" : "Active Targets"}</span>
            </div>
            <p className="text-2xl font-bold text-foreground">{filtered.length}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-5">
            <div className="flex items-center gap-2 mb-2">
              <DollarSign className="w-4 h-4 text-gold-500" />
              <span className="text-xs text-muted-foreground">{isRTL ? "قيمة المسار" : "Pipeline Value"}</span>
            </div>
            <p className="text-2xl font-bold text-foreground">{formatCurrency(totalValue, locale)}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-5">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="w-4 h-4 text-emerald-500" />
              <span className="text-xs text-muted-foreground">{isRTL ? "متوسط النقاط" : "Avg Score"}</span>
            </div>
            <p className="text-2xl font-bold text-foreground">
              {Math.round(filtered.reduce((s, l) => s + l.score, 0) / filtered.length)}
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-5">
            <div className="flex items-center gap-2 mb-2">
              <Crosshair className="w-4 h-4 text-amber-500" />
              <span className="text-xs text-muted-foreground">{isRTL ? "إجراءات اليوم" : "Today's Actions"}</span>
            </div>
            <p className="text-2xl font-bold text-foreground">{filtered.filter((l) => l.priority === "p0").length}</p>
          </CardContent>
        </Card>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-2 mb-6">
        {(["all", "p0", "p1", "p2"] as const).map((f) => (
          <Button
            key={f}
            variant={filter === f ? "default" : "outline"}
            size="sm"
            onClick={() => setFilter(f)}
          >
            {f === "all" ? (isRTL ? "الكل" : "All") : f.toUpperCase()}
          </Button>
        ))}
        <div className="flex-1" />
        <Button variant="outline" size="sm">
          <RefreshCw className="w-3.5 h-3.5 mr-1" />
          {isRTL ? "تحديث" : "Refresh"}
        </Button>
        <Button size="sm">
          <Plus className="w-3.5 h-3.5 mr-1" />
          {isRTL ? "إضافة هدف" : "Add Target"}
        </Button>
      </div>

      {/* Leads */}
      <div className="space-y-3">
        {filtered.map((lead, idx) => {
          const config = priorityConfig[lead.priority];
          return (
            <motion.div
              key={lead.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.05 }}
            >
              <Card className="hover:border-gold-500/30 transition-all group">
                <CardContent className="p-5">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-start gap-3">
                      <div className={cn("flex h-10 w-10 items-center justify-center rounded-xl", config.color)}>
                        <Target className="w-5 h-5" />
                      </div>
                      <div>
                        <div className="flex items-center gap-2 mb-0.5">
                          <h3 className="text-sm font-semibold text-foreground">{lead.company}</h3>
                          <Badge variant="outline" className={cn("text-[10px]", config.color)}>
                            {isRTL ? config.labelAr : config.label}
                          </Badge>
                        </div>
                        <p className="text-xs text-muted-foreground">{lead.contactName} · {lead.stage}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-bold text-foreground">{formatCurrency(lead.value, locale)}</p>
                      <Badge
                        variant="outline"
                        className={cn(
                          "text-[10px]",
                          lead.score >= 80 ? "bg-emerald-500/10 text-emerald-500" : lead.score >= 60 ? "bg-amber-500/10 text-amber-500" : "bg-muted text-muted-foreground",
                        )}
                      >
                        {lead.score} {isRTL ? "نقاط" : "score"}
                      </Badge>
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3 text-xs text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <MessageCircle className="w-3 h-3" />
                        {lead.nextAction}
                      </span>
                      <span>·</span>
                      <span>{formatRelativeTime(lead.lastActivity, locale)}</span>
                    </div>
                    <div className="hidden group-hover:flex items-center gap-1">
                      <Button variant="ghost" size="sm"><Phone className="w-3.5 h-3.5" /></Button>
                      <Button variant="ghost" size="sm"><Mail className="w-3.5 h-3.5" /></Button>
                    </div>
                  </div>

                  <Progress value={lead.score} className="h-1 mt-3" />
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>
    </AppLayout>
  );
}
