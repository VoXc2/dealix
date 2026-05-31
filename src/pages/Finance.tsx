import { useState } from "react";
import { trpc } from "@/providers/trpc";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { DollarSign, TrendingUp, CreditCard, Plus } from "lucide-react";
import { toast } from "sonner";

export default function Finance() {
  const utils = trpc.useUtils();
  const { data: payments } = trpc.finance.payments.useQuery();
  const { data: stats } = trpc.finance.stats.useQuery();
  const createPayment = trpc.finance.createPayment.useMutation({ onSuccess: () => { utils.finance.invalidate(); toast.success("تمت"); setOpen(false); } });
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ invoiceId: "", clientName: "", amountSar: "", status: "Pending" as const, notes: "" });
  const statusColors: Record<string, string> = { Received: "bg-emerald-100 text-emerald-800", Pending: "bg-amber-100 text-amber-800", Overdue: "bg-red-100 text-red-800", Cancelled: "bg-gray-100" };

  return (
    <div className="p-6 space-y-6 bg-gray-50 min-h-screen" dir="rtl">
      <div className="flex justify-between items-center"><div><h1 className="text-3xl font-bold text-gray-900">المالية</h1><p className="text-gray-500">تتبع الإيرادات والمدفوعات</p></div>
        <Dialog open={open} onOpenChange={setOpen}><DialogTrigger asChild><Button className="gap-2"><Plus className="w-4 h-4" />تسجيل دفعة</Button></DialogTrigger><DialogContent className="max-w-lg"><DialogHeader><DialogTitle>تسجيل دفعة</DialogTitle></DialogHeader><div className="space-y-4"><div><Label>رقم الفاتورة</Label><Input value={form.invoiceId} onChange={e => setForm({...form, invoiceId: e.target.value})} /></div><div><Label>العميل</Label><Input value={form.clientName} onChange={e => setForm({...form, clientName: e.target.value})} /></div><div><Label>المبلغ (ر.س)</Label><Input type="number" value={form.amountSar} onChange={e => setForm({...form, amountSar: e.target.value})} /></div><div><Label>الحالة</Label><Select value={form.status} onValueChange={(v: any) => setForm({...form, status: v})}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent><SelectItem value="Received">تم</SelectItem><SelectItem value="Pending">معلق</SelectItem></SelectContent></Select></div><Button onClick={() => createPayment.mutate(form)} disabled={!form.invoiceId || !form.clientName || !form.amountSar} className="w-full">حفظ</Button></div></DialogContent></Dialog>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="border-l-4 border-l-emerald-500"><CardContent className="pt-6"><div className="flex justify-between"><div><div className="text-2xl font-bold">{stats?.totalRevenue?.toLocaleString() || 0} ر.س</div><p className="text-sm text-gray-500">المقبوضات</p></div><DollarSign className="w-8 h-8 text-emerald-500" /></div></CardContent></Card>
        <Card className="border-l-4 border-l-blue-500"><CardContent className="pt-6"><div className="flex justify-between"><div><div className="text-2xl font-bold">{stats?.pendingRevenue?.toLocaleString() || 0} ر.س</div><p className="text-sm text-gray-500">معلق</p></div><TrendingUp className="w-8 h-8 text-blue-500" /></div></CardContent></Card>
        <Card className="border-l-4 border-l-purple-500"><CardContent className="pt-6"><div className="flex justify-between"><div><div className="text-2xl font-bold">{stats?.totalPayments || 0}</div><p className="text-sm text-gray-500">عدد المدفوعات</p></div><CreditCard className="w-8 h-8 text-purple-500" /></div></CardContent></Card>
      </div>
      <Card><CardHeader><CardTitle>سجل المدفوعات</CardTitle></CardHeader><CardContent className="p-0"><div className="overflow-x-auto"><table className="w-full text-sm"><thead className="bg-gray-50"><tr><th className="text-right py-3 px-4">الفاتورة</th><th className="text-right py-3 px-4">العميل</th><th className="text-right py-3 px-4">المبلغ</th><th className="text-right py-3 px-4">الحالة</th></tr></thead><tbody>{payments?.length === 0 ? <tr><td colSpan={4} className="text-center py-8 text-gray-500">لا توجد</td></tr> : payments?.map((p: any) => <tr key={p.id} className="border-b"><td className="py-3 px-4">{p.invoiceId}</td><td className="py-3 px-4">{p.clientName}</td><td className="py-3 px-4 font-bold">{Number(p.amountSar).toLocaleString()} ر.س</td><td className="py-3 px-4"><span className={`px-2 py-1 rounded-full text-xs ${statusColors[p.status] || ""}`}>{p.status}</span></td></tr>)}</tbody></table></div></CardContent></Card>
    </div>
  );
}
