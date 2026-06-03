import { Link } from "react-router";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";
import {
  type BusinessSystem,
  accentClasses,
  formatPrice,
  CURRENCY,
} from "@/data/systems";

export default function SystemCard({ system }: { system: BusinessSystem }) {
  const accent = accentClasses[system.accent];
  const Icon = system.icon;

  return (
    <Card className="flex flex-col border-0 shadow-md hover:shadow-xl transition-shadow h-full">
      <CardHeader>
        <div
          className={`w-12 h-12 ${accent.bgSoft} rounded-xl flex items-center justify-center mb-4`}
        >
          <Icon className={`w-6 h-6 ${accent.text}`} />
        </div>
        <CardTitle className="text-xl leading-snug">{system.nameAr}</CardTitle>
        <p className="text-sm text-gray-400 font-medium">{system.name}</p>
      </CardHeader>
      <CardContent className="flex flex-col flex-1">
        <p className="text-gray-600 text-sm leading-relaxed mb-4">
          {system.painShort}
        </p>
        <div className="mb-4">
          <p className="text-xs text-gray-400 mb-1">أول نتيجة</p>
          <p className="text-sm text-gray-800 font-medium">
            {system.firstResult}
          </p>
        </div>
        <div className="mt-auto pt-4 border-t flex items-center justify-between">
          <div>
            <p className="text-xs text-gray-400">يبدأ من</p>
            <p className={`text-lg font-bold ${accent.text}`}>
              {formatPrice(system.startingPrice)}{" "}
              <span className="text-sm font-normal text-gray-500">
                {CURRENCY}
              </span>
            </p>
          </div>
          <Link to={`/systems/${system.slug}`}>
            <Button variant="ghost" size="sm" className="gap-1">
              التفاصيل
              <ArrowLeft className="w-4 h-4" />
            </Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}
