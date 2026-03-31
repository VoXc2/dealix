export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-l border-gray-100 fixed right-0 top-0 bottom-0 z-40">
        <div className="p-4 border-b border-gray-100">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center"><span className="text-white font-bold text-sm">D</span></div>
            <span className="font-bold text-gray-900">Dealix</span>
          </div>
        </div>
        <nav className="p-4 space-y-1">
          {[
            {label: 'لوحة التحكم', href: '/dashboard', icon: '📊'},
            {label: 'الصفقات', href: '/dashboard/deals', icon: '💼'},
            {label: 'العملاء المحتملون', href: '/dashboard/leads', icon: '👥'},
            {label: 'التسويق بالعمولة', href: '/dashboard/affiliates', icon: '🔗'},
            {label: 'الاجتماعات', href: '/dashboard/meetings', icon: '📅'},
            {label: 'التقارير', href: '/dashboard/reports', icon: '📈'},
            {label: 'الإعدادات', href: '/dashboard/settings', icon: '⚙️'},
          ].map((item, i) => (
            <a key={i} href={item.href} className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-gray-700 hover:bg-gray-50 hover:text-primary-600 transition-colors text-sm">
              <span>{item.icon}</span>{item.label}
            </a>
          ))}
        </nav>
      </aside>
      {/* Main */}
      <main className="flex-1 mr-64">
        <header className="bg-white border-b border-gray-100 h-16 flex items-center justify-between px-6">
          <h1 className="font-semibold text-gray-900">لوحة التحكم</h1>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600">مرحباً، محمد</span>
            <div className="w-8 h-8 bg-primary-100 text-primary-700 rounded-full flex items-center justify-center text-sm font-bold">م</div>
          </div>
        </header>
        <div className="p-6">{children}</div>
      </main>
    </div>
  );
}
