import { CheckCircle2 } from 'lucide-react'

const deliverables = [
  { name: 'Revenue Leakage Map', desc: 'خريطة تفصيلية تظهر أين تضيع الفرص في كل مرحلة' },
  { name: 'Lead Response Audit', desc: 'تحليل سرعة الرد على العملاء مقارنة بأفضل المعايير' },
  { name: 'Follow-up Gap Report', desc: 'تقرير الفجوات في المتابعة مع توصيات للإصلاح' },
  { name: 'Offer Quality Review', desc: 'مراجعة جودة العروض وقوة التحويل' },
  { name: 'Objection Map', desc: 'حصر الاعتراضات الأكثر شيوعاً مع قوالب ردود جاهزة' },
  { name: '30-Day Revenue Plan', desc: 'خطة عمل قابلة للتنفيذ خلال 30 يوم' },
  { name: 'CEO Brief', desc: 'ملخص تنفيذي للإدارة بأهم النتائج والتوصيات' },
  { name: 'P2 Proposal', desc: 'عرض الانتقال لنظام التشغيل الشهري' },
]

export default function Deliverables() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div>
            <span className="text-[#15807A] text-sm font-semibold tracking-wide uppercase">المخرجات</span>
            <h2 className="text-3xl sm:text-4xl font-bold text-[#0A1F1E] mt-2 mb-4">
              ماذا تستلم بعد الـ Sprint؟
            </h2>
            <p className="text-[#4A6B69] text-lg mb-8 leading-relaxed">
              8 مخرجات عملية تكشف الحقيقة وتعطيك خطة واضحة للتحسين — كلها مُوثّقة ومُحكمة وقابلة للتنفيذ فوراً.
            </p>

            <div className="bg-[#F0F9F8] rounded-2xl p-6 border border-[#E8F4F3]">
              <h4 className="font-bold text-[#0A1F1E] mb-3">🎯 النتيجة المتوقعة</h4>
              <ul className="space-y-2 text-[#4A6B69]">
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-5 h-5 text-[#15807A] shrink-0 mt-0.5" />
                  <span>معرفة دقيقة بوين تضيع الفرص</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-5 h-5 text-[#15807A] shrink-0 mt-0.5" />
                  <span>خطة 30 يوم قابلة للتنفيذ</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-5 h-5 text-[#15807A] shrink-0 mt-0.5" />
                  <span>عرض الانتقال لنظام شهري</span>
                </li>
              </ul>
            </div>
          </div>

          <div className="space-y-4">
            {deliverables.map((item, index) => (
              <div
                key={item.name}
                className="flex items-start gap-4 p-4 rounded-xl border border-[#E8F4F3] hover:border-[#15807A]/30 hover:bg-[#F0F9F8] transition-all"
              >
                <div className="w-8 h-8 bg-[#15807A] rounded-lg flex items-center justify-center shrink-0">
                  <span className="text-white text-sm font-bold">{index + 1}</span>
                </div>
                <div>
                  <h4 className="font-bold text-[#0A1F1E]">{item.name}</h4>
                  <p className="text-[#4A6B69] text-sm mt-1">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
