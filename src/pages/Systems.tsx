import { Link } from "react-router";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { ArrowLeft, Sparkles } from "lucide-react";
import SystemsLayout from "@/components/systems/SystemsLayout";
import SystemCard from "@/components/systems/SystemCard";
import { SYSTEMS, formatSar, PRICING_DISCLAIMER } from "@/data/systems";

export default function Systems() {
  return (
    <SystemsLayout>
      {/* Hero */}
      <section className="relative overflow-hidden border-b">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-teal-50" />
        <div className="relative max-w-5xl mx-auto px-4 pt-16 pb-14 text-center">
          <Badge className="mb-6 px-4 py-2 bg-emerald-100 text-emerald-800 hover:bg-emerald-100">
            <Sparkles className="w-4 h-4 ml-2" />
            خمسة أنظمة تشغيل تغطي رحلة الشركة كاملة
          </Badge>
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            اختر النظام المناسب
            <br />
            <span className="bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
              لمشكلتك الآن
            </span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto leading-relaxed">
            لا نعرض «كل شيء». نعرض خمسة أنظمة قوية تغطي أهم آلام الشركات: الإيراد،
            القرار، المتابعة، واتساب، والعروض. ابدأ بالنظام الذي يحل ألمك الآن، أو
            ابدأ بتشخيص سريع ونقترح لك الأفضل.
          </p>
          <div className="flex flex-wrap gap-3 justify-center">
            <Button asChild size="lg" className="gap-2">
              <Link to="/pricing">
                شاهد الأسعار
                <ArrowLeft className="w-5 h-5" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="outline">
              <Link to="/dashboard">ابدأ بتشخيص سريع</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Comparison table */}
      <section className="max-w-6xl mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-gray-900 mb-2 text-center">
          مقارنة سريعة
        </h2>
        <p className="text-gray-500 text-center mb-10">
          أي نظام يناسب وضعك الحالي؟
        </p>
        <div className="rounded-xl border overflow-hidden">
          <Table>
            <TableHeader>
              <TableRow className="bg-gray-50">
                <TableHead className="text-right">النظام</TableHead>
                <TableHead className="text-right">أفضل إذا عندك</TableHead>
                <TableHead className="text-right">أول نتيجة</TableHead>
                <TableHead className="text-right">يبدأ من</TableHead>
                <TableHead className="text-right" />
              </TableRow>
            </TableHeader>
            <TableBody>
              {SYSTEMS.map((system) => (
                <TableRow key={system.slug}>
                  <TableCell className="font-medium text-gray-900">
                    {system.nameAr}
                    <span className="block text-xs text-gray-400">{system.name}</span>
                  </TableCell>
                  <TableCell className="text-gray-600">{system.bestIf}</TableCell>
                  <TableCell className="text-gray-600">{system.firstResult}</TableCell>
                  <TableCell className="font-bold text-gray-900 whitespace-nowrap">
                    {formatSar(system.startingPrice)}
                  </TableCell>
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
        <p className="text-xs text-gray-400 text-center mt-4">{PRICING_DISCLAIMER}</p>
      </section>

      {/* Card grid */}
      <section className="bg-gray-50 border-t">
        <div className="max-w-6xl mx-auto px-4 py-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-10 text-center">
            الأنظمة الخمسة
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {SYSTEMS.map((system) => (
              <SystemCard key={system.slug} system={system} />
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 bg-gradient-to-br from-emerald-600 to-teal-700">
        <div className="max-w-3xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            غير متأكد أي نظام يناسبك؟
          </h2>
          <p className="text-lg text-emerald-100 mb-8">
            ابدأ بتشخيص سريع، ونقترح لك النظام الأقرب لألمك الحالي وأول Sprint
            مناسب.
          </p>
          <Button
            asChild
            size="lg"
            className="bg-white text-emerald-700 hover:bg-emerald-50 text-lg px-10"
          >
            <Link to="/dashboard">ابدأ بتشخيص سريع</Link>
          </Button>
        </div>
      </section>
    </SystemsLayout>
  );
}
