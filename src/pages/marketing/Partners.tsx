import { Link } from 'react-router'
import { Megaphone, Database, Briefcase, GraduationCap, Globe, Handshake, CheckCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import SiteLayout from '@/components/site/SiteLayout'
import { buildMailto } from '@/lib/contact'

const PARTNER_TYPES = [
  { icon: Megaphone, title: 'وكالات التسويق', desc: 'أضيفوا طبقة متابعة وقرار فوق الحملات التي تديرونها لعملائكم.' },
  { icon: Database, title: 'مطبّقو CRM', desc: 'أنظمة تشغيل عملية تكمّل أدواتكم بدل أن تنافسها.' },
  { icon: Briefcase, title: 'المستشارون', desc: 'مخرجات جاهزة (متابعة، عروض، قرار) تسرّع توصياتكم لدى العملاء.' },
  { icon: GraduationCap, title: 'شركات التدريب', desc: 'حلول استعادة متابعة وواتساب تناسب طبيعة استفسارات التدريب.' },
  { icon: Globe, title: 'وكالات الويب', desc: 'أضيفوا أنظمة تشغيل بعد إطلاق الموقع لتحويل الزيارات إلى متابعة.' },
]

export default function Partners() {
  const mailto = buildMailto('طلب شراكة — Dealix', 'الجهة:\nنوع الشراكة:\nنبذة:')
  return (
    <SiteLayout>
      <section className="relative pt-16 pb-10 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-teal-50" />
        <div className="relative max-w-3xl mx-auto px-4 text-center">
          <div className="inline-flex items-center gap-2 text-emerald-700 bg-emerald-100 rounded-full px-4 py-1.5 text-sm mb-4">
            <Handshake className="w-4 h-4" />
            برنامج الشركاء
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900">اعملوا مع Dealix</h1>
          <p className="text-gray-600 mt-3">نكمّل عملكم بأنظمة تشغيل عملية لعملائكم: المتابعة، القرار، واتساب، العروض، والإيرادات.</p>
        </div>
      </section>

      <section className="py-12">
        <div className="max-w-5xl mx-auto px-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {PARTNER_TYPES.map((p, i) => {
            const Icon = p.icon
            return (
              <Card key={i} className="shadow-md border-0">
                <CardContent className="p-6">
                  <div className="w-11 h-11 rounded-xl bg-emerald-100 text-emerald-600 flex items-center justify-center mb-4">
                    <Icon className="w-5 h-5" />
                  </div>
                  <h3 className="font-bold text-gray-900 mb-1">{p.title}</h3>
                  <p className="text-gray-600 text-sm">{p.desc}</p>
                </CardContent>
              </Card>
            )
          })}
        </div>

        <div className="max-w-3xl mx-auto px-4 mt-12">
          <Card className="border-0 shadow-md">
            <CardContent className="p-8">
              <h2 className="text-xl font-bold text-gray-900 mb-4">لماذا الشراكة؟</h2>
              <ul className="space-y-3">
                {[
                  'مخرجات واضحة بمعايير قبول، تسهّل البيع لعملائكم.',
                  'أسعار Sprint افتتاحية تخفّض حاجز البداية.',
                  'حوكمة واضحة: كل بريد مسودة حتى الموافقة، ولا أتمتة باردة.',
                  'لا وعود قاطعة — قيمة قابلة للإثبات أسبوعيًا.',
                ].map((b, i) => (
                  <li key={i} className="flex items-start gap-3 text-gray-700">
                    <CheckCircle className="w-5 h-5 text-emerald-500 shrink-0 mt-0.5" />
                    {b}
                  </li>
                ))}
              </ul>
              <div className="flex gap-3 mt-8">
                <a href={mailto}>
                  <Button size="lg">قدّم طلب شراكة</Button>
                </a>
                <Link to="/systems">
                  <Button size="lg" variant="outline">تعرّف على الأنظمة</Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>
    </SiteLayout>
  )
}
