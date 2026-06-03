import { Link } from "react-router";
import SiteLayout from "@/components/site/SiteLayout";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { systems, formatPrice, CURRENCY, accentClasses } from "@/data/systems";
import { ArrowLeft, Info, CheckCircle2, AlertCircle } from "lucide-react";

const includedNotes = [
  "تشخيص أولي لتحديد أكبر تعطل",
  "Sprint افتتاحي محدد المخرجات",
  "حزمة تسليم واضحة لكل نظام",
  "مسودات وتقارير جاهزة للمراجعة",
];

const excludedNotes = [
  "تكاليف أدوات أو اشتراكات خارجية",
  "ربط متقدم مع أنظمة طرف ثالث",
  "تشغيل شهري مستمر بعد الـ Sprint",
  "حملات إعلانية أو إنتاج محتوى",
];

export default function Pricing() {
  const sorted = [...systems].sort((a, b) => a.startingPrice - b.startingPrice);

  return (
    <SiteLayout>
      <section className="relative pt-16 pb-12 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-teal-50" />
        <div className="relative max-w-4xl mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            ابدأ Sprint واضح، ثم وسّع حسب النتائج
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
            الأسعار التالية لبداية تنفيذية صغيرة ومحددة. المشاريع الكاملة أو
            الربط مع أنظمة خارجية أو التشغيل الشهري تُسعّر بعد التشخيص.
          </p>
        </div>
      </section>

      <section className="py-10">
        <div className="max-w-5xl mx-auto px-4">
          <div className="overflow-x-auto rounded-xl border bg-white shadow-sm">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="text-right">النظام</TableHead>
                  <TableHead className="text-right">السعر الافتتاحي</TableHead>
                  <TableHead className="text-right">المدة</TableHead>
                  <TableHead className="text-right">يشمل</TableHead>
                  <TableHead className="text-right" />
                </TableRow>
              </TableHeader>
              <TableBody>
                {sorted.map((s) => (
                  <TableRow key={s.slug}>
                    <TableCell className="font-medium">
                      <Link
                        to={`/systems/${s.slug}`}
                        className={`hover:underline ${accentClasses[s.accent].text}`}
                      >
                        {s.nameAr}
                      </Link>
                      <div className="text-xs text-gray-400">{s.name}</div>
                    </TableCell>
                    <TableCell className="font-semibold whitespace-nowrap">
                      {formatPrice(s.startingPrice)} {CURRENCY}
                    </TableCell>
                    <TableCell className="text-gray-600 whitespace-nowrap">
                      {s.duration}
                    </TableCell>
                    <TableCell className="text-gray-600 text-sm max-w-xs">
                      {s.firstResult}
                    </TableCell>
                    <TableCell>
                      <Link to={`/systems/${s.slug}`}>
                        <Button variant="ghost" size="sm" className="gap-1">
                          عرض
                          <ArrowLeft className="w-4 h-4" />
                        </Button>
                      </Link>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </div>
      </section>

      <section className="py-10">
        <div className="max-w-5xl mx-auto px-4 grid grid-cols-1 md:grid-cols-2 gap-6">
          <Card className="border-0 shadow-sm">
            <CardContent className="p-6">
              <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                السعر الافتتاحي يشمل
              </h3>
              <ul className="space-y-2">
                {includedNotes.map((n, i) => (
                  <li key={i} className="flex items-start gap-2 text-gray-700">
                    <CheckCircle2 className="w-4 h-4 mt-1 text-emerald-500 shrink-0" />
                    <span>{n}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>

          <Card className="border-0 shadow-sm">
            <CardContent className="p-6">
              <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                <AlertCircle className="w-5 h-5 text-amber-600" />
                لا يشمل السعر الافتتاحي
              </h3>
              <ul className="space-y-2">
                {excludedNotes.map((n, i) => (
                  <li key={i} className="flex items-start gap-2 text-gray-700">
                    <AlertCircle className="w-4 h-4 mt-1 text-amber-500 shrink-0" />
                    <span>{n}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </div>
      </section>

      <section className="py-10">
        <div className="max-w-4xl mx-auto px-4">
          <div className="flex items-start gap-3 rounded-xl bg-blue-50 border border-blue-100 p-6">
            <Info className="w-5 h-5 text-blue-600 mt-0.5 shrink-0" />
            <p className="text-gray-700 leading-relaxed">
              هذه أسعار بداية لـ Sprint افتتاحي. النطاق النهائي يعتمد على حجم
              البيانات، القنوات، عدد الـ workflows، الربط المطلوب، واحتياج
              التشغيل المستمر — ويُحدَّد بعد التشخيص.
            </p>
          </div>
        </div>
      </section>

      <section className="py-16">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            جاهز تبدأ؟
          </h2>
          <p className="text-gray-600 mb-8">
            ابدأ بالتشخيص، ونحدد معك أكبر تعطل والنظام الأنسب لأول Sprint.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/start">
              <Button size="lg" className="gap-2">
                ابدأ بالتشخيص
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
            <Link to="/diagnostic">
              <Button size="lg" variant="outline">
                تشخيص سريع
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </SiteLayout>
  );
}
