import { Link } from 'react-router'
import { Zap, ArrowRight } from 'lucide-react'
import { Button } from '@/components/ui/button'

const LINKS = [
  { to: '/systems', label: 'الأنظمة' },
  { to: '/pricing', label: 'الأسعار' },
  { to: '/diagnostic', label: 'التشخيص' },
  { to: '/resources', label: 'الموارد' },
  { to: '/partners', label: 'الشركاء' },
  { to: '/contact', label: 'تواصل' },
]

export default function SiteNav() {
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
          {LINKS.map((l) => (
            <Link key={l.to} to={l.to} className="text-sm text-gray-600 hover:text-gray-900">
              {l.label}
            </Link>
          ))}
        </div>
        <div className="flex gap-3">
          <Link to="/start">
            <Button size="sm" className="gap-2">
              ابدأ
              <ArrowRight className="w-4 h-4" />
            </Button>
          </Link>
        </div>
      </div>
    </nav>
  )
}
