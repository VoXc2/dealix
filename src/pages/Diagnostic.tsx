import { useState } from "react";
import { Link } from "react-router";
import MarketingLayout from "@/components/marketing/MarketingLayout";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, CheckCircle, RotateCcw } from "lucide-react";
import { coreSystems, sectorSolutions } from "@/marketing/catalog";

/**
 * A lightweight, fully client-side diagnostic: pick sector -> pick need ->
 * Dealix recommends the matching core system (1 of 5). It never exposes the
 * internal 40-system routing — only the public core recommendation.
 */
export default function Diagnostic() {
  const [sectorId, setSectorId] = useState<string | null>(null);
  const [needId, setNeedId] = useState<string | null>(null);

  const sector = sectorSolutions.find((s) => s.id === sectorId);
  const need = sector?.needs.find((n) => n.id === needId);
  const recommended = need ? coreSystems.find((c) => c.id === need.coreSystem) : null;

  const reset = () => {
    setSectorId(null);
    setNeedId(null);
  };

  return (
    <MarketingLayout>
      <section className="bg-gradient-to-br from-emerald-50 via-white to-teal-50 py-16">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <Badge className="mb-4 bg-emerald-100 text-emerald-800 hover:bg-emerald-100">تشخيص سريع</Badge>
          <h1 className="text-4xl font-bold text-gray-900 mb-3">أين تضيع إيراداتك؟</h1>
          <p className="text-gray-600">خطوتان فقط: اختر قطاعك ثم احتياجك الأهم، ونقترح لك النظام الأنسب.</p>
        </div>
      </section>

      <section className="py-12">
        <div className="max-w-3xl mx-auto px-4">
          {/* Step 1: sector */}
          <Card className="border-0 shadow-md mb-6">
            <CardContent className="p-6">
              <div className="flex items-center gap-2 mb-4">
                <span className="w-7 h-7 rounded-full bg-emerald-500 text-white text-sm flex items-center justify-center">1</span>
                <h2 className="text-lg font-bold">اختر قطاعك</h2>
              </div>
              <div className="flex flex-wrap gap-2">
                {sectorSolutions.map((s) => (
                  <button
                    key={s.id}
                    onClick={() => { setSectorId(s.id); setNeedId(null); }}
                    className={`text-sm px-3 py-2 rounded-lg border transition-colors ${
                      sectorId === s.id ? "bg-emerald-500 text-white border-emerald-500" : "bg-white text-gray-700 hover:bg-emerald-50 border-gray-200"
                    }`}
                  >
                    {s.nameAr}
                  </button>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Step 2: need */}
          {sector && (
            <Card className="border-0 shadow-md mb-6">
              <CardContent className="p-6">
                <div className="flex items-center gap-2 mb-4">
                  <span className="w-7 h-7 rounded-full bg-emerald-500 text-white text-sm flex items-center justify-center">2</span>
                  <h2 className="text-lg font-bold">ما أكبر احتياج لديك؟</h2>
                </div>
                <div className="flex flex-wrap gap-2">
                  {sector.needs.map((n) => (
                    <button
                      key={n.id}
                      onClick={() => setNeedId(n.id)}
                      className={`text-sm px-3 py-2 rounded-lg border transition-colors ${
                        needId === n.id ? "bg-emerald-500 text-white border-emerald-500" : "bg-white text-gray-700 hover:bg-emerald-50 border-gray-200"
                      }`}
                    >
                      {n.nameAr}
                    </button>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Result */}
          {recommended && (
            <Card className="border-2 border-emerald-500 shadow-lg">
              <CardContent className="p-8 text-center">
                <CheckCircle className="w-10 h-10 text-emerald-500 mx-auto mb-3" />
                <p className="text-gray-500 mb-1">النظام المقترح لك</p>
                <h3 className="text-2xl font-bold text-gray-900 mb-2">{recommended.nameAr}</h3>
                <p className="text-gray-600 max-w-xl mx-auto mb-6">{recommended.promiseAr}</p>
                <div className="flex flex-wrap gap-3 justify-center">
                  <Link to={`/systems/${recommended.id}`}>
                    <Button className="gap-2">تفاصيل النظام<ArrowLeft className="w-4 h-4" /></Button>
                  </Link>
                  <Button variant="outline" className="gap-2" onClick={reset}>
                    <RotateCcw className="w-4 h-4" />ابدأ من جديد
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </section>
    </MarketingLayout>
  );
}
