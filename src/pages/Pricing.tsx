import { Link } from "react-router";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { ArrowLeft, ShieldCheck } from "lucide-react";
import SystemsLayout from "@/components/systems/SystemsLayout";
import {
  SYSTEMS,
  formatSar,
  PRICING_NOTE,
  PRICING_DISCLAIMER,
} from "@/data/systems";
import { SYSTEM_ICONS } from "@/components/systems/icons";

// Pricing table is ordered by opening price (ascending) for clarity.
const BY_PRICE = [...SYSTEMS].sort((a, b) => a.startingPrice - b.startingPrice);

export default function Pricing() {
  return (
    <SystemsLayout>
      {/* Hero */}
      <section className="relative overflow-hidden border-b">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-teal-50" />
        <div className="relative max-w-4xl mx-auto px-4 pt-16 pb-12 text-center">
          <Badge className="mb-6 px-4 py-2 bg-emerald-100 text-emerald-800 hover:bg-emerald-100">
            أسعار Sprint افتتاحي
          </Badge>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-5 leading-tight">
            ابدأ بـ Sprint صغير، ثم وسّع حسب النتائج
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
            كل نظام يبدأ بسعر افتتاحي واضح و Sprint قصير يعطيك أول مخرج ملموس.
            بدون التزام طويل قبل أن ترى القيمة.
          </p>
        </div>
      </section>

      {/* Pricing table */}
      <section className="max-w-5xl mx-auto px-4 py-14">
        <div className="rounded-xl border overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow className="bg-gray-50">
                <TableHead className="text-right">النظام</TableHead>
                <TableHead className="text-right">السعر الافتتاحي</TableHead>
                <TableHead className="text-right">يشمل</TableHead>
                <TableHead className="text-right" />
              </TableRow>
            </TableHeader>
            <TableBody>
              {BY_PRICE.map((system) => (
                <TableRow key={system.slug}>
                  <TableCell className="font-medium text-gray-900">
                    {system.nameAr}
                    <span className="block text-xs text-gray-400">{system.name}</span>
                  </TableCell>
                  <TableCell className="font-bold text-gray-900 whitespace-nowrap">
                    {formatSar(system.startingPrice)}
                  </TableCell>
                  <TableCell className="text-gray-600">{system.priceIncludes}</TableCell>
                  <TableCell>
                    <Button asChild size="sm" variant="ghost" className="gap-1">
                      <Link to={`/systems/${system.slug}`}>
                        التفاصيل
                        <ArrowLeft className="w-4 h-4" />
                      </Link>
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
        <div className="mt-5 space-y-2">
          <p className="text-sm text-gray-500">{PRICING_NOTE}</p>
          <p className="text-sm text-gray-500">{PRICING_DISCLAIMER}</p>
        </div>
      </section>

      {/* Per-system price cards */}
      <section className="bg-gray-50 border-y">
        <div className="max-w-6xl mx-auto px-4 py-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-10 text-center">
            تفاصيل الأنظمة
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {BY_PRICE.map((system) => {
              const Icon = SYSTEM_ICONS[system.iconName];
              return (
                <Card key={system.slug} className="border-0 shadow-md flex flex-col">
                  <CardContent className="p-6 flex flex-col flex-1">
                    <div
                      className={`w-11 h-11 ${system.accent.iconBg} rounded-xl flex items-center justify-center mb-4`}
                    >
                      <Icon className={`w-5 h-5 ${system.accent.iconText}`} />
                    </div>
                    <h3 className="text-lg font-bold text-gray-900">{system.nameAr}</h3>
                    <p className="text-xs text-gray-400 mb-3">{system.name}</p>
                    <p className="text-3xl font-bold text-gray-900">
                      {formatSar(system.startingPrice)}
                    </p>
                    <p className="text-sm text-gray-500 mt-1 mb-4">
                      Sprint افتتاحي — {system.sprintDuration}
                    </p>
                    <p className="text-sm text-gray-600 flex-1">{system.priceIncludes}</p>
                    <Button asChild className="w-full mt-5 gap-2">
                      <Link to={`/systems/${system.slug}`}>
                        {system.cta}
                        <ArrowLeft className="w-4 h-4" />
                      </Link>
                    </Button>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* Trust / governance note */}
      <section className="max-w-4xl mx-auto px-4 py-16">
        <Card className="border-0 shadow-md bg-emerald-50">
          <CardContent className="p-8 flex items-start gap-4">
            <div className="shrink-0 w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center">
              <ShieldCheck className="w-6 h-6 text-emerald-600" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-gray-900 mb-2">
                تسعير شفّاف وحوكمة واضحة
              </h3>
              <p className="text-gray-700 leading-relaxed">
                هذه أسعار دخول لأول Sprint. أي مشروع كامل، أو ربط مع أنظمة خارجية،
                أو تشغيل شهري يُسعّر بعد التشخيص وباعتماد المؤسس. لا نقدّم وعودًا
                برقم محدد، بل نظامًا قابلًا للتنفيذ وتقريرًا يوضح أين القيمة.
              </p>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* CTA */}
      <section className="py-20 bg-gradient-to-br from-emerald-600 to-teal-700">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            جاهز تبدأ بأول Sprint؟
          </h2>
          <p className="text-lg text-emerald-100 mb-8">
            اختر النظام المناسب لمشكلتك الآن، أو ابدأ بتشخيص سريع ونقترح لك الأفضل.
          </p>
          <div className="flex flex-wrap gap-3 justify-center">
            <Button
              asChild
              size="lg"
              className="bg-white text-emerald-700 hover:bg-emerald-50 text-lg px-10"
            >
              <Link to="/systems">شاهد الأنظمة الخمسة</Link>
            </Button>
            <Button
              asChild
              size="lg"
              variant="outline"
              className="border-white text-white hover:bg-white/10 text-lg px-10"
            >
              <Link to="/dashboard">ابدأ بتشخيص سريع</Link>
            </Button>
          </div>
        </div>
      </section>
    </SystemsLayout>
  );
}
