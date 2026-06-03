import { Link } from "react-router";
import { Zap } from "lucide-react";
import { systems } from "@/data/systems";

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
            <p className="text-sm leading-relaxed">
              نبني نظام التشغيل المناسب لأكبر تعطل في شركتك الآن: الإيرادات،
              القرار التنفيذي، المتابعة، واتساب، أو العروض والإثبات.
            </p>
          </div>

          <div>
            <h4 className="text-white font-medium mb-4">الأنظمة الخمسة</h4>
            <ul className="space-y-2 text-sm">
              {systems.map((s) => (
                <li key={s.slug}>
                  <Link
                    to={`/systems/${s.slug}`}
                    className="hover:text-white transition-colors"
                  >
                    {s.nameAr}
                  </Link>
                </li>
              ))}
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
                <Link to="/diagnostic" className="hover:text-white">
                  تشخيص سريع
                </Link>
              </li>
              <li>
                <Link to="/start" className="hover:text-white">
                  ابدأ الآن
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-white font-medium mb-4">النظام</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/dashboard" className="hover:text-white">
                  لوحة التحكم
                </Link>
              </li>
              <li>
                <Link to="/prospects" className="hover:text-white">
                  العملاء
                </Link>
              </li>
              <li>
                <Link to="/governance" className="hover:text-white">
                  الحوكمة
                </Link>
              </li>
              <li>
                <Link to="/finance" className="hover:text-white">
                  المالية
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-12 pt-8 flex flex-col md:flex-row md:items-center md:justify-between gap-4 text-center md:text-right text-sm">
          <p>&copy; 2026 Dealix. جميع الحقوق محفوظة.</p>
          <p className="text-gray-500">
            الأسعار المعروضة أسعار بداية تنفيذية، والنطاق النهائي يُحدد بعد
            التشخيص.
          </p>
        </div>
      </div>
    </footer>
  );
}
