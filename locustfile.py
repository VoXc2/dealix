"""
Locust load test script — Dealix API.
سكريبت اختبار الحمل باستخدام Locust.

Usage:
  pip install locust
  locust -f locustfile.py --host=http://localhost:8000

  # Headless (CI / k6-style):
  locust -f locustfile.py --host=http://localhost:8000 \
    --users=50 --spawn-rate=5 --run-time=60s \
    --headless --csv=locust_results

Target: 50 concurrent virtual users, p95 < 500 ms, error rate < 1%

Scenarios modelled:
  - SalesBrowser (30%): list leads, get lead by ID, list deals
  - LeadSubmitter (25%): POST new lead
  - AdminOps (15%): health check, get sectors
  - WebhookReceiver (20%): POST WhatsApp / HubSpot webhook
  - AnalyticsDashboard (10%): growth OS, radar events, company brain
"""

from __future__ import annotations

import os
import random
import string
import time

from locust import HttpUser, between, task

# ── Shared config ──────────────────────────────────────────────────
API_KEY = os.getenv("LOAD_TEST_API_KEY", "your-api-key-here")
BASE_HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

SAUDI_SECTORS = ["real_estate", "healthcare", "education", "retail", "fintech", "logistics", "hospitality"]
LEAD_SOURCES = ["whatsapp", "website", "linkedin", "referral", "event"]


def _random_str(n: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=n))


def _random_phone() -> str:
    return f"+9665{random.randint(10000000, 99999999)}"


def _random_lead_payload() -> dict:
    return {
        "company_name": f"شركة {_random_str(6)} المحدودة",
        "contact_name": f"محمد {_random_str(5)}",
        "phone": _random_phone(),
        "email": f"{_random_str(8)}@example.sa",
        "sector": random.choice(SAUDI_SECTORS),
        "source": random.choice(LEAD_SOURCES),
        "city": random.choice(["riyadh", "jeddah", "dammam", "mecca"]),
        "notes": "load-test lead — do not process",
    }


# ── User classes ───────────────────────────────────────────────────

class SalesBrowserUser(HttpUser):
    """
    Simulates a sales rep browsing leads and deals.
    يحاكي مندوب مبيعات يتصفح قوائم العملاء المحتملين والصفقات.
    """
    wait_time = between(1, 3)
    weight = 30

    @task(3)
    def list_leads(self):
        self.client.get(
            "/api/v1/leads?limit=20",
            headers=BASE_HEADERS,
            name="/api/v1/leads [list]",
        )

    @task(2)
    def list_leads_with_cursor(self):
        self.client.get(
            "/api/v1/leads?limit=10&cursor=IA==",
            headers=BASE_HEADERS,
            name="/api/v1/leads [cursor]",
        )

    @task(1)
    def list_deals(self):
        self.client.get(
            "/api/v1/sales",
            headers=BASE_HEADERS,
            name="/api/v1/sales [list]",
        )

    @task(1)
    def get_pricing(self):
        self.client.get(
            "/api/v1/pricing",
            headers=BASE_HEADERS,
            name="/api/v1/pricing",
        )


class LeadSubmitterUser(HttpUser):
    """
    Simulates automated lead intake from marketing campaigns.
    يحاكي استيعاب العملاء المحتملين تلقائيًا من الحملات التسويقية.
    """
    wait_time = between(2, 5)
    weight = 25

    @task(1)
    def submit_lead(self):
        payload = _random_lead_payload()
        self.client.post(
            "/api/v1/leads",
            json=payload,
            headers=BASE_HEADERS,
            name="/api/v1/leads [create]",
        )


class AdminOpsUser(HttpUser):
    """
    Simulates internal admin and health monitoring.
    يحاكي المراقبة الداخلية وفحوصات الصحة.
    """
    wait_time = between(5, 15)
    weight = 15

    @task(3)
    def health_check(self):
        # Health is exempt from auth — no headers needed
        self.client.get("/health", name="/health")

    @task(2)
    def get_sectors(self):
        self.client.get(
            "/api/v1/sectors",
            headers=BASE_HEADERS,
            name="/api/v1/sectors",
        )

    @task(1)
    def get_root(self):
        self.client.get("/", name="/ [root]")


class WebhookReceiverUser(HttpUser):
    """
    Simulates inbound webhooks from HubSpot / WhatsApp.
    يحاكي استقبال الـ webhooks الواردة من HubSpot وWhatsApp.
    """
    wait_time = between(1, 2)
    weight = 20

    @task(2)
    def whatsapp_webhook(self):
        payload = {
            "entry": [{"changes": [{"value": {"messages": [{"from": _random_phone(), "text": {"body": "مرحبا"}}]}}]}]
        }
        self.client.post(
            "/api/v1/webhooks/whatsapp",
            json=payload,
            headers={"Content-Type": "application/json"},  # no API key for webhooks
            name="/api/v1/webhooks/whatsapp",
        )

    @task(1)
    def hubspot_webhook(self):
        payload = [{"subscriptionType": "contact.creation", "objectId": random.randint(1000, 9999)}]
        self.client.post(
            "/api/v1/webhooks/hubspot",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "X-HubSpot-Signature-v3": "test-sig",
                "X-HubSpot-Request-Timestamp": str(int(time.time() * 1000)),
            },
            name="/api/v1/webhooks/hubspot",
        )


class AnalyticsDashboardUser(HttpUser):
    """
    Simulates the analytics dashboard queries.
    يحاكي استعلامات لوحة التحليلات.
    """
    wait_time = between(3, 8)
    weight = 10

    @task(2)
    def growth_os(self):
        self.client.get(
            "/api/v1/growth-os/summary",
            headers=BASE_HEADERS,
            name="/api/v1/growth-os/summary",
        )

    @task(1)
    def radar_events(self):
        self.client.get(
            "/api/v1/radar/events?limit=20",
            headers=BASE_HEADERS,
            name="/api/v1/radar/events",
        )

    @task(1)
    def company_brain(self):
        self.client.get(
            "/api/v1/company-brain/snapshot",
            headers=BASE_HEADERS,
            name="/api/v1/company-brain/snapshot",
        )
