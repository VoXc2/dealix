import { useState } from "react";
import { Link } from "react-router";
import SiteLayout from "@/components/site/SiteLayout";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import {
  systems,
  getSystem,
  accentClasses,
  formatPrice,
  CURRENCY,
  type SystemSlug,
} from "@/data/systems";
import { ArrowLeft, RotateCcw, CheckCircle2 } from "lucide-react";

interface Option {
  label: string;
  value: SystemSlug;
}

const bottleneckQuestion = {
  title: "ما أكبر تعطل في شركتك الآن؟",
  options: [
    {
      label: "تأتينا فرص واستفسارات لكنها تضيع بلا إجراء تالٍ واضح",
      value: "revenue-operating-system" as SystemSlug,
    },
    {
      label: "المتابعة تتأخر أو تُنسى بعد أول تواصل مع العميل",
      value: "follow-up-recovery-os" as SystemSlug,
    },
    {
      label: "الإدارة لا ترى القرار اليومي وسط كثرة التقارير",
      value: "executive-command-os" as SystemSlug,
    },
    {
      label: "واتساب قناتنا الرئيسية لكنه مزدحم بلا نظام",
      value: "whatsapp-client-os" as SystemSlug,
    },
    {
      label: "عروضنا ضعيفة أو بطيئة ولا توضح الدليل",
      value: "proposal-proof-os" as SystemSlug,
    },
  ] satisfies Option[],
};

const channelQuestion = {
  title: "ما القناة الأساسية لوصول عملائك؟",
  options: [
    "واتساب",
    "المكالمات والاتصال المباشر",
    "البريد والنماذج على الموقع",
    "إحالات وعلاقات",
  ],
};

export default function Diagnostic() {
  const [step, setStep] = useState(0);
  const [bottleneck, setBottleneck] = useState<SystemSlug | null>(null);
  const [channel, setChannel] = useState<string | null>(null);

  const totalSteps = 2;
  const progress = (step / totalSteps) * 100;

  const recommended = bottleneck ? getSystem(bottleneck) : undefined;

  function reset() {
    setStep(0);
    setBottleneck(null);
    setChannel(null);
  }

  return (
    <SiteLayout>
      <section className="relative pt-16 pb-12 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-teal-50" />
        <div className="relative max-w-2xl mx-auto px-4 text-center">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            تشخيص سريع
          </h1>
          <p className="text-gray-600 leading-relaxed">
            أجب عن سؤالين قصيرين ونقترح عليك النظام الأنسب لأكبر تعطل لديك الآن.
            هذا اقتراح أولي، والتشخيص الكامل يتم قبل أي Sprint.
          </p>
        </div>
      </section>

      <section className="py-10">
        <div className="max-w-2xl mx-auto px-4">
          {step < totalSteps && (
            <div className="mb-8">
              <Progress value={progress} className="h-2" />
              <p className="text-sm text-gray-400 mt-2 text-center">
                خطوة {step + 1} من {totalSteps}
              </p>
            </div>
          )}

          {/* Step 0: bottleneck */}
          {step === 0 && (
            <Card className="border-0 shadow-md">
              <CardContent className="p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-6">
                  {bottleneckQuestion.title}
                </h2>
                <div className="space-y-3">
                  {bottleneckQuestion.options.map((o) => (
                    <button
                      key={o.value}
                      onClick={() => {
                        setBottleneck(o.value);
                        setStep(1);
                      }}
                      className={`w-full text-right p-4 rounded-xl border transition-all hover:border-emerald-400 hover:bg-emerald-50/50 ${
                        bottleneck === o.value
                          ? "border-emerald-500 bg-emerald-50"
                          : "border-gray-200"
                      }`}
                    >
                      <span className="text-gray-800">{o.label}</span>
                    </button>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Step 1: channel */}
          {step === 1 && (
            <Card className="border-0 shadow-md">
              <CardContent className="p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-6">
                  {channelQuestion.title}
                </h2>
                <div className="space-y-3">
                  {channelQuestion.options.map((o) => (
                    <button
                      key={o}
                      onClick={() => {
                        setChannel(o);
                        setStep(2);
                      }}
                      className={`w-full text-right p-4 rounded-xl border transition-all hover:border-emerald-400 hover:bg-emerald-50/50 ${
                        channel === o
                          ? "border-emerald-500 bg-emerald-50"
                          : "border-gray-200"
                      }`}
                    >
                      <span className="text-gray-800">{o}</span>
                    </button>
                  ))}
                </div>
                <button
                  onClick={() => setStep(0)}
                  className="mt-6 text-sm text-gray-400 hover:text-gray-700"
                >
                  رجوع
                </button>
              </CardContent>
            </Card>
          )}

          {/* Result */}
          {step === 2 && recommended && (
            <Result
              slug={recommended.slug}
              channel={channel}
              onReset={reset}
            />
          )}
        </div>
      </section>
    </SiteLayout>
  );
}

function Result({
  slug,
  channel,
  onReset,
}: {
  slug: SystemSlug;
  channel: string | null;
  onReset: () => void;
}) {
  const system = getSystem(slug)!;
  const accent = accentClasses[system.accent];
  const Icon = system.icon;
  const secondary = systems.filter((s) => s.slug !== slug).slice(0, 2);

  return (
    <div>
      <div className="text-center mb-6">
        <div className="inline-flex items-center gap-2 text-sm text-emerald-600 font-medium mb-2">
          <CheckCircle2 className="w-4 h-4" />
          النظام المقترح لك
        </div>
      </div>

      <Card className={`border-2 ${accent.border} shadow-lg`}>
        <CardContent className="p-8">
          <div className="flex items-start gap-4 mb-4">
            <div
              className={`w-14 h-14 shrink-0 ${accent.bgSoft} rounded-2xl flex items-center justify-center`}
            >
              <Icon className={`w-7 h-7 ${accent.text}`} />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">
                {system.nameAr}
              </h2>
              <p className="text-gray-400 font-medium text-sm">{system.name}</p>
            </div>
          </div>

          <p className="text-gray-700 leading-relaxed mb-4">{system.hero}</p>

          {channel && (
            <p className="text-sm text-gray-500 mb-6">
              بما أن قناتك الأساسية هي{" "}
              <span className="font-medium text-gray-700">{channel}</span>،
              سنبدأ الـ Sprint من حيث يصلك العملاء فعلًا.
            </p>
          )}

          <div className="rounded-xl bg-gray-50 p-4 mb-6">
            <p className="text-xs text-gray-400 mb-1">أول نتيجة</p>
            <p className="text-gray-800 font-medium">{system.firstResult}</p>
          </div>

          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div>
              <span className="text-sm text-gray-500">يبدأ من </span>
              <span className={`text-2xl font-bold ${accent.text}`}>
                {formatPrice(system.startingPrice)}
              </span>
              <span className="text-sm text-gray-500"> {CURRENCY}</span>
            </div>
            <div className="flex gap-3">
              <Link to={`/systems/${system.slug}`}>
                <Button variant="outline" className="gap-2">
                  تفاصيل النظام
                </Button>
              </Link>
              <Link to="/start">
                <Button className={`gap-2 ${accent.button}`}>
                  {system.cta}
                  <ArrowLeft className="w-4 h-4" />
                </Button>
              </Link>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="mt-8">
        <p className="text-sm text-gray-500 mb-3">أنظمة أخرى قد تهمك:</p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {secondary.map((s) => (
            <Link key={s.slug} to={`/systems/${s.slug}`}>
              <Card className="border-0 shadow-sm hover:shadow-md transition-shadow">
                <CardContent className="p-4 flex items-center gap-3">
                  <div
                    className={`w-9 h-9 ${accentClasses[s.accent].bgSoft} rounded-lg flex items-center justify-center shrink-0`}
                  >
                    <s.icon
                      className={`w-4 h-4 ${accentClasses[s.accent].text}`}
                    />
                  </div>
                  <span className="text-sm text-gray-700">{s.nameAr}</span>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      </div>

      <div className="text-center mt-8">
        <button
          onClick={onReset}
          className="inline-flex items-center gap-1 text-sm text-gray-400 hover:text-gray-700"
        >
          <RotateCcw className="w-4 h-4" />
          إعادة التشخيص
        </button>
      </div>
    </div>
  );
}
