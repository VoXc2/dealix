import { Megaphone, GraduationCap, Briefcase } from 'lucide-react'

const sectors = [
  {
    icon: Megaphone,
    name: 'وكالات التسويق',
    pain: [
      'عملاء كثير ونتائج غير موثقة',
      'Leads تضيع بين الاستفسار والرد',
      'Follow-up ضعيف أو معدوم',
      'يحتاجون Proof لعملائهم',
    ],
    solution: 'نظام يثبت وين تضيع فرص عملائك ويطلع تقارير أسبوعية تزيد ثقة العميل في الوكالة',
    color: 'from-[#15807A] to-[#0F5F5A]',
  },
  {
    icon: GraduationCap,
    name: 'شركات التدريب',
    pain: [
      'واتساب مليان استفسارات',
      'تسجيلات ناقصة مقابل الاستفسارات',
      'متابعة الدفع ضعيفة',
      'حملات موسمية بدون نظام',
    ],
    solution: 'نظام متابعة وتحويل للاستفسارات إلى تسجيلات مدفوعة مع أتمتة المتابعة',
    color: 'from-[#2A9D8F] to-[#1D7066]',
  },
  {
    icon: Briefcase,
    name: 'شركات B2B Services',
    pain: [
      'عروض كثيرة وصفقات بطيئة',
      'CRM ضعيف أو غير مستخدم',
      'المؤسس لا يرى الحقيقة اليومية',
      'لا يوجد نظام واضح للمبيعات',
    ],
    solution: 'War Room يوضح الفرص، التأخيرات، الاعتراضات، والخطوة التالية لكل صفقة',
    color: 'from-[#264653] to-[#1A323D]',
  },
]

export default function Sectors() {
  return (
  <section id="sectors" className="py-20 bg-white">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="text-center mb-16">
        <span className="text-[#15807A] text-sm font-semibold tracking-wide uppercase">القطاعات</span>
        <h2 className="text-3xl sm:text-4xl font-bold text-[#0A1F1E] mt-2 mb-4">
          مصمم لقطاعات محددة تشتري بسرعة
        </h2>
        <p className="text-[#4A6B69] text-lg max-w-2xl mx-auto">
          لا نشتغل مع الكل — نركز على القطاعات اللي عندها الألم واضح والقدرة على الشراء الآن
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        {sectors.map((sector) => (
          <div
            key={sector.name}
            className="group rounded-2xl border border-[#E8F4F3] overflow-hidden hover:shadow-xl transition-all duration-300"
          >
            <div className={`bg-gradient-to-br ${sector.color} p-6`}>
              <sector.icon className="w-10 h-10 text-white mb-4" />
              <h3 className="text-xl font-bold text-white">{sector.name}</h3>
            </div>
            <div className="p-6">
              <div className="mb-4">
                <h4 className="text-sm font-bold text-red-600 mb-2">💢 الألم</h4>
                <ul className="space-y-1.5">
                  {sector.pain.map((item) => (
                    <li key={item} className="text-[#4A6B69] text-sm flex items-start gap-2">
                      <span className="text-red-400 mt-1">•</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <h4 className="text-sm font-bold text-[#15807A] mb-2">✅ الحل</h4>
                <p className="text-[#4A6B69] text-sm leading-relaxed">{sector.solution}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  </section>
  )
}
