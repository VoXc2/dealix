import { redirect } from "next/navigation";

export const metadata = {
  title: "Dealix — التشخيص المجاني",
  description:
    "ابدأ بتشخيص مجاني مبني على الأدلة لفهم سير العمل والمشكلة والـbaseline قبل أي نطاق تنفيذ أو عرض سعر مخصص.",
};

export default function ArabicDiagnosticSprintPage() {
  redirect("/book");
}
