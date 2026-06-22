import { BarChart3, Shield, Brain, Zap, Send, Target } from 'lucide-react'

const features = [
  {
    icon: BarChart3,
    title: 'Revenue Command Room OS',
    description: 'War room يومي للإيرادات: Pipeline health, Top prospects, Outreach drafts للمراجعة, Follow-up queue, CEO daily report.',
  },
  {
    icon: Brain,
    title: 'Company Brain OS',
    description: 'القرارات اليومية مبنية على بيانات: Company brain map, Daily decision desk, Future radar, Bottleneck scanner.',
  },
  {
    icon: Zap,
    title: 'Client Delivery OS',
    description: 'نظام تسليم مشاريعك بحوكمة: Intake → Diagnosis → Blueprint → Delivery → Proof pack.',
  },
  {
    icon: Shield,
    title: 'AI Trust & Compliance OS',
    description: 'حوكمة AI متكاملة: Safety gates, Audit trail, Manual approval, SDAIA compliance, No auto-send.',
  },
  {
    icon: Send,
    title: 'WhatsApp / Inbox Follow-up OS',
    description: 'متابعات آلية بموافقة يدوية: AI drafts, Approval queue, Sequences, Performance analytics.',
  },
  {
    icon: Target,
    title: 'Proof Pack System',
    description: 'توثيق القيمة قبل وبعد كل مشروع: Before/after metrics, Command room reports, Decision log.',
  },
]

export default function Features() {
  return (
    <section id="features" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <span className="text-[#15807A] text-sm font-semibold tracking-wide uppercase">منتجات Dealix</span>
          <h2 className="text-3xl sm:text-4xl font-bold text-[#0A1F1E] mt-2 mb-4">
            5 أنظمة تشغيل لتحويل شركتك
          </h2>
          <p className="text-[#4A6B69] text-lg max-w-2xl mx-auto">
            لا نبيع "أداة". نبني أنظمة تشغيل (Operating Systems) تربط الإيرادات والمتابعة والقرارات والحوكمة في workflow يومي.
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
