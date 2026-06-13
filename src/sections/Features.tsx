import { BarChart3, Shield, MessageSquare, LineChart, Lock, Target } from 'lucide-react'

const features = [
  {
    icon: BarChart3,
    title: 'Revenue Leakage Map',
    description: 'اكتشف بالضبط أين تضيع فرص الإيراد في كل مرحلة من مراحل المبيعات — من الاستفسار إلى الإغلاق.',
  },
  {
    icon: MessageSquare,
    title: 'Follow-up Audit',
    description: 'تحليل كامل لجودة المتابعات وتوقيتها مع تحديد الفجوات وإنشاء نظام متابعة محسّن.',
  },
  {
    icon: LineChart,
    title: 'Objection Intelligence',
    description: 'حصر أكثر الاعتراضات تكراراً مع قوالب جاهزة للرد وتحسين نسبة التحويل.',
  },
  {
    icon: Shield,
    title: 'AI Governance',
    description: 'نظام حوكمة متكامل يضمن أن كل إجراء AI يتم بموافقة بشرية وتوثيق كامل ومطابق لمعايير SDAIA.',
  },
  {
    icon: Lock,
    title: 'PDPL Compliance',
    description: 'التزام كامل بنظام حماية البيانات الشخصية السعودي — تشفير، تجهيل، وسياسة احتفاف 90 يوم.',
  },
  {
    icon: Target,
    title: 'War Room أسبوعي',
    description: 'جلسات أسبوعية لمراجعة الأداء وتحديد الإجراءات وضمان التنفيذ المستمر لتحسين الإيرادات.',
  },
]

export default function Features() {
  return (
    <section id="features" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <span className="text-[#15807A] text-sm font-semibold tracking-wide uppercase">المميزات</span>
          <h2 className="text-3xl sm:text-4xl font-bold text-[#0A1F1E] mt-2 mb-4">
            نظام كامل لإدارة إيراداتك
          </h2>
          <p className="text-[#4A6B69] text-lg max-w-2xl mx-auto">
            ليس مجرد تقرير — بل نظام تشغيل متكامل يكشف التسريب ويحسّن التحويل ويثبت القيمة
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="group p-6 rounded-2xl border border-[#E8F4F3] hover:border-[#15807A]/30 hover:shadow-lg hover:shadow-[#15807A]/5 transition-all duration-300 bg-white"
            >
              <div className="w-12 h-12 bg-[#E8F4F3] rounded-xl flex items-center justify-center mb-4 group-hover:bg-[#15807A] transition-colors">
                <feature.icon className="w-6 h-6 text-[#15807A] group-hover:text-white transition-colors" />
              </div>
              <h3 className="text-xl font-bold text-[#0A1F1E] mb-3">{feature.title}</h3>
              <p className="text-[#4A6B69] leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
