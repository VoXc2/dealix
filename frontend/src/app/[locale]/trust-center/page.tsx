"use client";

import { Shield, CheckCircle, Lock, Server, FileText, Users, Eye, Activity, AlertTriangle, Database, Globe } from "lucide-react";
import { useLocale } from "next-intl";
import { cn } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

const securityScorecards = [
  { label: "Data Encryption", labelAr: "تشفير البيانات", score: 100, icon: Lock, status: "pass" },
  { label: "Access Control", labelAr: "التحكم في الوصول", score: 95, icon: Eye, status: "pass" },
  { label: "Infrastructure", labelAr: "البنية التحتية", score: 98, icon: Server, status: "pass" },
  { label: "Compliance", labelAr: "الامتثال", score: 92, icon: Shield, status: "pass" },
  { label: "Data Privacy", labelAr: "خصوصية البيانات", score: 97, icon: Users, status: "pass" },
  { label: "Monitoring", labelAr: "المراقبة", score: 90, icon: Activity, status: "pass" },
];

const complianceBadges = [
  { name: "PDPL", nameAr: "قانون حماية البيانات الشخصية", description: "Personal Data Protection Law compliant", descriptionAr: "متوافق مع قانون حماية البيانات الشخصية", icon: FileText },
  { name: "SOC 2", nameAr: "SOC 2", description: "Security, availability, processing integrity", descriptionAr: "الأمان والتوفر وسلامة المعالجة", icon: Shield },
  { name: "ISO 27001", nameAr: "ISO 27001", description: "Information security management", descriptionAr: "إدارة أمن المعلومات", icon: CheckCircle },
  { name: "ZATCA", nameAr: "زاتكا", description: "Saudi e-invoicing compliant", descriptionAr: "متوافق مع الفوترة الإلكترونية السعودية", icon: FileText },
];

export default function TrustCenterPage() {
  const locale = useLocale();
  const isRTL = locale === "ar";

  return (
    <div className="min-h-screen bg-background">
      {/* Hero */}
      <section className="border-b border-border bg-gradient-to-b from-background to-accent/30">
        <div className="mx-auto max-w-6xl px-4 py-16 text-center">
          <div className="flex justify-center mb-4">
            <Shield className="w-12 h-12 text-gold-500" />
          </div>
          <h1 className="text-4xl font-bold text-foreground mb-4">
            {isRTL ? "مركز الثقة" : "Trust Center"}
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            {isRTL
              ? "الأمان والخصوصية والامتثال هما أساس منصتنا"
              : "Security, privacy, and compliance are the foundation of our platform"}
          </p>
        </div>
      </section>

      <div className="mx-auto max-w-6xl px-4 py-12 space-y-12">
        {/* Security scorecard */}
        <section>
          <h2 className="text-2xl font-bold text-foreground mb-6">
            {isRTL ? "بطاقة أداء الأمان" : "Security Scorecard"}
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {securityScorecards.map((item) => {
              const Icon = item.icon;
              return (
                <Card key={item.label} className="hover:border-emerald-500/30 transition-colors">
                  <CardContent className="p-5">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/10">
                        <Icon className="w-5 h-5 text-emerald-500" />
                      </div>
                      <Badge className="bg-emerald-500/10 text-emerald-500 border-emerald-500/20">
                        {item.score}%
                      </Badge>
                    </div>
                    <h3 className="text-sm font-semibold text-foreground mb-2">
                      {isRTL ? item.labelAr : item.label}
                    </h3>
                    <Progress value={item.score} className="h-1.5" />
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </section>

        {/* Compliance badges */}
        <section>
          <h2 className="text-2xl font-bold text-foreground mb-6">
            {isRTL ? "الشهادات والامتثال" : "Certifications & Compliance"}
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {complianceBadges.map((badge) => {
              const Icon = badge.icon;
              return (
                <Card key={badge.name} className="border-gold-500/20">
                  <CardContent className="p-5 flex items-start gap-4">
                    <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-gold-500/10">
                      <Icon className="w-6 h-6 text-gold-500" />
                    </div>
                    <div>
                      <h3 className="text-sm font-semibold text-foreground">
                        {isRTL ? badge.nameAr : badge.name}
                      </h3>
                      <p className="text-xs text-muted-foreground">
                        {isRTL ? badge.descriptionAr : badge.description}
                      </p>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </section>

        {/* Key security features */}
        <section>
          <h2 className="text-2xl font-bold text-foreground mb-6">
            {isRTL ? "ميزات الأمان" : "Security Features"}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              { icon: Lock, title: "End-to-End Encryption", titleAr: "تشفير كامل", desc: "All data encrypted at rest and in transit using AES-256 and TLS 1.3", descAr: "جميع البيانات مشفرة في حالة السكون والنقل" },
              { icon: Eye, title: "Access Control", titleAr: "التحكم في الوصول", desc: "Role-based access control with MFA and SSO support", descAr: "التحكم في الوصول القائم على الأدوار مع دعم المصادقة متعددة العوامل" },
              { icon: Database, title: "Data Isolation", titleAr: "عزل البيانات", desc: "Customer data isolated with dedicated database instances", descAr: "بيانات العملاء معزولة مع مثيلات قاعدة بيانات مخصصة" },
              { icon: Activity, title: "24/7 Monitoring", titleAr: "مراقبة على مدار الساعة", desc: "Real-time threat detection and automated incident response", descAr: "كشف التهديدات في الوقت الفعلي والاستجابة التلقائية" },
              { icon: Globe, title: "Saudi Hosting", titleAr: "استضافة سعودية", desc: "Data hosted in Saudi Arabia with local redundancy", descAr: "البيانات مستضافة في المملكة العربية السعودية مع تكرار محلي" },
              { icon: Users, title: "Privacy First", titleAr: "الخصوصية أولاً", desc: "GDPR and PDPL compliant data handling practices", descAr: "ممارسات معالجة بيانات متوافقة مع اللائحة العامة لحماية البيانات" },
            ].map((feat, idx) => {
              const Icon = feat.icon;
              return (
                <Card key={idx} className="hover:border-gold-500/30 transition-colors">
                  <CardContent className="p-5">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gold-500/10 mb-3">
                      <Icon className="w-5 h-5 text-gold-500" />
                    </div>
                    <h3 className="text-sm font-semibold text-foreground mb-1">
                      {isRTL ? feat.titleAr : feat.title}
                    </h3>
                    <p className="text-xs text-muted-foreground">
                      {isRTL ? feat.descAr : feat.desc}
                    </p>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </section>
      </div>
    </div>
  );
}
