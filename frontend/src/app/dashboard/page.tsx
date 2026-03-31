export default function DashboardPage() {
  const stats = [
    {label: 'إجمالي الصفقات', value: '24', change: '+12%', icon: '💼', color: 'bg-blue-50 text-blue-700'},
    {label: 'العملاء المحتملون', value: '156', change: '+8%', icon: '👥', color: 'bg-green-50 text-green-700'},
    {label: 'الأرباح', value: '12,450 ر.س', change: '+23%', icon: '💰', color: 'bg-yellow-50 text-yellow-700'},
    {label: 'معدل التحويل', value: '18.5%', change: '+2.1%', icon: '📈', color: 'bg-purple-50 text-purple-700'},
  ];
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((s, i) => (
          <div key={i} className="card flex items-center gap-4">
            <div className={}>{s.icon}</div>
            <div>
              <p className="text-sm text-gray-500">{s.label}</p>
              <p className="text-xl font-bold text-gray-900">{s.value}</p>
              <p className="text-xs text-green-600">{s.change} من الشهر الماضي</p>
            </div>
          </div>
        ))}
      </div>
      <div className="grid lg:grid-cols-2 gap-6">
        <div className="card"><h3 className="font-bold text-gray-900 mb-4">قمع المبيعات</h3><div className="space-y-3">{[{s:'جديد',v:45},{s:'تواصل',v:32},{s:'مؤهل',v:20},{s:'عرض',v:15},{s:'تفاوض',v:10},{s:'مكتمل',v:8}].map((item,i)=>(<div key={i} className="flex items-center gap-3"><span className="text-sm text-gray-600 w-20">{item.s}</span><div className="flex-1 bg-gray-100 rounded-full h-3"><div className="bg-primary-600 rounded-full h-3" style={{width:}}/></div><span className="text-sm font-medium text-gray-900 w-8">{item.v}</span></div>))}</div></div>
        <div className="card"><h3 className="font-bold text-gray-900 mb-4">أحدث النشاطات</h3><div className="space-y-4">{[{t:'صفقة جديدة: خصم 30% على خدمات التصميم',time:'منذ 5 دقائق'},{t:'تحويل عميل محتمل إلى صفقة',time:'منذ ساعة'},{t:'اجتماع مجدول مع شركة النور',time:'منذ 3 ساعات'},{t:'طلب سحب عمولات 2,500 ر.س',time:'منذ 5 ساعات'}].map((a,i)=>(<div key={i} className="flex items-start gap-3 pb-4 border-b border-gray-50 last:border-0"><div className="w-2 h-2 bg-primary-600 rounded-full mt-2"/><div><p className="text-sm text-gray-700">{a.t}</p><p className="text-xs text-gray-400">{a.time}</p></div></div>))}</div></div>
      </div>
    </div>
  );
}
