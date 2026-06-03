"use client";

import { useState, useEffect } from "react";
import { useLocale } from "next-intl";
import { motion, AnimatePresence } from "framer-motion";
import {
  Users,
  BarChart3,
  Settings,
  FileText,
  Layout,
  Search,
  Plus,
  X,
  Download,
  ChevronLeft,
  ChevronRight,
  Eye,
  EyeOff,
  Shield,
  TrendingUp,
  TrendingDown,
  UserCheck,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type UserRole = "admin" | "customer" | "sales";
type UserStatus = "active" | "inactive";

interface AdminUser {
  id: string;
  nameAr: string;
  nameEn: string;
  email: string;
  role: UserRole;
  status: UserStatus;
  createdAt: string;
}

interface ContentSection {
  id: string;
  labelAr: string;
  labelEn: string;
  enabled: boolean;
}

interface ReportItem {
  id: string;
  titleAr: string;
  titleEn: string;
  lastGeneratedAr: string;
  lastGeneratedEn: string;
  fileSizeKb: number;
}

// ---------------------------------------------------------------------------
// Mock data
// ---------------------------------------------------------------------------

const MOCK_USERS: AdminUser[] = [
  {
    id: "u1",
    nameAr: "أحمد بن محمد الحربي",
    nameEn: "Ahmad Al-Harbi",
    email: "ahmad@dealix.ai",
    role: "admin",
    status: "active",
    createdAt: "2025-01-15",
  },
  {
    id: "u2",
    nameAr: "سارة عبدالله القحطاني",
    nameEn: "Sara Al-Qahtani",
    email: "sara@dealix.ai",
    role: "sales",
    status: "active",
    createdAt: "2025-02-03",
  },
  {
    id: "u3",
    nameAr: "محمد علي العسيري",
    nameEn: "Mohammed Al-Asiri",
    email: "mohammed@acmeco.sa",
    role: "customer",
    status: "active",
    createdAt: "2025-02-20",
  },
  {
    id: "u4",
    nameAr: "نورة سعد السلطان",
    nameEn: "Noura Al-Sultan",
    email: "noura@ncb.com.sa",
    role: "customer",
    status: "active",
    createdAt: "2025-03-01",
  },
  {
    id: "u5",
    nameAr: "فهد خالد الزهراني",
    nameEn: "Fahad Al-Zahrani",
    email: "fahad@aramco.com",
    role: "customer",
    status: "inactive",
    createdAt: "2025-03-14",
  },
  {
    id: "u6",
    nameAr: "خديجة عمر الغامدي",
    nameEn: "Khadijah Al-Ghamdi",
    email: "khadijah@stc.com.sa",
    role: "sales",
    status: "active",
    createdAt: "2025-03-28",
  },
  {
    id: "u7",
    nameAr: "عبدالرحمن يوسف الدوسري",
    nameEn: "Abdulrahman Al-Dosari",
    email: "ar@sabic.com",
    role: "customer",
    status: "active",
    createdAt: "2025-04-10",
  },
  {
    id: "u8",
    nameAr: "منى إبراهيم الشمري",
    nameEn: "Mona Al-Shammari",
    email: "mona@commerce.gov.sa",
    role: "customer",
    status: "inactive",
    createdAt: "2025-04-22",
  },
];

const REVENUE_DATA_AR = [
  { month: "ديسمبر", revenue: 310000 },
  { month: "يناير", revenue: 360000 },
  { month: "فبراير", revenue: 320000 },
  { month: "مارس", revenue: 410000 },
  { month: "أبريل", revenue: 390000 },
  { month: "مايو", revenue: 450000 },
];

const REVENUE_DATA_EN = [
  { month: "Dec", revenue: 310000 },
  { month: "Jan", revenue: 360000 },
  { month: "Feb", revenue: 320000 },
  { month: "Mar", revenue: 410000 },
  { month: "Apr", revenue: 390000 },
  { month: "May", revenue: 450000 },
];

const PIE_DATA_AR = [
  { name: "مؤسسي", value: 34 },
  { name: "احترافي", value: 41 },
  { name: "أساسي", value: 14 },
];

const PIE_DATA_EN = [
  { name: "Enterprise", value: 34 },
  { name: "Professional", value: 41 },
  { name: "Starter", value: 14 },
];

const PIE_COLORS = ["#001F3F", "#D4AF37", "#10B981"];

const REPORTS: ReportItem[] = [
  {
    id: "r1",
    titleAr: "تقرير الإيرادات الشهري",
    titleEn: "Monthly Revenue Report",
    lastGeneratedAr: "31 مايو 2026",
    lastGeneratedEn: "31 May 2026",
    fileSizeKb: 842,
  },
  {
    id: "r2",
    titleAr: "تقرير العملاء",
    titleEn: "Customer Report",
    lastGeneratedAr: "28 مايو 2026",
    lastGeneratedEn: "28 May 2026",
    fileSizeKb: 1240,
  },
  {
    id: "r3",
    titleAr: "تقرير الامتثال PDPL",
    titleEn: "PDPL Compliance Report",
    lastGeneratedAr: "15 مايو 2026",
    lastGeneratedEn: "15 May 2026",
    fileSizeKb: 2100,
  },
  {
    id: "r4",
    titleAr: "تقرير ZATCA",
    titleEn: "ZATCA Report",
    lastGeneratedAr: "1 مايو 2026",
    lastGeneratedEn: "1 May 2026",
    fileSizeKb: 668,
  },
  {
    id: "r5",
    titleAr: "تقرير المبيعات",
    titleEn: "Sales Report",
    lastGeneratedAr: "29 مايو 2026",
    lastGeneratedEn: "29 May 2026",
    fileSizeKb: 1530,
  },
];

const DEFAULT_CONTENT_SECTIONS: ContentSection[] = [
  { id: "hero", labelAr: "قسم الرئيسية", labelEn: "Hero Section", enabled: true },
  { id: "features", labelAr: "المميزات", labelEn: "Features", enabled: true },
  { id: "pricing", labelAr: "الأسعار", labelEn: "Pricing", enabled: true },
  { id: "testimonials", labelAr: "آراء العملاء", labelEn: "Testimonials", enabled: false },
  { id: "cta", labelAr: "الدعوة للعمل", labelEn: "Call to Action", enabled: true },
  { id: "faq", labelAr: "الأسئلة الشائعة", labelEn: "FAQ", enabled: false },
];

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

const USERS_PER_PAGE = 5;

type BadgeVariant = "default" | "secondary" | "destructive" | "outline" | "gold" | "emerald" | "red" | "blue";

const ROLE_BADGE_CONFIG: Record<
  UserRole,
  { labelAr: string; labelEn: string; variant: BadgeVariant }
> = {
  admin: { labelAr: "مدير", labelEn: "Admin", variant: "destructive" },
  customer: { labelAr: "عميل", labelEn: "Customer", variant: "blue" },
  sales: { labelAr: "مبيعات", labelEn: "Sales", variant: "emerald" },
};

// ---------------------------------------------------------------------------
// Sub-component: Loading skeleton
// ---------------------------------------------------------------------------

function SkeletonRow() {
  return (
    <div className="flex items-center gap-3 p-3 animate-pulse">
      <div className="w-8 h-8 rounded-full bg-muted flex-shrink-0" />
      <div className="flex-1 space-y-2">
        <div className="h-3 w-32 rounded bg-muted" />
        <div className="h-3 w-48 rounded bg-muted" />
      </div>
      <div className="h-5 w-16 rounded-full bg-muted" />
    </div>
  );
}

// ---------------------------------------------------------------------------
// Sub-component: KPI card
// ---------------------------------------------------------------------------

interface KPIStat {
  labelAr: string;
  labelEn: string;
  value: string;
  trend: "up" | "down" | "neutral";
  changeLabel: string;
  icon: React.ReactNode;
}

function StatCard({ stat, isAr, index }: { stat: KPIStat; isAr: boolean; index: number }) {
  const trendColor =
    stat.trend === "up"
      ? "text-emerald-400"
      : stat.trend === "down"
      ? "text-red-400"
      : "text-muted-foreground";

  const TrendIcon = stat.trend === "up" ? TrendingUp : stat.trend === "down" ? TrendingDown : null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35, delay: index * 0.07 }}
    >
      <Card className="hover:border-gold-500/30 transition-colors group">
        <CardContent className="p-5">
          <div className="flex items-start justify-between mb-3">
            <div className="w-9 h-9 rounded-xl bg-muted flex items-center justify-center text-gold-400">
              {stat.icon}
            </div>
            {TrendIcon && (
              <span className={cn("flex items-center gap-1 text-xs font-medium", trendColor)}>
                <TrendIcon className="w-3.5 h-3.5" />
                {stat.changeLabel}
              </span>
            )}
          </div>
          <p className="text-2xl font-bold tabular-nums">{stat.value}</p>
          <p className="text-sm text-muted-foreground mt-1">
            {isAr ? stat.labelAr : stat.labelEn}
          </p>
        </CardContent>
      </Card>
    </motion.div>
  );
}

// ---------------------------------------------------------------------------
// Tab 1: Users
// ---------------------------------------------------------------------------

function UsersTab({ isAr }: { isAr: boolean }) {
  const [loading, setLoading] = useState(true);
  const [users, setUsers] = useState<AdminUser[]>([]);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [showInviteForm, setShowInviteForm] = useState(false);
  const [inviteName, setInviteName] = useState("");
  const [inviteEmail, setInviteEmail] = useState("");
  const [inviteRole, setInviteRole] = useState<UserRole>("customer");

  useEffect(() => {
    const timer = setTimeout(() => {
      setUsers(MOCK_USERS);
      setLoading(false);
    }, 600);
    return () => clearTimeout(timer);
  }, []);

  const filtered = users.filter((u) => {
    const q = search.toLowerCase();
    return (
      u.nameAr.includes(search) ||
      u.nameEn.toLowerCase().includes(q) ||
      u.email.toLowerCase().includes(q)
    );
  });

  const totalPages = Math.ceil(filtered.length / USERS_PER_PAGE);
  const paginated = filtered.slice((page - 1) * USERS_PER_PAGE, page * USERS_PER_PAGE);

  function handleInviteSubmit() {
    if (!inviteName || !inviteEmail) return;
    const newUser: AdminUser = {
      id: `u${Date.now()}`,
      nameAr: inviteName,
      nameEn: inviteName,
      email: inviteEmail,
      role: inviteRole,
      status: "active",
      createdAt: new Date().toISOString().split("T")[0],
    };
    setUsers((prev) => [newUser, ...prev]);
    setInviteName("");
    setInviteEmail("");
    setInviteRole("customer");
    setShowInviteForm(false);
  }

  return (
    <motion.div
      key="users"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.25 }}
      className="space-y-4"
    >
      {/* Toolbar */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
        <div className="relative flex-1 w-full">
          <Search className="absolute start-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground pointer-events-none" />
          <Input
            className="ps-9"
            placeholder={isAr ? "بحث بالاسم أو البريد..." : "Search by name or email..."}
            value={search}
            onChange={(e) => { setSearch(e.target.value); setPage(1); }}
          />
        </div>
        <Button
          variant="gold"
          size="sm"
          onClick={() => setShowInviteForm((v) => !v)}
          className="shrink-0"
        >
          {showInviteForm ? <X className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
          {isAr ? "دعوة مستخدم" : "Invite User"}
        </Button>
      </div>

      {/* Inline invite form */}
      <AnimatePresence>
        {showInviteForm && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <Card className="border-gold-500/30 bg-gold-500/5">
              <CardContent className="p-4 space-y-4">
                <p className="text-sm font-semibold text-gold-400">
                  {isAr ? "دعوة مستخدم جديد" : "Invite New User"}
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div className="space-y-1.5">
                    <Label>{isAr ? "الاسم" : "Name"}</Label>
                    <Input
                      value={inviteName}
                      onChange={(e) => setInviteName(e.target.value)}
                      placeholder={isAr ? "الاسم الكامل" : "Full name"}
                    />
                  </div>
                  <div className="space-y-1.5">
                    <Label>{isAr ? "البريد الإلكتروني" : "Email"}</Label>
                    <Input
                      type="email"
                      value={inviteEmail}
                      onChange={(e) => setInviteEmail(e.target.value)}
                      placeholder="user@example.com"
                    />
                  </div>
                  <div className="space-y-1.5">
                    <Label>{isAr ? "الدور" : "Role"}</Label>
                    <Select value={inviteRole} onValueChange={(v) => setInviteRole(v as UserRole)}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="admin">{isAr ? "مدير" : "Admin"}</SelectItem>
                        <SelectItem value="customer">{isAr ? "عميل" : "Customer"}</SelectItem>
                        <SelectItem value="sales">{isAr ? "مبيعات" : "Sales"}</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                <div className="flex gap-2 justify-end">
                  <Button variant="outline" size="sm" onClick={() => setShowInviteForm(false)}>
                    {isAr ? "إلغاء" : "Cancel"}
                  </Button>
                  <Button variant="gold" size="sm" onClick={handleInviteSubmit}>
                    {isAr ? "إرسال الدعوة" : "Send Invite"}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Table */}
      <Card>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border">
                <th className="text-start px-4 py-3 font-medium text-muted-foreground">
                  {isAr ? "المستخدم" : "User"}
                </th>
                <th className="text-start px-4 py-3 font-medium text-muted-foreground hidden sm:table-cell">
                  {isAr ? "البريد" : "Email"}
                </th>
                <th className="text-start px-4 py-3 font-medium text-muted-foreground">
                  {isAr ? "الدور" : "Role"}
                </th>
                <th className="text-start px-4 py-3 font-medium text-muted-foreground">
                  {isAr ? "الحالة" : "Status"}
                </th>
                <th className="text-start px-4 py-3 font-medium text-muted-foreground hidden md:table-cell">
                  {isAr ? "تاريخ الإنشاء" : "Created"}
                </th>
              </tr>
            </thead>
            <tbody>
              {loading
                ? Array.from({ length: USERS_PER_PAGE }).map((_, i) => (
                    <tr key={i} className="border-b border-border/50 last:border-0">
                      <td colSpan={5} className="px-4">
                        <SkeletonRow />
                      </td>
                    </tr>
                  ))
                : paginated.map((user, i) => {
                    const roleConf = ROLE_BADGE_CONFIG[user.role];
                    return (
                      <motion.tr
                        key={user.id}
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: i * 0.04 }}
                        className="border-b border-border/50 last:border-0 hover:bg-muted/30 transition-colors"
                      >
                        <td className="px-4 py-3">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-navy-500/30 to-gold-500/30 flex items-center justify-center text-xs font-bold text-gold-400 shrink-0">
                              {(isAr ? user.nameAr : user.nameEn).charAt(0)}
                            </div>
                            <span className="font-medium truncate max-w-[120px]">
                              {isAr ? user.nameAr : user.nameEn}
                            </span>
                          </div>
                        </td>
                        <td className="px-4 py-3 text-muted-foreground hidden sm:table-cell">
                          {user.email}
                        </td>
                        <td className="px-4 py-3">
                          {/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
                          <Badge variant={roleConf.variant as any}>
                            {isAr ? roleConf.labelAr : roleConf.labelEn}
                          </Badge>
                        </td>
                        <td className="px-4 py-3">
                          <span
                            className={cn(
                              "inline-flex items-center gap-1.5 text-xs font-medium px-2 py-1 rounded-full",
                              user.status === "active"
                                ? "bg-emerald-400/10 text-emerald-400"
                                : "bg-muted text-muted-foreground"
                            )}
                          >
                            <span
                              className={cn(
                                "w-1.5 h-1.5 rounded-full",
                                user.status === "active" ? "bg-emerald-400" : "bg-muted-foreground"
                              )}
                            />
                            {isAr
                              ? user.status === "active"
                                ? "نشط"
                                : "غير نشط"
                              : user.status === "active"
                              ? "Active"
                              : "Inactive"}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-muted-foreground hidden md:table-cell">
                          {user.createdAt}
                        </td>
                      </motion.tr>
                    );
                  })}
              {!loading && paginated.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-4 py-8 text-center text-muted-foreground text-sm">
                    {isAr ? "لا توجد نتائج" : "No results found"}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {!loading && totalPages > 1 && (
          <div className="flex items-center justify-between px-4 py-3 border-t border-border">
            <p className="text-xs text-muted-foreground">
              {isAr
                ? `${filtered.length} مستخدم — صفحة ${page} من ${totalPages}`
                : `${filtered.length} users — Page ${page} of ${totalPages}`}
            </p>
            <div className="flex items-center gap-1">
              <Button
                variant="ghost"
                size="icon"
                disabled={page === 1}
                onClick={() => setPage((p) => Math.max(1, p - 1))}
              >
                <ChevronLeft className="w-4 h-4" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                disabled={page === totalPages}
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              >
                <ChevronRight className="w-4 h-4" />
              </Button>
            </div>
          </div>
        )}
      </Card>
    </motion.div>
  );
}

// ---------------------------------------------------------------------------
// Tab 2: Statistics
// ---------------------------------------------------------------------------

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function CustomBarTooltip({ active, payload, label }: any) {
  if (!active || !payload?.length) return null;
  return (
    <div className="bg-card border border-border rounded-xl p-3 shadow-xl text-sm">
      <p className="font-semibold mb-1">{label}</p>
      <p className="text-gold-400">{Number(payload[0].value).toLocaleString()} SAR</p>
    </div>
  );
}

function StatisticsTab({ isAr }: { isAr: boolean }) {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 700);
    return () => clearTimeout(timer);
  }, []);

  const kpiStats: KPIStat[] = [
    {
      labelAr: "إجمالي المستخدمين",
      labelEn: "Total Users",
      value: "247",
      trend: "up",
      changeLabel: "+12%",
      icon: <Users className="w-5 h-5" />,
    },
    {
      labelAr: "الاشتراكات النشطة",
      labelEn: "Active Subscriptions",
      value: "89",
      trend: "up",
      changeLabel: "+8%",
      icon: <UserCheck className="w-5 h-5" />,
    },
    {
      labelAr: "الإيرادات الشهرية",
      labelEn: "Monthly Revenue",
      value: "450,000 SAR",
      trend: "up",
      changeLabel: "+15%",
      icon: <BarChart3 className="w-5 h-5" />,
    },
    {
      labelAr: "معدل التراجع",
      labelEn: "Churn Rate",
      value: "2.3%",
      trend: "down",
      changeLabel: "-0.4%",
      icon: <TrendingDown className="w-5 h-5" />,
    },
  ];

  const revenueData = isAr ? REVENUE_DATA_AR : REVENUE_DATA_EN;
  const pieData = isAr ? PIE_DATA_AR : PIE_DATA_EN;

  if (loading) {
    return (
      <div className="space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="h-28 rounded-2xl bg-muted animate-pulse" />
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <div className="col-span-2 h-72 rounded-2xl bg-muted animate-pulse" />
          <div className="h-72 rounded-2xl bg-muted animate-pulse" />
        </div>
      </div>
    );
  }

  return (
    <motion.div
      key="stats"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.25 }}
      className="space-y-6"
    >
      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpiStats.map((stat, i) => (
          <StatCard key={stat.labelEn} stat={stat} isAr={isAr} index={i} />
        ))}
      </div>

      {/* Charts row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Bar chart */}
        <Card className="col-span-2">
          <CardHeader>
            <CardTitle className="text-base font-semibold">
              {isAr ? "الإيرادات الشهرية — آخر 6 أشهر" : "Monthly Revenue — Last 6 Months"}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={revenueData} margin={{ top: 5, right: 16, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" vertical={false} />
                <XAxis
                  dataKey="month"
                  tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis
                  tick={{ fontSize: 11, fill: "hsl(var(--muted-foreground))" }}
                  axisLine={false}
                  tickLine={false}
                  tickFormatter={(v: number) => `${(v / 1000).toFixed(0)}k`}
                  width={40}
                />
                <Tooltip content={<CustomBarTooltip />} />
                <Bar
                  dataKey="revenue"
                  name={isAr ? "الإيرادات" : "Revenue"}
                  fill="#D4AF37"
                  radius={[6, 6, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Pie chart */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base font-semibold">
              {isAr ? "توزيع الاشتراكات" : "Subscription Breakdown"}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={260}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="45%"
                  innerRadius={60}
                  outerRadius={90}
                  paddingAngle={3}
                  dataKey="value"
                >
                  {pieData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                  ))}
                </Pie>
                <Legend
                  wrapperStyle={{ fontSize: 12, color: "hsl(var(--muted-foreground))" }}
                  iconType="circle"
                />
                <Tooltip formatter={(value: number) => [`${value}`, isAr ? "مشترك" : "Subscribers"]} />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </motion.div>
  );
}

// ---------------------------------------------------------------------------
// Tab 3: Settings
// ---------------------------------------------------------------------------

function SettingsTab({ isAr }: { isAr: boolean }) {
  const [platformName, setPlatformName] = useState("Dealix");
  const [defaultLang, setDefaultLang] = useState("ar");
  const [timezone, setTimezone] = useState("Asia/Riyadh");
  const [maintenanceMode, setMaintenanceMode] = useState(false);
  const [apiKeyMasked, setApiKeyMasked] = useState(true);
  const [apiKey, setApiKey] = useState("sk-••••••••••••••••••••••••••••••");
  const [maxTokens, setMaxTokens] = useState("4096");
  const [temperature, setTemperature] = useState(0.7);
  const [saved, setSaved] = useState(false);

  function handleSave() {
    setSaved(true);
    setTimeout(() => setSaved(false), 2500);
  }

  return (
    <motion.div
      key="settings"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.25 }}
      className="space-y-5 max-w-2xl"
    >
      {/* Platform Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <Settings className="w-4 h-4 text-gold-400" />
            {isAr ? "إعدادات المنصة" : "Platform Settings"}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label>{isAr ? "اسم المنصة" : "Platform Name"}</Label>
              <Input value={platformName} onChange={(e) => setPlatformName(e.target.value)} />
            </div>
            <div className="space-y-1.5">
              <Label>{isAr ? "اللغة الافتراضية" : "Default Language"}</Label>
              <Select value={defaultLang} onValueChange={setDefaultLang}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="ar">{isAr ? "عربي" : "Arabic"}</SelectItem>
                  <SelectItem value="en">{isAr ? "إنجليزي" : "English"}</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-1.5">
              <Label>{isAr ? "المنطقة الزمنية" : "Timezone"}</Label>
              <Select value={timezone} onValueChange={setTimezone}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Asia/Riyadh">Asia/Riyadh (UTC+3)</SelectItem>
                  <SelectItem value="Asia/Dubai">Asia/Dubai (UTC+4)</SelectItem>
                  <SelectItem value="Europe/London">Europe/London (UTC+0)</SelectItem>
                  <SelectItem value="America/New_York">America/New_York (UTC-5)</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-1.5">
              <Label>{isAr ? "وضع الصيانة" : "Maintenance Mode"}</Label>
              <div
                className="flex items-center gap-3 p-2.5 rounded-xl border border-border cursor-pointer hover:bg-muted/40 transition-colors"
                onClick={() => setMaintenanceMode((v) => !v)}
              >
                <div
                  className={cn(
                    "relative w-10 h-5 rounded-full transition-colors",
                    maintenanceMode ? "bg-red-500" : "bg-muted"
                  )}
                >
                  <div
                    className={cn(
                      "absolute top-0.5 w-4 h-4 rounded-full bg-white shadow transition-transform",
                      maintenanceMode ? "translate-x-5" : "translate-x-0.5"
                    )}
                  />
                </div>
                <span className="text-sm text-muted-foreground">
                  {maintenanceMode
                    ? isAr ? "مفعّل" : "Enabled"
                    : isAr ? "معطّل" : "Disabled"}
                </span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* AI Settings */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <Shield className="w-4 h-4 text-emerald-400" />
            {isAr ? "إعدادات الذكاء الاصطناعي" : "AI Settings"}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-1.5">
            <Label>{isAr ? "مفتاح OpenAI API" : "OpenAI API Key"}</Label>
            <div className="relative">
              <Input
                type={apiKeyMasked ? "password" : "text"}
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                className="pe-10 font-mono text-xs"
              />
              <button
                type="button"
                className="absolute end-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                onClick={() => setApiKeyMasked((v) => !v)}
              >
                {apiKeyMasked ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
              </button>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <Label>{isAr ? "الحد الأقصى للرموز" : "Max Tokens"}</Label>
              <Input
                type="number"
                value={maxTokens}
                onChange={(e) => setMaxTokens(e.target.value)}
                min={256}
                max={16384}
              />
            </div>
            <div className="space-y-1.5">
              <Label>
                {isAr ? `درجة الحرارة: ${temperature}` : `Temperature: ${temperature}`}
              </Label>
              <input
                type="range"
                min={0}
                max={1}
                step={0.1}
                value={temperature}
                onChange={(e) => setTemperature(parseFloat(e.target.value))}
                className="w-full h-2 rounded-full accent-gold-400 cursor-pointer mt-3"
              />
              <div className="flex justify-between text-xs text-muted-foreground mt-1">
                <span>{isAr ? "دقيق" : "Precise"}</span>
                <span>{isAr ? "إبداعي" : "Creative"}</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Save */}
      <div className="flex items-center justify-end gap-3">
        {saved && (
          <motion.span
            initial={{ opacity: 0, x: 10 }}
            animate={{ opacity: 1, x: 0 }}
            className="text-sm text-emerald-400"
          >
            {isAr ? "تم الحفظ" : "Saved"}
          </motion.span>
        )}
        <Button variant="gold" onClick={handleSave}>
          {isAr ? "حفظ الإعدادات" : "Save Settings"}
        </Button>
      </div>
    </motion.div>
  );
}

// ---------------------------------------------------------------------------
// Tab 4: Reports
// ---------------------------------------------------------------------------

function ReportsTab({ isAr }: { isAr: boolean }) {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <motion.div
      key="reports"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.25 }}
      className="space-y-3"
    >
      {loading
        ? Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="h-20 rounded-2xl bg-muted animate-pulse" />
          ))
        : REPORTS.map((report, i) => (
            <motion.div
              key={report.id}
              initial={{ opacity: 0, x: isAr ? 10 : -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.06 }}
            >
              <Card className="hover:border-gold-500/30 transition-colors">
                <CardContent className="p-4 flex items-center justify-between gap-4">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-muted flex items-center justify-center shrink-0">
                      <FileText className="w-5 h-5 text-gold-400" />
                    </div>
                    <div>
                      <p className="font-medium text-sm">
                        {isAr ? report.titleAr : report.titleEn}
                      </p>
                      <p className="text-xs text-muted-foreground mt-0.5">
                        {isAr
                          ? `آخر تحديث: ${report.lastGeneratedAr}`
                          : `Last generated: ${report.lastGeneratedEn}`}
                        {" · "}
                        {report.fileSizeKb >= 1000
                          ? `${(report.fileSizeKb / 1024).toFixed(1)} MB`
                          : `${report.fileSizeKb} KB`}
                      </p>
                    </div>
                  </div>
                  <Button variant="outline" size="sm" className="shrink-0 gap-1.5">
                    <Download className="w-3.5 h-3.5" />
                    {isAr ? "تحميل PDF" : "Download PDF"}
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          ))}
    </motion.div>
  );
}

// ---------------------------------------------------------------------------
// Tab 5: Content
// ---------------------------------------------------------------------------

function ContentTab({ isAr }: { isAr: boolean }) {
  const [sections, setSections] = useState<ContentSection[]>(DEFAULT_CONTENT_SECTIONS);
  const [ctaText, setCtaText] = useState(
    isAr ? "ابدأ تحويل مبيعاتك اليوم" : "Start transforming your sales today"
  );
  const [pricingVisible, setPricingVisible] = useState(true);
  const [planVisibility, setPlanVisibility] = useState({
    starter: true,
    professional: true,
    enterprise: true,
  });

  function toggleSection(id: string) {
    setSections((prev) =>
      prev.map((s) => (s.id === id ? { ...s, enabled: !s.enabled } : s))
    );
  }

  return (
    <motion.div
      key="content"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.25 }}
      className="space-y-5 max-w-2xl"
    >
      {/* Landing page sections */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <Layout className="w-4 h-4 text-gold-400" />
            {isAr ? "أقسام الصفحة الرئيسية" : "Landing Page Sections"}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          {sections.map((section) => (
            <div
              key={section.id}
              className="flex items-center justify-between p-3 rounded-xl bg-muted/40 hover:bg-muted/60 transition-colors cursor-pointer"
              onClick={() => toggleSection(section.id)}
            >
              <span className="text-sm font-medium">
                {isAr ? section.labelAr : section.labelEn}
              </span>
              <div
                className={cn(
                  "relative w-10 h-5 rounded-full transition-colors",
                  section.enabled ? "bg-gold-500" : "bg-muted-foreground/30"
                )}
              >
                <div
                  className={cn(
                    "absolute top-0.5 w-4 h-4 rounded-full bg-white shadow transition-transform",
                    section.enabled ? "translate-x-5" : "translate-x-0.5"
                  )}
                />
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* CTA text */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">
            {isAr ? "نص الدعوة للعمل (CTA)" : "Call to Action Text"}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <textarea
            className="w-full min-h-[80px] rounded-xl border border-input bg-background px-4 py-2 text-sm resize-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring placeholder:text-muted-foreground transition-colors"
            value={ctaText}
            onChange={(e) => setCtaText(e.target.value)}
            placeholder={isAr ? "أدخل نص الدعوة للعمل..." : "Enter CTA text..."}
          />
        </CardContent>
      </Card>

      {/* Pricing visibility */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">
            {isAr ? "إظهار الأسعار" : "Pricing Visibility"}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div
            className="flex items-center justify-between p-3 rounded-xl bg-muted/40 cursor-pointer"
            onClick={() => setPricingVisible((v) => !v)}
          >
            <span className="text-sm font-medium">
              {isAr ? "عرض قسم الأسعار" : "Show Pricing Section"}
            </span>
            <div
              className={cn(
                "relative w-10 h-5 rounded-full transition-colors",
                pricingVisible ? "bg-gold-500" : "bg-muted-foreground/30"
              )}
            >
              <div
                className={cn(
                  "absolute top-0.5 w-4 h-4 rounded-full bg-white shadow transition-transform",
                  pricingVisible ? "translate-x-5" : "translate-x-0.5"
                )}
              />
            </div>
          </div>

          {pricingVisible && (
            <div className="space-y-2 ps-2">
              {(["starter", "professional", "enterprise"] as const).map((plan) => (
                <div
                  key={plan}
                  className="flex items-center justify-between p-3 rounded-xl border border-border cursor-pointer hover:bg-muted/30 transition-colors"
                  onClick={() =>
                    setPlanVisibility((prev) => ({ ...prev, [plan]: !prev[plan] }))
                  }
                >
                  <span className="text-sm text-muted-foreground capitalize">
                    {isAr
                      ? plan === "starter"
                        ? "أساسي"
                        : plan === "professional"
                        ? "احترافي"
                        : "مؤسسي"
                      : plan.charAt(0).toUpperCase() + plan.slice(1)}
                  </span>
                  <div
                    className={cn(
                      "relative w-9 h-4.5 rounded-full transition-colors",
                      planVisibility[plan] ? "bg-emerald-500" : "bg-muted-foreground/30"
                    )}
                  >
                    <div
                      className={cn(
                        "absolute top-0.5 w-3.5 h-3.5 rounded-full bg-white shadow transition-transform",
                        planVisibility[plan] ? "translate-x-4" : "translate-x-0.5"
                      )}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <div className="flex justify-end">
        <Button variant="gold">{isAr ? "حفظ المحتوى" : "Save Content"}</Button>
      </div>
    </motion.div>
  );
}

// ---------------------------------------------------------------------------
// Root component
// ---------------------------------------------------------------------------

const TAB_CONFIG = [
  { value: "users", labelAr: "المستخدمون", labelEn: "Users", icon: Users },
  { value: "statistics", labelAr: "الإحصائيات", labelEn: "Statistics", icon: BarChart3 },
  { value: "settings", labelAr: "الإعدادات", labelEn: "Settings", icon: Settings },
  { value: "reports", labelAr: "التقارير", labelEn: "Reports", icon: FileText },
  { value: "content", labelAr: "المحتوى", labelEn: "Content", icon: Layout },
];

export function AdminConsole() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [activeTab, setActiveTab] = useState("users");

  return (
    <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-5">
      {/* Tab list */}
      <TabsList className="h-auto flex flex-wrap gap-1 w-full bg-muted p-1 rounded-xl">
        {TAB_CONFIG.map((tab) => {
          const Icon = tab.icon;
          return (
            <TabsTrigger
              key={tab.value}
              value={tab.value}
              className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm"
            >
              <Icon className="w-4 h-4" />
              <span className="hidden sm:inline">
                {isAr ? tab.labelAr : tab.labelEn}
              </span>
            </TabsTrigger>
          );
        })}
      </TabsList>

      {/* Tab content panels */}
      <AnimatePresence mode="wait">
        <TabsContent value="users" className="mt-0">
          <UsersTab isAr={isAr} />
        </TabsContent>

        <TabsContent value="statistics" className="mt-0">
          <StatisticsTab isAr={isAr} />
        </TabsContent>

        <TabsContent value="settings" className="mt-0">
          <SettingsTab isAr={isAr} />
        </TabsContent>

        <TabsContent value="reports" className="mt-0">
          <ReportsTab isAr={isAr} />
        </TabsContent>

        <TabsContent value="content" className="mt-0">
          <ContentTab isAr={isAr} />
        </TabsContent>
      </AnimatePresence>
    </Tabs>
  );
}
