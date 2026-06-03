import type { ReactNode } from "react";
import { Link } from "react-router";
import { Button } from "@/components/ui/button";
import { Zap, ArrowRight } from "lucide-react";

/** Shared marketing chrome (nav + footer) for the systems & pricing pages. */
export default function SystemsLayout({ children }: { children: ReactNode }) {
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
            <Link to="/systems" className="text-sm text-gray-600 hover:text-gray-900">
              الأنظمة
            </Link>
            <Link to="/pricing" className="text-sm text-gray-600 hover:text-gray-900">
              الأسعار
            </Link>
            <Link to="/" className="text-sm text-gray-600 hover:text-gray-900">
              الرئيسية
            </Link>
          </div>
          <div className="flex gap-3">
            <Link to="/login">
              <Button variant="outline" size="sm">
                تسجيل الدخول
              </Button>
            </Link>
            <Link to="/systems">
              <Button size="sm" className="gap-2">
                ابدأ
                <ArrowRight className="w-4 h-4" />
              </Button>
            </Link>
          </div>
        </div>
      </nav>

      {children}

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
              <p className="text-sm">
                أنظمة تشغيل الأعمال للشركات السعودية: نحدد أين يتعطل الإيراد أو
                التشغيل، ثم نبني نظامًا عمليًا.
              </p>
            </div>
            <div>
              <h4 className="text-white font-medium mb-4">الأنظمة الخمسة</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link to="/systems/revenue-operating-system" className="hover:text-white">
                    Revenue Operating System
                  </Link>
                </li>
                <li>
                  <Link to="/systems/executive-command-os" className="hover:text-white">
                    Executive Command OS
                  </Link>
                </li>
                <li>
                  <Link to="/systems/follow-up-recovery-os" className="hover:text-white">
                    Follow-up Recovery OS
                  </Link>
                </li>
                <li>
                  <Link to="/systems/whatsapp-client-os" className="hover:text-white">
                    WhatsApp Client OS
                  </Link>
                </li>
                <li>
                  <Link to="/systems/proposal-proof-os" className="hover:text-white">
                    Proposal & Proof OS
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-medium mb-4">روابط</h4>
              <ul className="space-y-2 text-sm">
                <li>
                  <Link to="/systems" className="hover:text-white">
                    كل الأنظمة
                  </Link>
                </li>
                <li>
                  <Link to="/pricing" className="hover:text-white">
                    الأسعار
                  </Link>
                </li>
                <li>
                  <Link to="/dashboard" className="hover:text-white">
                    لوحة التحكم
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-white font-medium mb-4">القطاعات</h4>
              <ul className="space-y-2 text-sm">
                <li>وكالات التسويق</li>
                <li>شركات التدريب</li>
                <li>عيادات وعقار</li>
                <li>B2B Services</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-12 pt-8 text-center text-sm">
            <p>&copy; 2026 Dealix. جميع الحقوق محفوظة.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
