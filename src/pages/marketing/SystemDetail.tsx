import { Link, useParams } from 'react-router'
import { CheckCircle, ArrowLeft, AlertTriangle, Users, Package, ClipboardList, Target, Clock } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion'
import SiteLayout from '@/components/site/SiteLayout'
import { getSystem, SYSTEMS, formatSar } from '@/data/systems'
import { systemMeta } from '@/components/site/systemMeta'

function NotFoundSystem() {
  return (
    <SiteLayout>
      <div className="max-w-3xl mx-auto px-4 py-32 text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">النظام غير موجود</h1>
        <p className="text-gray-600 mb-8">الرابط الذي طلبته لا يطابق أيًا من أنظمتنا الخمسة.</p>
        <Link to="/systems">
          <Button>عرض كل الأنظمة</Button>
        </Link>
      </div>
    </SiteLayout>
  )
}

export default function SystemDetail() {
  const { slug } = useParams()
  const system = getSystem(slug)
  if (!system) return <NotFoundSystem />

  const meta = systemMeta(system.id)
  const Icon = meta.icon
  const others = SYSTEMS.filter((s) => s.slug !== system.slug)

  return (
    <SiteLayout>
      {/* Hero */}
      <section className="relative pt-16 pb-12 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-teal-50" />
        <div className="relative max-w-5xl mx-auto px-4">
          <div className="flex items-center gap-3 mb-5">
            <div className={`w-14 h-14 rounded-2xl flex items-center justify-center ${meta.iconBg}`}>
              <Icon className="w-7 h-7" />
            </div>
            <div>
              <Badge variant="outline" className="mb-1">يبدأ من {formatSar(system.startingPriceSar)} ر.س · {system.timelineAr}</Badge>
              <h1 className="text-3xl md:text-4xl font-bold text-gray-900">{system.nameAr}</h1>
            </div>
          </div>
          <p className="text-xl text-gray-700 leading-relaxed max-w-3xl">{system.taglineAr}</p>
          <div className="flex gap-3 mt-8">
            <Link to="/diagnostic">
              <Button size="lg" className="gap-2">
                {system.ctaAr}
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
            <Link to="/start">
              <Button size="lg" variant="outline">ابدأ هذا النظام</Button>
            </Link>
          </div>
        </div>
      </section>

      <div className="max-w-5xl mx-auto px-4 py-12 space-y-14">
        {/* Pain */}
        <section>
          <div className="flex items-center gap-2 mb-3">
            <AlertTriangle className="w-5 h-5 text-amber-500" />
            <h2 className="text-2xl font-bold text-gray-900">المشكلة</h2>
          </div>
          <p className="text-gray-700 leading-relaxed text-lg">{system.painAr}</p>
        </section>

        {/* Who it's for */}
        <section>
          <div className="flex items-center gap-2 mb-3">
            <Users className="w-5 h-5 text-emerald-600" />
            <h2 className="text-2xl font-bold text-gray-900">لمن هذا النظام؟</h2>
          </div>
          <p className="text-gray-700 leading-relaxed text-lg">{system.whoAr}</p>
        </section>

        {/* Benefits */}
        <section>
          <h2 className="text-2xl font-bold text-gray-900 mb-5">ماذا يعطيك؟</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {system.benefitsAr.map((b, i) => (
              <div key={i} className="flex items-start gap-3 p-4 bg-gray-50 rounded-xl">
                <CheckCircle className="w-5 h-5 text-emerald-500 shrink-0 mt-0.5" />
                <span className="text-gray-700">{b}</span>
              </div>
            ))}
          </div>
        </section>

        {/* First result */}
        <section>
          <Card className={`border-r-4 ${meta.accentBorder} shadow-md`}>
            <CardContent className="p-6 flex items-start gap-3">
              <Clock className={`w-6 h-6 shrink-0 ${meta.accentText}`} />
              <div>
                <h3 className="font-bold text-gray-900 mb-1">أول نتيجة خلال 5–14 يومًا</h3>
                <p className="text-gray-700">{system.firstResultAr}</p>
              </div>
            </CardContent>
          </Card>
        </section>

        {/* Delivery pack */}
        <section>
          <div className="flex items-center gap-2 mb-5">
            <Package className="w-5 h-5 text-emerald-600" />
            <h2 className="text-2xl font-bold text-gray-900">حزمة التسليم</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {system.deliveryPackAr.map((d, i) => (
              <div key={i} className="flex items-center gap-3 p-3 border rounded-lg">
                <span className={`w-7 h-7 rounded-full flex items-center justify-center text-sm font-bold ${meta.iconBg}`}>
                  {i + 1}
                </span>
                <span className="text-gray-700">{d}</span>
              </div>
            ))}
          </div>
        </section>

        {/* Required inputs + acceptance criteria */}
        <section className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <ClipboardList className="w-5 h-5 text-emerald-600" />
              <h2 className="text-xl font-bold text-gray-900">المدخلات المطلوبة</h2>
            </div>
            <ul className="space-y-2">
              {system.requiredInputsAr.map((r, i) => (
                <li key={i} className="flex items-start gap-2 text-gray-700">
                  <span className="text-emerald-500 mt-1">•</span>
                  {r}
                </li>
              ))}
            </ul>
            <p className="text-sm text-gray-500 mt-3">لا يبدأ التسليم قبل اكتمال المدخلات الأساسية.</p>
          </div>
          <div>
            <div className="flex items-center gap-2 mb-4">
              <Target className="w-5 h-5 text-emerald-600" />
              <h2 className="text-xl font-bold text-gray-900">معايير القبول</h2>
            </div>
            <ul className="space-y-2">
              {system.acceptanceCriteriaAr.map((a, i) => (
                <li key={i} className="flex items-start gap-2 text-gray-700">
                  <CheckCircle className="w-4 h-4 text-emerald-500 shrink-0 mt-1" />
                  {a}
                </li>
              ))}
            </ul>
          </div>
        </section>

        {/* Pricing */}
        <section>
          <Card className="bg-gradient-to-b from-gray-900 to-gray-800 text-white border-0">
            <CardContent className="p-8 text-center">
              <p className="text-gray-300 mb-1">السعر الافتتاحي</p>
              <div className="text-4xl font-bold mb-1">
                يبدأ من {formatSar(system.startingPriceSar)} <span className="text-lg font-normal">ر.س</span>
              </div>
              <p className="text-gray-400 text-sm mb-6">مدة Sprint افتتاحي: {system.timelineAr}</p>
              <p className="text-gray-300 text-sm max-w-xl mx-auto mb-6">
                هذه أسعار Sprint افتتاحي. المشاريع الكاملة، الربط مع أنظمة خارجية، أو التشغيل الشهري تُسعّر بعد التشخيص.
              </p>
              <Link to="/start">
                <Button size="lg" className="bg-emerald-500 hover:bg-emerald-600">{system.ctaAr}</Button>
              </Link>
            </CardContent>
          </Card>
        </section>

        {/* FAQ */}
        <section>
          <h2 className="text-2xl font-bold text-gray-900 mb-5">أسئلة شائعة</h2>
          <Accordion type="single" collapsible className="w-full">
            {system.faqAr.map((f, i) => (
              <AccordionItem key={i} value={`item-${i}`}>
                <AccordionTrigger className="text-right">{f.q}</AccordionTrigger>
                <AccordionContent className="text-gray-700 leading-relaxed">{f.a}</AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </section>

        {/* Final CTA */}
        <section className="text-center bg-emerald-50 rounded-2xl py-12 px-4">
          <h2 className="text-2xl font-bold text-gray-900 mb-3">جاهز تبدأ بـ {system.nameAr}؟</h2>
          <p className="text-gray-600 mb-6">ابدأ بتشخيص قصير، ثم Sprint واضح المخرجات والسعر.</p>
          <div className="flex gap-3 justify-center">
            <Link to="/diagnostic"><Button size="lg">ابدأ تشخيصًا سريعًا</Button></Link>
            <Link to="/contact"><Button size="lg" variant="outline">تواصل معنا</Button></Link>
          </div>
        </section>

        {/* Other systems */}
        <section>
          <h2 className="text-xl font-bold text-gray-900 mb-5">أنظمة أخرى</h2>
          <div className="flex flex-wrap gap-3">
            {others.map((s) => (
              <Link
                key={s.slug}
                to={`/systems/${s.slug}`}
                className="px-4 py-2 border rounded-full text-sm text-gray-700 hover:border-emerald-400 hover:text-emerald-700 transition-colors"
              >
                {s.nameAr}
              </Link>
            ))}
          </div>
        </section>
      </div>
    </SiteLayout>
  )
}
