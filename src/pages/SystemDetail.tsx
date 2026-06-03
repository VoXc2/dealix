import { Link, useParams } from "react-router";
import MarketingLayout from "@/components/marketing/MarketingLayout";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { CheckCircle, ArrowRight, ArrowLeft } from "lucide-react";
import { coreSystems, sectorSolutions } from "@/marketing/catalog";

export default function SystemDetail() {
  const { slug } = useParams();
  const system = coreSystems.find((s) => s.id === slug);

  if (!system) {
    return (
      <MarketingLayout>
        <div className="max-w-3xl mx-auto px-4 py-32 text-center">
          <h1 className="text-3xl font-bold mb-4">النظام غير موجود</h1>
          <Link to="/systems"><Button>العودة للأنظمة</Button></Link>
        </div>
      </MarketingLayout>
    );
  }

  const outcomes = system.outcomeAr.split("+").map((s) => s.trim()).filter(Boolean);
  const relatedSectors = sectorSolutions.filter((sec) => sec.coreSystems.includes(system.id)).slice(0, 6);

  return (
    <MarketingLayout>
      <section className="bg-gradient-to-br from-emerald-50 via-white to-teal-50 py-16">
        <div className="max-w-5xl mx-auto px-4">
          <Link to="/systems" className="text-sm text-emerald-700 inline-flex items-center gap-1 mb-6">
            <ArrowRight className="w-4 h-4" />كل الأنظمة
          </Link>
          <Badge className="mb-4 bg-emerald-100 text-emerald-800 hover:bg-emerald-100">{system.nameEn}</Badge>
          <h1 className="text-4xl font-bold text-gray-900 mb-4">{system.nameAr}</h1>
          <p className="text-xl text-gray-600 max-w-3xl">{system.promiseAr}</p>
        </div>
      </section>

      <section className="py-14">
        <div className="max-w-5xl mx-auto px-4 grid md:grid-cols-2 gap-8">
          <Card className="border-0 shadow-md">
            <CardContent className="p-8">
              <h2 className="text-2xl font-bold mb-6">ماذا تستلم</h2>
              <ul className="space-y-4">
                {outcomes.map((o, i) => (
                  <li key={i} className="flex items-start gap-3">
                    <CheckCircle className="w-5 h-5 text-emerald-500 mt-0.5 shrink-0" />
                    <span className="text-gray-700">{o}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
          <Card className="border-0 shadow-md bg-gray-900 text-white">
            <CardContent className="p-8">
              <h2 className="text-2xl font-bold mb-4">كيف نبدأ</h2>
              <p className="text-gray-300 mb-6">
                نبدأ بسبرنت قصير محدد المخرجات وسعر مبدئي ثابت — تقيس القيمة قبل أي التزام أكبر. بلا وعود مضمونة، وبمعايير قبول واضحة.
              </p>
              <Link to="/diagnostic">
                <Button className="w-full bg-emerald-500 hover:bg-emerald-600 gap-2">
                  ابدأ بتشخيص سريع<ArrowLeft className="w-4 h-4" />
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>

        {relatedSectors.length > 0 && (
          <div className="max-w-5xl mx-auto px-4 mt-12">
            <h3 className="text-lg font-bold text-gray-900 mb-4">قطاعات يخدمها هذا النظام</h3>
            <div className="flex flex-wrap gap-3">
              {relatedSectors.map((sec) => (
                <Link key={sec.id} to={`/solutions/${sec.id}`}>
                  <Badge variant="outline" className="px-4 py-2 hover:bg-emerald-50 cursor-pointer">{sec.nameAr}</Badge>
                </Link>
              ))}
            </div>
          </div>
        )}
      </section>
    </MarketingLayout>
  );
}
