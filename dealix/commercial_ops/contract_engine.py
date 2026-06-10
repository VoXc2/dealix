"""
Contract Engine — generates bilingual contracts and manages e-signature workflows.
محرك العقود — يُنشئ عقوداً ثنائية اللغة ويدير سير عمل التوقيع الإلكتروني.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)

_TERMS_TEMPLATE_AR = """
بسم الله الرحمن الرحيم

اتفاقية خدمات Dealix

بين:
شركة Dealix للتكنولوجيا (الطرف الأول)
و
{company_name} (الطرف الثاني)

المادة الأولى: مدة الاتفاقية
تبدأ مدة هذه الاتفاقية من تاريخ {start_date} ولمدة {duration_months} أشهر.

المادة الثانية: الخدمات
يقدم الطرف الأول للطرف الثاني خدمات منصة Dealix وفقاً للباقة {plan}، وتشمل:
{features_list}

المادة الثالثة: الرسوم والدفع
يلتزم الطرف الثاني بدفع مبلغ {price_sar} ريال سعودي شهرياً.
{setup_fee_clause}

المادة الرابعة: الالتزامات
- يلتزم الطرف الأول بتقديم الخدمات وفقاً لأعلى معايير الجودة.
- يلتزم الطرف الثاني بتقديم المعلومات اللازمة لتقديم الخدمة.

المادة الخامسة: السرية
تظل جميع المعلومات المشتركة بين الطرفين سرية لمدة 5 سنوات.

المادة السادسة: إنهاء الاتفاقية
يجوز لأي طرف إنهاء الاتفاقية بإشعار خطي قبل 30 يوماً.

وافق الطرفان على بنود هذه الاتفاقية.
"""

_TERMS_TEMPLATE_EN = """
DEALIX SERVICES AGREEMENT

Between:
Dealix Technology Company (Provider)
and
{company_name} (Client)

Article 1: Term
This agreement commences on {start_date} for a duration of {duration_months} months.

Article 2: Services
Provider shall grant Client access to the Dealix platform per the {plan} plan, including:
{features_list}

Article 3: Fees and Payment
Client shall pay SAR {price_sar} monthly.
{setup_fee_clause}

Article 4: Obligations
- Provider shall deliver services per highest quality standards.
- Client shall provide necessary information for service delivery.

Article 5: Confidentiality
All shared information shall remain confidential for 5 years.

Article 6: Termination
Either party may terminate with 30 days written notice.

Both parties agree to the terms herein.
"""


@dataclass
class Contract:
    id: str
    customer_id: str
    company_name: str
    plan: str
    price_sar: float
    duration_months: int
    start_date: str
    end_date: str
    body_ar: str = ""
    body_en: str = ""
    status: str = "draft"
    signed_at: datetime | None = None
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "company_name": self.company_name,
            "plan": self.plan,
            "price_sar": self.price_sar,
            "duration_months": self.duration_months,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "body_ar_preview": self.body_ar[:200] + "..." if len(self.body_ar) > 200 else self.body_ar,
            "body_en_preview": self.body_en[:200] + "..." if len(self.body_en) > 200 else self.body_en,
            "status": self.status,
            "signed_at": self.signed_at.isoformat() if self.signed_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class SigningResult:
    success: bool
    contract_id: str
    signing_url: str = ""
    status: str = "pending"
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "contract_id": self.contract_id,
            "signing_url": self.signing_url,
            "status": self.status,
            "errors": self.errors,
        }


PLAN_FEATURES = {
    "starter": ["- لوحة تحكم أساسية", "- تقارير أسبوعية", "- دعم عبر البريد"],
    "growth": ["- لوحة تحكم متقدمة", "- تقارير يومية", "- دعم فوري", "- مولد مقدمات دافئة"],
    "scale": ["- جميع ميزات النمو", "- API كامل", "- مدير حساب مخصص", "- علامة بيضاء"],
    "enterprise": ["- حل مخصص", "- فريق مخصص", "- ضمان مستوى الخدمة", "- نشر داخلي"],
}


class ContractEngine:
    def __init__(self):
        self._contracts: dict[str, Contract] = {}
        self.log = logger.bind(component="contract_engine")

    async def generate(self, customer_id: str, plan: str, duration_months: int) -> Contract:
        now = utcnow()
        start_date = now.strftime("%Y-%m-%d")
        end_date = (now + timedelta(days=30 * duration_months)).strftime("%Y-%m-%d")

        features_list = "\n".join(PLAN_FEATURES.get(plan, PLAN_FEATURES["growth"]))
        setup_fee = 0 if plan == "starter" else (2999 if plan == "growth" else 7999)
        setup_fee_clause_ar = f"رسوم التفعيل: {setup_fee} ريال (مرة واحدة)." if setup_fee > 0 else ""
        setup_fee_clause_en = f"Setup fee: SAR {setup_fee} (one-time)." if setup_fee > 0 else ""

        from dealix.payments.subscription_manager import SubscriptionManager
        mgr = SubscriptionManager()
        plan_config = mgr.PLANS.get(plan, mgr.PLANS["growth"])

        context = {
            "company_name": f"عميل {customer_id[:8]}",
            "start_date": start_date,
            "duration_months": duration_months,
            "plan": plan,
            "features_list": features_list,
            "price_sar": plan_config["price_sar"],
            "setup_fee_clause": setup_fee_clause_ar,
        }
        body_ar = _TERMS_TEMPLATE_AR.format(**context)

        context_en = {**context, "setup_fee_clause": setup_fee_clause_en}
        body_en = _TERMS_TEMPLATE_EN.format(**context_en)

        contract = Contract(
            id=generate_id("ctr"),
            customer_id=customer_id,
            company_name=context["company_name"],
            plan=plan,
            price_sar=plan_config["price_sar"],
            duration_months=duration_months,
            start_date=start_date,
            end_date=end_date,
            body_ar=body_ar,
            body_en=body_en,
            status="draft",
        )
        self._contracts[contract.id] = contract
        self.log.info("contract_generated", id=contract.id, customer=customer_id, plan=plan)
        return contract

    async def render_pdf(self, contract_id: str) -> bytes:
        contract = self._contracts.get(contract_id)
        if not contract:
            raise ValueError(f"Contract {contract_id} not found")

        body = f"{contract.body_ar}\n\n---\n\n{contract.body_en}"
        return body.encode("utf-8")

    async def send_for_signature(self, contract_id: str) -> SigningResult:
        contract = self._contracts.get(contract_id)
        if not contract:
            return SigningResult(
                success=False,
                contract_id=contract_id,
                errors=["Contract not found"],
            )

        if contract.status != "draft":
            return SigningResult(
                success=False,
                contract_id=contract_id,
                errors=[f"Invalid status: {contract.status}"],
            )

        contract.status = "sent_for_signature"

        result = SigningResult(
            success=True,
            contract_id=contract_id,
            signing_url=f"https://dealix.ai/contracts/sign/{contract_id}",
            status="sent",
        )
        self.log.info("contract_sent_for_signature", contract_id=contract_id)
        return result

    def get_contract(self, contract_id: str) -> Contract | None:
        return self._contracts.get(contract_id)

    def list_contracts(self, customer_id: str | None = None) -> list[Contract]:
        if customer_id:
            return [c for c in self._contracts.values() if c.customer_id == customer_id]
        return list(self._contracts.values())

    def get_stats(self) -> dict[str, Any]:
        contracts = self._contracts.values()
        total_value = sum(c.price_sar * c.duration_months for c in contracts if c.status in ("sent_for_signature", "signed"))
        return {
            "total_contracts": len(contracts),
            "draft": sum(1 for c in contracts if c.status == "draft"),
            "sent_for_signature": sum(1 for c in contracts if c.status == "sent_for_signature"),
            "signed": sum(1 for c in contracts if c.status == "signed"),
            "total_contract_value_sar": total_value,
            "avg_duration_months": round(
                sum(c.duration_months for c in contracts) / len(contracts), 1
            ) if contracts else 0,
        }
