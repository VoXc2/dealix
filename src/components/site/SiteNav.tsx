import { Link, useLocation } from "react-router";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Zap, ArrowLeft, Menu, X } from "lucide-react";

const navLinks = [
  { to: "/systems", label: "الأنظمة" },
  { to: "/pricing", label: "الأسعار" },
  { to: "/diagnostic", label: "تشخيص سريع" },
];

export default function SiteNav() {
  const [open, setOpen] = useState(false);
  const { pathname } = useLocation();

  return (
    <nav className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-2">
          <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-lg flex items-center justify-center">
            <Zap className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-bold text-gray-900">Dealix</span>
        </Link>

        <div className="hidden md:flex items-center gap-6">
          {navLinks.map((l) => (
            <Link
              key={l.to}
              to={l.to}
              className={`text-sm transition-colors ${
                pathname.startsWith(l.to)
                  ? "text-emerald-600 font-medium"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              {l.label}
            </Link>
          ))}
        </div>

        <div className="hidden md:flex gap-3">
          <Link to="/login">
            <Button variant="outline" size="sm">
              تسجيل الدخول
            </Button>
          </Link>
          <Link to="/start">
            <Button size="sm" className="gap-2">
              ابدأ
              <ArrowLeft className="w-4 h-4" />
            </Button>
          </Link>
        </div>

        <button
          className="md:hidden p-2 text-gray-700"
          onClick={() => setOpen((v) => !v)}
          aria-label="القائمة"
        >
          {open ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>
      </div>

      {open && (
        <div className="md:hidden border-t bg-white px-4 py-4 space-y-3">
          {navLinks.map((l) => (
            <Link
              key={l.to}
              to={l.to}
              className="block text-gray-700 py-1"
              onClick={() => setOpen(false)}
            >
              {l.label}
            </Link>
          ))}
          <div className="flex gap-3 pt-2">
            <Link to="/login" className="flex-1" onClick={() => setOpen(false)}>
              <Button variant="outline" size="sm" className="w-full">
                تسجيل الدخول
              </Button>
            </Link>
            <Link to="/start" className="flex-1" onClick={() => setOpen(false)}>
              <Button size="sm" className="w-full">
                ابدأ
              </Button>
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
}
