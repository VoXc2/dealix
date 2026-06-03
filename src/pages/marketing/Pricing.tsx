import { Link } from 'react-router'
import { ArrowLeft, CheckCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import SiteLayout from '@/components/site/SiteLayout'
import { SYSTEMS, formatSar } from '@/data/systems'
import { systemMeta } from '@/components/site/systemMeta'

export default function Pricing() {
  // Cheapest first — lowest entry barrier leads.
  const ordered = [...SYSTEMS].sort((a, b) => a.startingPriceSar - b.startingPriceSar)

  return (
    <SiteLayout>
      <section className="relative pt-16 pb-12 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-teal-50" />
        <div className="relative max-w-3xl mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">الأسعار</h1>
          <p className="text-lg text-gray-600">ابدأ Sprint واضح، ثم وسّع حسب النتائج. كل سعر هو نقطة بداية، وليس سقفًا للمشروع.</p>
        </div>
      </section>

      <section className="py-12">
        <div className="max-w-5xl mx-auto px-4 space-y-4">
          {ordered.map((s) => {
            const meta = systemMeta(s.id)
            const Icon = meta.icon
            return (
              <Card key={s.slug} className="border shadow-sm hover:shadow-md transition-shadow">
                <CardContent className="p-6 flex flex-col md:flex-row md:items-center gap-6">
                  <div className="flex items-center gap-4 md:w-1/3">
                    <div className={`w-12 h-12 rounded-xl flex items-center justify-center shrink-0 ${meta.iconBg}`}>
                      <Icon className="w-6 h-6" />
                    </div>
                    <div>
                      <Link to={`/systems/${s.slug}`} className="font-bold text-gray-900 hover:text-emerald-700">
                        {s.nameAr}
                      </Link>
                      <p className="text-sm text-gray-500">{s.timelineAr}</p>
                    </div>
                  </div>
                  <p className="text-gray-600 text-sm md:flex-1 leading-relaxed">{s.taglineAr}</p>
                  <div className="md:w-48 md:text-left flex items-center justify-between md:block">
                    <div className={`text-2xl font-bold ${meta.accentText}`}>
                      {formatSar(s.startingPriceSar)} <span className="text-sm font-normal text-gray-500">ر.س</span>
                    </div>
                    <span className="text-xs text-gray-400">يبدأ من</span>
                  </div>
                  <Link to={`/systems/${s.slug}`} className="md:w-auto">
                    <Button variant="outline" className="w-full gap-2">
                      التفاصيل
                      <ArrowLeft className="w-4 h-4" />
                    </Button>
                  </Link>
                </CardContent>
              </Card>
            )
          })}
        </div>

        <div className="max-w-3xl mx-auto px-4 mt-10">
          <div className="bg-amber-50 border border-amber-200 rounded-xl p-5 text-sm text-amber-900 leading-relaxed">
            هذه أسعار Sprint افتتاحي. المشاريع الكاملة، الربط مع أنظمة خارجية، أو التشغيل الشهري يتم تسعيرها بعد التشخيص.
            لا نقدّم أي وعود رقمية قاطعة — نلتزم بمخرجات ومعايير قبول واضحة.
          </div>
          <ul className="mt-6 space-y-2 text-gray-600 text-sm">
            <li className="flex items-center gap-2"><CheckCircle className="w-4 h-4 text-emerald-500" /> سعر واضح يفلتر المناسب ويعطي ثقة.</li>
            <li className="flex items-center gap-2"><CheckCircle className="w-4 h-4 text-emerald-500" /> كل Sprint بمخرجات محددة ومعايير قبول.</li>
            <li className="flex items-center gap-2"><CheckCircle className="w-4 h-4 text-emerald-500" /> لا يبدأ التسليم قبل اكتمال المدخلات الأساسية.</li>
          </ul>
        </div>

        <div className="max-w-3xl mx-auto px-4 mt-10 text-center">
          <Link to="/diagnostic">
            <Button size="lg" className="gap-2">
              غير متأكد؟ ابدأ تشخيصًا سريعًا
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
        </div>
      </section>
    </SiteLayout>
  )
}
