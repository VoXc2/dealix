"use client";

import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Bell, CheckCheck, X, ExternalLink, Loader2, Bot, UserPlus, TrendingUp, CheckCircle, FileText, Clock, Shield, Megaphone, Handshake, AlertTriangle, CreditCard } from "lucide-react";
import { useLocale } from "next-intl";
import { cn, formatRelativeTime } from "@/lib/utils";
import {
  type Notification,
  type NotificationType,
  getUnreadCount,
  getNotificationColor,
  getNotificationsByPriority,
  markAsRead,
  markAllAsRead,
} from "@/lib/notifications/service";

const iconMap: Record<NotificationType, React.ElementType> = {
  lead_new: UserPlus,
  deal_update: TrendingUp,
  approval_required: CheckCircle,
  approval_resolved: CheckCircle,
  agent_completed: Bot,
  agent_failed: Bot,
  payment_received: CreditCard,
  invoice_created: FileText,
  subscription_expiring: Clock,
  compliance_alert: Shield,
  marketing_published: Megaphone,
  partner_referral: Handshake,
  system_alert: AlertTriangle,
};

interface NotificationCenterProps {
  notifications: Notification[];
  onMarkRead: (id: string) => void;
  onMarkAllRead: () => void;
  onAction?: (notification: Notification) => void;
  isLoading?: boolean;
}

export function NotificationCenter({
  notifications,
  onMarkRead,
  onMarkAllRead,
  onAction,
  isLoading,
}: NotificationCenterProps) {
  const [open, setOpen] = useState(false);
  const locale = useLocale();
  const isRTL = locale === "ar";
  const unreadCount = getUnreadCount(notifications);
  const sorted = getNotificationsByPriority(notifications);

  const handleToggle = useCallback(() => {
    setOpen((prev) => !prev);
  }, []);

  return (
    <div className="relative">
      <button
        onClick={handleToggle}
        className="relative rounded-lg p-2 text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
        aria-label={isRTL ? "الإشعارات" : "Notifications"}
      >
        <Bell className="w-5 h-5" />
        {unreadCount > 0 && (
          <span className="absolute -top-0.5 -right-0.5 flex h-4 min-w-[16px] items-center justify-center rounded-full bg-red-500 px-1 text-[10px] font-bold text-white">
            {unreadCount > 99 ? "99+" : unreadCount}
          </span>
        )}
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: -8 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: -8 }}
            transition={{ duration: 0.15 }}
            className={cn(
              "absolute top-full mt-2 w-80 sm:w-96 rounded-2xl border border-border bg-card shadow-xl overflow-hidden",
              isRTL ? "left-0" : "right-0",
            )}
          >
            {/* Header */}
            <div className="flex items-center justify-between border-b border-border px-4 py-3">
              <h3 className="text-sm font-semibold text-foreground">
                {isRTL ? "الإشعارات" : "Notifications"}
              </h3>
              <div className="flex items-center gap-1">
                {unreadCount > 0 && (
                  <button
                    onClick={onMarkAllRead}
                    className="flex items-center gap-1 rounded-lg px-2 py-1 text-xs text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
                  >
                    <CheckCheck className="w-3.5 h-3.5" />
                    {isRTL ? "تحديد الكل" : "Mark all read"}
                  </button>
                )}
                <button
                  onClick={() => setOpen(false)}
                  className="rounded-lg p-1 text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* List */}
            <div className="max-h-[400px] overflow-y-auto">
              {isLoading && (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="w-5 h-5 animate-spin text-muted-foreground" />
                </div>
              )}

              {!isLoading && sorted.length === 0 && (
                <div className="flex flex-col items-center justify-center py-12 text-center">
                  <Bell className="w-8 h-8 text-muted-foreground/50 mb-2" />
                  <p className="text-sm text-muted-foreground">
                    {isRTL ? "لا توجد إشعارات" : "No notifications"}
                  </p>
                </div>
              )}

              {!isLoading &&
                sorted.map((notification) => {
                  const Icon = iconMap[notification.type] || Bell;
                  const isUnread = !notification.read;
                  return (
                    <button
                      key={notification.id}
                      onClick={() => {
                        onMarkRead(notification.id);
                        onAction?.(notification);
                      }}
                      className={cn(
                        "flex w-full items-start gap-3 px-4 py-3 text-left transition-colors hover:bg-accent/50 border-b border-border/50 last:border-0",
                        isUnread && "bg-accent/20",
                      )}
                    >
                      <div
                        className={cn(
                          "flex h-8 w-8 shrink-0 items-center justify-center rounded-full",
                          isUnread ? "bg-accent" : "bg-muted",
                        )}
                      >
                        <Icon className={cn("w-4 h-4", getNotificationColor(notification.priority))} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <p
                          className={cn(
                            "text-sm truncate",
                            isUnread ? "font-semibold text-foreground" : "text-foreground/80",
                          )}
                        >
                          {isRTL ? notification.titleAr : notification.title}
                        </p>
                        <p className="text-xs text-muted-foreground mt-0.5 line-clamp-2">
                          {isRTL ? notification.descriptionAr : notification.description}
                        </p>
                        <p className="text-[10px] text-muted-foreground/60 mt-1">
                          {formatRelativeTime(notification.createdAt, locale)}
                        </p>
                      </div>
                      {notification.actionUrl && (
                        <ExternalLink className="w-3.5 h-3.5 text-muted-foreground/40 shrink-0 mt-1" />
                      )}
                      {isUnread && (
                        <span className="h-2 w-2 rounded-full bg-blue-500 shrink-0 mt-2" />
                      )}
                    </button>
                  );
                })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
