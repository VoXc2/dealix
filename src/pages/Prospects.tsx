import { useState } from "react";
import { trpc } from "@/providers/trpc";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Plus, Search, Filter, Trash2 } from "lucide-react";
import { toast } from "sonner";

const SEGMENTS = ["Marketing Agency", "Training", "B2B Services", "Other"] as const;

export default function Prospects() {
  const utils = trpc.useUtils();
  const { data: prospects, isLoading } = trpc.prospects.list.useQuery();
  const { data: stats } = trpc.prospects.stats.useQuery();
  const createMutation = trpc.prospects.create.useMutation({
    onSuccess: () => { utils.prospects.list.invalidate(); utils.prospects.stats.invalidate(); toast.success("تم الإضافة"); setOpen(false); },
  });
  const deleteMutation = trpc.prospects.delete.useMutation({
    onSuccess: () => { utils.prospects.list.invalidate(); utils.prospects.stats.invalidate(); toast.success("تم الحذف"); },
  });
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");
  const [filterSegment, setFilterSegment] = useState("all");
  const [form, setForm] = useState({ company: "", segment: "B2B Services" as typeof SEGMENTS[number], pain: "", score: 5 });

  const filtered = prospects?.filter(p => (p.company.toLowerCase().includes(search.toLowerCase()) || (p.pain || "").toLowerCase().includes(search.toLowerCase())) && (filterSegment === "all" || p.segment === filterSegment));

  return (
    <div className="p-6 space-y-6 bg-gray-50 min-h-screen" dir="rtl">
      <div className="flex justify-between items-center"><div><h1 className="text-3xl font-bold text-gray-900">العملاء المحتملين</h1><p className="text-gray-500 mt-1">إدارة العملاء المحتملين</p></div>
        <Dialog open={open} onOpenChange={setOpen}><DialogTrigger asChild><Button className="gap-2"><Plus className="w-4 h-4" />إضافة عميل</Button></DialogTrigger>
          <DialogContent className="max-w-lg"><DialogHeader><DialogTitle>إضافة عميل محتمل</DialogTitle></DialogHeader>
            <div className="space-y-4"><div><Label>اسم الشركة *</Label><Input value={form.company} onChange={e => setForm({...form, company: e.target.value})} /></div><div><Label>القطاع</Label><Select value={form.segment} onValueChange={(v: any) => setForm({...form, segment: v})}><SelectTrigger><SelectValue /></SelectTrigger><SelectContent>{SEGMENTS.map(s => <SelectItem key={s} value={s}>{s}</SelectItem>)}</SelectContent></Select></div><div><Label>نقطة الألم</Label><Input value={form.pain} onChange={e => setForm({...form, pain: e.target.value})} /></div><div><Label>التقييم 1-10</Label><Input type="number" min={1} max={10} value={form.score} onChange={e => setForm({...form, score: parseInt(e.target.value) || 5})} /></div><Button onClick={() => createMutation.mutate(form)} disabled={!form.company} className="w-full">إضافة</Button></div>
          </DialogContent></Dialog>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4"><Card><CardContent className="pt-6"><div className="text-2xl font-bold">{stats?.total || 0}</div><p className="text-sm text-gray-500">الإجمالي</p></CardContent></Card>{SEGMENTS.map(seg => <Card key={seg}><CardContent className="pt-6"><div className="text-2xl font-bold">{(stats?.bySegment as any)?.[seg] || 0}</div><p className="text-sm text-gray-500">{seg}</p></CardContent></Card>)}</div>
      <div className="flex gap-4"><div className="relative flex-1"><Search className="absolute right-3 top-3 w-4 h-4 text-gray-400" /><Input className="pr-10" placeholder="بحث..." value={search} onChange={e => setSearch(e.target.value)} /></div><Select value={filterSegment} onValueChange={setFilterSegment}><SelectTrigger className="w-48"><Filter className="w-4 h-4 ml-2" /><SelectValue /></SelectTrigger><SelectContent><SelectItem value="all">الكل</SelectItem>{SEGMENTS.map(s => <SelectItem key={s} value={s}>{s}</SelectItem>)}</SelectContent></Select></div>
      <Card><CardContent className="p-0"><div className="overflow-x-auto"><table className="w-full text-sm"><thead className="bg-gray-50"><tr><th className="text-right py-3 px-4">الشركة</th><th className="text-right py-3 px-4">القطاع</th><th className="text-right py-3 px-4">نقطة الألم</th><th className="text-right py-3 px-4">التقييم</th><th></th></tr></thead>
        <tbody>{isLoading ? <tr><td colSpan={5} className="text-center py-8">جاري التحميل...</td></tr> : filtered?.length === 0 ? <tr><td colSpan={5} className="text-center py-8 text-gray-500">لا توجد نتائج</td></tr> : filtered?.map(p => <tr key={p.id} className="border-b hover:bg-gray-50"><td className="py-3 px-4 font-medium">{p.company}</td><td className="py-3 px-4"><Badge variant="outline">{p.segment}</Badge></td><td className="py-3 px-4 text-gray-600">{p.pain}</td><td className="py-3 px-4 font-bold">{p.score}</td><td className="py-3 px-4"><Button variant="ghost" size="sm" onClick={() => deleteMutation.mutate({ id: p.id })}><Trash2 className="w-4 h-4 text-red-500" /></Button></td></tr>)}</tbody></table></div></CardContent></Card>
    </div>
  );
}
