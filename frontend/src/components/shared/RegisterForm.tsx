"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useTranslations, useLocale } from "next-intl";
import { motion } from "framer-motion";
import { Zap, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

export function RegisterForm() {
  const t = useTranslations("auth");
  const locale = useLocale();
  const isAr = locale === "ar";
  const router = useRouter();
  const [form, setForm] = useState({
    fullName: "",
    company: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (form.password !== form.confirmPassword) {
      toast.error(isAr ? "كلمات المرور غير متطابقة" : "Passwords do not match");
      return;
    }
    setIsLoading(true);
    try {
      // In real app would call authApi.register(...)
      // For demo, simulate login
      await new Promise((r) => setTimeout(r, 1000));
      router.push(`/${locale}/dashboard`);
    } catch {
      toast.error(isAr ? "حدث خطأ في التسجيل" : "Registration failed");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background grid-pattern px-4 py-8">
      <div className="fixed top-1/3 right-1/4 w-96 h-96 bg-gold-500/5 rounded-full blur-3xl pointer-events-none" />
      <div className="fixed bottom-1/3 left-1/4 w-80 h-80 bg-emerald-500/5 rounded-full blur-3xl pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md"
      >
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-gold-400 to-gold-600 shadow-xl shadow-gold-500/20 mb-4">
            <Zap className="w-7 h-7 text-white" strokeWidth={2.5} />
          </div>
          <h1 className="text-2xl font-bold text-foreground mb-1">{t("registerTitle")}</h1>
          <p className="text-muted-foreground text-sm">{t("registerSubtitle")}</p>
        </div>

        <div className="bg-card border border-border rounded-3xl p-8 shadow-xl">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <Label>{t("fullName")}</Label>
                <Input
                  name="fullName"
                  value={form.fullName}
                  onChange={handleChange}
                  placeholder={isAr ? "الاسم الكامل" : "Full name"}
                  required
                />
              </div>
              <div className="space-y-1.5">
                <Label>{t("company")}</Label>
                <Input
                  name="company"
                  value={form.company}
                  onChange={handleChange}
                  placeholder={isAr ? "اسم الشركة" : "Company name"}
                  required
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <Label>{t("email")}</Label>
              <Input
                name="email"
                type="email"
                value={form.email}
                onChange={handleChange}
                placeholder="you@company.com"
                required
                dir="ltr"
              />
            </div>

            <div className="space-y-1.5">
              <Label>{t("password")}</Label>
              <Input
                name="password"
                type="password"
                value={form.password}
                onChange={handleChange}
                placeholder="••••••••"
                required
                dir="ltr"
              />
            </div>

            <div className="space-y-1.5">
              <Label>{t("confirmPassword")}</Label>
              <Input
                name="confirmPassword"
                type="password"
                value={form.confirmPassword}
                onChange={handleChange}
                placeholder="••••••••"
                required
                dir="ltr"
              />
            </div>

            <Button type="submit" variant="gold" className="w-full" size="lg" disabled={isLoading}>
              {isLoading ? (
                <span className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  {isAr ? "جارٍ التسجيل..." : "Creating account..."}
                </span>
              ) : (
                <span className="flex items-center gap-2">
                  {t("registerBtn")}
                  <ArrowRight className={cn("w-4 h-4", isAr && "rotate-180")} />
                </span>
              )}
            </Button>
          </form>

          <div className="mt-5 text-center">
            <p className="text-sm text-muted-foreground">
              {t("hasAccount")}{" "}
              <Link href={`/${locale}/login`} className="text-gold-400 hover:text-gold-300 font-medium transition-colors">
                {t("login")}
              </Link>
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
