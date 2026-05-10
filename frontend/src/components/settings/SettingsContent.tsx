"use client";

import { useLocale } from "next-intl";
import { motion } from "framer-motion";
import { User, Shield, Bell, Plug, CreditCard, Users } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { cn } from "@/lib/utils";

const settingsNav = [
  { icon: User, labelAr: "الملف الشخصي", labelEn: "Profile", value: "profile" },
  { icon: Shield, labelAr: "الأمان", labelEn: "Security", value: "security" },
  { icon: Bell, labelAr: "الإشعارات", labelEn: "Notifications", value: "notifications" },
  { icon: Plug, labelAr: "التكاملات", labelEn: "Integrations", value: "integrations" },
  { icon: CreditCard, labelAr: "الفواتير", labelEn: "Billing", value: "billing" },
  { icon: Users, labelAr: "الفريق", labelEn: "Team", value: "team" },
];

export function SettingsContent() {
  const locale = useLocale();
  const isAr = locale === "ar";

  return (
    <div className="max-w-4xl">
      <Tabs defaultValue="profile" orientation="vertical">
        <div className="flex gap-6">
          {/* Sidebar nav */}
          <TabsList className="flex flex-col h-auto w-48 bg-transparent p-0 gap-1 shrink-0">
            {settingsNav.map((item) => {
              const Icon = item.icon;
              return (
                <TabsTrigger
                  key={item.value}
                  value={item.value}
                  className="w-full justify-start gap-2.5 px-3 py-2.5 rounded-xl data-[state=active]:bg-muted data-[state=active]:text-foreground text-muted-foreground text-sm"
                >
                  <Icon className="w-4 h-4" />
                  {isAr ? item.labelAr : item.labelEn}
                </TabsTrigger>
              );
            })}
          </TabsList>

          {/* Content */}
          <div className="flex-1">
            <TabsContent value="profile" className="mt-0">
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
                <Card>
                  <CardHeader>
                    <CardTitle className="text-base">{isAr ? "المعلومات الشخصية" : "Personal Information"}</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center gap-4 mb-6">
                      <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-gold-400 to-emerald-600 flex items-center justify-center text-white text-2xl font-bold">
                        D
                      </div>
                      <div>
                        <Button variant="outline" size="sm">{isAr ? "تغيير الصورة" : "Change Photo"}</Button>
                        <p className="text-xs text-muted-foreground mt-1">{isAr ? "PNG أو JPG حتى 2MB" : "PNG or JPG up to 2MB"}</p>
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-1.5">
                        <Label>{isAr ? "الاسم الكامل" : "Full Name"}</Label>
                        <Input defaultValue={isAr ? "مشرف النظام" : "System Admin"} />
                      </div>
                      <div className="space-y-1.5">
                        <Label>{isAr ? "البريد الإلكتروني" : "Email"}</Label>
                        <Input defaultValue="admin@dealix.ai" type="email" />
                      </div>
                      <div className="space-y-1.5">
                        <Label>{isAr ? "الشركة" : "Company"}</Label>
                        <Input defaultValue="Dealix" />
                      </div>
                      <div className="space-y-1.5">
                        <Label>{isAr ? "الدور" : "Role"}</Label>
                        <Input defaultValue={isAr ? "مدير" : "Administrator"} disabled />
                      </div>
                    </div>
                    <Separator />
                    <div className="flex justify-end">
                      <Button variant="gold">{isAr ? "حفظ التغييرات" : "Save Changes"}</Button>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </TabsContent>

            <TabsContent value="security" className="mt-0">
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
                <Card>
                  <CardHeader>
                    <CardTitle className="text-base">{isAr ? "تغيير كلمة المرور" : "Change Password"}</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-1.5">
                      <Label>{isAr ? "كلمة المرور الحالية" : "Current Password"}</Label>
                      <Input type="password" placeholder="••••••••" />
                    </div>
                    <div className="space-y-1.5">
                      <Label>{isAr ? "كلمة المرور الجديدة" : "New Password"}</Label>
                      <Input type="password" placeholder="••••••••" />
                    </div>
                    <div className="space-y-1.5">
                      <Label>{isAr ? "تأكيد كلمة المرور" : "Confirm Password"}</Label>
                      <Input type="password" placeholder="••••••••" />
                    </div>
                    <div className="flex justify-end">
                      <Button variant="gold">{isAr ? "تحديث كلمة المرور" : "Update Password"}</Button>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </TabsContent>

            <TabsContent value="notifications" className="mt-0">
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
                <Card>
                  <CardHeader>
                    <CardTitle className="text-base">{isAr ? "تفضيلات الإشعارات" : "Notification Preferences"}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {[
                        { labelAr: "إشعارات الموافقة", labelEn: "Approval notifications", checked: true },
                        { labelAr: "تقارير الوكلاء اليومية", labelEn: "Daily agent reports", checked: true },
                        { labelAr: "تحديثات الصفقات", labelEn: "Deal updates", checked: false },
                        { labelAr: "تنبيهات الامتثال", labelEn: "Compliance alerts", checked: true },
                      ].map((item) => (
                        <div key={item.labelEn} className="flex items-center justify-between p-3 rounded-xl bg-muted/40">
                          <span className="text-sm">{isAr ? item.labelAr : item.labelEn}</span>
                          <div className={cn(
                            "w-10 h-5 rounded-full cursor-pointer transition-colors",
                            item.checked ? "bg-gold-500" : "bg-muted"
                          )}>
                            <div className={cn(
                              "w-4 h-4 rounded-full bg-white m-0.5 transition-transform",
                              item.checked ? "translate-x-5" : "translate-x-0"
                            )} />
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </TabsContent>

            <TabsContent value="integrations" className="mt-0">
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
                <Card>
                  <CardHeader>
                    <CardTitle className="text-base">{isAr ? "التكاملات المتاحة" : "Available Integrations"}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      {[
                        { name: "Salesforce", status: "connected", icon: "☁️" },
                        { name: "HubSpot", status: "disconnected", icon: "🟠" },
                        { name: "Slack", status: "connected", icon: "💬" },
                        { name: "Microsoft Teams", status: "disconnected", icon: "🔵" },
                        { name: "Zapier", status: "disconnected", icon: "⚡" },
                        { name: "Webhook API", status: "connected", icon: "🔗" },
                      ].map((integration) => (
                        <div key={integration.name} className="flex items-center justify-between p-3 rounded-xl border border-border">
                          <div className="flex items-center gap-3">
                            <span className="text-xl">{integration.icon}</span>
                            <div>
                              <p className="text-sm font-medium">{integration.name}</p>
                              <p className={cn("text-xs", integration.status === "connected" ? "text-emerald-400" : "text-muted-foreground")}>
                                {integration.status === "connected" ? (isAr ? "متصل" : "Connected") : (isAr ? "غير متصل" : "Disconnected")}
                              </p>
                            </div>
                          </div>
                          <Button variant={integration.status === "connected" ? "outline" : "gold"} size="sm">
                            {integration.status === "connected" ? (isAr ? "قطع" : "Disconnect") : (isAr ? "ربط" : "Connect")}
                          </Button>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </TabsContent>

            <TabsContent value="billing" className="mt-0">
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
                <Card>
                  <CardHeader>
                    <CardTitle className="text-base">{isAr ? "خطة الاشتراك" : "Subscription Plan"}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="p-5 rounded-2xl bg-gradient-to-br from-gold-500/10 to-emerald-500/10 border border-gold-500/20 mb-6">
                      <div className="flex items-center justify-between">
                        <div>
                          <h3 className="text-lg font-bold text-foreground">{isAr ? "مؤسسي" : "Enterprise"}</h3>
                          <p className="text-sm text-muted-foreground">{isAr ? "وصول غير محدود" : "Unlimited access"}</p>
                        </div>
                        <div className="text-end">
                          <p className="text-2xl font-bold text-gold-400">9,999</p>
                          <p className="text-xs text-muted-foreground">{isAr ? "ريال/شهر" : "SAR/month"}</p>
                        </div>
                      </div>
                    </div>
                    <Button variant="outline">{isAr ? "إدارة الفاتورة" : "Manage Billing"}</Button>
                  </CardContent>
                </Card>
              </motion.div>
            </TabsContent>

            <TabsContent value="team" className="mt-0">
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
                <Card>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-base">{isAr ? "أعضاء الفريق" : "Team Members"}</CardTitle>
                      <Button variant="gold" size="sm">{isAr ? "دعوة عضو" : "Invite Member"}</Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {[
                        { name: "أحمد الحربي", role: isAr ? "مدير المبيعات" : "Sales Manager", status: "active" },
                        { name: "سارة القحطاني", role: isAr ? "محلل إيرادات" : "Revenue Analyst", status: "active" },
                        { name: "محمد العسيري", role: isAr ? "مدير العملاء" : "Account Manager", status: "active" },
                      ].map((member) => (
                        <div key={member.name} className="flex items-center gap-3 p-3 rounded-xl hover:bg-muted/50 transition-colors">
                          <div className="w-9 h-9 rounded-full bg-gradient-to-br from-gold-400/30 to-emerald-400/30 flex items-center justify-center text-sm font-bold text-gold-400">
                            {member.name[0]}
                          </div>
                          <div className="flex-1">
                            <p className="text-sm font-medium">{member.name}</p>
                            <p className="text-xs text-muted-foreground">{member.role}</p>
                          </div>
                          <span className="text-xs text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded-full">
                            {isAr ? "نشط" : "Active"}
                          </span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </TabsContent>
          </div>
        </div>
      </Tabs>
    </div>
  );
}
