import { redirect } from "next/navigation";

export const metadata = {
  title: "Dealix — ابدأ التشخيص المجاني",
  description:
    "قناة Dealix الرسمية لبدء التشخيص المجاني وجمع معلومات المشكلة والـworkflow والـbaseline مع موافقة واضحة على المتابعة.",
};

export default function ArabicIntakePage() {
  redirect("/book");
}
