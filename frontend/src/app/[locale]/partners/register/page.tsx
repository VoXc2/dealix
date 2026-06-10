"use client";

import { useState } from "react";
import { Handshake, Check, Loader2, ArrowRight } from "lucide-react";
import { useLocale } from "next-intl";
import { cn } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import { useRegisterPartner } from "@/lib/hooks/usePartners";

export default function PartnerRegisterPage() {
  const [form, setForm] = useState({
    company: "",
    contactName: "",
    contactEmail: "",
    contactPhone: "",
    website: "",
  });
  const locale = useLocale();
  const isRTL = locale === "ar";
  const register = useRegisterPartner();

  const updateField = (field: string, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await register.mutateAsync(form);
      toast.success(isRTL ? "تم التسجيل بنجاح" : "Registered successfully");
    } catch {
      toast.error(isRTL ? "فشل التسجيل" : "Registration failed");
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="mx-auto max-w-xl px-4 py-16">
        <Card>
          <CardHeader className="text-center">
            <div className="flex justify-center mb-4">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gold-500/10">
                <Handshake className="w-8 h-8 text-gold-500" />
              </div>
            </div>
            <CardTitle className="text-2xl font-bold">
              {isRTL ? "تسجيل شريك" : "Partner Registration"}
            </CardTitle>
            <CardDescription>
              {isRTL
                ? "انضم إلى برنامج شركاء ديليكس"
                : "Join the Dealix Partner Program"}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label>{isRTL ? "اسم الشركة" : "Company Name"} *</Label>
                <Input
                  value={form.company}
                  onChange={(e) => updateField("company", e.target.value)}
                  required
                  dir={isRTL ? "rtl" : "ltr"}
                />
              </div>
              <div>
                <Label>{isRTL ? "اسم جهة الاتصال" : "Contact Name"} *</Label>
                <Input
                  value={form.contactName}
                  onChange={(e) => updateField("contactName", e.target.value)}
                  required
                  dir={isRTL ? "rtl" : "ltr"}
                />
              </div>
              <div>
                <Label>{isRTL ? "البريد الإلكتروني" : "Email"} *</Label>
                <Input
                  type="email"
                  value={form.contactEmail}
                  onChange={(e) => updateField("contactEmail", e.target.value)}
                  required
                  dir="ltr"
                />
              </div>
              <div>
                <Label>{isRTL ? "رقم الجوال" : "Phone"}</Label>
                <Input
                  type="tel"
                  value={form.contactPhone}
                  onChange={(e) => updateField("contactPhone", e.target.value)}
                  dir="ltr"
                />
              </div>
              <div>
                <Label>{isRTL ? "الموقع الإلكتروني" : "Website"}</Label>
                <Input
                  type="url"
                  value={form.website}
                  onChange={(e) => updateField("website", e.target.value)}
                  dir="ltr"
                />
              </div>
              <Button
                type="submit"
                className="w-full"
                disabled={register.isPending}
              >
                {register.isPending ? (
                  <Loader2 className="w-4 h-4 animate-spin mr-1" />
                ) : null}
                {register.isPending
                  ? (isRTL ? "جاري التسجيل..." : "Registering...")
                  : (isRTL ? "تسجيل" : "Register")}
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
