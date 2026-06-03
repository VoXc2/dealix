import { useMemo, useState } from 'react'
import { Link } from 'react-router'
import { ArrowLeft, RotateCcw, Sparkles } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import SiteLayout from '@/components/site/SiteLayout'
import { SYSTEMS, getSystem, formatSar } from '@/data/systems'
import { systemMeta } from '@/components/site/systemMeta'

type SystemId = (typeof SYSTEMS)[number]['id']
type Weights = Partial<Record<SystemId, number>>

interface Option {
  label: string
  weights: Weights
}
interface Question {
  id: string
  q: string
  options: Option[]
}

const QUESTIONS: Question[] = [
  {
    id: 'type',
    q: 'ما نوع الشركة؟',
    options: [
      { label: 'وكالة تسويق', weights: { 'revenue-operating-system': 2, 'proposal-proof-os': 1 } },
      { label: 'شركة تدريب', weights: { 'follow-up-recovery-os': 2 } },
      { label: 'عقار', weights: { 'follow-up-recovery-os': 1, 'whatsapp-client-os': 1 } },
      { label: 'عيادات', weights: { 'whatsapp-client-os': 2 } },
      { label: 'استشارات / خدمات B2B', weights: { 'proposal-proof-os': 2, 'revenue-operating-system': 1 } },
    ],
  },
  {
    id: 'breakdown',
    q: 'أين أكبر تعطل حاليًا؟',
    options: [
      { label: 'متابعة الفرص لا تحدث في وقتها', weights: { 'follow-up-recovery-os': 3 } },
      { label: 'القرار اليومي والإدارة غير واضحين', weights: { 'executive-command-os': 3 } },
      { label: 'واتساب فوضى ومحادثات متفرقة', weights: { 'whatsapp-client-os': 3 } },
      { label: 'العروض بطيئة وبلا إثبات', weights: { 'proposal-proof-os': 3 } },
      { label: 'لا أعرف أين يتسرب الإيراد', weights: { 'revenue-operating-system': 3 } },
    ],
  },
  {
    id: 'leads',
    q: 'هل عندكم leads أو استفسارات؟',
    options: [
      { label: 'نعم، كثيرة', weights: { 'revenue-operating-system': 1, 'follow-up-recovery-os': 1 } },
      { label: 'بعضها', weights: { 'follow-up-recovery-os': 1 } },
      { label: 'قليلة', weights: { 'revenue-operating-system': 1 } },
    ],
  },
  {
    id: 'whatsapp',
    q: 'هل واتساب قناة رئيسية لديكم؟',
    options: [
      { label: 'نعم، أساسية', weights: { 'whatsapp-client-os': 3 } },
      { label: 'أحيانًا', weights: { 'whatsapp-client-os': 1 } },
      { label: 'لا', weights: {} },
    ],
  },
  {
    id: 'proposals',
    q: 'هل العروض أو الـ proposals متكررة؟',
    options: [
      { label: 'نعم، باستمرار', weights: { 'proposal-proof-os': 3 } },
      { label: 'أحيانًا', weights: { 'proposal-proof-os': 1 } },
      { label: 'لا', weights: {} },
    ],
  },
  {
    id: 'exec',
    q: 'هل الإدارة تحتاج تقرير قرار يومي؟',
    options: [
      { label: 'نعم، بشدة', weights: { 'executive-command-os': 3 } },
      { label: 'ربما', weights: { 'executive-command-os': 1 } },
      { label: 'لا', weights: {} },
    ],
  },
  {
    id: 'goal',
    q: 'ما هدفك خلال 14 يومًا؟',
    options: [
      { label: 'تنظيم المتابعة واستعادة الفرص', weights: { 'follow-up-recovery-os': 2 } },
      { label: 'لوحة قرار يومية واضحة', weights: { 'executive-command-os': 2 } },
      { label: 'تنظيم واتساب', weights: { 'whatsapp-client-os': 2 } },
      { label: 'عرض احترافي و Proof Pack', weights: { 'proposal-proof-os': 2 } },
      { label: 'كشف تسرب الإيراد', weights: { 'revenue-operating-system': 2 } },
    ],
  },
]

const REASONS: Record<SystemId, string> = {
  'revenue-operating-system': 'إجاباتك تشير إلى فرص وإيراد بلا مسار قرار واضح — وهذا تخصص نظام تشغيل الإيرادات.',
  'executive-command-os': 'إجاباتك تشير إلى حاجة لقرار إداري يومي مجمّع — وهذا تخصص نظام القيادة التنفيذية.',
  'follow-up-recovery-os': 'إجاباتك تشير إلى استفسارات تحتاج متابعة منظمة — وهذا تخصص نظام استعادة المتابعة.',
  'whatsapp-client-os': 'إجاباتك تشير إلى اعتماد كبير على واتساب يحتاج تنظيمًا — وهذا تخصص نظام عملاء واتساب.',
  'proposal-proof-os': 'إجاباتك تشير إلى عروض متكررة تحتاج وضوحًا وإثباتًا — وهذا تخصص نظام العروض والإثبات.',
}

const FIRST_SPRINT: Record<SystemId, string> = {
  'revenue-operating-system': 'خريطة تسرب الإيراد ومسار متابعة خلال 7–10 أيام.',
  'executive-command-os': 'أول تقرير قيادة يومي وخريطة مؤشرات خلال 7–14 يومًا.',
  'follow-up-recovery-os': 'قائمة متابعة ومجموعة رسائل خلال 7 أيام.',
  'whatsapp-client-os': 'خريطة مسارات واتساب وبطاقات إجراء خلال 7–10 أيام.',
  'proposal-proof-os': 'قالب عرض و Proof Pack خلال 5–7 أيام.',
}

export default function Diagnostic() {
  const [step, setStep] = useState(0)
  const [scores, setScores] = useState<Record<string, number>>({})
  const [finished, setFinished] = useState(false)

  function choose(option: Option) {
    setScores((prev) => {
      const next = { ...prev }
      for (const [k, v] of Object.entries(option.weights)) next[k] = (next[k] ?? 0) + (v ?? 0)
      return next
    })
    if (step < QUESTIONS.length - 1) setStep(step + 1)
    else setFinished(true)
  }

  function restart() {
    setScores({})
    setStep(0)
    setFinished(false)
  }

  const recommendedId = useMemo<SystemId>(() => {
    let best: SystemId = 'revenue-operating-system'
    let bestScore = -1
    for (const s of SYSTEMS) {
      const sc = scores[s.id] ?? 0
      if (sc > bestScore) {
        bestScore = sc
        best = s.id
      }
    }
    return best
  }, [scores])

  const recommended = getSystem(recommendedId)!
  const meta = systemMeta(recommendedId)
  const Icon = meta.icon

  return (
    <SiteLayout>
      <section className="relative pt-16 pb-10 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-teal-50" />
        <div className="relative max-w-2xl mx-auto px-4 text-center">
          <div className="inline-flex items-center gap-2 text-emerald-700 bg-emerald-100 rounded-full px-4 py-1.5 text-sm mb-4">
            <Sparkles className="w-4 h-4" />
            تشخيص سريع — أقل من دقيقة
          </div>
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900">أي نظام يناسب شركتك؟</h1>
          <p className="text-gray-600 mt-3">سبعة أسئلة قصيرة، ونقترح لك النظام الأنسب وأول Sprint وسعره.</p>
        </div>
      </section>

      <section className="pb-20">
        <div className="max-w-2xl mx-auto px-4">
          {!finished ? (
            <Card className="shadow-lg border-0">
              <CardContent className="p-8">
                <div className="mb-6">
                  <div className="flex justify-between text-sm text-gray-500 mb-2">
                    <span>سؤال {step + 1} من {QUESTIONS.length}</span>
                    <span>{Math.round(((step) / QUESTIONS.length) * 100)}%</span>
                  </div>
                  <Progress value={(step / QUESTIONS.length) * 100} />
                </div>
                <h2 className="text-xl font-bold text-gray-900 mb-6">{QUESTIONS[step].q}</h2>
                <div className="space-y-3">
                  {QUESTIONS[step].options.map((opt, i) => (
                    <button
                      key={i}
                      onClick={() => choose(opt)}
                      className="w-full text-right p-4 rounded-xl border border-gray-200 hover:border-emerald-400 hover:bg-emerald-50 transition-colors text-gray-700"
                    >
                      {opt.label}
                    </button>
                  ))}
                </div>
                {step > 0 && (
                  <button onClick={() => setStep(step - 1)} className="text-sm text-gray-400 hover:text-gray-600 mt-6">
                    رجوع
                  </button>
                )}
              </CardContent>
            </Card>
          ) : (
            <Card className="shadow-lg border-0">
              <CardContent className="p-8">
                <p className="text-sm text-gray-500 mb-4 text-center">بناءً على إجاباتك، النظام الأنسب لك:</p>
                <div className="flex flex-col items-center text-center mb-6">
                  <div className={`w-16 h-16 rounded-2xl flex items-center justify-center mb-3 ${meta.iconBg}`}>
                    <Icon className="w-8 h-8" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900">{recommended.nameAr}</h2>
                  <p className="text-gray-600 mt-2 max-w-md">{REASONS[recommendedId]}</p>
                </div>

                <div className="space-y-3 mb-6">
                  <div className="flex items-start gap-3 p-4 bg-gray-50 rounded-xl">
                    <span className="font-bold text-gray-900 shrink-0">أول Sprint:</span>
                    <span className="text-gray-700">{FIRST_SPRINT[recommendedId]}</span>
                  </div>
                  <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-xl">
                    <span className="font-bold text-gray-900 shrink-0">السعر يبدأ من:</span>
                    <span className={`text-xl font-bold ${meta.accentText}`}>{formatSar(recommended.startingPriceSar)} ر.س</span>
                  </div>
                </div>

                <div className="flex flex-col sm:flex-row gap-3">
                  <Link to={`/systems/${recommended.slug}`} className="flex-1">
                    <Button className="w-full gap-2" size="lg">
                      تفاصيل النظام
                      <ArrowLeft className="w-5 h-5" />
                    </Button>
                  </Link>
                  <Link to="/start" className="flex-1">
                    <Button variant="outline" className="w-full" size="lg">
                      احجز مكالمة
                    </Button>
                  </Link>
                </div>
                <button onClick={restart} className="flex items-center gap-2 text-sm text-gray-400 hover:text-gray-600 mx-auto mt-6">
                  <RotateCcw className="w-4 h-4" />
                  إعادة التشخيص
                </button>
              </CardContent>
            </Card>
          )}
        </div>
      </section>
    </SiteLayout>
  )
}
