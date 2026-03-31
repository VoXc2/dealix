import os

def w(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Cleaned: {path}")

# 1. Root Layout
w('frontend/src/app/layout.tsx', '''
import './globals.css';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ar" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
''')

# 2. Main Page (Landing)
w('frontend/src/app/page.tsx', '''
export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4">
      <h1 className="text-4xl font-bold text-primary-600 mb-4">Dealix - ديليكس</h1>
      <p className="text-xl text-gray-600 mb-8">منصة إدارة الصفقات والتسويق بالعمولة الذكية</p>
      <a href="/dashboard" className="bg-blue-600 text-white px-8 py-3 rounded-lg font-medium">دخول لوحة التحكم</a>
    </div>
  );
}
''')

# 3. Dashboard Page
w('frontend/src/app/dashboard/page.tsx', '''
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
''')

# 4. Globals CSS
w('frontend/src/app/globals.css', '''
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --primary: #2563eb;
}
''')
