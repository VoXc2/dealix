import { Link } from 'react-router'
import { ArrowLeft } from 'lucide-react'
import { Button } from '@/components/ui/button'
import SiteLayout from '@/components/site/SiteLayout'
import SystemCard from '@/components/site/SystemCard'
import { SYSTEMS } from '@/data/systems'

export default function Systems() {
  return (
    <SiteLayout>
      <section className="relative pt-16 pb-12 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-teal-50" />
        <div className="relative max-w-7xl mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">خمسة أنظمة تشغيل لمشكلتك المحددة</h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto leading-relaxed">
            اختر النظام المناسب لمشكلتك الآن، أو ابدأ بتشخيص سريع ونقترح لك الأفضل. كل نظام يبدأ بـ Sprint واضح بمخرجات
            ومعايير قبول وسعر افتتاحي.
          </p>
          <div className="flex gap-3 justify-center mt-8">
            <Link to="/diagnostic">
              <Button size="lg" className="gap-2">
                ابدأ تشخيصًا سريعًا
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
            <Link to="/pricing">
              <Button size="lg" variant="outline">
                عرض الأسعار
              </Button>
            </Link>
          </div>
        </div>
      </section>

      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {SYSTEMS.map((s) => (
              <SystemCard key={s.slug} system={s} />
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-3">غير متأكد أي نظام يناسبك؟</h2>
          <p className="text-gray-600 mb-6">سبعة أسئلة قصيرة تكفي لاقتراح النظام الأنسب وأول Sprint وسعره.</p>
          <Link to="/diagnostic">
            <Button size="lg">ابدأ التشخيص</Button>
          </Link>
        </div>
      </section>
    </SiteLayout>
  )
}
