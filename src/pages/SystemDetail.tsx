import { Link, useParams } from "react-router";
import SiteLayout from "@/components/site/SiteLayout";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import {
  getSystem,
  systems,
  accentClasses,
  formatPrice,
  CURRENCY,
} from "@/data/systems";
import {
  CheckCircle2,
  ArrowLeft,
  Target,
  Package,
  CalendarClock,
  Users,
  Sparkles,
  XCircle,
} from "lucide-react";

const alternatives = [
  {
    label: "ليس CRM فقط",
    desc: "الـ CRM يخزن البيانات. Dealix يحدد الإجراء التالي، يجهز الرسائل، ويرفع القرار للإدارة.",
  },
  {
    label: "ليس وكالة تسويق",
    desc: "لا نبيعك حملات إعلانية. نرتب ما لديك من فرص ومتابعات وعروض إلى نظام تشغيل واضح.",
  },
  {
    label: "ليس بوت واتساب عام",
    desc: "لا نطلق بوتًا مفتوحًا. نبني مسارات وبطاقات إجراء تعمل بعد اهتمام العميل مع تصعيد للإنسان.",
  },
];

export default function SystemDetail() {
  const { slug } = useParams();
  const system = slug ? getSystem(slug) : undefined;

  if (!system) {
    return (
      <SiteLayout>
        <div className="max-w-2xl mx-auto px-4 py-32 text-center">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            النظام غير موجود
          </h1>
          <p className="text-gray-600 mb-8">
            الرابط الذي فتحته لا يطابق أيًا من الأنظمة الخمسة.
          </p>
          <Link to="/systems">
            <Button className="gap-2">
              عودة إلى الأنظمة
              <ArrowLeft className="w-4 h-4" />
            </Button>
          </Link>
        </div>
      </SiteLayout>
    );
  }

  const accent = accentClasses[system.accent];
  const Icon = system.icon;
  const others = systems.filter((s) => s.slug !== system.slug).slice(0, 3);

  return (
    <SiteLayout>
      {/* Hero */}
      <section className="relative pt-16 pb-16 overflow-hidden">
        <div
          className={`absolute inset-0 bg-gradient-to-br ${accent.gradient} opacity-[0.07]`}
        />
        <div className="relative max-w-5xl mx-auto px-4">
          <Link
            to="/systems"
            className="inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-800 mb-6"
          >
            <ArrowLeft className="w-4 h-4" />
            كل الأنظمة
          </Link>
          <div className="flex items-start gap-4 mb-6">
            <div
              className={`w-14 h-14 shrink-0 ${accent.bgSoft} rounded-2xl flex items-center justify-center`}
            >
              <Icon className={`w-7 h-7 ${accent.text}`} />
            </div>
            <div>
              <h1 className="text-3xl md:text-5xl font-bold text-gray-900 leading-tight">
                {system.nameAr}
              </h1>
              <p className="text-gray-400 font-medium mt-1">{system.name}</p>
            </div>
          </div>
          <p className="text-lg md:text-xl text-gray-700 leading-relaxed max-w-3xl mb-6">
            {system.hero}
          </p>
          <p className="text-base text-gray-600 leading-relaxed max-w-3xl mb-8">
            <span className="font-semibold text-gray-900">المشكلة: </span>
            {system.painShort}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center">
            <Link to="/start">
              <Button size="lg" className={`gap-2 ${accent.button}`}>
                {system.cta}
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
            <div className="text-gray-600">
              <span className="text-sm">يبدأ من </span>
              <span className={`text-2xl font-bold ${accent.text}`}>
                {formatPrice(system.startingPrice)}
              </span>
              <span className="text-sm"> {CURRENCY}</span>
              <span className="text-sm text-gray-400">
                {" "}
                · {system.duration}
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Who is it for */}
      <section className="py-12 bg-gray-50">
        <div className="max-w-5xl mx-auto px-4">
          <div className="flex items-center gap-2 mb-6">
            <Users className={`w-5 h-5 ${accent.text}`} />
            <h2 className="text-2xl font-bold text-gray-900">من يناسبه؟</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {system.whoFor.map((w, i) => (
              <Card key={i} className="border-0 shadow-sm">
                <CardContent className="p-6 text-gray-700 leading-relaxed">
                  {w}
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits */}
      <section className="py-12">
        <div className="max-w-5xl mx-auto px-4">
          <div className="flex items-center gap-2 mb-6">
            <Sparkles className={`w-5 h-5 ${accent.text}`} />
            <h2 className="text-2xl font-bold text-gray-900">
              ماذا يستفيد العميل؟
            </h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {system.benefits.map((b, i) => (
              <div key={i} className="flex items-start gap-3">
                <CheckCircle2
                  className={`w-5 h-5 mt-0.5 shrink-0 ${accent.text}`}
                />
                <span className="text-gray-700 leading-relaxed">{b}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* First sprint + delivery pack */}
      <section className="py-12 bg-gray-50">
        <div className="max-w-5xl mx-auto px-4 grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <CalendarClock className={`w-5 h-5 ${accent.text}`} />
              <h2 className="text-2xl font-bold text-gray-900">
                أول Sprint
              </h2>
            </div>
            <Badge className={`mb-4 ${accent.bgSoft} ${accent.text} border-0`}>
              خلال {system.firstSprint.window}
            </Badge>
            <p className="text-gray-700 leading-relaxed mb-6">
              {system.firstSprint.summary}
            </p>
            <Card className="border-0 shadow-sm">
              <CardContent className="p-6">
                <div className="flex items-center gap-2 mb-2 text-gray-900 font-semibold">
                  <Target className={`w-5 h-5 ${accent.text}`} />
                  أول نتيجة ملموسة
                </div>
                <p className="text-gray-700">{system.firstResult}</p>
              </CardContent>
            </Card>
          </div>

          <div>
            <div className="flex items-center gap-2 mb-4">
              <Package className={`w-5 h-5 ${accent.text}`} />
              <h2 className="text-2xl font-bold text-gray-900">
                حزمة التسليم
              </h2>
            </div>
            <Card className="border-0 shadow-sm">
              <CardContent className="p-6 space-y-3">
                {system.deliveryPack.map((d, i) => (
                  <div key={i} className="flex items-start gap-3">
                    <CheckCircle2
                      className={`w-5 h-5 mt-0.5 shrink-0 ${accent.text}`}
                    />
                    <span className="text-gray-700">{d}</span>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Pricing band */}
      <section className="py-12">
        <div className="max-w-5xl mx-auto px-4">
          <Card className={`border-2 ${accent.border} shadow-md`}>
            <CardContent className="p-8 flex flex-col md:flex-row md:items-center md:justify-between gap-6">
              <div>
                <p className="text-sm text-gray-500 mb-1">
                  السعر الافتتاحي ({system.duration})
                </p>
                <p className="text-4xl font-bold text-gray-900">
                  {formatPrice(system.startingPrice)}{" "}
                  <span className="text-lg font-normal text-gray-500">
                    {CURRENCY}
                  </span>
                </p>
                <p className="text-sm text-gray-500 mt-2 max-w-md">
                  سعر بداية لـ Sprint تنفيذي محدد. لا يشمل أدوات خارجية أو
                  اشتراكات أو ربطًا متقدمًا أو تشغيلًا شهريًا مستمرًا.
                </p>
              </div>
              <Link to="/start">
                <Button size="lg" className={`gap-2 ${accent.button}`}>
                  {system.cta}
                  <ArrowLeft className="w-5 h-5" />
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Alternatives */}
      <section className="py-12 bg-gray-50">
        <div className="max-w-5xl mx-auto px-4">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
            وش الفرق عن CRM أو وكالة أو بوت؟
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {alternatives.map((a, i) => (
              <Card key={i} className="border-0 shadow-sm">
                <CardContent className="p-6">
                  <div className="flex items-center gap-2 mb-2 font-semibold text-gray-900">
                    <XCircle className="w-5 h-5 text-gray-400" />
                    {a.label}
                  </div>
                  <p className="text-gray-600 text-sm leading-relaxed">
                    {a.desc}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="py-12">
        <div className="max-w-3xl mx-auto px-4">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
            أسئلة شائعة
          </h2>
          <Accordion type="single" collapsible className="w-full">
            {system.faq.map((f, i) => (
              <AccordionItem key={i} value={`item-${i}`}>
                <AccordionTrigger className="text-right text-gray-900 font-medium">
                  {f.q}
                </AccordionTrigger>
                <AccordionContent className="text-gray-600 leading-relaxed">
                  {f.a}
                </AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>
      </section>

      {/* Other systems */}
      <section className="py-12 bg-gray-50">
        <div className="max-w-5xl mx-auto px-4">
          <h2 className="text-xl font-bold text-gray-900 mb-6">
            أنظمة أخرى قد تناسبك
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {others.map((s) => (
              <Link
                key={s.slug}
                to={`/systems/${s.slug}`}
                className="block group"
              >
                <Card className="border-0 shadow-sm group-hover:shadow-md transition-shadow h-full">
                  <CardContent className="p-6">
                    <div
                      className={`w-10 h-10 ${accentClasses[s.accent].bgSoft} rounded-lg flex items-center justify-center mb-3`}
                    >
                      <s.icon
                        className={`w-5 h-5 ${accentClasses[s.accent].text}`}
                      />
                    </div>
                    <p className="font-semibold text-gray-900 mb-1">
                      {s.nameAr}
                    </p>
                    <p className="text-sm text-gray-500">{s.painShort}</p>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section
        className={`py-16 bg-gradient-to-br ${accent.gradient}`}
      >
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">{system.cta}</h2>
          <p className="text-white/90 mb-8 leading-relaxed">
            ابدأ بنظام واحد خلال أيام، ثم وسّعه حسب النتائج. نبدأ بتشخيص سريع ثم
            أول Sprint محدد المخرجات.
          </p>
          <Link to="/start">
            <Button
              size="lg"
              className="bg-white text-gray-900 hover:bg-gray-100 gap-2"
            >
              ابدأ الآن
              <ArrowLeft className="w-5 h-5" />
            </Button>
          </Link>
        </div>
      </section>
    </SiteLayout>
  );
}
