import { Link } from "react-router";
import MarketingLayout from "@/components/marketing/MarketingLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft } from "lucide-react";
import { sectorSolutions } from "@/marketing/catalog";

export default function Solutions() {
  return (
    <MarketingLayout>
      <section className="bg-gradient-to-br from-emerald-50 via-white to-teal-50 py-20">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <Badge className="mb-4 bg-emerald-100 text-emerald-800 hover:bg-emerald-100">20 قطاعًا</Badge>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">حلول حسب قطاعك</h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            لكل قطاع احتياجاته. نختار لك النظام الجوهري الأنسب ونبدأ بسبرنت محدد المخرجات.
          </p>
        </div>
      </section>

      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {sectorSolutions.map((sec) => (
            <Link key={sec.id} to={`/solutions/${sec.id}`}>
              <Card className="border-0 shadow-md hover:shadow-lg transition-shadow h-full">
                <CardHeader>
                  <CardTitle className="text-lg flex items-center justify-between">
                    {sec.nameAr}
                    <ArrowLeft className="w-4 h-4 text-emerald-500" />
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-500 mb-2">أبرز الاحتياجات:</p>
                  <div className="flex flex-wrap gap-2">
                    {sec.needs.slice(0, 3).map((n) => (
                      <span key={n.id} className="text-xs bg-emerald-50 text-emerald-700 px-2 py-1 rounded">{n.nameAr}</span>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      </section>
    </MarketingLayout>
  );
}
