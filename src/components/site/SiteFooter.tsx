import { Link } from 'react-router'
import { Zap } from 'lucide-react'
import { SYSTEMS } from '@/data/systems'

export default function SiteFooter() {
  return (
    <footer className="bg-gray-900 text-gray-400 py-16">
      <div className="max-w-7xl mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-lg flex items-center justify-center">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-white">Dealix</span>
            </div>
            <p className="text-sm">أنظمة تشغيل الأعمال للشركات السعودية: المتابعة، القرار، واتساب، العروض، والإيرادات.</p>
          </div>
          <div>
            <h4 className="text-white font-medium mb-4">الأنظمة</h4>
            <ul className="space-y-2 text-sm">
              {SYSTEMS.map((s) => (
                <li key={s.slug}>
                  <Link to={`/systems/${s.slug}`} className="hover:text-white">
                    {s.nameAr}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="text-white font-medium mb-4">روابط</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/systems" className="hover:text-white">كل الأنظمة</Link></li>
              <li><Link to="/pricing" className="hover:text-white">الأسعار</Link></li>
              <li><Link to="/diagnostic" className="hover:text-white">التشخيص السريع</Link></li>
              <li><Link to="/resources" className="hover:text-white">الموارد</Link></li>
              <li><Link to="/partners" className="hover:text-white">الشركاء</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-medium mb-4">ابدأ</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/start" className="hover:text-white">ابدأ Sprint</Link></li>
              <li><Link to="/contact" className="hover:text-white">تواصل معنا</Link></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-800 mt-12 pt-8 text-center text-sm">
          <p>&copy; 2026 Dealix. جميع الحقوق محفوظة.</p>
        </div>
      </div>
    </footer>
  )
}
