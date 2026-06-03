"use client";

import { useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Zap,
  CheckCircle2,
  Clock,
  TrendingUp,
  Users,
  ArrowRight,
  Eye,
  BarChart3,
  Building2,
  Truck,
  Heart,
  ShoppingBag,
  Cpu,
} from "lucide-react";

// ===== TYPES =====

type LeadStatus = "new" | "qualified" | "routed" | "approved" | "skipped";
type CampaignStatus = "active" | "scheduled" | "paused";
type ApprovalStatus = "pending" | "approved" | "skipped";

interface Lead {
  id: string;
  nameAr: string;
  nameEn: string;
  sector: string;
  icpScore: number;
  recommendedProduct: string;
  status: LeadStatus;
}

interface PendingApproval {
  id: string;
  leadNameAr: string;
  leadNameEn: string;
  product: string;
  price: string;
  confidence: number;
  status: ApprovalStatus;
}

interface Campaign {
  id: string;
  sectorAr: string;
  sectorEn: string;
  contentPieces: number;
  status: CampaignStatus;
  icon: React.ComponentType<{ className?: string }>;
}

interface Product {
  nameAr: string;
  nameEn: string;
  leadsIn: number;
  converted: number;
  rate: number;
}

// ===== MOCK DATA =====

const initialLeads: Lead[] = [
  {
    id: "1",
    nameAr: "شركة العقارات السعودية",
    nameEn: "Saudi Real Estate Co.",
    sector: "عقارات",
    icpScore: 92,
    recommendedProduct: "Revenue Audit",
    status: "routed",
  },
  {
    id: "2",
    nameAr: "مجموعة الرياض الطبية",
    nameEn: "Riyadh Medical Group",
    sector: "رعاية صحية",
    icpScore: 88,
    recommendedProduct: "GTM Sprint",
    status: "qualified",
  },
  {
    id: "3",
    nameAr: "شركة نجم للخدمات اللوجستية",
    nameEn: "Najm Logistics",
    sector: "لوجستيات",
    icpScore: 79,
    recommendedProduct: "Diagnostic Funnel",
    status: "new",
  },
  {
    id: "4",
    nameAr: "مؤسسة التقنية المتقدمة",
    nameEn: "Advanced Technology Est.",
    sector: "تقنية",
    icpScore: 95,
    recommendedProduct: "Revenue Autopilot",
    status: "approved",
  },
  {
    id: "5",
    nameAr: "شركة الجيل الجديد للتجزئة",
    nameEn: "New Generation Retail Co.",
    sector: "تجزئة",
    icpScore: 74,
    recommendedProduct: "Proof Pack",
    status: "routed",
  },
];

const initialApprovals: PendingApproval[] = [
  {
    id: "a1",
    leadNameAr: "شركة العقارات السعودية",
    leadNameEn: "Saudi Real Estate Co.",
    product: "Revenue Audit",
    price: "SAR 18,000",
    confidence: 91,
    status: "pending",
  },
  {
    id: "a2",
    leadNameAr: "مجموعة الرياض الطبية",
    leadNameEn: "Riyadh Medical Group",
    product: "GTM Sprint",
    price: "SAR 35,000",
    confidence: 86,
    status: "pending",
  },
  {
    id: "a3",
    leadNameAr: "مؤسسة التقنية المتقدمة",
    leadNameEn: "Advanced Technology Est.",
    product: "Revenue Autopilot",
    price: "SAR 72,000 / yr",
    confidence: 94,
    status: "pending",
  },
];

const campaigns: Campaign[] = [
  {
    id: "c1",
    sectorAr: "عقارات",
    sectorEn: "Real Estate",
    contentPieces: 12,
    status: "active",
    icon: Building2,
  },
  {
    id: "c2",
    sectorAr: "رعاية صحية",
    sectorEn: "Healthcare",
    contentPieces: 8,
    status: "active",
    icon: Heart,
  },
  {
    id: "c3",
    sectorAr: "لوجستيات",
    sectorEn: "Logistics",
    contentPieces: 6,
    status: "scheduled",
    icon: Truck,
  },
];

const products: Product[] = [
  { nameAr: "تدقيق الإيرادات", nameEn: "Revenue Audit", leadsIn: 34, converted: 18, rate: 53 },
  { nameAr: "سبرينت GTM", nameEn: "GTM Sprint", leadsIn: 27, converted: 11, rate: 41 },
  { nameAr: "قمع التشخيص", nameEn: "Diagnostic Funnel", leadsIn: 41, converted: 22, rate: 54 },
  { nameAr: "الطيار الآلي للإيرادات", nameEn: "Revenue Autopilot", leadsIn: 15, converted: 9, rate: 60 },
  { nameAr: "حزمة الإثبات", nameEn: "Proof Pack", leadsIn: 22, converted: 8, rate: 36 },
];

// ===== HELPER: STATUS BADGE =====

function LeadStatusBadge({ status }: { status: LeadStatus }) {
  const map: Record<LeadStatus, { label: string; variant: "default" | "secondary" | "outline" | "gold" | "emerald" | "blue" | "red" }> = {
    new: { label: "جديد", variant: "outline" },
    qualified: { label: "مؤهل", variant: "blue" },
    routed: { label: "تم التوجيه", variant: "gold" },
    approved: { label: "معتمد", variant: "emerald" },
    skipped: { label: "تم التخطي", variant: "secondary" },
  };
  const { label, variant } = map[status];
  return <Badge variant={variant}>{label}</Badge>;
}

function CampaignStatusBadge({ status }: { status: CampaignStatus }) {
  const map: Record<CampaignStatus, { label: string; variant: "default" | "secondary" | "outline" | "gold" | "emerald" | "blue" | "red" }> = {
    active: { label: "نشط", variant: "emerald" },
    scheduled: { label: "مجدول", variant: "gold" },
    paused: { label: "موقوف", variant: "secondary" },
  };
  const { label, variant } = map[status];
  return <Badge variant={variant}>{label}</Badge>;
}

// ===== ICP SCORE BAR =====

function IcpScoreBar({ score }: { score: number }) {
  const color =
    score >= 90
      ? "bg-emerald-500"
      : score >= 75
      ? "bg-[#D4AF37]"
      : "bg-blue-500";

  return (
    <div className="flex items-center gap-2">
      <div className="w-20 h-1.5 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full ${color}`}
          style={{ width: `${score}%` }}
        />
      </div>
      <span className="text-xs font-mono font-semibold text-[#001F3F]">{score}</span>
    </div>
  );
}

// ===== MAIN COMPONENT =====

export default function AutoDistributionDashboard() {
  const [leads] = useState<Lead[]>(initialLeads);
  const [approvals, setApprovals] = useState<PendingApproval[]>(initialApprovals);

  const totalLeads = 138;
  const pendingCount = approvals.filter((a) => a.status === "pending").length;
  const routedCount = leads.filter((l) => l.status === "routed" || l.status === "approved").length;
  const activeCampaigns = campaigns.filter((c) => c.status === "active").length;

  function handleApprove(id: string) {
    setApprovals((prev) =>
      prev.map((a) => (a.id === id ? { ...a, status: "approved" } : a))
    );
  }

  function handleSkip(id: string) {
    setApprovals((prev) =>
      prev.map((a) => (a.id === id ? { ...a, status: "skipped" } : a))
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* PAGE HEADER */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-xl bg-[#001F3F] flex items-center justify-center">
            <Cpu className="w-5 h-5 text-[#D4AF37]" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-[#001F3F] font-display leading-tight">
              محرك التوزيع الذاتي
            </h1>
            <p className="text-sm text-gray-500 font-body">Autonomous Distribution Engine</p>
          </div>
        </div>
        <p className="text-sm text-gray-600 mt-1 max-w-2xl">
          توجيه العملاء المحتملين تلقائياً إلى المنتج الأنسب بناءً على نقاط ICP وبيانات القطاع.
        </p>
      </div>

      {/* KPI CARDS */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 mb-8">
        {/* Total Leads */}
        <div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
              إجمالي العملاء المعالجين
            </span>
            <div className="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center">
              <Users className="w-4 h-4 text-blue-600" />
            </div>
          </div>
          <div className="text-3xl font-bold text-[#001F3F]">{totalLeads}</div>
          <div className="text-xs text-gray-500 mt-1">Total Leads Processed</div>
        </div>

        {/* Pending Approvals */}
        <div className="bg-white rounded-xl border border-amber-200 p-5 shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-amber-600 uppercase tracking-wide">
              موافقات معلقة
            </span>
            <div className="w-8 h-8 rounded-lg bg-amber-50 flex items-center justify-center">
              <Clock className="w-4 h-4 text-amber-600" />
            </div>
          </div>
          <div className="text-3xl font-bold text-amber-600">{pendingCount}</div>
          <div className="text-xs text-amber-500 mt-1">Pending Approvals — requires action</div>
        </div>

        {/* Products Routed */}
        <div className="bg-white rounded-xl border border-gray-200 p-5 shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">
              المنتجات الموجهة
            </span>
            <div className="w-8 h-8 rounded-lg bg-emerald-50 flex items-center justify-center">
              <TrendingUp className="w-4 h-4 text-emerald-600" />
            </div>
          </div>
          <div className="text-3xl font-bold text-emerald-600">{routedCount}</div>
          <div className="text-xs text-gray-500 mt-1">Products Routed (this view)</div>
        </div>

        {/* Active Campaigns */}
        <div className="bg-[#001F3F] rounded-xl p-5 shadow-sm">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-semibold text-[#D4AF37] uppercase tracking-wide">
              حملات نشطة
            </span>
            <div className="w-8 h-8 rounded-lg bg-white/10 flex items-center justify-center">
              <Zap className="w-4 h-4 text-[#D4AF37]" />
            </div>
          </div>
          <div className="text-3xl font-bold text-white">{activeCampaigns}</div>
          <div className="text-xs text-white/60 mt-1">Active Campaigns</div>
        </div>
      </div>

      {/* PRODUCT LADDER */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm mb-8 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 bg-[#001F3F] flex items-center gap-2">
          <BarChart3 className="w-4 h-4 text-[#D4AF37]" />
          <h2 className="font-semibold text-white text-sm">
            سلم المنتجات — Product Ladder
          </h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-100 bg-gray-50">
                <th className="px-4 py-3 text-right font-semibold text-gray-600">المنتج</th>
                <th className="px-4 py-3 text-right font-semibold text-gray-600">Product</th>
                <th className="px-4 py-3 text-center font-semibold text-gray-600">عملاء داخلون</th>
                <th className="px-4 py-3 text-center font-semibold text-gray-600">محولون</th>
                <th className="px-4 py-3 text-center font-semibold text-gray-600">معدل التحويل</th>
              </tr>
            </thead>
            <tbody>
              {products.map((p, i) => (
                <tr key={i} className="border-b border-gray-50 hover:bg-gray-50 transition-colors">
                  <td className="px-4 py-3 font-medium text-[#001F3F]">{p.nameAr}</td>
                  <td className="px-4 py-3 text-gray-500">{p.nameEn}</td>
                  <td className="px-4 py-3 text-center text-gray-700">{p.leadsIn}</td>
                  <td className="px-4 py-3 text-center text-gray-700">{p.converted}</td>
                  <td className="px-4 py-3 text-center">
                    <span
                      className={`inline-block px-2 py-0.5 rounded-full text-xs font-semibold ${
                        p.rate >= 50
                          ? "bg-emerald-100 text-emerald-700"
                          : p.rate >= 40
                          ? "bg-[#D4AF37]/15 text-[#8a6f18]"
                          : "bg-gray-100 text-gray-600"
                      }`}
                    >
                      {p.rate}%
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* DISTRIBUTION PIPELINE */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm mb-8 overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100 bg-[#001F3F] flex items-center gap-2">
          <ArrowRight className="w-4 h-4 text-[#D4AF37]" />
          <h2 className="font-semibold text-white text-sm">
            خط التوزيع — Distribution Pipeline
          </h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-100 bg-gray-50">
                <th className="px-4 py-3 text-right font-semibold text-gray-600">العميل المحتمل</th>
                <th className="px-4 py-3 text-right font-semibold text-gray-600">القطاع</th>
                <th className="px-4 py-3 text-center font-semibold text-gray-600">ICP Score</th>
                <th className="px-4 py-3 text-right font-semibold text-gray-600">المنتج المقترح</th>
                <th className="px-4 py-3 text-center font-semibold text-gray-600">الحالة</th>
                <th className="px-4 py-3 text-center font-semibold text-gray-600">Action</th>
              </tr>
            </thead>
            <tbody>
              {leads.map((lead) => (
                <tr
                  key={lead.id}
                  className="border-b border-gray-50 hover:bg-gray-50 transition-colors"
                >
                  <td className="px-4 py-3">
                    <div className="font-medium text-[#001F3F]">{lead.nameAr}</div>
                    <div className="text-xs text-gray-400">{lead.nameEn}</div>
                  </td>
                  <td className="px-4 py-3 text-gray-600">{lead.sector}</td>
                  <td className="px-4 py-3">
                    <IcpScoreBar score={lead.icpScore} />
                  </td>
                  <td className="px-4 py-3">
                    <span className="px-2 py-1 rounded-md bg-[#001F3F]/5 text-[#001F3F] text-xs font-medium border border-[#001F3F]/10">
                      {lead.recommendedProduct}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <LeadStatusBadge status={lead.status} />
                  </td>
                  <td className="px-4 py-3 text-center">
                    <Button size="sm" variant="outline" className="text-xs h-7 px-2">
                      <Eye className="w-3 h-3 mr-1" />
                      عرض
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {/* PENDING APPROVALS PANEL */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-100 bg-[#001F3F] flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-[#D4AF37]" />
            <h2 className="font-semibold text-white text-sm">
              الموافقات المعلقة — Pending Approvals
            </h2>
          </div>
          <div className="divide-y divide-gray-50">
            {approvals.map((item) => (
              <div key={item.id} className="px-5 py-4">
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <div className="font-medium text-[#001F3F] text-sm truncate">
                      {item.leadNameAr}
                    </div>
                    <div className="text-xs text-gray-400 mb-1">{item.leadNameEn}</div>
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="px-2 py-0.5 rounded bg-[#D4AF37]/10 text-[#8a6f18] text-xs font-semibold border border-[#D4AF37]/20">
                        {item.product}
                      </span>
                      <span className="text-xs text-gray-500">{item.price}</span>
                      <span
                        className={`text-xs font-semibold ${
                          item.confidence >= 90
                            ? "text-emerald-600"
                            : "text-[#D4AF37]"
                        }`}
                      >
                        {item.confidence}% confidence
                      </span>
                    </div>
                  </div>
                  <div className="flex-shrink-0">
                    {item.status === "pending" ? (
                      <div className="flex gap-2">
                        <Button
                          size="sm"
                          variant="default"
                          className="h-7 px-3 text-xs bg-[#001F3F] hover:bg-[#000a1e]"
                          onClick={() => handleApprove(item.id)}
                        >
                          موافقة
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          className="h-7 px-3 text-xs"
                          onClick={() => handleSkip(item.id)}
                        >
                          تخطي
                        </Button>
                      </div>
                    ) : (
                      <Badge
                        variant={item.status === "approved" ? "emerald" : "secondary"}
                        className="text-xs"
                      >
                        {item.status === "approved" ? "معتمد" : "تم التخطي"}
                      </Badge>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* AUTONOMOUS CAMPAIGN STATUS */}
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-100 bg-[#001F3F] flex items-center gap-2">
            <Zap className="w-4 h-4 text-[#D4AF37]" />
            <h2 className="font-semibold text-white text-sm">
              حملات القطاعات — Sector Campaigns
            </h2>
          </div>
          <div className="divide-y divide-gray-50">
            {campaigns.map((campaign) => {
              const Icon = campaign.icon;
              return (
                <div key={campaign.id} className="px-5 py-4 flex items-center gap-4">
                  <div className="w-10 h-10 rounded-xl bg-[#001F3F]/5 border border-[#001F3F]/10 flex items-center justify-center flex-shrink-0">
                    <Icon className="w-5 h-5 text-[#001F3F]" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="font-semibold text-[#001F3F] text-sm">
                      {campaign.sectorAr}
                    </div>
                    <div className="text-xs text-gray-400">{campaign.sectorEn}</div>
                    <div className="text-xs text-gray-500 mt-0.5">
                      {campaign.contentPieces} قطعة محتوى مجدولة
                      <span className="text-gray-400 mr-1">
                        · {campaign.contentPieces} content pieces scheduled
                      </span>
                    </div>
                  </div>
                  <div className="flex-shrink-0">
                    <CampaignStatusBadge status={campaign.status} />
                  </div>
                </div>
              );
            })}
          </div>
          <div className="px-5 py-4 bg-gray-50 border-t border-gray-100">
            <div className="flex items-center gap-2 text-xs text-gray-500">
              <ShoppingBag className="w-3.5 h-3.5 text-[#D4AF37]" />
              <span>
                جميع المحتويات تخضع لمراجعة الحوكمة قبل الإرسال.
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
