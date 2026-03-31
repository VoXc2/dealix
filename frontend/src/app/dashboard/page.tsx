
export default function DashboardPage() {
  const stats = [
    {label: 'إجمالي الصفقات', value: '1,284', change: '+12%'},
    {label: 'المسوقين النشطين', value: '456', change: '+5%'},
    {label: 'العمولات المعلقة', value: 'SR 12,400', change: '+8%'},
    {label: 'معدل التحويل', value: '18.5%', change: '+2.1%'},
  ];

  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold mb-6">الإحصائيات العامة</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((s, i) => (
          <div key={i} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <p className="text-sm text-gray-500">{s.label}</p>
            <p className="text-2xl font-bold mt-1">{s.value}</p>
            <span className="text-green-500 text-xs font-medium">{s.change}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
