import { Link } from "react-router";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Clock } from "lucide-react";
import type { BusinessSystem } from "@/data/systems";
import { startingPriceLabel } from "@/data/systems";
import { SYSTEM_ICONS } from "./icons";

/** Hero band for a single system detail page. */
export default function SystemHero({ system }: { system: BusinessSystem }) {
  const Icon = SYSTEM_ICONS[system.iconName];

  return (
    <section className="relative overflow-hidden border-b">
      <div
        className={`absolute inset-0 bg-gradient-to-br ${system.accent.gradient} opacity-[0.07]`}
      />
      <div className="relative max-w-5xl mx-auto px-4 pt-16 pb-14">
        <Link
          to="/systems"
          className="text-sm text-gray-500 hover:text-gray-900 inline-flex items-center gap-1 mb-6"
        >
          الأنظمة الخمسة
          <ArrowLeft className="w-4 h-4" />
        </Link>

        <div className="flex items-start gap-4">
          <div
            className={`shrink-0 w-14 h-14 ${system.accent.iconBg} rounded-2xl flex items-center justify-center`}
          >
            <Icon className={`w-7 h-7 ${system.accent.iconText}`} />
          </div>
          <div>
            <Badge className={`mb-3 ${system.accent.badge}`}>{system.name}</Badge>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 leading-tight">
              {system.nameAr}
            </h1>
            <p className="text-xl text-gray-600 mt-4 max-w-2xl leading-relaxed">
              {system.tagline}
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3 mt-8">
          <Button asChild size="lg" className="gap-2">
            <Link to="/pricing">
              {system.cta}
              <ArrowLeft className="w-4 h-4" />
            </Link>
          </Button>
          <span className="text-lg font-bold text-gray-900">
            {startingPriceLabel(system)}
          </span>
          <span className="inline-flex items-center gap-1 text-sm text-gray-500">
            <Clock className="w-4 h-4" />
            أول Sprint {system.sprintDuration}
          </span>
        </div>
      </div>
    </section>
  );
}
