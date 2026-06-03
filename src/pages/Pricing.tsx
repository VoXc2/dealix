import { Link } from "react-router";
import MarketingLayout from "@/components/marketing/MarketingLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { CheckCircle, ArrowLeft } from "lucide-react";

const TIERS = [
  {
    name: "سبرنت تأسيسي",
    tag: "Starter",
    price: "2,500",
    highlight: false,
    points: ["تشخيص سريع لاحتياج واحد", "خطة تنفيذ 30 يومًا", "قوالب جاهزة", "تقرير قيمة"],
  },
  {
    name: "سبرنت متكامل",
    tag: "Standard",
    price: "5,000",
    highlight: true,
    points: ["تنفيذ كامل لنظام جوهري", "قوالب + لوحة متابعة", "تدريب فريقك (جلسة)", "مراجعة بعد أسبوعين"],
  },
  {
    name: "تشغيل شهري",
    tag: "Retainer",
    price: "من 9,000",
    highlight: false,
    points: ["تشغيل مستمر للنظام", "تقرير قيمة أسبوعي", "تحسين مستمر للرسائل", "أولويات يومية للمؤسس"],
  },
];

export default function Pricing() {
  return (
    <MarketingLayout>
      <section className="bg-gradient-to-br from-emerald-50 via-white to-teal-50 py-20">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <Badge className="mb-4 bg-emerald-100 text-emerald-800 hover:bg-emerald-100">أسعار مبدئية ثابتة</Badge>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">ابدأ صغيرًا، اقِس القيمة</h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            كل نظام يبدأ بسبرنت قصير محدد المخرجات. لا التزام طويل قبل إثبات القيمة، ولا وعود مضمونة.
          </p>
        </div>
      </section>

      <section className="py-16">
        <div className="max-w-5xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-6">
          {TIERS.map((t) => (
            <Card key={t.name} className={t.highlight ? "border-2 border-emerald-500 shadow-xl relative" : "border-0 shadow-md"}>
              {t.highlight && (
                <Badge className="absolute -top-3 left-1/2 -translate-x-1/2 bg-emerald-500">الأكثر شيوعًا</Badge>
              )}
              <CardHeader className="text-center pb-2">
                <p className="text-xs text-gray-400">{t.tag}</p>
                <CardTitle className="text-lg text-gray-700">{t.name}</CardTitle>
                <div className={`text-4xl font-bold mt-2 ${t.highlight ? "text-emerald-600" : "text-gray-900"}`}>
                  {t.price} <span className="text-base font-normal">ر.س</span>
                </div>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3 mb-6">
                  {t.points.map((p, i) => (
                    <li key={i} className="flex items-center gap-2">
                      <CheckCircle className="w-4 h-4 text-emerald-500 shrink-0" />
                      <span className="text-sm text-gray-700">{p}</span>
                    </li>
                  ))}
                </ul>
                <Link to="/diagnostic">
                  <Button className={`w-full gap-2 ${t.highlight ? "" : "variant-outline"}`} variant={t.highlight ? "default" : "outline"}>
                    ابدأ<ArrowLeft className="w-4 h-4" />
                  </Button>
                </Link>
              </CardContent>
            </Card>
          ))}
        </div>
        <p className="text-center text-sm text-gray-400 mt-8">
          الأسعار مبدئية وتُحدَّد نهائيًا بعد التشخيص حسب نطاق العمل. كل عرض يحتاج اعتمادك قبل البدء.
        </p>
      </section>
    </MarketingLayout>
  );
}
