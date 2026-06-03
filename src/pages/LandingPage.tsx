import { Link } from "react-router";
import SiteLayout from "@/components/site/SiteLayout";
import SystemCard from "@/components/site/SystemCard";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { systems } from "@/data/systems";
import {
  Shield,
  Lock,
  ArrowLeft,
  Sparkles,
  HelpCircle,
  ListChecks,
  Search,
  Layers,
  BrainCircuit,
} from "lucide-react";

const whyPoints = [
  "من يحتاج متابعة الآن؟",
  "ما القرار التالي؟",
  "أين تضيع الفرص؟",
  "ما العرض المناسب؟",
  "وما الذي يجب تسليمه الآن؟",
];

const howSteps = [
  { icon: Search, label: "نفهم الشركة" },
  { icon: Layers, label: "نحدد النظام المناسب" },
  { icon: ListChecks, label: "نبني أول Sprint" },
  { icon: Sparkles, label: "نجهز التقارير والمسودات" },
  { icon: ArrowLeft, label: "نربط المتابعة والتسليم" },
  { icon: BrainCircuit, label: "نوسّع حسب النتائج" },
];

export default function LandingPage() {
  return (
    <SiteLayout>
      {/* Hero */}
      <section className="relative pt-20 pb-28 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-teal-50" />
        <div className="relative max-w-5xl mx-auto px-4 text-center">
          <Badge className="mb-6 px-4 py-2 bg-emerald-100 text-emerald-800 hover:bg-emerald-100">
            <Sparkles className="w-4 h-4 ml-2" />
            أنظمة تشغيل الأعمال للشركات السعودية
          </Badge>
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            نحدد أين يتعطل عملك،
            <br />
            <span className="bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
              ثم نبني لك النظام الذي يشغّله
            </span>
          </h1>
          <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto leading-relaxed">
            نحدد أين يتعطل الإيراد أو التشغيل، ثم نبني لك نظامًا عمليًا للمتابعة،
            القرار، واتساب، العروض، أو الإيرادات. ابدأ بنظام واحد خلال أيام، ثم
            وسّعه حسب النتائج.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/diagnostic">
              <Button size="lg" className="text-lg px-8 gap-2">
                ابدأ بتشخيص سريع
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
            <Link to="/systems">
              <Button size="lg" variant="outline" className="text-lg px-8">
                شاهد الأنظمة الخمسة
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Why Dealix */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            لماذا Dealix؟
          </h2>
          <p className="text-lg text-gray-600 mb-10">
            الشركات لا تحتاج أدوات أكثر فقط. تحتاج نظامًا يحدد بوضوح:
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {whyPoints.map((p, i) => (
              <div
                key={i}
                className="flex items-center gap-3 bg-white rounded-xl border p-4 text-right"
              >
                <HelpCircle className="w-5 h-5 text-emerald-600 shrink-0" />
                <span className="text-gray-800">{p}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* The five systems */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              الأنظمة الخمسة
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              كل نظام يعالج تعطلًا محددًا، ويبدأ بـ Sprint افتتاحي بمخرجات قابلة
              للتسليم.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {systems.map((s) => (
              <SystemCard key={s.slug} system={s} />
            ))}
          </div>
          <div className="text-center mt-10">
            <Link to="/systems">
              <Button variant="outline" size="lg" className="gap-2">
                قارن بين الأنظمة
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* How we work */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-5xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-gray-900 mb-12 text-center">
            كيف نشتغل؟
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
            {howSteps.map((s, i) => (
              <div
                key={i}
                className="bg-white rounded-xl border p-6 flex items-start gap-4"
              >
                <div className="w-10 h-10 shrink-0 bg-emerald-100 rounded-xl flex items-center justify-center">
                  <s.icon className="w-5 h-5 text-emerald-600" />
                </div>
                <div>
                  <p className="text-xs text-gray-400 mb-1">خطوة {i + 1}</p>
                  <p className="text-gray-800 font-medium leading-snug">
                    {s.label}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Not just AI */}
      <section className="py-20">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">
            ليس مجرد ذكاء اصطناعي
          </h2>
          <p className="text-lg text-gray-600 leading-relaxed">
            Dealix ليس CRM عاديًا، وليس بوت واتساب، وليس وكالة تسويق. Dealix يبني
            نظام تشغيل عملي يحوّل الفوضى إلى قرارات، متابعات، عروض، وتقارير.
          </p>
        </div>
      </section>

      {/* Governance */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-6xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              حوكمة واضحة لكل إجراء
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              المسودات تُجهَّز آليًا، لكن لا شيء يُرسل أو يُنفّذ إلا بموافقتك. كل
              إجراء مسجّل.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <Card className="border-0 shadow-sm">
              <CardContent className="p-8">
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-14 h-14 bg-emerald-100 rounded-xl flex items-center justify-center">
                    <Shield className="w-7 h-7 text-emerald-600" />
                  </div>
                  <h3 className="text-xl font-bold">
                    الذكاء يجهّز. الإنسان يعتمد.
                  </h3>
                </div>
                <div className="space-y-3">
                  {[
                    "كل إجراء مسجّل في سجل واضح",
                    "قائمة موافقات قبل أي إرسال",
                    "لا إرسال تلقائي دون اعتماد",
                    "حماية البيانات وعدم تسجيل الأسرار",
                  ].map((item, i) => (
                    <div
                      key={i}
                      className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg"
                    >
                      <Lock className="w-5 h-5 text-emerald-500 shrink-0" />
                      <span className="text-gray-700">{item}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card className="border-0 shadow-sm">
              <CardContent className="p-8">
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-14 h-14 bg-blue-100 rounded-xl flex items-center justify-center">
                    <BrainCircuit className="w-7 h-7 text-blue-600" />
                  </div>
                  <h3 className="text-xl font-bold">نموذج الصلاحيات</h3>
                </div>
                <div className="space-y-2">
                  {[
                    { l: "المستوى 1: المراقبة", a: true },
                    { l: "المستوى 2: التوصية", a: true },
                    { l: "المستوى 3: تجهيز المسودات", a: true },
                    { l: "المستوى 4: التنفيذ بموافقة", a: false },
                    { l: "المستوى 5: تنفيذ ذاتي", a: false },
                  ].map((level, i) => (
                    <div
                      key={i}
                      className={`flex justify-between p-3 rounded-lg ${
                        level.a ? "bg-emerald-50" : "bg-gray-50"
                      }`}
                    >
                      <span
                        className={level.a ? "font-medium" : "text-gray-500"}
                      >
                        {level.l}
                      </span>
                      <Badge
                        variant={level.a ? "default" : "outline"}
                        className={level.a ? "bg-emerald-500" : ""}
                      >
                        {level.a ? "نشط" : "بموافقة"}
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-20 bg-gradient-to-br from-emerald-600 to-teal-700">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            ابدأ بنظام واحد خلال أيام
          </h2>
          <p className="text-xl text-emerald-50 mb-10 leading-relaxed">
            نبني نظام التشغيل المناسب لأكبر تعطل في شركتك الآن: الإيرادات، القرار
            التنفيذي، المتابعة، واتساب، أو العروض والإثبات.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/start">
              <Button
                size="lg"
                className="bg-white text-emerald-700 hover:bg-emerald-50 text-lg px-10 gap-2"
              >
                ابدأ الآن
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
            <Link to="/diagnostic">
              <Button
                size="lg"
                variant="outline"
                className="border-white text-white hover:bg-white/10 text-lg px-10"
              >
                تشخيص سريع
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </SiteLayout>
  );
}
