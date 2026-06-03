import { Link } from "react-router";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";
import type { BusinessSystem } from "@/data/systems";
import { startingPriceLabel } from "@/data/systems";
import { SYSTEM_ICONS } from "./icons";

/** Compact system card used on the /systems index grid. */
export default function SystemCard({ system }: { system: BusinessSystem }) {
  const Icon = SYSTEM_ICONS[system.iconName];

  return (
    <Card className="flex flex-col h-full border-0 shadow-md hover:shadow-xl transition-shadow">
      <CardHeader>
        <div
          className={`w-12 h-12 ${system.accent.iconBg} rounded-xl flex items-center justify-center mb-4`}
        >
          <Icon className={`w-6 h-6 ${system.accent.iconText}`} />
        </div>
        <h3 className="text-xl font-bold text-gray-900">{system.nameAr}</h3>
        <p className="text-sm text-gray-400">{system.name}</p>
      </CardHeader>
      <CardContent className="flex flex-col flex-1">
        <p className="text-gray-600 text-sm leading-relaxed flex-1">{system.tagline}</p>

        <dl className="mt-5 space-y-2 text-sm">
          <div className="flex justify-between gap-4">
            <dt className="text-gray-500">أول نتيجة</dt>
            <dd className="font-medium text-gray-800 text-left">{system.firstResult}</dd>
          </div>
          <div className="flex justify-between gap-4">
            <dt className="text-gray-500">أول Sprint</dt>
            <dd className="font-medium text-gray-800 text-left">{system.sprintDuration}</dd>
          </div>
          <div className="flex justify-between gap-4">
            <dt className="text-gray-500">السعر</dt>
            <dd className="font-bold text-gray-900 text-left">
              {startingPriceLabel(system)}
            </dd>
          </div>
        </dl>

        <Button asChild className="w-full mt-6 gap-2">
          <Link to={`/systems/${system.slug}`}>
            {system.cta}
            <ArrowLeft className="w-4 h-4" />
          </Link>
        </Button>
      </CardContent>
    </Card>
  );
}
