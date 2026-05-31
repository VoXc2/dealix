import { trpc } from "@/providers/trpc";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Users, MessageSquare, FileText, ShieldCheck, Clock, Target, CheckCircle, AlertTriangle, DollarSign, BarChart3, Activity, Zap } from "lucide-react";

export default function Dashboard() {
  const { data: warRoomData, isLoading } = trpc.warRoom.dashboard.useQuery();

  if (isLoading) {
    return <div className="flex items-center justify-center h-screen"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div></div>;
  }

  const summary = warRoomData?.summary;
  const pipeline = warRoomData?.pipeline;

  return (
    <div className="p-6 space-y-6 bg-gray-50 min-h-screen" dir="rtl">
      <div className="flex justify-between items-center">
        <div><h1 className="text-3xl font-bold text-gray-900">Dealix War Room</h1><p className="text-gray-500 mt-1">لوحة التحكم — {new Date().toLocaleDateString("ar-SA")}</p></div>
        <Badge variant="default" className="text-sm px-4 py-2 bg-emerald-600"><Activity className="w-4 h-4 ml-2" />النظام يعمل</Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="border-l-4 border-l-blue-500"><CardHeader className="pb-2"><CardTitle className="text-sm font-medium text-gray-500 flex items-center gap-2"><Users className="w-4 h-4" />العملاء المحتملين</CardTitle></CardHeader><CardContent><div className="text-3xl font-bold">{summary?.totalProspects || 0}</div></CardContent></Card>
        <Card className="border-l-4 border-l-amber-500"><CardHeader className="pb-2"><CardTitle className="text-sm font-medium text-gray-500 flex items-center gap-2"><Clock className="w-4 h-4" />المتابعات المعلقة</CardTitle></CardHeader><CardContent><div className="text-3xl font-bold">{summary?.pendingFollowups || 0}</div></CardContent></Card>
        <Card className="border-l-4 border-l-purple-500"><CardHeader className="pb-2"><CardTitle className="text-sm font-medium text-gray-500 flex items-center gap-2"><FileText className="w-4 h-4" />العروض النشطة</CardTitle></CardHeader><CardContent><div className="text-3xl font-bold">{summary?.activeProposals || 0}</div></CardContent></Card>
        <Card className="border-l-4 border-l-emerald-500"><CardHeader className="pb-2"><CardTitle className="text-sm font-medium text-gray-500 flex items-center gap-2"><DollarSign className="w-4 h-4" />الإيرادات</CardTitle></CardHeader><CardContent><div className="text-3xl font-bold">{summary?.revenueCollected?.toLocaleString() || 0} ر.س</div></CardContent></Card>
      </div>

      <Card>
        <CardHeader><CardTitle className="flex items-center gap-2"><BarChart3 className="w-5 h-5" />مسار المبيعات</CardTitle></CardHeader>
        <CardContent>
          <div className="space-y-4">
            {pipeline && Object.entries(pipeline).map(([key, value]) => {
              const max = Math.max(...Object.values(pipeline as Record<string, number>));
              const percent = max > 0 ? ((value as number) / max) * 100 : 0;
              const labels: Record<string, string> = { target: "مستهدف", researched: "تم البحث", contacted: "تم التواصل", replied: "تم الرد", discoveryBooked: "تم حجز الاجتماع", proposalSent: "تم إرسال العرض", won: "تم الفوز" };
              return <div key={key} className="space-y-1"><div className="flex justify-between text-sm"><span className="font-medium">{labels[key] || key}</span><span className="text-gray-500">{value as number}</span></div><Progress value={percent} className="h-2" /></div>;
            })}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader><CardTitle className="flex items-center gap-2"><Target className="w-5 h-5" />أفضل العملاء المحتملين</CardTitle></CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead><tr className="border-b"><th className="text-right py-3 px-4">الشركة</th><th className="text-right py-3 px-4">القطاع</th><th className="text-right py-3 px-4">الحالة</th><th className="text-right py-3 px-4">التقييم</th></tr></thead>
              <tbody>{warRoomData?.topProspects?.map((p: any) => <tr key={p.id} className="border-b hover:bg-gray-50"><td className="py-3 px-4 font-medium">{p.company}</td><td className="py-3 px-4">{p.segment}</td><td className="py-3 px-4"><Badge variant="secondary">{p.status}</Badge></td><td className="py-3 px-4"><Progress value={(p.score || 0) * 10} className="w-16 h-2 inline mr-2" /><span>{p.score}</span></td></tr>)}</tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card>
          <CardHeader><CardTitle className="flex items-center gap-2 text-amber-600"><ShieldCheck className="w-5 h-5" />الموافقات ({summary?.pendingApprovals || 0})</CardTitle></CardHeader>
          <CardContent>{warRoomData?.pendingApprovals?.length === 0 ? <p className="text-gray-500 text-center py-4">لا توجد عناصر معلقة</p> : <div className="space-y-3">{warRoomData?.pendingApprovals?.map((item: any) => <div key={item.id} className="flex items-center justify-between p-3 bg-amber-50 rounded-lg"><div><p className="font-medium">{item.company}</p><p className="text-sm text-gray-500">{item.itemType}</p></div><Badge variant={item.risk === "high" ? "destructive" : "outline"}>{item.risk}</Badge></div>)}</div>}</CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="flex items-center gap-2 text-blue-600"><MessageSquare className="w-5 h-5" />المتابعات المستحقة</CardTitle></CardHeader>
          <CardContent>{warRoomData?.pendingFollowups?.length === 0 ? <p className="text-gray-500 text-center py-4">لا توجد متابعات</p> : <div className="space-y-3">{warRoomData?.pendingFollowups?.map((fu: any) => <div key={fu.id} className="flex items-center justify-between p-3 bg-blue-50 rounded-lg"><div><p className="font-medium">{fu.company}</p><p className="text-sm text-gray-500">{fu.draftMessage?.substring(0, 50)}...</p></div><Badge variant={fu.priority === "high" ? "destructive" : "secondary"}>{fu.priority}</Badge></div>)}</div>}</CardContent>
        </Card>
      </div>

      <Card className="bg-gradient-to-r from-slate-900 to-slate-800 text-white">
        <CardHeader><CardTitle className="flex items-center gap-2 text-white"><Zap className="w-5 h-5" />إجراءات اليوم</CardTitle></CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[{t: "فتح War Room", d: true}, {t: "إضافة 10 عملاء محتملين", d: false}, {t: "تحضير 5-10 رسائل", d: false}, {t: "مراجعة الموافقات", d: false}, {t: "إرسال رسائل يدوياً", d: false}, {t: "تسجيل الردود", d: false}, {t: "متابعة 5 شركات", d: false}, {t: "تحضير Proof Event", d: false}, {t: "تحديث Scorecard", d: false}].map((a, i) => <div key={i} className={`flex items-center gap-3 p-3 rounded-lg ${a.d ? 'bg-emerald-600/20' : 'bg-white/10'}`}>{a.d ? <CheckCircle className="w-5 h-5 text-emerald-400" /> : <AlertTriangle className="w-5 h-5 text-amber-400" />}<span className={a.d ? 'line-through opacity-70' : ''}>{a.t}</span></div>)}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
