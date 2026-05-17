import { DiagnosticFunnel } from "@/components/diagnostic/DiagnosticFunnel";

interface DiagnosticPageProps {
  params: Promise<{ locale: string }>;
}

export default async function DealixDiagnosticPage({ params }: DiagnosticPageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";

  return (
    <main className="min-h-screen bg-background py-12 px-4">
      <div className="max-w-2xl mx-auto mb-8 text-center">
        <h1 className="text-2xl font-bold">
          {isAr ? "تشخيص ديليكس" : "Dealix Diagnostic"}
        </h1>
        <p className="text-sm text-muted-foreground mt-1">
          {isAr
            ? "افهم جاهزية عمليات الإيراد لديك في دقائق."
            : "Understand your revenue-ops readiness in minutes."}
        </p>
      </div>
      <DiagnosticFunnel />
    </main>
  );
}
