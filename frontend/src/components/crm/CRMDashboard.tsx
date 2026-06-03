"use client";

import { useState } from "react";
import { useLocale } from "next-intl";
import { motion, AnimatePresence } from "framer-motion";
import {
  Users, TrendingUp, Phone, Mail, Calendar, Plus, Search,
  MoreHorizontal, Star, Target, Activity,
  MessageSquare, Clock, DollarSign, ArrowUpRight, X, Check
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { cn } from "@/lib/utils";

type LeadStatus = "new" | "contacted" | "qualified" | "proposal" | "won" | "lost";
type Priority = "high" | "medium" | "low";

interface Lead {
  id: string;
  name: string;
  company: string;
  email: string;
  phone: string;
  status: LeadStatus;
  priority: Priority;
  value: number;
  source: string;
  assignedTo: string;
  lastContact: string;
  nextAction: string;
  aiScore: number;
  notes: string;
  tags: string[];
}

interface Deal {
  id: string;
  title: string;
  company: string;
  value: number;
  stage: string;
  probability: number;
  closeDate: string;
  owner: string;
}

const MOCK_LEADS: Lead[] = [
  { id: "l1", name: "فهد الحربي", company: "شركة المملكة القابضة", email: "fahad@kingdom.sa", phone: "+966501234567", status: "qualified", priority: "high", value: 150000, source: "Website", assignedTo: "أحمد السلمان", lastContact: "منذ ساعتين", nextAction: "إرسال العرض التجاري", aiScore: 88, notes: "عميل مهتم جداً بحل CRM", tags: ["enterprise", "hot"] },
  { id: "l2", name: "نورة القحطاني", company: "بنك الرياض", email: "noura@riyadhbank.com", phone: "+966502345678", status: "contacted", priority: "high", value: 250000, source: "LinkedIn", assignedTo: "سارة العتيبي", lastContact: "أمس", nextAction: "مكالمة تقنية", aiScore: 76, notes: "تحتاج عرض تقني مفصل", tags: ["banking", "warm"] },
  { id: "l3", name: "عبدالله الشمري", company: "شركة زين السعودية", email: "a.shamri@zain.sa", phone: "+966503456789", status: "proposal", priority: "medium", value: 180000, source: "Referral", assignedTo: "محمد الدوسري", lastContact: "منذ 3 أيام", nextAction: "متابعة العرض", aiScore: 65, notes: "في انتظار الموافقة الداخلية", tags: ["telecom"] },
  { id: "l4", name: "ريم البكر", company: "مجموعة MBC", email: "r.baker@mbc.net", phone: "+966504567890", status: "new", priority: "medium", value: 95000, source: "Cold Email", assignedTo: "لم يُعيَّن", lastContact: "لم يتم التواصل", nextAction: "الاتصال الأول", aiScore: 52, notes: "Lead جديد من حملة Q4", tags: ["media"] },
  { id: "l5", name: "خالد العمر", company: "أرامكو السعودية", email: "k.omar@aramco.com", phone: "+966505678901", status: "won", priority: "high", value: 500000, source: "Conference", assignedTo: "أحمد السلمان", lastContact: "اليوم", nextAction: "Onboarding", aiScore: 96, notes: "تم الإغلاق بنجاح!", tags: ["enterprise", "closed"] },
  { id: "l6", name: "منى الزهراني", company: "STC Pay", email: "mona@stc.com.sa", phone: "+966506789012", status: "lost", priority: "low", value: 75000, source: "Website", assignedTo: "سارة العتيبي", lastContact: "أسبوع", nextAction: "إعادة التواصل بعد 3 أشهر", aiScore: 23, notes: "اختاروا منافسًا", tags: ["fintech", "cold"] },
];

const MOCK_DEALS: Deal[] = [
  { id: "d1", title: "منصة إدارة العملاء", company: "شركة المملكة", value: 150000, stage: "proposal", probability: 65, closeDate: "2026-06-15", owner: "أحمد السلمان" },
  { id: "d2", title: "نظام التحليلات المتقدمة", company: "بنك الرياض", value: 250000, stage: "negotiation", probability: 80, closeDate: "2026-06-01", owner: "سارة العتيبي" },
  { id: "d3", title: "حل ZATCA المتكامل", company: "زين السعودية", value: 180000, stage: "demo", probability: 45, closeDate: "2026-07-30", owner: "محمد الدوسري" },
  { id: "d4", title: "تطوير AI مخصص", company: "أرامكو", value: 500000, stage: "closed_won", probability: 100, closeDate: "2026-05-20", owner: "أحمد السلمان" },
];

const STATUS_CONFIG: Record<LeadStatus, { label: string; labelEn: string; color: string; bg: string }> = {
  new: { label: "جديد", labelEn: "New", color: "text-blue-400", bg: "bg-blue-400/10 border-blue-400/30" },
  contacted: { label: "تم التواصل", labelEn: "Contacted", color: "text-purple-400", bg: "bg-purple-400/10 border-purple-400/30" },
  qualified: { label: "مؤهّل", labelEn: "Qualified", color: "text-yellow-400", bg: "bg-yellow-400/10 border-yellow-400/30" },
  proposal: { label: "عرض مقدَّم", labelEn: "Proposal", color: "text-orange-400", bg: "bg-orange-400/10 border-orange-400/30" },
  won: { label: "مُغلَق ✓", labelEn: "Won ✓", color: "text-emerald-400", bg: "bg-emerald-400/10 border-emerald-400/30" },
  lost: { label: "خُسِر", labelEn: "Lost", color: "text-red-400", bg: "bg-red-400/10 border-red-400/30" },
};

const PRIORITY_CONFIG: Record<Priority, { label: string; color: string }> = {
  high: { label: "عالية", color: "text-red-400" },
  medium: { label: "متوسطة", color: "text-yellow-400" },
  low: { label: "منخفضة", color: "text-gray-400" },
};

function formatSAR(v: number) {
  return v >= 1_000_000
    ? `${(v / 1_000_000).toFixed(1)}م ر.س`
    : v >= 1_000
    ? `${(v / 1_000).toFixed(0)}ألف ر.س`
    : `${v} ر.س`;
}

function ScoreRing({ score }: { score: number }) {
  const color = score >= 80 ? "#10b981" : score >= 60 ? "#D4AF37" : score >= 40 ? "#f97316" : "#ef4444";
  return (
    <div className="relative w-10 h-10 flex-shrink-0">
      <svg viewBox="0 0 36 36" className="w-10 h-10 -rotate-90">
        <circle cx="18" cy="18" r="14" fill="none" stroke="currentColor" strokeWidth="3" className="text-muted/30" />
        <circle
          cx="18" cy="18" r="14" fill="none" strokeWidth="3"
          stroke={color}
          strokeDasharray={`${(score / 100) * 87.96} 87.96`}
          strokeLinecap="round"
        />
      </svg>
      <span className="absolute inset-0 flex items-center justify-center text-[10px] font-bold" style={{ color }}>{score}</span>
    </div>
  );
}

function AddLeadModal({ onClose, onAdd }: { onClose: () => void; onAdd: (l: Lead) => void }) {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [form, setForm] = useState({ name: "", company: "", email: "", phone: "", value: "" });

  const handleSubmit = () => {
    if (!form.name || !form.company) return;
    onAdd({
      id: `l${Date.now()}`, name: form.name, company: form.company,
      email: form.email, phone: form.phone, status: "new", priority: "medium",
      value: Number(form.value) || 0, source: "Manual", assignedTo: "غير معيَّن",
      lastContact: "لم يتم التواصل", nextAction: "الاتصال الأول",
      aiScore: Math.floor(40 + Math.random() * 30), notes: "", tags: [],
    });
    onClose();
  };

  return (
    <motion.div
      initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, y: 20 }} animate={{ scale: 1, y: 0 }}
        className="w-full max-w-md bg-card border border-border rounded-2xl p-6 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-bold">{isAr ? "إضافة عميل محتمل جديد" : "Add New Lead"}</h3>
          <Button variant="ghost" size="sm" onClick={onClose}><X className="w-4 h-4" /></Button>
        </div>
        <div className="space-y-4">
          {[
            { key: "name", label: isAr ? "الاسم الكامل" : "Full Name", placeholder: isAr ? "أحمد الشمري" : "Ahmed Al-Shamri" },
            { key: "company", label: isAr ? "الشركة" : "Company", placeholder: isAr ? "شركة الرياض" : "Riyadh Corp" },
            { key: "email", label: "Email", placeholder: "email@company.sa" },
            { key: "phone", label: isAr ? "الهاتف" : "Phone", placeholder: "+966 5X XXX XXXX" },
            { key: "value", label: isAr ? "القيمة المتوقعة (ر.س)" : "Expected Value (SAR)", placeholder: "50000" },
          ].map(({ key, label, placeholder }) => (
            <div key={key}>
              <label className="text-sm text-muted-foreground mb-1 block">{label}</label>
              <Input
                value={form[key as keyof typeof form]}
                onChange={(e) => setForm((p) => ({ ...p, [key]: e.target.value }))}
                placeholder={placeholder}
              />
            </div>
          ))}
        </div>
        <div className="flex gap-3 mt-6">
          <Button onClick={handleSubmit} className="flex-1 bg-gold-500 hover:bg-gold-600 text-black">
            <Check className="w-4 h-4 me-2" /> {isAr ? "إضافة" : "Add Lead"}
          </Button>
          <Button variant="outline" onClick={onClose}>{isAr ? "إلغاء" : "Cancel"}</Button>
        </div>
      </motion.div>
    </motion.div>
  );
}

export function CRMDashboard() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [leads, setLeads] = useState<Lead[]>(MOCK_LEADS);
  const [search, setSearch] = useState("");
  const [filterStatus, setFilterStatus] = useState<LeadStatus | "all">("all");
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);
  const [activeTab, setActiveTab] = useState("leads");

  const filtered = leads.filter((l) => {
    const matchSearch = !search || l.name.includes(search) || l.company.includes(search) || l.email.includes(search);
    const matchStatus = filterStatus === "all" || l.status === filterStatus;
    return matchSearch && matchStatus;
  });

  const kpis = [
    { icon: Users, label: isAr ? "إجمالي العملاء" : "Total Leads", value: leads.length.toString(), change: "+12%", color: "text-blue-400" },
    { icon: Target, label: isAr ? "العملاء المؤهلون" : "Qualified Leads", value: leads.filter((l) => l.status === "qualified" || l.status === "proposal").length.toString(), change: "+8%", color: "text-yellow-400" },
    { icon: DollarSign, label: isAr ? "قيمة Pipeline" : "Pipeline Value", value: formatSAR(leads.filter((l) => l.status !== "lost").reduce((s, l) => s + l.value, 0)), change: "+23%", color: "text-emerald-400" },
    { icon: TrendingUp, label: isAr ? "معدل الإغلاق" : "Close Rate", value: `${Math.round((leads.filter((l) => l.status === "won").length / leads.length) * 100)}%`, change: "+5%", color: "text-gold-400" },
  ];

  return (
    <div className="space-y-6" dir={isAr ? "rtl" : "ltr"}>
      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map((kpi, i) => (
          <motion.div
            key={kpi.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.08 }}
          >
            <Card className="p-4 hover:shadow-lg transition-shadow">
              <div className="flex items-center justify-between mb-3">
                <div className={cn("p-2 rounded-xl bg-muted/50", kpi.color)}>
                  <kpi.icon className="w-4 h-4" />
                </div>
                <span className="text-xs font-medium text-emerald-400 flex items-center gap-0.5">
                  <ArrowUpRight className="w-3 h-3" />{kpi.change}
                </span>
              </div>
              <p className="text-2xl font-bold">{kpi.value}</p>
              <p className="text-xs text-muted-foreground mt-0.5">{kpi.label}</p>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
          <TabsList className="w-full sm:w-auto">
            <TabsTrigger value="leads">{isAr ? "العملاء المحتملون" : "Leads"}</TabsTrigger>
            <TabsTrigger value="pipeline">{isAr ? "خط الصفقات" : "Pipeline"}</TabsTrigger>
            <TabsTrigger value="activities">{isAr ? "النشاطات" : "Activities"}</TabsTrigger>
          </TabsList>
          <div className="flex gap-2">
            <div className="relative flex-1 sm:w-64">
              <Search className="absolute start-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                placeholder={isAr ? "بحث عن عميل..." : "Search leads..."}
                className="ps-9"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <Button
              onClick={() => setShowAddModal(true)}
              className="bg-gold-500 hover:bg-gold-600 text-black font-medium"
            >
              <Plus className="w-4 h-4 me-1" />
              {isAr ? "إضافة" : "Add"}
            </Button>
          </div>
        </div>

        {/* Status Filter Pills */}
        <div className="flex flex-wrap gap-2 mb-4">
          {(["all", "new", "contacted", "qualified", "proposal", "won", "lost"] as const).map((s) => (
            <button
              key={s}
              onClick={() => setFilterStatus(s)}
              className={cn(
                "px-3 py-1 rounded-full text-xs font-medium border transition-colors",
                filterStatus === s
                  ? "bg-primary text-primary-foreground border-primary"
                  : "border-border text-muted-foreground hover:border-primary/50"
              )}
            >
              {s === "all" ? (isAr ? "الكل" : "All") : (isAr ? STATUS_CONFIG[s].label : STATUS_CONFIG[s].labelEn)}
              {s !== "all" && <span className="ms-1.5 opacity-60">{leads.filter((l) => l.status === s).length}</span>}
            </button>
          ))}
        </div>

        {/* Leads Tab */}
        <TabsContent value="leads">
          <Card>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border">
                    {[isAr ? "العميل" : "Lead", isAr ? "الحالة" : "Status", isAr ? "الأولوية" : "Priority", isAr ? "القيمة" : "Value", isAr ? "درجة AI" : "AI Score", isAr ? "الإجراء التالي" : "Next Action", ""].map((h, i) => (
                      <th key={i} className="text-start px-4 py-3 text-muted-foreground font-medium whitespace-nowrap">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  <AnimatePresence>
                    {filtered.map((lead, i) => (
                      <motion.tr
                        key={lead.id}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        transition={{ delay: i * 0.05 }}
                        className="border-b border-border/50 hover:bg-muted/30 transition-colors cursor-pointer"
                        onClick={() => setSelectedLead(lead)}
                      >
                        <td className="px-4 py-3">
                          <div>
                            <p className="font-medium">{lead.name}</p>
                            <p className="text-xs text-muted-foreground">{lead.company}</p>
                          </div>
                        </td>
                        <td className="px-4 py-3">
                          <Badge variant="outline" className={cn("text-xs", STATUS_CONFIG[lead.status].bg, STATUS_CONFIG[lead.status].color)}>
                            {isAr ? STATUS_CONFIG[lead.status].label : STATUS_CONFIG[lead.status].labelEn}
                          </Badge>
                        </td>
                        <td className="px-4 py-3">
                          <span className={cn("text-xs font-medium", PRIORITY_CONFIG[lead.priority].color)}>
                            {isAr ? PRIORITY_CONFIG[lead.priority].label : lead.priority}
                          </span>
                        </td>
                        <td className="px-4 py-3 font-medium">{formatSAR(lead.value)}</td>
                        <td className="px-4 py-3">
                          <ScoreRing score={lead.aiScore} />
                        </td>
                        <td className="px-4 py-3 text-xs text-muted-foreground max-w-[150px] truncate">{lead.nextAction}</td>
                        <td className="px-4 py-3">
                          <Button variant="ghost" size="sm" className="h-7 w-7 p-0">
                            <MoreHorizontal className="w-4 h-4" />
                          </Button>
                        </td>
                      </motion.tr>
                    ))}
                  </AnimatePresence>
                </tbody>
              </table>
              {filtered.length === 0 && (
                <div className="py-12 text-center text-muted-foreground">
                  <Users className="w-8 h-8 mx-auto mb-2 opacity-40" />
                  <p>{isAr ? "لا توجد نتائج" : "No results found"}</p>
                </div>
              )}
            </div>
          </Card>
        </TabsContent>

        {/* Pipeline Tab */}
        <TabsContent value="pipeline">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {[
              { stage: "demo", labelAr: "عرض تجريبي", color: "border-t-purple-400" },
              { stage: "proposal", labelAr: "عرض مقدَّم", color: "border-t-yellow-400" },
              { stage: "negotiation", labelAr: "تفاوض", color: "border-t-orange-400" },
              { stage: "closed_won", labelAr: "مُغلَق ✓", color: "border-t-emerald-400" },
            ].map((col) => {
              const deals = MOCK_DEALS.filter((d) => d.stage === col.stage);
              return (
                <div key={col.stage}>
                  <div className="flex items-center justify-between mb-3">
                    <h4 className="text-sm font-semibold">{isAr ? col.labelAr : col.stage.replace("_", " ")}</h4>
                    <Badge variant="secondary" className="text-xs">{deals.length}</Badge>
                  </div>
                  <div className="space-y-3">
                    {deals.map((deal) => (
                      <motion.div
                        key={deal.id}
                        whileHover={{ y: -2 }}
                        className={cn("rounded-xl border-t-2 bg-card border border-border p-4 cursor-pointer shadow-sm", col.color)}
                      >
                        <p className="font-medium text-sm mb-1">{deal.title}</p>
                        <p className="text-xs text-muted-foreground mb-3">{deal.company}</p>
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-bold text-emerald-400">{formatSAR(deal.value)}</span>
                          <span className="text-xs text-muted-foreground">{deal.probability}%</span>
                        </div>
                        <div className="mt-2 h-1 rounded-full bg-muted overflow-hidden">
                          <div className="h-full bg-emerald-400 rounded-full" style={{ width: `${deal.probability}%` }} />
                        </div>
                        <p className="text-xs text-muted-foreground mt-2 flex items-center gap-1">
                          <Clock className="w-3 h-3" />{deal.closeDate}
                        </p>
                      </motion.div>
                    ))}
                    {deals.length === 0 && (
                      <div className="rounded-xl border border-dashed border-border p-4 text-center text-xs text-muted-foreground">
                        {isAr ? "لا توجد صفقات" : "No deals"}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </TabsContent>

        {/* Activities Tab */}
        <TabsContent value="activities">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">{isAr ? "سجل النشاطات" : "Activity Log"}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  { icon: Phone, color: "text-green-400 bg-green-400/10", labelAr: "مكالمة هاتفية مع فهد الحربي", labelEn: "Phone call with Fahad Al-Harbi", time: "10:30 ص", desc: isAr ? "مناقشة العرض التجاري وجدول التنفيذ" : "Discussed proposal and implementation timeline" },
                  { icon: Mail, color: "text-blue-400 bg-blue-400/10", labelAr: "إرسال عرض تجاري لبنك الرياض", labelEn: "Sent proposal to Riyadh Bank", time: "9:15 ص", desc: isAr ? "عرض حل ZATCA المتكامل بقيمة 250,000 ر.س" : "ZATCA integrated solution proposal SAR 250,000" },
                  { icon: Calendar, color: "text-purple-400 bg-purple-400/10", labelAr: "اجتماع قادم مع STC", labelEn: "Upcoming meeting with STC", time: "غداً 2:00 م", desc: isAr ? "عرض تقديمي تقني لفريق IT" : "Technical presentation to IT team" },
                  { icon: Star, color: "text-gold-400 bg-gold-400/10", labelAr: "تم إغلاق صفقة أرامكو", labelEn: "Aramco deal closed!", time: "أمس", desc: isAr ? "قيمة الصفقة: 500,000 ر.س 🎉" : "Deal value: SAR 500,000 🎉" },
                  { icon: MessageSquare, color: "text-orange-400 bg-orange-400/10", labelAr: "رد من مجموعة MBC", labelEn: "Reply from MBC Group", time: "منذ يومين", desc: isAr ? "اهتمام بحل CRM المتكامل" : "Interest in integrated CRM solution" },
                  { icon: Activity, color: "text-emerald-400 bg-emerald-400/10", labelAr: "تقييم AI لـ 12 عميلاً محتملاً", labelEn: "AI scored 12 new leads", time: "منذ 3 أيام", desc: isAr ? "متوسط درجة AI: 72" : "Average AI score: 72" },
                ].map((act, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: isAr ? 10 : -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.07 }}
                    className="flex gap-4 p-3 rounded-xl hover:bg-muted/30 transition-colors"
                  >
                    <div className={cn("w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0", act.color)}>
                      <act.icon className="w-4 h-4" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2">
                        <p className="text-sm font-medium">{isAr ? act.labelAr : act.labelEn}</p>
                        <span className="text-xs text-muted-foreground flex-shrink-0">{act.time}</span>
                      </div>
                      <p className="text-xs text-muted-foreground mt-0.5">{act.desc}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Lead Detail Drawer */}
      <AnimatePresence>
        {selectedLead && (
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-40 bg-black/50 backdrop-blur-sm"
            onClick={() => setSelectedLead(null)}
          >
            <motion.div
              initial={{ x: isAr ? -400 : 400 }} animate={{ x: 0 }} exit={{ x: isAr ? -400 : 400 }}
              transition={{ type: "spring", damping: 25 }}
              className={cn("fixed top-0 h-full w-full max-w-md bg-card border-border shadow-2xl p-6 overflow-y-auto", isAr ? "left-0 border-e" : "right-0 border-s")}
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-lg font-bold">{selectedLead.name}</h3>
                <Button variant="ghost" size="sm" onClick={() => setSelectedLead(null)}><X className="w-4 h-4" /></Button>
              </div>
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <ScoreRing score={selectedLead.aiScore} />
                  <div>
                    <p className="font-semibold">{selectedLead.company}</p>
                    <p className="text-xs text-muted-foreground">{isAr ? "درجة AI" : "AI Score"}: {selectedLead.aiScore}/100</p>
                  </div>
                </div>
                {[
                  { label: isAr ? "البريد الإلكتروني" : "Email", value: selectedLead.email, icon: Mail },
                  { label: isAr ? "الهاتف" : "Phone", value: selectedLead.phone, icon: Phone },
                  { label: isAr ? "القيمة المتوقعة" : "Expected Value", value: formatSAR(selectedLead.value), icon: DollarSign },
                  { label: isAr ? "المصدر" : "Source", value: selectedLead.source, icon: Target },
                  { label: isAr ? "المسؤول" : "Assigned To", value: selectedLead.assignedTo, icon: Users },
                  { label: isAr ? "آخر تواصل" : "Last Contact", value: selectedLead.lastContact, icon: Clock },
                ].map(({ label, value, icon: Icon }) => (
                  <div key={label} className="flex items-center gap-3 p-3 rounded-xl bg-muted/30">
                    <Icon className="w-4 h-4 text-muted-foreground flex-shrink-0" />
                    <div>
                      <p className="text-xs text-muted-foreground">{label}</p>
                      <p className="text-sm font-medium">{value}</p>
                    </div>
                  </div>
                ))}
                <div className="p-3 rounded-xl bg-muted/30">
                  <p className="text-xs text-muted-foreground mb-1">{isAr ? "الإجراء التالي" : "Next Action"}</p>
                  <p className="text-sm font-medium text-gold-400">{selectedLead.nextAction}</p>
                </div>
                {selectedLead.notes && (
                  <div className="p-3 rounded-xl bg-muted/30">
                    <p className="text-xs text-muted-foreground mb-1">{isAr ? "ملاحظات" : "Notes"}</p>
                    <p className="text-sm">{selectedLead.notes}</p>
                  </div>
                )}
                {selectedLead.tags.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {selectedLead.tags.map((tag) => (
                      <Badge key={tag} variant="secondary" className="text-xs">{tag}</Badge>
                    ))}
                  </div>
                )}
                <div className="flex gap-2 pt-2">
                  <Button size="sm" className="flex-1 bg-emerald-600 hover:bg-emerald-700">
                    <Phone className="w-3.5 h-3.5 me-1.5" />{isAr ? "اتصال" : "Call"}
                  </Button>
                  <Button size="sm" variant="outline" className="flex-1">
                    <Mail className="w-3.5 h-3.5 me-1.5" />{isAr ? "إيميل" : "Email"}
                  </Button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Add Lead Modal */}
      <AnimatePresence>
        {showAddModal && (
          <AddLeadModal
            onClose={() => setShowAddModal(false)}
            onAdd={(l) => setLeads((prev) => [l, ...prev])}
          />
        )}
      </AnimatePresence>
    </div>
  );
}
