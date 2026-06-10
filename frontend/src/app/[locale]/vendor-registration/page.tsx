"use client";

import { useState } from "react";
import { Building2, Mail, Phone, Globe, FileText, Check, Loader2, ArrowRight } from "lucide-react";
import { useLocale } from "next-intl";
import { cn } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";

interface VendorForm {
  company: string;
  contactName: string;
  email: string;
  phone: string;
  website: string;
  services: string;
  experience: string;
}

export default function VendorRegistrationPage() {
  const [step, setStep] = useState(0);
  const [form, setForm] = useState<VendorForm>({
    company: "",
    contactName: "",
    email: "",
    phone: "",
    website: "",
    services: "",
    experience: "",
  });
  const [submitting, setSubmitting] = useState(false);
  const locale = useLocale();
  const isRTL = locale === "ar";

  const updateField = (field: keyof VendorForm, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      await new Promise((r) => setTimeout(r, 1500));
      toast.success(isRTL ? "تم إرسال طلب التسجيل" : "Registration submitted");
      setStep(2);
    } catch {
      toast.error(isRTL ? "فشل الإرسال" : "Submission failed");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="mx-auto max-w-2xl px-4 py-16">
        <Card>
          <CardHeader className="text-center">
            <div className="flex justify-center mb-4">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gold-500/10">
                <Building2 className="w-8 h-8 text-gold-500" />
              </div>
            </div>
            <CardTitle className="text-2xl font-bold">
              {isRTL ? "تسجيل مورد/شريك" : "Vendor Registration"}
            </CardTitle>
            <CardDescription>
              {isRTL
                ? "سجل كمورد أو شريك مع ديليكس"
                : "Register as a vendor or partner with Dealix"}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {step === 0 && (
              <div className="space-y-4">
                <div>
                  <Label>{isRTL ? "اسم الشركة" : "Company Name"} *</Label>
                  <Input
                    value={form.company}
                    onChange={(e) => updateField("company", e.target.value)}
                    placeholder={isRTL ? "اسم الشركة" : "Company name"}
                    dir={isRTL ? "rtl" : "ltr"}
                  />
                </div>
                <div>
                  <Label>{isRTL ? "اسم جهة الاتصال" : "Contact Name"} *</Label>
                  <Input
                    value={form.contactName}
                    onChange={(e) => updateField("contactName", e.target.value)}
                    placeholder={isRTL ? "الاسم الكامل" : "Full name"}
                    dir={isRTL ? "rtl" : "ltr"}
                  />
                </div>
                <div>
                  <Label>{isRTL ? "البريد الإلكتروني" : "Email"} *</Label>
                  <Input
                    type="email"
                    value={form.email}
                    onChange={(e) => updateField("email", e.target.value)}
                    placeholder="email@company.com"
                    dir="ltr"
                  />
                </div>
                <div>
                  <Label>{isRTL ? "رقم الجوال" : "Phone"}</Label>
                  <Input
                    type="tel"
                    value={form.phone}
                    onChange={(e) => updateField("phone", e.target.value)}
                    placeholder="+966"
                    dir="ltr"
                  />
                </div>
                <Button
                  className="w-full"
                  onClick={() => setStep(1)}
                  disabled={!form.company || !form.contactName || !form.email}
                >
                  {isRTL ? "التالي" : "Next"}
                  <ArrowRight className={cn("w-4 h-4 ml-1", isRTL && "rotate-180")} />
                </Button>
              </div>
            )}

            {step === 1 && (
              <div className="space-y-4">
                <div>
                  <Label>{isRTL ? "الموقع الإلكتروني" : "Website"}</Label>
                  <Input
                    type="url"
                    value={form.website}
                    onChange={(e) => updateField("website", e.target.value)}
                    placeholder="https://example.com"
                    dir="ltr"
                  />
                </div>
                <div>
                  <Label>{isRTL ? "الخدمات المقدمة" : "Services Offered"} *</Label>
                  <textarea
                    value={form.services}
                    onChange={(e) => updateField("services", e.target.value)}
                    placeholder={isRTL ? "صف الخدمات التي تقدمها" : "Describe services you offer"}
                    className="w-full rounded-lg border border-border bg-background px-4 py-2.5 text-sm min-h-[100px]"
                    dir={isRTL ? "rtl" : "ltr"}
                  />
                </div>
                <div>
                  <Label>{isRTL ? "سنوات الخبرة" : "Years of Experience"}</Label>
                  <Input
                    type="number"
                    value={form.experience}
                    onChange={(e) => updateField("experience", e.target.value)}
                    placeholder="5"
                    dir="ltr"
                  />
                </div>
                <div className="flex items-center gap-3">
                  <Button variant="ghost" onClick={() => setStep(0)}>
                    {isRTL ? "رجوع" : "Back"}
                  </Button>
                  <Button
                    className="flex-1"
                    onClick={handleSubmit}
                    disabled={submitting || !form.services}
                  >
                    {submitting ? (
                      <Loader2 className="w-4 h-4 animate-spin mr-1" />
                    ) : null}
                    {submitting
                      ? (isRTL ? "جاري الإرسال..." : "Submitting...")
                      : (isRTL ? "إرسال الطلب" : "Submit Registration")}
                  </Button>
                </div>
              </div>
            )}

            {step === 2 && (
              <div className="text-center py-8">
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-emerald-500/10 mx-auto mb-4">
                  <Check className="w-8 h-8 text-emerald-500" />
                </div>
                <h3 className="text-lg font-bold text-foreground mb-2">
                  {isRTL ? "تم إرسال الطلب بنجاح" : "Registration Submitted"}
                </h3>
                <p className="text-sm text-muted-foreground">
                  {isRTL
                    ? "سنراجع طلبك ونتواصل معك قريباً"
                    : "We'll review your application and get back to you soon"}
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
