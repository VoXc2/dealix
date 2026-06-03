import { useState } from "react";
import { Link, useSearchParams } from "react-router";
import SiteLayout from "@/components/site/SiteLayout";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { systems } from "@/data/systems";
import { ArrowLeft, CheckCircle2, Mail } from "lucide-react";

// Founder configures the real intake address here before launch.
const CONTACT_EMAIL = "founder@dealix.sa";

const steps = [
  "نفهم الشركة وأكبر تعطل",
  "نحدد النظام المناسب",
  "نبني أول Sprint بمخرجات واضحة",
  "نجهز التقارير والمسودات",
  "نربط المتابعة والتسليم",
  "نوسّع حسب النتائج",
];

export default function Start() {
  const [params] = useSearchParams();
  const preselected = params.get("system") ?? "";

  const [company, setCompany] = useState("");
  const [name, setName] = useState("");
  const [contact, setContact] = useState("");
  const [system, setSystem] = useState(preselected);
  const [note, setNote] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const canSubmit = company.trim() && name.trim() && contact.trim();

  const chosen = systems.find((s) => s.slug === system);

  function mailtoHref() {
    const subject = `طلب تشخيص Dealix — ${company || "شركة"}`;
    const body = [
      `الشركة: ${company}`,
      `الاسم: ${name}`,
      `وسيلة التواصل: ${contact}`,
      `النظام المهتم به: ${chosen ? chosen.nameAr : "غير محدد — نحتاج تشخيص"}`,
      "",
      `ملاحظات: ${note || "—"}`,
    ].join("\n");
    return `mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent(
      subject,
    )}&body=${encodeURIComponent(body)}`;
  }

  return (
    <SiteLayout>
      <section className="relative pt-16 pb-12 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-teal-50" />
        <div className="relative max-w-3xl mx-auto px-4 text-center">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            ابدأ بتشخيص سريع
          </h1>
          <p className="text-gray-600 leading-relaxed max-w-2xl mx-auto">
            أرسل لنا معلومات مختصرة عن شركتك وأكبر تعطل لديك، ونعود إليك بتصور
            مبدئي لأول Sprint مناسب — دون التزام.
          </p>
        </div>
      </section>

      <section className="py-10">
        <div className="max-w-5xl mx-auto px-4 grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Form */}
          <div className="lg:col-span-2">
            {!submitted ? (
              <Card className="border-0 shadow-md">
                <CardContent className="p-6 space-y-5">
                  <div className="space-y-2">
                    <Label htmlFor="company">اسم الشركة *</Label>
                    <Input
                      id="company"
                      value={company}
                      onChange={(e) => setCompany(e.target.value)}
                      placeholder="مثال: شركة النخبة للتدريب"
                    />
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="name">اسمك *</Label>
                      <Input
                        id="name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="الاسم"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="contact">بريد أو جوال للتواصل *</Label>
                      <Input
                        id="contact"
                        value={contact}
                        onChange={(e) => setContact(e.target.value)}
                        placeholder="email@company.sa"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="system">النظام المهتم به (اختياري)</Label>
                    <select
                      id="system"
                      value={system}
                      onChange={(e) => setSystem(e.target.value)}
                      className="w-full h-10 rounded-md border border-input bg-background px-3 text-sm"
                    >
                      <option value="">غير محدد — أحتاج تشخيص</option>
                      {systems.map((s) => (
                        <option key={s.slug} value={s.slug}>
                          {s.nameAr}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="note">
                      صف أكبر تعطل لديك الآن (اختياري)
                    </Label>
                    <Textarea
                      id="note"
                      value={note}
                      onChange={(e) => setNote(e.target.value)}
                      placeholder="مثال: تأتينا استفسارات على واتساب لكن كثير منها لا يُتابع."
                      rows={4}
                    />
                  </div>

                  <Button
                    className="w-full gap-2"
                    disabled={!canSubmit}
                    onClick={() => setSubmitted(true)}
                  >
                    تجهيز الطلب
                    <ArrowLeft className="w-4 h-4" />
                  </Button>
                  <p className="text-xs text-gray-400 text-center">
                    لا نرسل أي رسائل تلقائية. بياناتك تُستخدم فقط للتواصل بشأن
                    طلبك.
                  </p>
                </CardContent>
              </Card>
            ) : (
              <Card className="border-2 border-emerald-500 shadow-md">
                <CardContent className="p-8 text-center">
                  <div className="w-14 h-14 bg-emerald-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                    <CheckCircle2 className="w-7 h-7 text-emerald-600" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    طلبك جاهز للإرسال
                  </h2>
                  <p className="text-gray-600 mb-6 leading-relaxed">
                    راجعنا ملخص طلبك أدناه. اضغط الزر لإرساله إلينا عبر بريدك،
                    ونعود إليك بتصور مبدئي لأول Sprint.
                  </p>

                  <div className="text-right bg-gray-50 rounded-xl p-5 mb-6 space-y-2 text-sm">
                    <p>
                      <span className="text-gray-400">الشركة: </span>
                      <span className="text-gray-800 font-medium">
                        {company}
                      </span>
                    </p>
                    <p>
                      <span className="text-gray-400">الاسم: </span>
                      <span className="text-gray-800">{name}</span>
                    </p>
                    <p>
                      <span className="text-gray-400">التواصل: </span>
                      <span className="text-gray-800">{contact}</span>
                    </p>
                    <p>
                      <span className="text-gray-400">النظام: </span>
                      <span className="text-gray-800">
                        {chosen ? chosen.nameAr : "نحتاج تشخيص"}
                      </span>
                    </p>
                  </div>

                  <a href={mailtoHref()}>
                    <Button className="w-full gap-2 mb-3">
                      <Mail className="w-4 h-4" />
                      إرسال الطلب عبر البريد
                    </Button>
                  </a>
                  <button
                    onClick={() => setSubmitted(false)}
                    className="text-sm text-gray-400 hover:text-gray-700"
                  >
                    تعديل الطلب
                  </button>
                </CardContent>
              </Card>
            )}
          </div>

          {/* How we work */}
          <div>
            <Card className="border-0 shadow-sm bg-gray-50">
              <CardContent className="p-6">
                <h3 className="font-bold text-gray-900 mb-4">كيف نشتغل؟</h3>
                <ol className="space-y-3">
                  {steps.map((s, i) => (
                    <li key={i} className="flex items-start gap-3">
                      <span className="w-6 h-6 shrink-0 rounded-full bg-emerald-100 text-emerald-700 text-xs font-bold flex items-center justify-center">
                        {i + 1}
                      </span>
                      <span className="text-sm text-gray-700 leading-relaxed">
                        {s}
                      </span>
                    </li>
                  ))}
                </ol>
                <div className="mt-6 pt-6 border-t">
                  <p className="text-sm text-gray-500 mb-3">
                    لست متأكدًا أي نظام يناسبك؟
                  </p>
                  <Link to="/diagnostic">
                    <Button variant="outline" size="sm" className="w-full">
                      جرّب التشخيص السريع
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>
    </SiteLayout>
  );
}
