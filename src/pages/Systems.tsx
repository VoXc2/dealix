import { Link } from "react-router";
import MarketingLayout from "@/components/marketing/MarketingLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, TrendingUp, Command, RefreshCw, MessageSquare, FileText } from "lucide-react";
import { coreSystems } from "@/marketing/catalog";

const ICONS: Record<string, React.ComponentType<{ className?: string }>> = {
  "revenue-operating-system": TrendingUp,
  "executive-command-os": Command,
  "follow-up-recovery-os": RefreshCw,
  "whatsapp-client-os": MessageSquare,
  "proposal-proof-os": FileText,
};

export default function Systems() {
  return (
    <MarketingLayout>
      <section className="bg-gradient-to-br from-emerald-50 via-white to-teal-50 py-20">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <Badge className="mb-4 bg-emerald-100 text-emerald-800 hover:bg-emerald-100">5 أنظمة جوهرية</Badge>
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">أنظمة تشغيل الإيرادات</h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            لا نبيع أدوات. خمسة أنظمة بمخرجات ومعايير قبول واضحة. اختر ما يناسب أولويتك اليوم.
          </p>
        </div>
      </section>

      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {coreSystems.map((s) => {
            const Icon = ICONS[s.id] ?? TrendingUp;
            return (
              <Card key={s.id} className="border-0 shadow-md hover:shadow-lg transition-shadow flex flex-col">
                <CardHeader>
                  <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center mb-3">
                    <Icon className="w-6 h-6 text-emerald-600" />
                  </div>
                  <CardTitle className="text-xl">{s.nameAr}</CardTitle>
                  <p className="text-xs text-gray-400 mt-1">{s.nameEn}</p>
                </CardHeader>
                <CardContent className="flex flex-col flex-1">
                  <p className="text-gray-600 mb-4 flex-1">{s.promiseAr}</p>
                  <Link to={`/systems/${s.id}`}>
                    <Button variant="outline" className="w-full gap-2">
                      التفاصيل<ArrowLeft className="w-4 h-4" />
                    </Button>
                  </Link>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </section>
    </MarketingLayout>
  );
}
