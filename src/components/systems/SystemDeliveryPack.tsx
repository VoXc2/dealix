import { Card, CardContent } from "@/components/ui/card";
import { Package, Calendar } from "lucide-react";
import type { BusinessSystem } from "@/data/systems";

/** "What the company gets" — first-sprint outcome + tangible delivery pack. */
export default function SystemDeliveryPack({ system }: { system: BusinessSystem }) {
  return (
    <section className="bg-gray-50 border-y">
      <div className="max-w-5xl mx-auto px-4 py-14 grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <div className="flex items-center gap-2 mb-4">
            <Calendar className={`w-5 h-5 ${system.accent.iconText}`} />
            <h2 className="text-2xl font-bold text-gray-900">ماذا تحصل عليه خلال أول Sprint؟</h2>
          </div>
          <p className="text-gray-600 leading-relaxed">{system.sevenDayOutcome}</p>
        </div>

        <Card className="border-0 shadow-md">
          <CardContent className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <Package className={`w-5 h-5 ${system.accent.iconText}`} />
              <h3 className="text-lg font-bold text-gray-900">Delivery Pack</h3>
            </div>
            <ul className="space-y-2.5">
              {system.deliveryPack.map((item) => (
                <li key={item} className="flex items-start gap-2 text-sm text-gray-700">
                  <span
                    className={`mt-1.5 w-1.5 h-1.5 rounded-full shrink-0 ${system.accent.iconText} bg-current`}
                  />
                  {item}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>
    </section>
  );
}
