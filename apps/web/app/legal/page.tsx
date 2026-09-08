"use client";

import PageShell from "@/components/PageShell";

const founderEmail = process.env.NEXT_PUBLIC_FOUNDER_EMAIL ?? "sami.assiri11@gmail.com";

export default function LegalPage() {
  return (
    <PageShell>
      <section className="card" style={{ paddingTop: "clamp(40px,6vw,72px)", paddingBottom: "clamp(40px,6vw,72px)" }}>
        <p className="eyebrow">الشروط والخصوصية</p>
        <h1>الإطار القانوني والخصوصية</h1>
        <p style={{ maxWidth: 780 }}>
          Dealix تتعامل مع البيانات على أساس الغرض المحدد، الحد الأدنى اللازم، والصلاحيات المناسبة.
          لا نعتبر البيانات العامة موافقة على التسويق، ولا نرفع Research أو Draft إلى علاقة أو إرسال فعلي بلا أساس مناسب.
        </p>

        <h3>مبادئ التعامل مع البيانات</h3>
        <ul style={{ maxWidth: 780 }}>
          <li>استخدام البيانات فقط للغرض المعلن أو المتفق عليه.</li>
          <li>تقليل الوصول إلى البيانات وحصره في من يحتاجه للتنفيذ.</li>
          <li>فصل بيانات الاختبار والـsynthetic عن بيانات العملاء الحقيقية.</li>
          <li>احترام طلبات الإيقاف أو السحب وتسجيلها في المسار المناسب.</li>
          <li>عدم الاحتفاظ بالبيانات أطول من الحاجة التشغيلية أو الالتزام النظامي المطبق.</li>
        </ul>

        <h3>الرسائل والتسويق المباشر</h3>
        <p style={{ maxWidth: 780 }}>
          قنوات مثل WhatsApp أو البريد تُستخدم وفق سياق العلاقة والموافقة والغرض. وجود رقم أو بريد منشور لا يعني تلقائيًا أن الشخص وافق على تلقي رسائل تسويقية.
        </p>

        <h3>التواصل</h3>
        <p>
          للاستفسارات المتعلقة بالخصوصية أو الشروط: <a href={`mailto:${founderEmail}`}>{founderEmail}</a>
        </p>
      </section>
    </PageShell>
  );
}
