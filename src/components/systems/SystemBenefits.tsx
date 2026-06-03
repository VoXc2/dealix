import { CheckCircle } from "lucide-react";
import type { BusinessSystem } from "@/data/systems";

/** Benefits + "who it is for" block for a system detail page. */
export default function SystemBenefits({ system }: { system: BusinessSystem }) {
  return (
    <section className="max-w-5xl mx-auto px-4 py-12 grid grid-cols-1 md:grid-cols-3 gap-10">
      <div className="md:col-span-2">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">ماذا تستفيد الشركة؟</h2>
        <ul className="space-y-3">
          {system.benefits.map((benefit) => (
            <li key={benefit} className="flex items-start gap-3">
              <CheckCircle
                className={`w-5 h-5 mt-0.5 shrink-0 ${system.accent.iconText}`}
              />
              <span className="text-gray-700">{benefit}</span>
            </li>
          ))}
        </ul>
      </div>

      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-6">لمن هذا النظام؟</h2>
        <div className="flex flex-wrap gap-2">
          {system.whoFor.map((audience) => (
            <span
              key={audience}
              className={`px-3 py-1.5 rounded-full text-sm font-medium ${system.accent.badge}`}
            >
              {audience}
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}
