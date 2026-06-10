"use client";

import { useState, useEffect } from "react";
import { Bell, BellOff, Mail, Smartphone, Moon, Save } from "lucide-react";
import { useLocale } from "next-intl";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Separator } from "@/components/ui/separator";
import { toast } from "sonner";
import {
  getNotificationPreferences,
  saveNotificationPreferences,
  type NotificationPreferences,
  type NotificationType,
} from "@/lib/notifications/service";

const notificationTypeLabels: Record<NotificationType, { en: string; ar: string }> = {
  lead_new: { en: "New Leads", ar: "عملاء محتملون جدد" },
  deal_update: { en: "Deal Updates", ar: "تحديثات الصفقات" },
  approval_required: { en: "Approvals Required", ar: "موافقات مطلوبة" },
  approval_resolved: { en: "Approvals Resolved", ar: "تم حل الموافقات" },
  agent_completed: { en: "Agent Completed", ar: "اكتمل الوكيل" },
  agent_failed: { en: "Agent Failed", ar: "فشل الوكيل" },
  payment_received: { en: "Payments Received", ar: "المدفوعات المستلمة" },
  invoice_created: { en: "Invoices Created", ar: "الفواتير المنشأة" },
  subscription_expiring: { en: "Subscription Expiring", ar: "الاشتراك على وشك الانتهاء" },
  compliance_alert: { en: "Compliance Alerts", ar: "تنبيهات الامتثال" },
  marketing_published: { en: "Marketing Published", ar: "التسويق المنشور" },
  partner_referral: { en: "Partner Referrals", ar: "إحالات الشركاء" },
  system_alert: { en: "System Alerts", ar: "تنبيهات النظام" },
};

export function NotificationPreferences() {
  const [prefs, setPrefs] = useState<NotificationPreferences>(getNotificationPreferences());
  const [saving, setSaving] = useState(false);
  const locale = useLocale();
  const isRTL = locale === "ar";

  useEffect(() => {
    setPrefs(getNotificationPreferences());
  }, []);

  const handleSave = async () => {
    setSaving(true);
    try {
      saveNotificationPreferences(prefs);
      toast.success(isRTL ? "تم حفظ التفضيلات" : "Preferences saved");
    } catch {
      toast.error(isRTL ? "فشل في الحفظ" : "Failed to save");
    } finally {
      setSaving(false);
    }
  };

  const toggleType = (type: NotificationType) => {
    setPrefs((prev) => ({
      ...prev,
      types: { ...prev.types, [type]: !prev.types[type] },
    }));
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>{isRTL ? "تفضيلات الإشعارات" : "Notification Preferences"}</CardTitle>
        <CardDescription>
          {isRTL
            ? "تحكم في كيفية ومتى تتلقى الإشعارات"
            : "Control how and when you receive notifications"}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Delivery channels */}
        <div className="space-y-4">
          <h4 className="text-sm font-medium text-foreground">
            {isRTL ? "قنوات التوصيل" : "Delivery Channels"}
          </h4>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Mail className="w-4 h-4 text-muted-foreground" />
              <Label htmlFor="email-notifs">{isRTL ? "بريد إلكتروني" : "Email"}</Label>
            </div>
            <Switch
              id="email-notifs"
              checked={prefs.email}
              onCheckedChange={(v) => setPrefs((prev) => ({ ...prev, email: v }))}
            />
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Smartphone className="w-4 h-4 text-muted-foreground" />
              <Label htmlFor="push-notifs">{isRTL ? "إشعارات push" : "Push"}</Label>
            </div>
            <Switch
              id="push-notifs"
              checked={prefs.push}
              onCheckedChange={(v) => setPrefs((prev) => ({ ...prev, push: v }))}
            />
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Bell className="w-4 h-4 text-muted-foreground" />
              <Label htmlFor="inapp-notifs">{isRTL ? "داخل التطبيق" : "In-App"}</Label>
            </div>
            <Switch
              id="inapp-notifs"
              checked={prefs.inApp}
              onCheckedChange={(v) => setPrefs((prev) => ({ ...prev, inApp: v }))}
            />
          </div>
        </div>

        <Separator />

        {/* Notification types */}
        <div className="space-y-4">
          <h4 className="text-sm font-medium text-foreground">
            {isRTL ? "أنواع الإشعارات" : "Notification Types"}
          </h4>
          {Object.entries(notificationTypeLabels).map(([type, labels]) => (
            <div key={type} className="flex items-center justify-between">
              <Label htmlFor={`notif-${type}`} className="text-sm">
                {isRTL ? labels.ar : labels.en}
              </Label>
              <Switch
                id={`notif-${type}`}
                checked={prefs.types[type as NotificationType]}
                onCheckedChange={() => toggleType(type as NotificationType)}
              />
            </div>
          ))}
        </div>

        <Separator />

        {/* Quiet hours */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Moon className="w-4 h-4 text-muted-foreground" />
              <Label htmlFor="quiet-hours">{isRTL ? "ساعات الهدوء" : "Quiet Hours"}</Label>
            </div>
            <Switch
              id="quiet-hours"
              checked={prefs.quietHours.enabled}
              onCheckedChange={(v) =>
                setPrefs((prev) => ({
                  ...prev,
                  quietHours: { ...prev.quietHours, enabled: v },
                }))
              }
            />
          </div>
          {prefs.quietHours.enabled && (
            <div className="flex items-center gap-4">
              <div className="flex-1">
                <Label className="text-xs text-muted-foreground">
                  {isRTL ? "من" : "From"}
                </Label>
                <input
                  type="time"
                  value={prefs.quietHours.start}
                  onChange={(e) =>
                    setPrefs((prev) => ({
                      ...prev,
                      quietHours: { ...prev.quietHours, start: e.target.value },
                    }))
                  }
                  className="mt-1 block w-full rounded-lg border border-border bg-background px-3 py-2 text-sm"
                />
              </div>
              <div className="flex-1">
                <Label className="text-xs text-muted-foreground">
                  {isRTL ? "إلى" : "To"}
                </Label>
                <input
                  type="time"
                  value={prefs.quietHours.end}
                  onChange={(e) =>
                    setPrefs((prev) => ({
                      ...prev,
                      quietHours: { ...prev.quietHours, end: e.target.value },
                    }))
                  }
                  className="mt-1 block w-full rounded-lg border border-border bg-background px-3 py-2 text-sm"
                />
              </div>
            </div>
          )}
        </div>

        <Button onClick={handleSave} disabled={saving} className="w-full">
          <Save className="w-4 h-4 mr-2" />
          {saving ? (isRTL ? "جاري الحفظ..." : "Saving...") : isRTL ? "حفظ التفضيلات" : "Save Preferences"}
        </Button>
      </CardContent>
    </Card>
  );
}
