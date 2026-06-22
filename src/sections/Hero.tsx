import { ArrowLeft, BarChart3, Shield, Clock } from 'lucide-react'

export default function Hero() {
  return (
    <section className="relative pt-32 pb-20 overflow-hidden bg-[#0A1F1E]">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute top-20 right-20 w-72 h-72 bg-[#15807A] rounded-full blur-3xl" />
        <div className="absolute bottom-20 left-20 w-96 h-96 bg-[#15807A] rounded-full blur-3xl" />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div>
            <div className="inline-flex items-center gap-2 bg-[#15807A]/20 border border-[#15807A]/30 rounded-full px-4 py-1.5 mb-6">
              <span className="w-2 h-2 bg-[#15807A] rounded-full animate-pulse" />
              <span className="text-[#E8F4F3] text-sm">نظام Revenue Intelligence مدعوم بالذكاء الاصطناعي</span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white leading-tight mb-6">
              حوّل فوضى المبيعات والمتابعات إلى{' '}
              <span className="text-[#15807A]">War Room</span> للإيرادات خلال 5 أيام
            </h1>

            <p className="text-lg text-[#8CB3B0] mb-8 leading-relaxed max-w-xl">
              نكشف أين تضيع فرصك، نحلل متابعاتك وعروضك، ونبني لك خطة تشغيل واضحة لتحسين التحويل — مع حوكمة AI وتوثيق يناسب بيئة الأعمال السعودية.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 mb-12">
              <a
                href="/book-call"
                className="inline-flex items-center justify-center gap-2 bg-[#15807A] text-white px-8 py-4 rounded-xl text-lg font-semibold hover:bg-[#0F5F5A] transition-all hover:scale-105"
              >
                احجز تشخيص AI Revenue — 30 دقيقة
                <ArrowLeft className="w-5 h-5" />
              </a>
              <a
                href="/dashboard"
                className="inline-flex items-center justify-center gap-2 border border-[#15807A]/40 text-[#E8F4F3] px-8 py-4 rounded-xl text-lg font-medium hover:bg-[#15807A]/10 transition-all"
              >
                دخول Command Room
              </a>
            </div>

            <div className="grid grid-cols-3 gap-6">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-[#15807A]/20 rounded-lg flex items-center justify-center">
                  <BarChart3 className="w-5 h-5 text-[#15807A]" />
                </div>
                <div>
                  <div className="text-white font-bold text-lg">5 أيام</div>
                  <div className="text-[#8CB3B0] text-sm">مدة الـ Sprint</div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-[#15807A]/20 rounded-lg flex items-center justify-center">
                  <Shield className="w-5 h-5 text-[#15807A]" />
                </div>
                <div>
                  <div className="text-white font-bold text-lg">100%</div>
                  <div className="text-[#8CB3B0] text-sm">حوكمة AI</div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-[#15807A]/20 rounded-lg flex items-center justify-center">
                  <Clock className="w-5 h-5 text-[#15807A]" />
                </div>
                <div>
                  <div className="text-white font-bold text-lg">15 دقيقة</div>
                  <div className="text-[#8CB3B0] text-sm">SLA للرد</div>
                </div>
              </div>
            </div>
          </div>

          <div className="relative hidden lg:block">
            <div className="relative bg-[#0F2E2C] rounded-2xl border border-[#15807A]/20 p-6 shadow-2xl">
              {/* War Room Preview */}
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-red-500" />
                  <div className="w-3 h-3 rounded-full bg-yellow-500" />
                  <div className="w-3 h-3 rounded-full bg-green-500" />
                </div>
                <span className="text-[#8CB3B0] text-xs font-mono">Dealix War Room — Live</span>
              </div>

              <div className="space-y-3">
                {/* Metric Cards */}
                <div className="grid grid-cols-2 gap-3">
                  <div className="bg-[#0A1F1E] rounded-lg p-3 border border-[#15807A]/10">
                    <div className="text-[#8CB3B0] text-xs mb-1">فرص مفتوحة</div>
                    <div className="text-white text-xl font-bold">12</div>
                    <div className="text-[#15807A] text-xs mt-1">+3 هذا الأسبوع</div>
                  </div>
                  <div className="bg-[#0A1F1E] rounded-lg p-3 border border-red-500/20">
                    <div className="text-[#8CB3B0] text-xs mb-1">تسريب إيرادات</div>
                    <div className="text-red-400 text-xl font-bold">37%</div>
                    <div className="text-red-400/70 text-xs mt-1">⚠️ يحتاج اهتمام</div>
                  </div>
                </div>

                {/* Pipeline */}
                <div className="bg-[#0A1F1E] rounded-lg p-3 border border-[#15807A]/10">
                  <div className="text-[#8CB3B0] text-xs mb-2">Pipeline المراحل</div>
                  <div className="flex gap-1">
                    {[
                      { label: 'جديد', count: 8, color: 'bg-[#15807A]' },
                      { label: 'تواصل', count: 5, color: 'bg-[#15807A]/70' },
                      { label: 'عرض', count: 3, color: 'bg-yellow-600' },
                      { label: 'إغلاق', count: 1, color: 'bg-[#15807A]/40' },
                    ].map((stage) => (
                      <div key={stage.label} className="flex-1">
                        <div className={`${stage.color} h-8 rounded flex items-center justify-center text-white text-xs font-bold`}>
                          {stage.count}
                        </div>
                        <div className="text-[#8CB3B0] text-[10px] text-center mt-1">{stage.label}</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Follow-up Alert */}
                <div className="bg-yellow-900/20 border border-yellow-600/30 rounded-lg p-3">
                  <div className="flex items-center gap-2">
                    <span className="text-yellow-500">⚠️</span>
                    <span className="text-yellow-200 text-sm">5 عملاء لم تتم متابعتهم بعد أول رد</span>
                  </div>
                </div>

                {/* Today's Actions */}
                <div className="bg-[#0A1F1E] rounded-lg p-3 border border-[#15807A]/10">
                  <div className="text-[#8CB3B0] text-xs mb-2">إجراءات اليوم</div>
                  <div className="space-y-1.5">
                    {[
                      'إرسال رسائل P1 intro',
                      'متابعة العملاء المتأخرين',
                      'تحديث تقرير الأداء',
                    ].map((action) => (
                      <div key={action} className="flex items-center gap-2">
                        <div className="w-4 h-4 rounded border border-[#15807A]/30 flex items-center justify-center">
                          <div className="w-2 h-2 rounded-full bg-[#15807A]" />
                        </div>
                        <span className="text-[#E8F4F3] text-xs">{action}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
