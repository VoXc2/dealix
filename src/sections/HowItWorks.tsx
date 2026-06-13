const steps = [
  {
    day: 'يوم 0',
    title: 'Intake + جمع البيانات',
    description: 'نجمع أقل البيانات المطلوبة: CRM export، نماذج محادثات، وعروض أسعار. كل البيانات تجهّل وتُعالج محلياً.',
    color: 'bg-[#15807A]',
  },
  {
    day: 'يوم 1',
    title: 'Revenue Map',
    description: 'نرسم خريطة كاملة لمصادر العملاء والمراحل ونحدد أكبر نقاط التسريب في pipeline.',
    color: 'bg-[#15807A]/80',
  },
  {
    day: 'يوم 2',
    title: 'Follow-up Audit',
    description: 'نحلل جودة وتوقيت المتابعات ونحدد الفجوات ونقترح نظام متابعة محسّن.',
    color: 'bg-[#15807A]/60',
  },
  {
    day: 'يوم 3',
    title: 'Offer & Objection Review',
    description: 'نحلل قوة عروضك وحجم الاعتراضات ونبني قوالب محسّنة للردود والعروض.',
    color: 'bg-[#15807A]/50',
  },
  {
    day: 'يوم 4',
    title: 'Proof Pack',
    description: 'نُجمّل كل النتائج في تقرير تنفيذي + خطة 30 يوم قابلة للتنفيذ فوراً.',
    color: 'bg-[#15807A]/40',
  },
  {
    day: 'يوم 5',
    title: 'Executive Review + P2',
    description: 'نقدم النتائج في call 30 دقيقة ونعرض الانتقال لنظام التشغيل الشهري.',
    color: 'bg-[#15807A]/30',
  },
]

export default function HowItWorks() {
  return (
    <section id="how" className="py-20 bg-[#F0F9F8]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <span className="text-[#15807A] text-sm font-semibold tracking-wide uppercase">العملية</span>
          <h2 className="text-3xl sm:text-4xl font-bold text-[#0A1F1E] mt-2 mb-4">
            5 أيام تكشف وين تروح فلوسك
          </h2>
          <p className="text-[#4A6B69] text-lg max-w-2xl mx-auto">
            Sprint سريع ومنظّم — نبدأ بالبيانات وننتهي بخطة عمل واضحة
          </p>
        </div>

        <div className="relative">
          {/* Timeline line */}
          <div className="hidden lg:block absolute top-1/2 right-12 left-12 h-0.5 bg-[#15807A]/20 -translate-y-1/2" />

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {steps.map((step, index) => (
              <div
                key={step.day}
                className="relative bg-white rounded-2xl p-6 shadow-sm border border-[#E8F4F3] hover:shadow-md transition-shadow"
              >
                <div className={`${step.color} text-white text-sm font-bold px-3 py-1 rounded-full inline-block mb-4`}>
                  {step.day}
                </div>
                <h3 className="text-lg font-bold text-[#0A1F1E] mb-2">{step.title}</h3>
                <p className="text-[#4A6B69] text-sm leading-relaxed">{step.description}</p>
                <div className="mt-4 text-xs text-[#8CB3B0]">
                  الخطوة {index + 1} من 6
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
