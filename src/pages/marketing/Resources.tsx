import { Link } from 'react-router'
import { ArrowLeft, FileText } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'
import SiteLayout from '@/components/site/SiteLayout'
import { getSystem } from '@/data/systems'
import { systemMeta } from '@/components/site/systemMeta'

interface Resource {
  title: string
  desc: string
  systemId: string
}

const RESOURCES: Resource[] = [
  { title: 'قائمة فحص تسرب الإيراد', desc: 'نقاط عملية لاكتشاف أين تتسرب الفرص عبر مراحل البيع.', systemId: 'revenue-operating-system' },
  { title: 'دليل استعادة المتابعة', desc: 'كيف تبني قائمة متابعة تعيد تفعيل الفرص المتروكة.', systemId: 'follow-up-recovery-os' },
  { title: 'دليل تنظيم واتساب', desc: 'تحويل واتساب من محادثات متفرقة إلى مسارات وبطاقات إجراء.', systemId: 'whatsapp-client-os' },
  { title: 'قالب العرض و Proof Pack', desc: 'هيكل عرض واضح وإثبات يطمئن العميل ويسرّع القرار.', systemId: 'proposal-proof-os' },
  { title: 'نموذج تقرير القيادة اليومي', desc: 'شكل تقرير القرار اليومي: أهم فرصة، أكبر خطر، القرار التالي.', systemId: 'executive-command-os' },
]

export default function Resources() {
  return (
    <SiteLayout>
      <section className="relative pt-16 pb-10 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-teal-50" />
        <div className="relative max-w-3xl mx-auto px-4 text-center">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900">الموارد</h1>
          <p className="text-gray-600 mt-3">أدلة وقوالب عملية مرتبطة بكل نظام. تفضّل تطبيقًا مباشرًا؟ ابدأ Sprint.</p>
        </div>
      </section>

      <section className="py-12">
        <div className="max-w-5xl mx-auto px-4 grid grid-cols-1 md:grid-cols-2 gap-6">
          {RESOURCES.map((r, i) => {
            const system = getSystem(r.systemId)
            const meta = systemMeta(r.systemId)
            const Icon = meta.icon
            return (
              <Card key={i} className="shadow-md border-0 hover:shadow-lg transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className={`w-11 h-11 rounded-xl flex items-center justify-center ${meta.iconBg}`}>
                      <Icon className="w-5 h-5" />
                    </div>
                    <Badge variant="outline" className="gap-1">
                      <FileText className="w-3 h-3" />
                      دليل
                    </Badge>
                  </div>
                  <h3 className="font-bold text-gray-900 mb-1">{r.title}</h3>
                  <p className="text-gray-600 text-sm mb-4">{r.desc}</p>
                  {system && (
                    <Link
                      to={`/systems/${system.slug}`}
                      className={`inline-flex items-center gap-1 text-sm font-medium ${meta.accentText}`}
                    >
                      {system.nameAr}
                      <ArrowLeft className="w-4 h-4" />
                    </Link>
                  )}
                </CardContent>
              </Card>
            )
          })}
        </div>
      </section>
    </SiteLayout>
  )
}
