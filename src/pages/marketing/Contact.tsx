import { useState } from 'react'
import { Mail, MessageSquare, CheckCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import SiteLayout from '@/components/site/SiteLayout'
import { buildMailto, CONTACT_EMAIL } from '@/lib/contact'

export default function Contact() {
  const [name, setName] = useState('')
  const [message, setMessage] = useState('')
  const [sent, setSent] = useState(false)
  const mailto = buildMailto('استفسار من موقع Dealix', `الاسم: ${name}\n\n${message}`)

  return (
    <SiteLayout>
      <section className="relative pt-16 pb-10 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-teal-50" />
        <div className="relative max-w-2xl mx-auto px-4 text-center">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900">تواصل معنا</h1>
          <p className="text-gray-600 mt-3">سؤال سريع أو رغبة في معرفة النظام الأنسب؟ نرد عادة خلال يوم عمل.</p>
        </div>
      </section>

      <section className="pb-20">
        <div className="max-w-2xl mx-auto px-4 grid grid-cols-1 md:grid-cols-5 gap-6">
          <Card className="md:col-span-3 shadow-md border-0">
            <CardContent className="p-8">
              {!sent ? (
                <form
                  onSubmit={(e) => {
                    e.preventDefault()
                    setSent(true)
                  }}
                  className="space-y-5"
                >
                  <div>
                    <Label htmlFor="cname">الاسم</Label>
                    <Input id="cname" value={name} onChange={(e) => setName(e.target.value)} required className="mt-1.5" placeholder="اسمك" />
                  </div>
                  <div>
                    <Label htmlFor="cmsg">رسالتك</Label>
                    <Textarea id="cmsg" value={message} onChange={(e) => setMessage(e.target.value)} required rows={5} className="mt-1.5" placeholder="كيف نقدر نساعدك؟" />
                  </div>
                  <Button type="submit" className="w-full" size="lg">متابعة</Button>
                </form>
              ) : (
                <div className="text-center py-6">
                  <div className="w-14 h-14 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <CheckCircle className="w-7 h-7 text-emerald-600" />
                  </div>
                  <p className="text-gray-600 mb-6">اضغط لإرسال رسالتك عبر بريدك — لا يتم إرسال أي شيء تلقائيًا.</p>
                  <a href={mailto}>
                    <Button size="lg" className="gap-2">
                      <Mail className="w-5 h-5" />
                      أرسل الرسالة
                    </Button>
                  </a>
                </div>
              )}
            </CardContent>
          </Card>

          <div className="md:col-span-2 space-y-4">
            <Card className="shadow-md border-0">
              <CardContent className="p-6">
                <Mail className="w-6 h-6 text-emerald-600 mb-2" />
                <h3 className="font-bold text-gray-900 mb-1">البريد</h3>
                <a href={`mailto:${CONTACT_EMAIL}`} className="text-emerald-600 text-sm hover:underline break-all">
                  {CONTACT_EMAIL}
                </a>
              </CardContent>
            </Card>
            <Card className="shadow-md border-0">
              <CardContent className="p-6">
                <MessageSquare className="w-6 h-6 text-emerald-600 mb-2" />
                <h3 className="font-bold text-gray-900 mb-1">تفضّل البدء بسرعة؟</h3>
                <p className="text-gray-600 text-sm">جرّب التشخيص السريع لاقتراح النظام الأنسب خلال أقل من دقيقة.</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
    </SiteLayout>
  )
}
