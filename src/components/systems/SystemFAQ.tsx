import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import type { BusinessSystem } from "@/data/systems";

/** FAQ accordion for a system detail page. */
export default function SystemFAQ({ system }: { system: BusinessSystem }) {
  return (
    <section className="max-w-3xl mx-auto px-4 py-14">
      <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
        أسئلة شائعة
      </h2>
      <Accordion type="single" collapsible className="w-full">
        {system.faq.map((item, index) => (
          <AccordionItem key={item.q} value={`item-${index}`}>
            <AccordionTrigger className="text-right text-base font-medium">
              {item.q}
            </AccordionTrigger>
            <AccordionContent className="text-gray-600 leading-relaxed">
              {item.a}
            </AccordionContent>
          </AccordionItem>
        ))}
      </Accordion>
    </section>
  );
}
