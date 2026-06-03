import { Link } from "react-router";
import { Button } from "@/components/ui/button";
import { Zap, ArrowRight } from "lucide-react";

/**
 * Shared shell for the public marketing pages (RTL, Arabic-first).
 * Mirrors the look of the landing page so the site feels like one product.
 */
export default function MarketingLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-white" dir="rtl">
      <nav className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-lg flex items-center justify-center">
              <Zap className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">Dealix</span>
          </Link>
          <div className="hidden md:flex items-center gap-6">
            <Link to="/systems" className="text-sm text-gray-600 hover:text-gray-900">الأنظمة</Link>
            <Link to="/solutions" className="text-sm text-gray-600 hover:text-gray-900">الحلول</Link>
            <Link to="/pricing" className="text-sm text-gray-600 hover:text-gray-900">الأسعار</Link>
            <Link to="/diagnostic" className="text-sm text-gray-600 hover:text-gray-900">تشخيص سريع</Link>
          </div>
          <div className="flex gap-3">
            <Link to="/diagnostic"><Button size="sm" className="gap-2">ابدأ التشخيص<ArrowRight className="w-4 h-4" /></Button></Link>
          </div>
        </div>
      </nav>

      {children}

      <footer className="bg-gray-900 text-gray-400 py-12">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between gap-6">
            <div className="max-w-sm">
              <div className="flex items-center gap-2 mb-3">
                <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-lg flex items-center justify-center">
                  <Zap className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold text-white">Dealix</span>
              </div>
              <p className="text-sm">خمسة أنظمة تشغيل إيرادات، وحلول حسب قطاعك، وتشخيص سريع — للسعودية والخليج.</p>
            </div>
            <div className="flex gap-12 text-sm">
              <div>
                <h4 className="text-white font-medium mb-3">الأنظمة</h4>
                <ul className="space-y-2">
                  <li><Link to="/systems" className="hover:text-white">الأنظمة الخمسة</Link></li>
                  <li><Link to="/solutions" className="hover:text-white">الحلول القطاعية</Link></li>
                  <li><Link to="/pricing" className="hover:text-white">الأسعار</Link></li>
                </ul>
              </div>
              <div>
                <h4 className="text-white font-medium mb-3">ابدأ</h4>
                <ul className="space-y-2">
                  <li><Link to="/diagnostic" className="hover:text-white">تشخيص سريع</Link></li>
                  <li><Link to="/dashboard" className="hover:text-white">لوحة التحكم</Link></li>
                </ul>
              </div>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-10 pt-6 text-center text-sm">
            <p>&copy; 2026 Dealix. جميع الحقوق محفوظة.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
