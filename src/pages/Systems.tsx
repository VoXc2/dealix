import { Link } from "react-router";
import SiteLayout from "@/components/site/SiteLayout";
import SystemCard from "@/components/site/SystemCard";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { systems, formatPrice, CURRENCY, accentClasses } from "@/data/systems";
import { ArrowLeft } from "lucide-react";

export default function Systems() {
  return (
    <SiteLayout>
      <section className="relative pt-16 pb-12 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 via-white to-teal-50" />
        <div className="relative max-w-5xl mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6 leading-tight">
            اختر النظام الذي يعالج أكبر تعطل في شركتك الآن
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto leading-relaxed">
            كل نظام يبدأ بـ Sprint افتتاحي واضح، بمخرجات قابلة للتسليم، ثم يمكن
            توسيعه إلى نظام أعمق حسب حجم الشركة.
          </p>
        </div>
      </section>

      <section className="py-12">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {systems.map((s) => (
              <SystemCard key={s.slug} system={s} />
            ))}
          </div>
        </div>
      </section>

      <section className="py-12 bg-gray-50">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">
            مقارنة سريعة بين الأنظمة
          </h2>
          <div className="overflow-x-auto rounded-xl border bg-white shadow-sm">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead className="text-right">النظام</TableHead>
                  <TableHead className="text-right">أفضل إذا عندك</TableHead>
                  <TableHead className="text-right">أول نتيجة</TableHead>
                  <TableHead className="text-right">السعر الافتتاحي</TableHead>
                  <TableHead className="text-right" />
                </TableRow>
              </TableHeader>
              <TableBody>
                {systems.map((s) => (
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
                    <TableCell className="text-gray-600 text-sm max-w-xs">
                      {s.painShort}
                    </TableCell>
                    <TableCell className="text-gray-600 text-sm max-w-xs">
                      {s.firstResult}
                    </TableCell>
                    <TableCell className="font-semibold whitespace-nowrap">
                      {formatPrice(s.startingPrice)} {CURRENCY}
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
          <p className="text-xs text-gray-400 text-center mt-4">
            الأسعار أسعار بداية لـ Sprint افتتاحي محدد. المشاريع الكاملة أو الربط
            مع أنظمة خارجية أو التشغيل الشهري تُسعّر بعد التشخيص.
          </p>
        </div>
      </section>

      <section className="py-16">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            غير متأكد أي نظام يناسبك؟
          </h2>
          <p className="text-gray-600 mb-8">
            ابدأ بتشخيص سريع من أربع خطوات، ونقترح عليك النظام الأنسب لأكبر تعطل
            لديك الآن.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/diagnostic">
              <Button size="lg" className="gap-2">
                ابدأ بتشخيص سريع
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
            <Link to="/pricing">
              <Button size="lg" variant="outline">
                شاهد كل الأسعار
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </SiteLayout>
  );
}
