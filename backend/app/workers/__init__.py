"""Dealix - Workers Package"""
from app.workers.email_tasks import send_email_task, send_bulk_email_task
from app.workers.deal_tasks import expire_deals_task, update_deal_metrics_task, generate_deal_report_task
from app.workers.affiliate_tasks import calculate_commissions_task, process_payout_task, update_affiliate_tiers_task
from app.workers.notification_tasks import send_reminder_task, process_notifications_task
from app.workers.analytics_tasks import generate_daily_report_task, generate_weekly_report_task, update_leaderboard_task

__all__ = [
    "send_email_task", "send_bulk_email_task",
    "expire_deals_task", "update_deal_metrics_task", "generate_deal_report_task",
    "calculate_commissions_task", "process_payout_task", "update_affiliate_tiers_task",
    "send_reminder_task", "process_notifications_task",
    "generate_daily_report_task", "generate_weekly_report_task", "update_leaderboard_task",
]
