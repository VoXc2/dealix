import { Link } from "react-router";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";
import type { BusinessSystem } from "@/data/systems";
import { formatSar, PRICING_NOTE, PRICING_DISCLAIMER } from "@/data/systems";

/** Starting-price block for a system detail page. */
export default function SystemPricing({ system }: { system: BusinessSystem }) {
  return (
    <section className="max-w-5xl mx-auto px-4 py-14">
      <Card className="border-0 shadow-lg overflow-hidden">
        <div className={`h-1.5 bg-gradient-to-r ${system.accent.gradient}`} />
        <CardContent className="p-8 flex flex-col md:flex-row md:items-center md:justify-between gap-6">
          <div>
            <p className="text-sm text-gray-500 mb-1">يبدأ من</p>
            <p className="text-4xl font-bold text-gray-900">
              {formatSar(system.startingPrice)}
            </p>
            <p className="text-gray-600 mt-2">
              Sprint افتتاحي لمدة {system.sprintDuration} — يشمل التشخيص + أول
              workflow + تقرير تنفيذي.
            </p>
            <p className="text-sm text-gray-500 mt-3 max-w-xl">{PRICING_NOTE}</p>
            <p className="text-xs text-gray-400 mt-2 max-w-xl">{PRICING_DISCLAIMER}</p>
          </div>
          <div className="shrink-0">
            <Button asChild size="lg" className="gap-2 w-full md:w-auto">
              <Link to="/pricing">
                {system.cta}
                <ArrowLeft className="w-4 h-4" />
              </Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    </section>
  );
}
