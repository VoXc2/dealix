"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useTranslations, useLocale } from "next-intl";
import { motion } from "framer-motion";
import { Eye, EyeOff, Zap, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/lib/hooks/useAuth";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

export function LoginForm() {
  const t = useTranslations("auth");
  const locale = useLocale();
  const isAr = locale === "ar";
  const router = useRouter();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await login(email, password);
      router.push(`/${locale}/dashboard`);
    } catch {
      toast.error(isAr ? "بيانات الدخول غير صحيحة" : "Invalid credentials");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background grid-pattern px-4">
      {/* Background orbs */}
      <div className="fixed top-1/4 left-1/3 w-96 h-96 bg-gold-500/5 rounded-full blur-3xl pointer-events-none" />
      <div className="fixed bottom-1/4 right-1/3 w-80 h-80 bg-emerald-500/5 rounded-full blur-3xl pointer-events-none" />

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
          <h1 className="text-2xl font-bold text-foreground mb-1">
            {t("loginTitle")}
          </h1>
          <p className="text-muted-foreground text-sm">{t("loginSubtitle")}</p>
        </div>

        {/* Card */}
        <div className="bg-card border border-border rounded-3xl p-8 shadow-xl">
          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="space-y-1.5">
              <Label>{t("email")}</Label>
              <Input
                type="email"
                placeholder="you@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                autoComplete="email"
                dir="ltr"
              />
            </div>

            <div className="space-y-1.5">
              <div className="flex items-center justify-between">
                <Label>{t("password")}</Label>
                <Link
                  href="#"
                  className="text-xs text-gold-400 hover:text-gold-300 transition-colors"
                >
                  {t("forgotPassword")}
                </Link>
              </div>
              <div className="relative">
                <Input
                  type={showPassword ? "text" : "password"}
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  autoComplete="current-password"
                  dir="ltr"
                  className={isAr ? "pr-4 pl-10" : "pe-10"}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label={
                    showPassword
                      ? isAr
                        ? "إخفاء كلمة المرور"
                        : "Hide password"
                      : isAr
                        ? "إظهار كلمة المرور"
                        : "Show password"
                  }
                  className={cn(
                    "absolute top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground",
                    isAr ? "left-3" : "right-3"
                  )}
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <Button
              type="submit"
              variant="gold"
              className="w-full"
              size="lg"
              disabled={isLoading}
            >
              {isLoading ? (
                <span className="flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  {isAr ? "جارٍ الدخول..." : "Signing in..."}
                </span>
              ) : (
                <span className="flex items-center gap-2">
                  {t("loginBtn")}
                  <ArrowRight className={cn("w-4 h-4", isAr && "rotate-180")} />
                </span>
              )}
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-sm text-muted-foreground">
              {t("noAccount")}{" "}
              <Link
                href={`/${locale}/register`}
                className="text-gold-400 hover:text-gold-300 font-medium transition-colors"
              >
                {t("register")}
              </Link>
            </p>
          </div>
        </div>

        {/* Demo note */}
        <p className="text-center text-xs text-muted-foreground mt-4">
          {isAr ? "للعرض: " : "Demo: "}
          <span className="text-foreground/70 font-mono">demo@dealix.ai / demo123</span>
        </p>
      </motion.div>
    </div>
  );
}
