import { Link } from 'react-router'
import {
  ArrowLeft,
  Sparkles,
  Shield,
  Lock,
  Search,
  Boxes,
  Rocket,
  LineChart,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'
import SiteLayout from '@/components/site/SiteLayout'
import SystemCard from '@/components/site/SystemCard'
import { SYSTEMS, formatSar } from '@/data/systems'

const STEPS = [
  { icon: Search, title: 'تشخيص', desc: 'سبعة أسئلة تحدد أين التعطل والنظام الأنسب.' },
  { icon: Boxes, title: 'نظام', desc: 'نختار واحدًا من خمسة أنظمة تشغيل واضحة.' },
  { icon: Rocket, title: 'Sprint', desc: 'أول مخرج عملي خلال 5–14 يومًا بسعر افتتاحي.' },
  { icon: LineChart, title: 'تقرير قيمة', desc: 'إثبات أسبوعي لما تم تسليمه، بلا وعود قاطعة.' },
]

const LEVELS = [
  { l: 'Level 1: Observe', a: true },
  { l: 'Level 2: Advise', a: true },
  { l: 'Level 3: Draft', a: true },
  { l: 'Level 4: Act with Approval', a: false },
  { l: 'Level 5: Autonomous', a: false },
]

export default function LandingPage() {
  return (
    <SiteLayout>
      {/* Hero */}
      <section className="relative pt-20 pb-28 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-teal-50" />
        <div className="relative max-w-7xl mx-auto px-4 text-center">
          <Badge className="mb-6 px-4 py-2 bg-emerald-100 text-emerald-800 hover:bg-emerald-100">
            <Sparkles className="w-4 h-4 ml-2" />
            أنظمة تشغيل الأعمال للشركات السعودية
          </Badge>
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            نحدد أين يتعطل
            <br />
            <span className="bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
              الإيراد أو التشغيل
            </span>
          </h1>
          <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto leading-relaxed">
            ثم نبني لك نظامًا عمليًا للمتابعة، القرار، واتساب، العروض، أو الإيرادات. اختر النظام المناسب لمشكلتك الآن، أو
            ابدأ بتشخيص سريع ونقترح لك الأفضل.
          </p>
          <div className="flex flex-wrap gap-4 justify-center">
            <Link to="/diagnostic">
              <Button size="lg" className="text-lg px-8 gap-2">
                ابدأ تشخيصًا سريعًا
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
            <Link to="/systems">
              <Button size="lg" variant="outline" className="text-lg px-8">
                تصفّح الأنظمة الخمسة
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Problem */}
      <section className="py-16 bg-white">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">المشكلة ليست نقص الجهد</h2>
          <p className="text-lg text-gray-600 leading-relaxed">
            أغلب الشركات لا تخسر بسبب قلة العمل، بل بسبب غياب نظام: فرص بلا متابعة، قرارات بلا صورة واضحة، واتساب فوضى،
            عروض بطيئة، وإيراد يتسرب بهدوء. Dealix يحوّل هذه الفوضى إلى أنظمة تشغيل واضحة.
          </p>
        </div>
      </section>

      {/* 5 Systems */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-3">خمسة أنظمة لمشكلتك المحددة</h2>
            <p className="text-gray-600">كل نظام يبدأ بـ Sprint واضح بمخرجات ومعايير قبول وسعر افتتاحي.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {SYSTEMS.map((s) => (
              <SystemCard key={s.slug} system={s} />
            ))}
            <Card className="h-full border-2 border-dashed border-emerald-300 bg-emerald-50/40 flex items-center justify-center">
              <CardContent className="p-6 text-center">
                <p className="text-gray-700 mb-4">غير متأكد أي نظام يناسبك؟</p>
                <Link to="/diagnostic">
                  <Button>ابدأ التشخيص</Button>
                </Link>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900">كيف نعمل؟</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {STEPS.map((s, i) => {
              const Icon = s.icon
              return (
                <Card key={i} className="border-0 shadow-md">
                  <CardContent className="p-6">
                    <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center mb-4">
                      <Icon className="w-6 h-6 text-emerald-600" />
                    </div>
                    <div className="text-sm text-emerald-600 font-bold mb-1">{i + 1}</div>
                    <h3 className="font-bold text-gray-900 mb-1">{s.title}</h3>
                    <p className="text-gray-600 text-sm">{s.desc}</p>
                  </CardContent>
                </Card>
              )
            })}
          </div>
        </div>
      </section>

      {/* Pricing preview */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-5xl mx-auto px-4">
          <div className="text-center mb-10">
            <h2 className="text-3xl font-bold text-gray-900 mb-3">أسعار Sprint افتتاحية</h2>
            <p className="text-gray-600">ابدأ واضحًا، ثم وسّع حسب النتائج.</p>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {[...SYSTEMS]
              .sort((a, b) => a.startingPriceSar - b.startingPriceSar)
              .map((s) => (
                <Link key={s.slug} to={`/systems/${s.slug}`}>
                  <Card className="border-0 shadow-sm hover:shadow-md transition-shadow h-full">
                    <CardContent className="p-5 text-center">
                      <div className="text-2xl font-bold text-emerald-600">{formatSar(s.startingPriceSar)}</div>
                      <div className="text-xs text-gray-400 mb-2">ر.س — يبدأ من</div>
                      <div className="text-sm text-gray-700 leading-snug">{s.nameAr}</div>
                    </CardContent>
                  </Card>
                </Link>
              ))}
          </div>
          <div className="text-center mt-8">
            <Link to="/pricing">
              <Button variant="outline" className="gap-2">
                عرض كل الأسعار
                <ArrowLeft className="w-4 h-4" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Diagnostic CTA */}
      <section className="py-16 bg-gradient-to-br from-emerald-600 to-teal-700">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">لا تعرف من أين تبدأ؟</h2>
          <p className="text-lg text-emerald-100 mb-8">سبعة أسئلة قصيرة تكفي لاقتراح النظام الأنسب وأول Sprint وسعره.</p>
          <Link to="/diagnostic">
            <Button size="lg" className="bg-white text-emerald-700 hover:bg-emerald-50 text-lg px-10">
              ابدأ التشخيص الآن
            </Button>
          </Link>
        </div>
      </section>

      {/* Governance */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-3">حوكمة واضحة</h2>
            <p className="text-gray-600">الذكاء الاصطناعي يكتب المسودات، والإنسان يوافق، والنظام يسجّل.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <Card className="border-0 shadow-md">
              <CardContent className="p-8">
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-14 h-14 bg-emerald-100 rounded-xl flex items-center justify-center">
                    <Shield className="w-7 h-7 text-emerald-600" />
                  </div>
                  <h3 className="text-xl font-bold">AI drafts. Human approves.</h3>
                </div>
                <div className="space-y-3">
                  {['كل بريد يبقى مسودة حتى موافقة المؤسس', 'لا إرسال خارجي افتراضيًا', 'لا اتصال آلي ولا أتمتة واتساب باردة', 'بيانات عامة أو مقدّمة من العميل فقط'].map(
                    (item, i) => (
                      <div key={i} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                        <Lock className="w-5 h-5 text-emerald-500 shrink-0" />
                        <span className="text-gray-700">{item}</span>
                      </div>
                    ),
                  )}
                </div>
              </CardContent>
            </Card>
            <Card className="border-0 shadow-md">
              <CardContent className="p-8">
                <h3 className="text-xl font-bold mb-6">نموذج الصلاحيات</h3>
                <div className="space-y-2">
                  {LEVELS.map((level, i) => (
                    <div
                      key={i}
                      className={`flex justify-between p-3 rounded-lg ${level.a ? 'bg-emerald-50' : 'bg-gray-50'}`}
                    >
                      <span className={level.a ? 'font-medium' : 'text-gray-500'}>{level.l}</span>
                      <Badge variant={level.a ? 'default' : 'outline'} className={level.a ? 'bg-emerald-500' : ''}>
                        {level.a ? 'نشط' : 'قريبًا'}
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-20 bg-gray-900">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">ابدأ بنظام واحد واضح</h2>
          <p className="text-lg text-gray-300 mb-8">
            اختر النظام المناسب لمشكلتك الآن، أو ابدأ بتشخيص سريع ونقترح لك الأفضل.
          </p>
          <div className="flex flex-wrap gap-4 justify-center">
            <Link to="/diagnostic">
              <Button size="lg" className="bg-emerald-500 hover:bg-emerald-600 text-lg px-8">
                ابدأ تشخيصًا سريعًا
              </Button>
            </Link>
            <Link to="/systems">
              <Button size="lg" variant="outline" className="text-lg px-8 bg-transparent text-white border-gray-600 hover:bg-gray-800">
                تصفّح الأنظمة
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </SiteLayout>
  )
}
