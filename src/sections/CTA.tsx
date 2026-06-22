import { ArrowLeft, Phone, MessageCircle } from 'lucide-react'

export default function CTA() {
  return (
    <section id="cta" className="py-20 bg-[#F0F9F8]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-[#0A1F1E] rounded-3xl p-8 sm:p-12 lg:p-16 relative overflow-hidden">
          {/* Background decoration */}
          <div className="absolute top-0 left-0 w-64 h-64 bg-[#15807A] rounded-full blur-3xl opacity-10 -translate-x-1/2 -translate-y-1/2" />
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-[#15807A] rounded-full blur-3xl opacity-10 translate-x-1/3 translate-y-1/3" />

          <div className="relative grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
                جاهز تكشف وين تضيع فلوسك؟
              </h2>
              <p className="text-[#8CB3B0] text-lg mb-8 leading-relaxed">
                احجز Revenue Diagnostic Call مجاناً — 20 دقيقة نكشف فيها أكبر نقطة تسريب في نظام مبيعاتك ونحدد إذا كان Sprint مناسب لك.
              </p>

              <div className="flex flex-col sm:flex-row gap-4">
                <a
                  href="/book-call"
                  className="inline-flex items-center justify-center gap-2 bg-[#15807A] text-white px-8 py-4 rounded-xl text-lg font-semibold hover:bg-[#0F5F5A] transition-all hover:scale-105"
                >
                  <Phone className="w-5 h-5" />
                  احجز تشخيص AI — 30 دقيقة
                  <ArrowLeft className="w-5 h-5" />
                </a>
                <a
                  href="/dashboard"
                  className="inline-flex items-center justify-center gap-2 border border-[#15807A]/40 text-[#E8F4F3] px-8 py-4 rounded-xl text-lg font-medium hover:bg-[#15807A]/10 transition-all"
                >
                  <MessageCircle className="w-5 h-5" />
                  دخول Command Room
                </a>
              </div>

              <div className="mt-8 flex flex-wrap items-center gap-4 text-sm text-[#8CB3B0]">
                <div className="flex items-center gap-1">
                  <svg className="w-4 h-4 text-[#15807A]" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  <span>بدون commitment</span>
                </div>
                <div className="flex items-center gap-1">
                  <svg className="w-4 h-4 text-[#15807A]" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  <span>بدون إرسال آلي</span>
                </div>
                <div className="flex items-center gap-1">
                  <svg className="w-4 h-4 text-[#15807A]" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                  <span>تحليل فوري</span>
                </div>
              </div>
            </div>

            <div className="hidden lg:block">
              <div className="bg-[#0F2E2C] rounded-2xl p-6 border border-[#15807A]/20">
                <h4 className="text-white font-bold mb-4">ماذا تحصل في الجلسة؟</h4>
                <ul className="space-y-3">
                  {[
                    'تشخيص سريع لأكبر نقطة تسريب إيرادات',
                    'تقييم سرعة المتابعة لديك',
                    'خريطة فرص واضحة',
                    'عرض Sprint إذا كان مناسب',
                  ].map((item, index) => (
                    <li key={item} className="flex items-center gap-3">
                      <div className="w-8 h-8 bg-[#15807A]/20 rounded-lg flex items-center justify-center text-[#15807A] font-bold text-sm">
                        {index + 1}
                      </div>
                      <span className="text-[#E8F4F3]">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
