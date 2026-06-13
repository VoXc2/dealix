import { BarChart3 } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="bg-[#0A1F1E] py-12 border-t border-[#15807A]/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-4 gap-8 mb-8">
          <div className="md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-[#15807A] rounded-lg flex items-center justify-center">
                <BarChart3 className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">Dealix</span>
            </div>
            <p className="text-[#8CB3B0] text-sm leading-relaxed max-w-md">
              Dealix يساعد الشركات في السعودية والخليج على كشف ضياع الإيرادات، تنظيم المتابعات، تحسين المبيعات، وبناء War Room تشغيلي مدعوم بالذكاء الاصطناعي — مع حوكمة وموافقات وسجلات تناسب بيئة الأعمال المحلية.
            </p>
          </div>

          <div>
            <h4 className="text-white font-bold mb-4">الخدمات</h4>
            <ul className="space-y-2">
              {['Revenue Intelligence Sprint', 'AI Sales Ops Retainer', 'War Room Weekly', 'AI Governance Setup'].map((item) => (
                <li key={item}>
                  <span className="text-[#8CB3B0] text-sm hover:text-[#15807A] transition-colors cursor-pointer">{item}</span>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-white font-bold mb-4">القطاعات</h4>
            <ul className="space-y-2">
              {['وكالات التسويق', 'شركات التدريب', 'B2B Services', 'الشركات الناشئة'].map((item) => (
                <li key={item}>
                  <span className="text-[#8CB3B0] text-sm hover:text-[#15807A] transition-colors cursor-pointer">{item}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="border-t border-[#15807A]/10 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-[#8CB3B0] text-sm">
            © 2026 Dealix. جميع الحقوق محفوظة.
          </div>
          <div className="flex items-center gap-6 text-[#8CB3B0] text-sm">
            <span className="hover:text-[#15807A] transition-colors cursor-pointer">سياسة الخصوصية</span>
            <span className="hover:text-[#15807A] transition-colors cursor-pointer">شروط الاستخدام</span>
            <span className="hover:text-[#15807A] transition-colors cursor-pointer">الحوكمة</span>
          </div>
          <div className="text-[#8CB3B0] text-xs">
            مُطابق لمعايير SDAIA للذكاء الاصطناعي وحماية البيانات
          </div>
        </div>
      </div>
    </footer>
  )
}
