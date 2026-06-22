import { useState } from "react";
import { trpc } from "@/providers/trpc";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { CalendarClock, CheckCircle, ArrowLeft, BarChart3 } from "lucide-react";

export default function Booking() {
  const [submitted, setSubmitted] = useState(false);

  const form = trpc.booking.create.useMutation({
    onSuccess: () => setSubmitted(true),
  });

  const [data, setData] = useState({
    name: "",
    company: "",
    role: "",
    website: "",
    pain: "",
    currentSystems: "",
    consentEmail: false,
    scheduledAt: "",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    form.mutate(data);
  };

  return (
    <div className="min-h-screen bg-[#F0F9F8]" dir="rtl">
      {/* Top Bar */}
      <nav className="bg-[#0A1F1E] border-b border-[#15807A]/20 px-6 py-4 flex items-center justify-between">
        <a href="/" className="flex items-center gap-3">
          <div className="w-8 h-8 bg-[#15807A] rounded-lg flex items-center justify-center">
            <BarChart3 className="w-5 h-5 text-white" />
          </div>
          <span className="text-lg font-bold text-white">Dealix</span>
        </a>
        <a
          href="/"
          className="text-sm text-[#E8F4F3] hover:text-white transition-colors flex items-center gap-1"
        >
          <ArrowLeft className="w-4 h-4" />
          العودة للرئيسية
        </a>
      </nav>

      <div className="max-w-2xl mx-auto px-4 sm:px-6 py-12">
        <Card className="bg-white border-[#E8F4F3] shadow-sm">
          <CardHeader className="text-center pb-2">
            <div className="w-14 h-14 bg-[#E8F4F3] rounded-full flex items-center justify-center mx-auto mb-4">
              <CalendarClock className="w-7 h-7 text-[#15807A]" />
            </div>
            <CardTitle className="text-2xl text-[#0A1F1E]">
              احجز تشخيص AI Revenue
            </CardTitle>
            <CardDescription className="text-[#4A6B69] mt-2">
              جلسة قصيرة (30 دقيقة) نسوي فيها Diagnostic سريع لإيرادات شركتك. بدون commitment، بدون إرسال آلي.
            </CardDescription>
          </CardHeader>

          {!submitted ? (
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-5">
                {/* Name */}
                <div>
                  <Label className="text-[#0A1F1E] text-sm">
                    الاسم الكامل <span className="text-red-500">*</span>
                  </Label>
                  <Input
                    required
                    placeholder="أحمد آل راشد"
                    value={data.name}
                    onChange={(e) => setData({ ...data, name: e.target.value })}
                    className="mt-1 border-[#E8F4F3] focus:border-[#15807A] focus:ring-[#15807A]"
                  />
                </div>

                {/* Company + Role */}
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <Label className="text-[#0A1F1E] text-sm">
                      اسم الشركة <span className="text-red-500">*</span>
                    </Label>
                    <Input
                      required
                      placeholder="مثال: Digital Rise Agency"
                      value={data.company}
                      onChange={(e) =>
                        setData({ ...data, company: e.target.value })
                      }
                      className="mt-1 border-[#E8F4F3] focus:border-[#15807A] focus:ring-[#15807A]"
                    />
                  </div>
                  <div>
                    <Label className="text-[#0A1F1E] text-sm">
                      المسمى الوظيفي <span className="text-red-500">*</span>
                    </Label>
                    <Input
                      required
                      placeholder="مثال: مدير التسويق"
                      value={data.role}
                      onChange={(e) =>
                        setData({ ...data, role: e.target.value })
                      }
                      className="mt-1 border-[#E8F4F3] focus:border-[#15807A] focus:ring-[#15807A]"
                    />
                  </div>
                </div>

                {/* Website */}
                <div>
                  <Label className="text-[#0A1F1E] text-sm">
                    الموقع الإلكتروني
                  </Label>
                  <Input
                    placeholder="https://example.sa"
                    value={data.website}
                    onChange={(e) =>
                      setData({ ...data, website: e.target.value })
                    }
                    className="mt-1 border-[#E8F4F3] focus:border-[#15807A] focus:ring-[#15807A]"
                  />
                </div>

                {/* Main Pain */}
                <div>
                  <Label className="text-[#0A1F1E] text-sm">
                    ألم رئيسي في التشغيل اليومي
                  </Label>
                  <Select
                    value={data.pain}
                    onValueChange={(v) => setData({ ...data, pain: v })}
                  >
                    <SelectTrigger className="mt-1 border-[#E8F4F3] focus:border-[#15807A] focus:ring-[#15807A]">
                      <SelectValue placeholder="اختر التحدي الأساسي..." />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="leads">
                        قلة العملاء المحتملين / صعوبة الوصول لهم
                      </SelectItem>
                      <SelectItem value="followup">
                        المتابعة تتأخر أو تضيع
                      </SelectItem>
                      <SelectItem value="reporting">
                        لا توجد تقارير واضحة للإيرادات
                      </SelectItem>
                      <SelectItem value="ai_workflows">
                        نريد AI لكن لا ندري من أين نبدأ
                      </SelectItem>
                      <SelectItem value="internal_knowledge">
                        المعرفة الداخلية مبعثرة
                      </SelectItem>
                      <SelectItem value="other">أخرى</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Current Systems */}
                <div>
                  <Label className="text-[#0A1F1E] text-sm">
                    الأنظمة الحالية
                  </Label>
                  <Select
                    value={data.currentSystems}
                    onValueChange={(v) =>
                      setData({ ...data, currentSystems: v })
                    }
                  >
                    <SelectTrigger className="mt-1 border-[#E8F4F3] focus:border-[#15807A] focus:ring-[#15807A]">
                      <SelectValue placeholder="اختر النظام الحالي..." />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="excel">Excel / Sheets</SelectItem>
                      <SelectItem value="crm">CRM (HubSpot / Zoho / Salesforce)</SelectItem>
                      <SelectItem value="whatsapp">WhatsApp فقط</SelectItem>
                      <SelectItem value="notion">Notion / Confluence</SelectItem>
                      <SelectItem value="erp">ERP (SAP / Oracle)</SelectItem>
                      <SelectItem value="other">أخرى</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Consent */}
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    id="consent"
                    checked={data.consentEmail}
                    onChange={(e) =>
                      setData({ ...data, consentEmail: e.target.checked })
                    }
                    className="w-4 h-4 accent-[#15807A]"
                  />
                  <Label
                    htmlFor="consent"
                    className="text-sm text-[#4A6B69] cursor-pointer"
                  >
                    أوافق على التواصل بالبريد الإلكتروني
                  </Label>
                </div>

                {/* Submit */}
                <Button
                  type="submit"
                  disabled={form.isPending}
                  className="w-full bg-[#15807A] hover:bg-[#0F5F5A] text-white h-12 text-base"
                >
                  {form.isPending
                    ? "جاري الحجز..."
                    : "احجز جلسة التشخيص"}
                </Button>

                <p className="text-xs text-[#8CB3B0] text-center">
                  بدون commitment. كل رسائل المتابعة تمر على مراجعة يدوية قبل الإرسال.
                </p>
              </form>
            </CardContent>
          ) : (
            <CardContent className="text-center py-12">
              <CheckCircle className="w-16 h-16 text-[#15807A] mx-auto mb-4" />
              <h3 className="text-xl font-bold text-[#0A1F1E] mb-2">
                تم إرسال طلب الحجز بنجاح
              </h3>
              <p className="text-[#4A6B69] mb-6">
                سنراجع طلبك ونحدد موعد مناسب. ستصلك رسالة تأكيد في أقرب وقت.
              </p>
              <a href="/">
                <Button className="bg-[#15807A] hover:bg-[#0F5F5A] text-white">
                  العودة للرئيسية
                </Button>
              </a>
            </CardContent>
          )}
        </Card>

        {/* Trust signals */}
        <div className="grid grid-cols-3 gap-4 mt-8">
          {[
            { label: "لا إرسال آلي", desc: "كل رسالة تمر على مراجعة" },
            { label: "30 دقيقة فقط", desc: "Diagnostic سريع ومفيد" },
            { label: "بدون commitment", desc: "قرارك الحر بعد الجلسة" },
          ].map((item) => (
            <div
              key={item.label}
              className="bg-white rounded-lg p-4 text-center border border-[#E8F4F3]"
            >
              <p className="font-bold text-[#0A1F1E] text-sm">{item.label}</p>
              <p className="text-xs text-[#4A6B69] mt-1">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
