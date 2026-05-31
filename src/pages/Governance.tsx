import { trpc } from "@/providers/trpc";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ShieldCheck, ShieldAlert, CheckCircle, XCircle, FileText, Clock, Activity } from "lucide-react";
import { toast } from "sonner";

export default function Governance() {
  const utils = trpc.useUtils();
  const { data: approvals } = trpc.governance.pendingApprovals.useQuery();
  const { data: allApprovals } = trpc.governance.approvalQueue.useQuery();
  const { data: ledger } = trpc.governance.ledger.useQuery();
  const { data: stats } = trpc.governance.stats.useQuery();
  const approveMutation = trpc.governance.approve.useMutation({ onSuccess: () => { utils.governance.invalidate(); toast.success("تمت"); } });

  return (
    <div className="p-6 space-y-6 bg-gray-50 min-h-screen" dir="rtl">
      <div className="flex justify-between items-center"><div><h1 className="text-3xl font-bold text-gray-900">نظام الحوكمة</h1><p className="text-gray-500">AI drafts. Human approves. System logs.</p></div><Badge variant="outline"><ShieldCheck className="w-4 h-4" />{stats?.approvals?.pending || 0} معلق</Badge></div>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card><CardContent className="pt-6"><div className="flex justify-between"><div><div className="text-2xl font-bold">{stats?.approvals?.total || 0}</div><p className="text-sm text-gray-500">إجمالي</p></div><FileText className="w-8 h-8 text-blue-500" /></div></CardContent></Card>
        <Card><CardContent className="pt-6"><div className="flex justify-between"><div><div className="text-2xl font-bold text-amber-600">{stats?.approvals?.pending || 0}</div><p className="text-sm text-gray-500">معلق</p></div><Clock className="w-8 h-8 text-amber-500" /></div></CardContent></Card>
        <Card><CardContent className="pt-6"><div className="flex justify-between"><div><div className="text-2xl font-bold text-emerald-600">{stats?.approvals?.approved || 0}</div><p className="text-sm text-gray-500">تمت</p></div><CheckCircle className="w-8 h-8 text-emerald-500" /></div></CardContent></Card>
        <Card><CardContent className="pt-6"><div className="flex justify-between"><div><div className="text-2xl font-bold">{stats?.ledger?.total || 0}</div><p className="text-sm text-gray-500">AI Actions</p></div><Activity className="w-8 h-8 text-purple-500" /></div></CardContent></Card>
      </div>
      <Tabs defaultValue="pending"><TabsList><TabsTrigger value="pending">معلقة</TabsTrigger><TabsTrigger value="all">الكل</TabsTrigger><TabsTrigger value="ledger">Ledger</TabsTrigger></TabsList>
        <TabsContent value="pending"><Card><CardHeader><CardTitle className="flex items-center gap-2 text-amber-500"><ShieldAlert />طلبات معلقة</CardTitle></CardHeader><CardContent>{approvals?.length === 0 ? <p className="text-center py-8 text-gray-500">لا يوجد</p> : <div className="space-y-4">{approvals?.map((item: any) => <div key={item.id} className="border rounded-lg p-4"><div className="flex justify-between"><div><Badge>{item.itemType}</Badge><p className="font-medium mt-2">{item.company}</p><p className="text-sm text-gray-600">{item.draft}</p></div><div className="flex gap-2"><Button size="sm" variant="outline" onClick={() => approveMutation.mutate({ id: item.id, approvedBy: "admin", rejectionReason: "مرفوض" })}><XCircle className="w-4 h-4" />رفض</Button><Button size="sm" onClick={() => approveMutation.mutate({ id: item.id, approvedBy: "admin" })}><CheckCircle className="w-4 h-4" />موافقة</Button></div></div></div>)}</div>}</CardContent></Card></TabsContent>
        <TabsContent value="all"><Card><CardContent className="p-0"><div className="overflow-x-auto"><table className="w-full text-sm"><thead className="bg-gray-50"><tr><th className="text-right py-3 px-4">النوع</th><th className="text-right py-3 px-4">الشركة</th><th className="text-right py-3 px-4">الحالة</th></tr></thead><tbody>{allApprovals?.map((item: any) => <tr key={item.id} className="border-b"><td className="py-3 px-4"><Badge variant="outline">{item.itemType}</Badge></td><td className="py-3 px-4">{item.company}</td><td className="py-3 px-4">{item.approved ? <span className="text-emerald-600">تمت</span> : item.rejected ? <span className="text-red-600">مرفوض</span> : <span className="text-amber-600">معلق</span>}</td></tr>)}</tbody></table></div></CardContent></Card></TabsContent>
        <TabsContent value="ledger"><Card><CardContent className="p-0"><div className="overflow-x-auto max-h-96"><table className="w-full text-sm"><thead className="bg-gray-50 sticky top-0"><tr><th className="text-right py-3 px-4">الوكيل</th><th className="text-right py-3 px-4">الإجراء</th><th className="text-right py-3 px-4">المخاطرة</th></tr></thead><tbody>{ledger?.map((entry: any) => <tr key={entry.id} className="border-b"><td className="py-3 px-4 font-medium">{entry.agent}</td><td className="py-3 px-4">{entry.action}</td><td className="py-3 px-4"><Badge variant="outline">{entry.risk}</Badge></td></tr>)}</tbody></table></div></CardContent></Card></TabsContent>
      </Tabs>
    </div>
  );
}
