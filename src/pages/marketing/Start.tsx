import { useState, type FormEvent } from 'react'
import { Link, useSearchParams } from 'react-router'
import { CheckCircle, Mail, ArrowLeft } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import SiteLayout from '@/components/site/SiteLayout'
import { SYSTEMS, getSystem, formatSar } from '@/data/systems'
import { buildMailto } from '@/lib/contact'

export default function Start() {
  const [params] = useSearchParams()
  const preset = getSystem(params.get('system') ?? undefined)
  const [name, setName] = useState('')
  const [company, setCompany] = useState('')
  const [systemId, setSystemId] = useState(preset?.id ?? '')
  const [message, setMessage] = useState('')
  const [submitted, setSubmitted] = useState(false)

  const chosen = getSystem(systemId)

  function onSubmit(e: FormEvent) {
    e.preventDefault()
    setSubmitted(true)
  }

  const mailto = buildMailto(
    `طلب بدء Sprint${chosen ? ' — ' + chosen.nameAr : ''}`,
    `الاسم: ${name}\nالشركة: ${company}\nالنظام المطلوب: ${chosen ? chosen.nameAr : 'غير محدد'}\n\n${message}`,
  )

  return (
    <SiteLayout>
      <section className="relative pt-16 pb-10 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-teal-50" />
        <div className="relative max-w-2xl mx-auto px-4 text-center">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900">ابدأ Sprint واضح</h1>
          <p className="text-gray-600 mt-3">عبّئ التفاصيل المختصرة، ونرتّب مكالمة قصيرة لتحديد أول مخرج وسعره.</p>
        </div>
      </section>

      <section className="pb-20">
        <div className="max-w-2xl mx-auto px-4">
          {!submitted ? (
            <Card className="shadow-lg border-0">
              <CardContent className="p-8">
                <form onSubmit={onSubmit} className="space-y-5">
                  <div>
                    <Label htmlFor="name">الاسم</Label>
                    <Input id="name" value={name} onChange={(e) => setName(e.target.value)} required className="mt-1.5" placeholder="اسمك" />
                  </div>
                  <div>
                    <Label htmlFor="company">الشركة</Label>
                    <Input id="company" value={company} onChange={(e) => setCompany(e.target.value)} required className="mt-1.5" placeholder="اسم الشركة" />
                  </div>
                  <div>
                    <Label>النظام المطلوب</Label>
                    <Select value={systemId} onValueChange={setSystemId}>
                      <SelectTrigger className="mt-1.5">
                        <SelectValue placeholder="اختر النظام (أو ابدأ بتشخيص)" />
                      </SelectTrigger>
                      <SelectContent>
                        {SYSTEMS.map((s) => (
                          <SelectItem key={s.id} value={s.id}>
                            {s.nameAr} — يبدأ من {formatSar(s.startingPriceSar)} ر.س
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <p className="text-xs text-gray-400 mt-1.5">
                      غير متأكد؟{' '}
                      <Link to="/diagnostic" className="text-emerald-600 hover:underline">ابدأ بالتشخيص السريع</Link>
                    </p>
                  </div>
                  <div>
                    <Label htmlFor="message">نبذة عن وضعكم الحالي</Label>
                    <Textarea id="message" value={message} onChange={(e) => setMessage(e.target.value)} className="mt-1.5" rows={4} placeholder="ما أكبر تعطل تواجهونه الآن؟" />
                  </div>
                  <Button type="submit" size="lg" className="w-full">متابعة</Button>
                </form>
              </CardContent>
            </Card>
          ) : (
            <Card className="shadow-lg border-0">
              <CardContent className="p-8 text-center">
                <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <CheckCircle className="w-8 h-8 text-emerald-600" />
                </div>
                <h2 className="text-2xl font-bold text-gray-900 mb-2">جاهز للإرسال</h2>
                <p className="text-gray-600 mb-6 max-w-md mx-auto">
                  لا يتم إرسال أي شيء تلقائيًا. اضغط الزر أدناه لإرسال طلبك إلينا عبر بريدك، وسنتواصل معك لترتيب المكالمة.
                </p>
                <a href={mailto}>
                  <Button size="lg" className="gap-2">
                    <Mail className="w-5 h-5" />
                    أرسل الطلب عبر البريد
                  </Button>
                </a>
                <div className="mt-6">
                  <button onClick={() => setSubmitted(false)} className="text-sm text-gray-400 hover:text-gray-600">
                    تعديل التفاصيل
                  </button>
                </div>
              </CardContent>
            </Card>
          )}

          <div className="mt-8 text-center">
            <Link to="/systems" className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700">
              تصفّح الأنظمة أولًا
              <ArrowLeft className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </section>
    </SiteLayout>
  )
}
