import { useParams, Link } from "react-router";
import { Button } from "@/components/ui/button";
import { AlertTriangle, ArrowLeft } from "lucide-react";
import SystemsLayout from "@/components/systems/SystemsLayout";
import SystemHero from "@/components/systems/SystemHero";
import SystemBenefits from "@/components/systems/SystemBenefits";
import SystemDeliveryPack from "@/components/systems/SystemDeliveryPack";
import SystemPricing from "@/components/systems/SystemPricing";
import SystemFAQ from "@/components/systems/SystemFAQ";
import { getSystem } from "@/data/systems";

export default function SystemDetail() {
  const { slug } = useParams();
  const system = getSystem(slug);

  if (!system) {
    return (
      <SystemsLayout>
        <section className="max-w-3xl mx-auto px-4 py-24 text-center">
          <AlertTriangle className="w-10 h-10 text-amber-500 mx-auto mb-4" />
          <h1 className="text-3xl font-bold text-gray-900 mb-3">
            النظام غير موجود
          </h1>
          <p className="text-gray-600 mb-8">
            الرابط الذي طلبته لا يطابق أيًا من الأنظمة الخمسة.
          </p>
          <Button asChild className="gap-2">
            <Link to="/systems">
              عرض الأنظمة الخمسة
              <ArrowLeft className="w-4 h-4" />
            </Link>
          </Button>
        </section>
      </SystemsLayout>
    );
  }

  return (
    <SystemsLayout>
      <SystemHero system={system} />

      {/* Pain statement */}
      <section className="max-w-5xl mx-auto px-4 pt-12">
        <div
          className={`rounded-2xl border bg-gray-50 p-6 md:p-8 border-r-4 ${system.accent.border}`}
        >
          <p className="text-sm font-medium text-gray-400 mb-2">الألم الذي يحله</p>
          <p className="text-lg text-gray-800 leading-relaxed">{system.pain}</p>
        </div>
      </section>

      <SystemBenefits system={system} />
      <SystemDeliveryPack system={system} />
      <SystemPricing system={system} />
      <SystemFAQ system={system} />

      {/* Closing CTA */}
      <section
        className={`py-16 bg-gradient-to-br ${system.accent.gradient}`}
      >
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">{system.cta}</h2>
          <p className="text-lg text-white/90 mb-8">
            ابدأ بـ Sprint افتتاحي صغير، ثم وسّع حسب النتائج.
          </p>
          <div className="flex flex-wrap gap-3 justify-center">
            <Button
              asChild
              size="lg"
              className="bg-white text-gray-900 hover:bg-gray-100 text-lg px-10"
            >
              <Link to="/pricing">شاهد الأسعار</Link>
            </Button>
            <Button
              asChild
              size="lg"
              variant="outline"
              className="border-white text-white hover:bg-white/10 text-lg px-10"
            >
              <Link to="/systems">بقية الأنظمة</Link>
            </Button>
          </div>
        </div>
      </section>
    </SystemsLayout>
  );
}
