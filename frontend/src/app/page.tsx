export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-white border-b border-gray-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">D</span>
            </div>
            <span className="text-xl font-bold text-gray-900">Dealix</span>
          </div>
          <nav className="hidden md:flex items-center gap-8 text-sm text-gray-600">
            <a href="#features" className="hover:text-primary-600">المميزات</a>
            <a href="#pricing" className="hover:text-primary-600">الأسعار</a>
            <a href="#about" className="hover:text-primary-600">عن المنصة</a>
          </nav>
          <div className="flex items-center gap-3">
            <a href="/login" className="text-sm text-gray-600 hover:text-primary-600">تسجيل الدخول</a>
            <a href="/register" className="btn-primary text-sm">ابدأ مجاناً</a>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary-600 via-primary-700 to-primary-900 text-white">
        <div className="absolute inset-0 opacity-10" style={{backgroundImage: 'url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")'}} />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 lg:py-36 relative z-10">
          <div className="max-w-3xl">
            <h1 className="text-4xl lg:text-6xl font-bold leading-tight mb-6">
              أدِر صفقاتك ووسّع أعمالك بالتسويق بالعمولة
            </h1>
            <p className="text-xl text-primary-100 mb-8 leading-relaxed">
              منصة سعودية متكاملة تساعدك على إدارة الصفقات، تتبع العملاء المحتملين، وبناء شبكة تسويق بالعمولة فعّالة
            </p>
            <div className="flex flex-wrap gap-4">
              <a href="/register" className="bg-white text-primary-700 font-bold py-3 px-8 rounded-lg hover:bg-primary-50 transition-colors text-lg">
                ابدأ مجاناً
              </a>
              <a href="#features" className="border-2 border-white/30 text-white font-medium py-3 px-8 rounded-lg hover:bg-white/10 transition-colors text-lg">
                اكتشف المزيد
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">كل ما تحتاجه في مكان واحد</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">أدوات متكاملة لإدارة الصفقات والتسويق بالعمولة مصممة خصيصاً للسوق السعودي</p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {title: 'إدارة الصفقات', desc: 'تتبع صفقاتك من البداية حتى الإغلاق مع قمع مبيعات مرئي', icon: '💼'},
              {title: 'تتبع العملاء', desc: 'إدارة العملاء المحتملين وتقييمهم تلقائياً حسب جاهزيتهم', icon: '👥'},
              {title: 'التسويق بالعمولة', desc: 'بناء وإدارة شبكة تسويق بالعمولة مع روابط تتبع فريدة', icon: '🔗'},
              {title: 'لوحة تحكم ذكية', desc: 'إحصائيات ومقاييس في الوقت الفعلي لاتخاذ قرارات أفضل', icon: '📊'},
              {title: 'إدارة الاجتماعات', desc: 'جدولة الاجتماعات وإرسال التذكيرات تلقائياً', icon: '📅'},
              {title: 'التقارير والتحليلات', desc: 'تقارير مفصلة عن الأداء والأرباح والتحويلات', icon: '📈'},
            ].map((f, i) => (
              <div key={i} className="card hover:shadow-md transition-shadow">
                <div className="text-3xl mb-4">{f.icon}</div>
                <h3 className="text-lg font-bold text-gray-900 mb-2">{f.title}</h3>
                <p className="text-gray-600 leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">أسعار تنافسية</h2>
            <p className="text-lg text-gray-600">ابدأ مجاناً وطور عند الحاجة</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {[
              {name: 'مجاني', price: '0', features: ['10 صفقات شهرياً', '50 عميل محتمل', 'تقارير أساسية', 'دعم بالبريد']},
              {name: 'احترافي', price: '299', features: ['صفقات غير محدودة', 'عملاء غير محدودين', 'تقارير متقدمة', 'التسويق بالعمولة', 'دعم أولوية', badge: 'الأكثر طلباً'},
              {name: 'المؤسسات', price: '799', features: ['كل مميزات الاحترافي', 'API كامل', 'تخصيص كامل', 'مدير حساب مخصص', 'SLA مضمون']},
            ].map((p, i) => (
              <div key={i} className={}>
                {p.badge && <span className="absolute -top-3 right-4 bg-primary-600 text-white text-xs px-3 py-1 rounded-full">{p.badge}</span>}
                <h3 className="text-lg font-bold text-gray-900">{p.name}</h3>
                <div className="mt-4 mb-6"><span className="text-4xl font-bold text-gray-900">{p.price}</span><span className="text-gray-500 mr-1">ر.س/شهرياً</span></div>
                <ul className="space-y-3 mb-8">{p.features.map((f, j) => <li key={j} className="flex items-center gap-2 text-gray-600"><span className="text-green-500">✓</span>{f}</li>)}</ul>
                <a href="/register" className={}>ابدأ الآن</a>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center"><span className="text-white font-bold text-sm">D</span></div>
            <span className="text-xl font-bold text-white">Dealix</span>
          </div>
          <p className="text-sm">© 2024 Dealix. جميع الحقوق محفوظة.</p>
        </div>
      </footer>
    </div>
  );
}
