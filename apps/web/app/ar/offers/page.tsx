import { redirect } from "next/navigation";

export const metadata = {
  title: "Dealix — ابدأ بالتشخيص المجاني",
  description:
    "ابدأ بتشخيص Dealix المجاني. بعد التحقق والاكتشاف نحدد نطاق الحل ونجهز عرضاً وسعراً خاصاً بالحالة؛ لا توجد أسعار عامة ملزمة.",
};

export default function ArabicOffersPage() {
  redirect("/book");
}
