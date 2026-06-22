import { useEffect, useState } from "react";
import { trpc } from "@/providers/trpc";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  BarChart3,
  Brain,
  Users,
  DollarSign,
  Activity,
  TrendingUp,
  Target,
  Mail,
  Phone,
  MessageSquare,
  Zap,
  RefreshCw,
  Plus,
} from "lucide-react";

const statusColors: Record<string, string> = {
  target: "bg-gray-200 text-gray-800",
  researched: "bg-blue-100 text-blue-800",
  contacted: "bg-yellow-100 text-yellow-800",
  replied: "bg-orange-100 text-orange-800",
  discovery_booked: "bg-purple-100 text-purple-800",
  proposal_sent: "bg-indigo-100 text-indigo-800",
  won: "bg-emerald-100 text-emerald-800",
  delivery: "bg-teal-100 text-teal-800",
  retainer: "bg-green-100 text-green-800",
  lost: "bg-red-100 text-red-800",
};

const segmentLabels: Record<string, string> = {
  marketing_agency: "Marketing Agency",
  training_company: "Training Company",
  b2b_services: "B2B Services",
  other: "Other",
};

export default function Dashboard() {
  const [seeded, setSeeded] = useState(false);
  const warRoom = trpc.warRoom.today.useQuery();
  const prospectStats = trpc.prospect.stats.useQuery();
  const dealStats = trpc.deal.stats.useQuery();
  const activityStats = trpc.activity.stats.useQuery();
  const seedMutation = trpc.warRoom.seed.useMutation();

  const seedData = async () => {
    await seedMutation.mutateAsync();
    setSeeded(true);
    warRoom.refetch();
    prospectStats.refetch();
    dealStats.refetch();
    activityStats.refetch();
  };

  useEffect(() => {
    if (warRoom.data && !warRoom.data.metrics.totalProspects && !seeded) {
      seedData();
    }
  }, [warRoom.data, seeded]);

  const metrics = warRoom.data?.metrics;
  const hotProspects = warRoom.data?.hotProspects ?? [];
  const pipeline = warRoom.data?.pipeline ?? [];
  const dealsSummary = warRoom.data?.dealsSummary ?? [];
  const recentActivities = warRoom.data?.recentActivities ?? [];

  const pipelineStages = [
    "target", "researched", "contacted", "replied",
    "discovery_booked", "proposal_sent", "won", "delivery", "retainer",
  ];

  return (
    <div className="min-h-screen bg-[#F0F9F8]" dir="rtl">
      {/* Top Bar */}
      <nav className="bg-[#0A1F1E] border-b border-[#15807A]/20 px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-[#15807A] rounded-lg flex items-center justify-center">
            <BarChart3 className="w-5 h-5 text-white" />
          </div>
          <span className="text-lg font-bold text-white">Dealix</span>
          <Badge className="bg-[#15807A]/20 text-[#15807A] border-[#15807A]/30 text-xs">War Room</Badge>
        </div>
        
        <div className="flex items-center gap-3">
          <Button
            size="sm"
            variant="outline"
            className="border-[#15807A]/30 text-[#E8F4F3] hover:bg-[#15807A]/20"
            onClick={() => window.open("/command-room", "_self")}
          >
            <BarChart3 className="w-4 h-4 ml-1" />
            Command Room
          </Button>
          <Button
            size="sm"
            variant="outline"
            className="border-[#15807A]/30 text-[#E8F4F3] hover:bg-[#15807A]/20"
            onClick={() => window.open("/brain", "_self")}
          >
            <Brain className="w-4 h-4 ml-1" />
            Brain OS
          </Button>

          <Button
            size="sm"
            variant="outline"
            className="border-[#15807A]/30 text-[#E8F4F3] hover:bg-[#15807A]/20"
            onClick={() => {
              warRoom.refetch();
              prospectStats.refetch();
              dealStats.refetch();
            }}
          >
            <RefreshCw className="w-4 h-4 ml-1" />
            تحديث
          </Button>
          <Button
            size="sm"
            className="bg-[#15807A] hover:bg-[#0F5F5A] text-white"
            onClick={seedData}
            disabled={seedMutation.isPending}
          >
            <Zap className="w-4 h-4 ml-1" />
            {seedMutation.isPending ? "جاري..." : "تعبئة البيانات"}
          </Button>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6 space-y-6">
        {/* KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card className="bg-white border-[#E8F4F3]">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-[#4A6B69]">العملاء المحتملين</p>
                  <p className="text-2xl font-bold text-[#0A1F1E]">{metrics?.totalProspects ?? 0}</p>
                </div>
                <div className="w-10 h-10 bg-[#E8F4F3] rounded-lg flex items-center justify-center">
                  <Users className="w-5 h-5 text-[#15807A]" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white border-[#E8F4F3]">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-[#4A6B69]">الصفقات</p>
                  <p className="text-2xl font-bold text-[#0A1F1E]">{metrics?.totalDeals ?? 0}</p>
                </div>
                <div className="w-10 h-10 bg-[#E8F4F3] rounded-lg flex items-center justify-center">
                  <DollarSign className="w-5 h-5 text-[#15807A]" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white border-[#E8F4F3]">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-[#4A6B69]">الأنشطة</p>
                  <p className="text-2xl font-bold text-[#0A1F1E]">{metrics?.totalActivities ?? 0}</p>
                </div>
                <div className="w-10 h-10 bg-[#E8F4F3] rounded-lg flex items-center justify-center">
                  <Activity className="w-5 h-5 text-[#15807A]" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-white border-[#E8F4F3]">
            <CardContent className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-[#4A6B69]">الإيرادات (SAR)</p>
                  <p className="text-2xl font-bold text-[#15807A]">{Number(metrics?.revenueWon ?? 0).toLocaleString()}</p>
                </div>
                <div className="w-10 h-10 bg-[#15807A]/10 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-5 h-5 text-[#15807A]" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Pipeline + Deals Summary */}
        <div className="grid lg:grid-cols-2 gap-6">
          {/* Pipeline Health */}
          <Card className="bg-white border-[#E8F4F3]">
            <CardHeader className="pb-3">
              <CardTitle className="text-[#0A1F1E] text-lg flex items-center gap-2">
                <Target className="w-5 h-5 text-[#15807A]" />
                صحة Pipeline
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {pipelineStages.map((stage) => {
                  const data = pipeline.find((p: any) => p.status === stage);
                  const count = data?.count ?? 0;
                  const value = data?.totalValue ?? 0;
                  const maxCount = Math.max(...pipeline.map((p: any) => p.count), 1);
                  const width = `${(count / maxCount) * 100}%`;
                  return (
                    <div key={stage} className="flex items-center gap-3">
                      <span className="text-xs text-[#4A6B69] w-28 shrink-0 text-right capitalize">
                        {stage.replace(/_/g, " ")}
                      </span>
                      <div className="flex-1 h-6 bg-[#F0F9F8] rounded overflow-hidden">
                        <div
                          className="h-full bg-[#15807A] rounded transition-all"
                          style={{ width: count > 0 ? width : "0%" }}
                        />
                      </div>
                      <span className="text-xs font-bold text-[#0A1F1E] w-8 text-left">{count}</span>
                      {value > 0 && (
                        <span className="text-xs text-[#4A6B69] w-16 text-left">{Number(value).toLocaleString()}</span>
                      )}
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>

          {/* Deals Summary */}
          <Card className="bg-white border-[#E8F4F3]">
            <CardHeader className="pb-3">
              <CardTitle className="text-[#0A1F1E] text-lg flex items-center gap-2">
                <DollarSign className="w-5 h-5 text-[#15807A]" />
                ملخص الصفقات
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {dealsSummary.map((d: any) => (
                  <div key={d.stage} className="flex items-center justify-between p-2 bg-[#F0F9F8] rounded-lg">
                    <div className="flex items-center gap-2">
                      <div className={`w-3 h-3 rounded-full ${
                        d.stage === "won" ? "bg-emerald-500" :
                        d.stage === "lost" ? "bg-red-400" :
                        d.stage === "proposal" ? "bg-indigo-400" :
                        "bg-[#15807A]"
                      }`} />
                      <span className="text-sm text-[#0A1F1E] capitalize">{d.stage}</span>
                    </div>
                    <div className="flex items-center gap-4">
                      <span className="text-sm font-bold text-[#0A1F1E]">{d.count}</span>
                      <span className="text-sm text-[#15807A]">{Number(d.value).toLocaleString()} SAR</span>
                    </div>
                  </div>
                ))}
                {dealsSummary.length === 0 && (
                  <p className="text-sm text-[#8CB3B0] text-center py-4">لا توجد صفقات بعد</p>
                )}
              </div>
              <div className="mt-4 pt-3 border-t border-[#E8F4F3]">
                <div className="flex justify-between text-sm">
                  <span className="text-[#4A6B69]">إجمالي القيمة:</span>
                  <span className="font-bold text-[#0A1F1E]">{Number(dealStats.data?.totalValue ?? 0).toLocaleString()} SAR</span>
                </div>
                <div className="flex justify-between text-sm mt-1">
                  <span className="text-[#4A6B69]">القيمة المرجحة:</span>
                  <span className="font-bold text-[#D4A843]">{Number(dealStats.data?.weightedValue ?? 0).toLocaleString()} SAR</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Hot Prospects */}
        <Card className="bg-white border-[#E8F4F3]">
          <CardHeader className="pb-3">
            <CardTitle className="text-[#0A1F1E] text-lg flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-[#D4A843]" />
              أهم العملاء المحتملين
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow className="border-[#E8F4F3]">
                    <TableHead className="text-right text-[#4A6B69]">الشركة</TableHead>
                    <TableHead className="text-right text-[#4A6B69]">القطاع</TableHead>
                    <TableHead className="text-right text-[#4A6B69]">القرار</TableHead>
                    <TableHead className="text-right text-[#4A6B69]">الألم</TableHead>
                    <TableHead className="text-right text-[#4A6B69]">الحالة</TableHead>
                    <TableHead className="text-right text-[#4A6B69]">الدرجة</TableHead>
                    <TableHead className="text-right text-[#4A6B69]">القيمة</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {hotProspects.map((prospect: any) => (
                    <TableRow key={prospect.id} className="border-[#E8F4F3]">
                      <TableCell className="font-medium text-[#0A1F1E]">{prospect.company}</TableCell>
                      <TableCell>{segmentLabels[prospect.segment] ?? prospect.segment}</TableCell>
                      <TableCell>{prospect.decisionMaker ?? "-"}</TableCell>
                      <TableCell className="text-sm text-[#4A6B69] max-w-[200px] truncate">{prospect.pain ?? "-"}</TableCell>
                      <TableCell>
                        <Badge className={`${statusColors[prospect.status] ?? "bg-gray-100 text-gray-800"} text-xs`}>
                          {prospect.status.replace(/_/g, " ")}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <span className={`font-bold ${prospect.score >= 8 ? "text-[#15807A]" : prospect.score >= 6 ? "text-[#D4A843]" : "text-[#4A6B69]"}`}>
                          {prospect.score}
                        </span>
                      </TableCell>
                      <TableCell className="text-[#15807A] font-medium">
                        {prospect.value ? `${Number(prospect.value).toLocaleString()} SAR` : "-"}
                      </TableCell>
                    </TableRow>
                  ))}
                  {hotProspects.length === 0 && (
                    <TableRow>
                      <TableCell colSpan={7} className="text-center text-[#8CB3B0] py-6">
                        لا يوجد عملاء محتملين بعد. اضغط "تعبئة البيانات" لإضافة بيانات تجريبية.
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>

        {/* Recent Activities */}
        <Card className="bg-white border-[#E8F4F3]">
          <CardHeader className="pb-3">
            <CardTitle className="text-[#0A1F1E] text-lg flex items-center gap-2">
              <Activity className="w-5 h-5 text-[#15807A]" />
              آخر الأنشطة
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {recentActivities.map((activity: any) => (
                <div key={activity.id} className="flex items-start gap-3 p-3 bg-[#F0F9F8] rounded-lg">
                  <div className="w-8 h-8 bg-[#15807A]/10 rounded-lg flex items-center justify-center shrink-0 mt-0.5">
                    {activity.type === "email" && <Mail className="w-4 h-4 text-[#15807A]" />}
                    {activity.type === "call" && <Phone className="w-4 h-4 text-[#15807A]" />}
                    {activity.type === "meeting" && <Users className="w-4 h-4 text-[#15807A]" />}
                    {activity.type === "followup" && <MessageSquare className="w-4 h-4 text-[#15807A]" />}
                    {!["email", "call", "meeting", "followup"].includes(activity.type) && <Activity className="w-4 h-4 text-[#15807A]" />}
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-[#0A1F1E]">{activity.subject ?? activity.type}</p>
                    <p className="text-xs text-[#4A6B69] mt-0.5 line-clamp-2">{activity.body ?? "-"}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <Badge className={`text-[10px] ${activity.status === "completed" ? "bg-emerald-100 text-emerald-700" : "bg-yellow-100 text-yellow-700"}`}>
                        {activity.status}
                      </Badge>
                      {activity.aiGenerated && (
                        <Badge className="text-[10px] bg-purple-100 text-purple-700">AI</Badge>
                      )}
                    </div>
                  </div>
                </div>
              ))}
              {recentActivities.length === 0 && (
                <p className="text-sm text-[#8CB3B0] text-center py-4">لا توجد أنشطة بعد</p>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            { label: "إضافة عميل", icon: Plus, color: "bg-[#15807A]" },
            { label: "Command Room", icon: BarChart3, color: "bg-[#2A9D8F]", href: "/command-room" },
            { label: "Brain OS", icon: Brain, color: "bg-[#264653]", href: "/brain" },
            { label: "تتبع المتابعات", icon: MessageSquare, color: "bg-[#D4A843]" },
          ].map((action) => (
            <Button
              key={action.label}
              className={`${action.color} hover:opacity-90 text-white h-14`}
              onClick={() => action.href ? window.open(action.href, "_self") : alert("Coming soon: " + action.label)}
            >
              <action.icon className="w-4 h-4 ml-2" />
              {action.label}
            </Button>
          ))}
        </div>
      </div>
    </div>
  );
}
