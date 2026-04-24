"""
Prospector Agent — discovers real leads matching a natural-language ICP.

Inputs:
    icp: str           — Arabic or English description of the ideal target
    use_case: str      — sales | partnership | collaboration | investor | b2c_audience
    count: int         — how many leads to return (max 20)

Output: list[LeadCandidate] with:
    company_ar, company_en, industry, est_size, website, linkedin, decision_maker_hints,
    signals, outreach_opening (Saudi Khaliji Arabic), fit_score (0-100), evidence

Design principles:
  - Public-data only; no scraping behind auth walls
  - LLM is grounded with strict "only real entities you're confident exist" prompt
  - Output is normalized JSON; invalid entries are dropped
  - Use case steers both the query and the scoring
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict
from typing import Any

from core.agents.base import BaseAgent
from core.config.models import Task
from core.llm import Message

MAX_COUNT = 20
USE_CASES = {
    "sales": "استهداف مبيعات B2B — بحث عن شركات عندها الألم ومتخذي قرار واضحين.",
    "partnership": "شراكات استراتيجية — شركات عندها قنوات توزيع أو منتجات مكمّلة.",
    "collaboration": "تعاون محتوى/تقني — صانعي محتوى، thought leaders، منتجات متكاملة.",
    "investor": "مستثمرون/VC — صناديق ومستثمرين نشطين في السوق السعودي.",
    "b2c_audience": "جمهور B2C — شرائح ديموغرافية محددة بسلوك شرائي واضح.",
}

SYSTEM_PROMPT = """أنت محلل أسواق خليجي خبير في السوق السعودي ومنطقة الخليج.
مهمتك: توليد قائمة leads حقيقية مطابقة لوصف العميل المثالي (ICP).

قواعد صارمة:
1. **لا تختلق شركات**. اقترح فقط كيانات أنت متأكد منها من معرفتك الموسوعية.
2. إذا الطلب يصعب تلبيته بدقة، أرجع قائمة أقصر بدل اختراع أسماء.
3. لكل lead، قدّر نسبة الثقة من 0-100 في صحة البيانات.
4. للتخصصات السعودية/الخليجية، استخدم الاسم العربي الرسمي + الاسم الإنجليزي.
5. المواقع (website) فقط لو متأكد — وإلا اترك الحقل فاضي (null).
6. LinkedIn URLs فقط لو شبه متأكد من صحة الرابط — وإلا اتركه فاضي.
7. أشر للإشارات المنشورة علناً فقط (إعلانات تمويل، إطلاقات، توظيف، تصريحات).
8. أعد JSON صالح فقط بدون أي نص آخر.

تنسيق JSON المطلوب:
{
  "leads": [
    {
      "company_ar": "الاسم العربي",
      "company_en": "English Name",
      "industry": "SaaS / E-commerce / Fintech / ...",
      "est_size": "1-10 | 10-50 | 50-200 | 200-1000 | 1000+",
      "website": "https://example.com or null",
      "linkedin": "https://linkedin.com/company/X or null",
      "decision_maker_hints": ["CEO الاسم", "CTO الاسم"],
      "signals": ["جولة Series A 2025", "توسع في الرياض"],
      "outreach_opening": "سطر افتتاحي قصير باللهجة الخليجية يذكر إشارة واحدة محددة",
      "fit_score": 85,
      "confidence": 80,
      "evidence": "السبب اللي خلاك تقترحه — معلومة واحدة محددة"
    }
  ],
  "search_notes": "ملاحظات وجيزة — مصادر المعلومات وحدود الدقة"
}
"""


@dataclass
class LeadCandidate:
    company_ar: str
    company_en: str
    industry: str
    est_size: str
    website: str | None
    linkedin: str | None
    decision_maker_hints: list[str]
    signals: list[str]
    outreach_opening: str
    fit_score: int
    confidence: int
    evidence: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ProspectResult:
    use_case: str
    icp: str
    count_requested: int
    count_returned: int
    leads: list[LeadCandidate]
    search_notes: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "use_case": self.use_case,
            "icp": self.icp,
            "count_requested": self.count_requested,
            "count_returned": self.count_returned,
            "leads": [l.to_dict() for l in self.leads],
            "search_notes": self.search_notes,
        }


class ProspectorAgent(BaseAgent):
    """
    Natural-language ICP → ranked list of real leads.
    Uses the LLM router's RESEARCH task (Gemini primary, with fallback chain).
    """

    name = "prospector"

    async def run(
        self,
        icp: str,
        use_case: str = "sales",
        count: int = 10,
    ) -> ProspectResult:
        count = max(1, min(MAX_COUNT, int(count)))
        use_case = (use_case or "sales").strip().lower()
        if use_case not in USE_CASES:
            use_case = "sales"

        user_prompt = self._build_user_prompt(icp=icp, use_case=use_case, count=count)

        self.log.info(
            "prospector_run use_case=%s count=%d icp_len=%d",
            use_case,
            count,
            len(icp or ""),
        )

        response = await self.router.run(
            task=Task.RESEARCH,
            messages=[Message(role="user", content=user_prompt)],
            system=SYSTEM_PROMPT,
            max_tokens=4096,
            temperature=0.3,
        )

        parsed = self._parse_json(response.text)
        raw_leads = parsed.get("leads") or []
        search_notes = str(parsed.get("search_notes") or "")

        leads: list[LeadCandidate] = []
        for item in raw_leads[:count]:
            lead = self._safe_lead(item)
            if lead is not None:
                leads.append(lead)

        # Sort by combined fit * confidence
        leads.sort(key=lambda l: l.fit_score * l.confidence, reverse=True)

        return ProspectResult(
            use_case=use_case,
            icp=icp,
            count_requested=count,
            count_returned=len(leads),
            leads=leads,
            search_notes=search_notes,
        )

    # ── internals ──────────────────────────────────────────────
    def _build_user_prompt(self, *, icp: str, use_case: str, count: int) -> str:
        return (
            f"حالة الاستخدام: {use_case} — {USE_CASES[use_case]}\n\n"
            f"وصف العميل المثالي (ICP):\n{icp.strip()}\n\n"
            f"أعد {count} leads حقيقية مطابقة للـ ICP، مرتّبة من الأعلى fit_score.\n"
            f"إذا الطلب متعلق بالسعودية أو الخليج، ركّز على الشركات المحلية أولاً.\n"
            f"تذكير: لا تختلق شركات. أعد JSON فقط — بدون markdown code fences."
        )

    @staticmethod
    def _parse_json(text: str) -> dict[str, Any]:
        if not text:
            return {}
        # Strip optional code fences
        t = text.strip()
        t = re.sub(r"^```(?:json)?\s*", "", t)
        t = re.sub(r"\s*```$", "", t)
        try:
            return json.loads(t)
        except Exception:
            # Try to extract the first {...} block
            m = re.search(r"\{.*\}", t, re.DOTALL)
            if not m:
                return {}
            try:
                return json.loads(m.group(0))
            except Exception:
                return {}

    @staticmethod
    def _safe_lead(item: Any) -> LeadCandidate | None:
        if not isinstance(item, dict):
            return None
        try:
            company_ar = str(item.get("company_ar") or "").strip()
            company_en = str(item.get("company_en") or "").strip()
            if not (company_ar or company_en):
                return None
            return LeadCandidate(
                company_ar=company_ar or company_en,
                company_en=company_en or company_ar,
                industry=str(item.get("industry") or "").strip(),
                est_size=str(item.get("est_size") or "").strip(),
                website=(str(item.get("website")).strip() if item.get("website") else None),
                linkedin=(str(item.get("linkedin")).strip() if item.get("linkedin") else None),
                decision_maker_hints=[
                    str(x) for x in (item.get("decision_maker_hints") or []) if x
                ][:5],
                signals=[str(x) for x in (item.get("signals") or []) if x][:5],
                outreach_opening=str(item.get("outreach_opening") or "").strip()[:280],
                fit_score=int(max(0, min(100, item.get("fit_score") or 0))),
                confidence=int(max(0, min(100, item.get("confidence") or 0))),
                evidence=str(item.get("evidence") or "").strip()[:280],
            )
        except Exception:
            return None
