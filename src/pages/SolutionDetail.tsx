import { Link, useParams } from "react-router";
import MarketingLayout from "@/components/marketing/MarketingLayout";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowRight, ArrowLeft, Target } from "lucide-react";
import { coreSystems, sectorSolutions } from "@/marketing/catalog";

export default function SolutionDetail() {
  const { sector } = useParams();
  const solution = sectorSolutions.find((s) => s.id === sector);

  if (!solution) {
    return (
      <MarketingLayout>
        <div className="max-w-3xl mx-auto px-4 py-32 text-center">
          <h1 className="text-3xl font-bold mb-4">القطاع غير موجود</h1>
          <Link to="/solutions"><Button>العودة للحلول</Button></Link>
        </div>
      </MarketingLayout>
    );
  }

  const systems = coreSystems.filter((c) => solution.coreSystems.includes(c.id));

  return (
    <MarketingLayout>
      <section className="bg-gradient-to-br from-emerald-50 via-white to-teal-50 py-16">
        <div className="max-w-5xl mx-auto px-4">
          <Link to="/solutions" className="text-sm text-emerald-700 inline-flex items-center gap-1 mb-6">
            <ArrowRight className="w-4 h-4" />كل القطاعات
          </Link>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">حلول قطاع {solution.nameAr}</h1>
          <p className="text-lg text-gray-600">نبدأ من احتياجك الفعلي، ونوجّهك إلى النظام الجوهري الأنسب.</p>
        </div>
      </section>

      <section className="py-14">
        <div className="max-w-5xl mx-auto px-4">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <Target className="w-6 h-6 text-emerald-600" />أبرز الاحتياجات في هذا القطاع
          </h2>
          <div className="grid sm:grid-cols-2 gap-3 mb-12">
            {solution.needs.map((n) => (
              <div key={n.id} className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
                <div className="w-2 h-2 rounded-full bg-emerald-500" />
                <span className="text-gray-700">{n.nameAr}</span>
              </div>
            ))}
          </div>

          <h2 className="text-2xl font-bold mb-6">الأنظمة المقترحة لهذا القطاع</h2>
          <div className="grid md:grid-cols-2 gap-5">
            {systems.map((s) => (
              <Card key={s.id} className="border-0 shadow-md">
                <CardContent className="p-6">
                  <h3 className="text-lg font-bold mb-2">{s.nameAr}</h3>
                  <p className="text-gray-600 text-sm mb-4">{s.promiseAr}</p>
                  <Link to={`/systems/${s.id}`}>
                    <Button variant="outline" size="sm" className="gap-2">التفاصيل<ArrowLeft className="w-4 h-4" /></Button>
                  </Link>
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="mt-12 text-center">
            <Link to="/diagnostic">
              <Button size="lg" className="gap-2">ابدأ تشخيصًا سريعًا لقطاعك<ArrowLeft className="w-5 h-5" /></Button>
            </Link>
          </div>
        </div>
      </section>
    </MarketingLayout>
  );
}
