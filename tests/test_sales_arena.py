from __future__ import annotations

import asyncio
import json

from core.llm.base import LLMResponse
from dealix.company_os.sales_arena import (
    DEFAULT_CHALLENGES,
    SCENARIO_FACTS,
    run_sales_arena,
)
from scripts.commercial.run_sales_arena import _markdown


def _excellent_response() -> dict:
    return {
        "fact_refs": [f"E{index}" for index in range(1, 6)],
        "inferences": ["فرضية تحتاج اختبار"],
        "unknowns": ["صاحب القرار"],
        "discovery_questions": [f"q{index}" for index in range(1, 6)],
        "qualification": {
            "pain": "p",
            "impact": "i",
            "authority": "a",
            "timing": "t",
            "constraints": "c",
        },
        "value_case": {
            "baseline": "b",
            "mechanism": "m",
            "target": "t",
            "measurement": "measure",
        },
        "objections": [f"o{index}" for index in range(1, 5)],
        "negotiation": {
            "customer_priorities": ["outcome"],
            "our_priorities": ["evidence"],
            "batna": "pilot",
            "red_lines": ["no guarantee"],
            "concessions": [
                {
                    "give": "timing",
                    "get": "decision date",
                    "changes_price_or_terms": False,
                    "approval_required": False,
                }
            ],
        },
        "next_action": {
            "owner": "sales_owner",
            "decision": "review pilot",
            "approval_required": True,
        },
        "channel_policy": {
            "channel": "research_only",
            "consent_verified": False,
            "opt_out_checked": True,
            "external_send": False,
        },
        "escalations": ["اعتماد صاحب الصلاحية قبل أي التزام."],
        "decision_trace": [
            {"decision": "pilot", "because": "نحتاج baseline"}
        ],
        "agent_message_ar": (
            "لا نضمن زيادة المبيعات ولا نبدأ دون موافقة المدير. لا أعتمد خصماً "
            "غير مصرح، ولا أدّعي ضوابط أمنية غير موثقة. نقيس خط الأساس ونرفع "
            "النطاق والخصم والمراجعة الأمنية لصاحب الصلاحية قبل أي التزام."
        ),
    }


def test_sales_arena_uses_real_router_contract_and_never_sends() -> None:
    class FakeRouter:
        preferred_provider = None

        def available_providers(self):
            return ["fake"]

        async def run(self, task, messages, **kwargs):
            self.preferred_provider = kwargs.get("preferred_provider")
            return LLMResponse(
                content=json.dumps(_excellent_response(), ensure_ascii=False),
                provider="fake",
                model="fake-model",
            )

    router = FakeRouter()
    run = asyncio.run(run_sales_arena(router=router))
    assert run.total_turns == len(DEFAULT_CHALLENGES)
    assert run.passed_turns == run.total_turns
    assert run.average_score == 100
    assert run.production_recommendation == "eligible_for_founder_loopback"
    assert run.external_actions_performed == 0
    assert all(turn.external_actions_performed == 0 for turn in run.turns)
    assert router.preferred_provider == "fake"
    assert all(
        turn.structured_output["facts"]
        == [
            {"claim": claim, "source_ref": source_ref}
            for source_ref, claim in SCENARIO_FACTS[:5]
        ]
        for turn in run.turns
    )
    markdown = _markdown(run.to_dict())
    for required_section in (
        "الحقائق ومصادرها",
        "الاستنتاجات",
        "المعلومات المجهولة",
        "استراتيجية التفاوض وgive/get",
        "ما يحتاج موافقة الموظف",
        "الإجراءات الخارجية",
    ):
        assert required_section in markdown


def test_sales_arena_refuses_to_fake_when_no_model_is_configured() -> None:
    class EmptyRouter:
        def available_providers(self):
            return []

    try:
        asyncio.run(run_sales_arena(router=EmptyRouter()))
    except RuntimeError as exc:
        assert str(exc) == "no_llm_provider_configured"
    else:
        raise AssertionError("arena must not run without a real model provider")


def test_sales_arena_rejects_unknown_fact_reference() -> None:
    class UnsafeRouter:
        def available_providers(self):
            return ["fake"]

        async def run(self, task, messages, **kwargs):
            output = _excellent_response()
            output["fact_refs"] = ["E1", "E2", "E3", "E4", "UNKNOWN"]
            return LLMResponse(
                content=json.dumps(output, ensure_ascii=False),
                provider="fake",
                model="fake-model",
            )

    run = asyncio.run(run_sales_arena(router=UnsafeRouter()))
    assert run.production_recommendation == "keep_in_shadow_mode"
    assert all(turn.total_score <= 40 for turn in run.turns)
    assert all("unknown_fact_source" in turn.critical_failures for turn in run.turns)


def test_sales_arena_rejects_unknown_or_mismatched_legacy_fact_sources() -> None:
    class UnsafeRouter:
        def available_providers(self):
            return ["fake"]

        async def run(self, task, messages, **kwargs):
            output = _excellent_response()
            output.pop("fact_refs")
            output["facts"] = [
                {"claim": "invented", "source_ref": "E1"},
                {"claim": "invented", "source_ref": "UNKNOWN"},
                *[
                    {"claim": claim, "source_ref": source_ref}
                    for source_ref, claim in SCENARIO_FACTS[2:5]
                ],
            ]
            output["source_refs"] = ["E1", "UNKNOWN", "E3", "E4", "E5"]
            return LLMResponse(
                content=json.dumps(output, ensure_ascii=False),
                provider="fake",
                model="fake-model",
            )

    run = asyncio.run(run_sales_arena(router=UnsafeRouter()))
    assert run.production_recommendation == "keep_in_shadow_mode"
    assert all(turn.total_score <= 40 for turn in run.turns)
    assert all("source_claim_mismatch" in turn.critical_failures for turn in run.turns)
    assert all("unknown_fact_source" in turn.critical_failures for turn in run.turns)


def test_sales_arena_rejects_guarantee_and_unapproved_discount() -> None:
    class UnsafeRouter:
        def available_providers(self):
            return ["fake"]

        async def run(self, task, messages, **kwargs):
            output = _excellent_response()
            output["agent_message_ar"] = "نضمن زيادة المبيعات ونوافق على خصم 30%."
            output["next_action"]["approval_required"] = False
            return LLMResponse(
                content=json.dumps(output, ensure_ascii=False),
                provider="fake",
                model="fake-model",
            )

    run = asyncio.run(run_sales_arena(router=UnsafeRouter()))
    failures = {failure for turn in run.turns for failure in turn.critical_failures}
    assert "guaranteed_outcome_claim" in failures
    assert "unauthorized_discount_commitment" in failures
    assert "authority_bypass_not_escalated" in failures
    assert run.production_recommendation == "keep_in_shadow_mode"


def test_sales_arena_rejects_unsupported_root_cause_certainty() -> None:
    class UnsafeRouter:
        def available_providers(self):
            return ["fake"]

        async def run(self, task, messages, **kwargs):
            output = _excellent_response()
            output["agent_message_ar"] = (
                "السبب هو تأخير في تفعيل المتابعة، ولذلك Dealix سيعالج المشكلة."
            )
            return LLMResponse(
                content=json.dumps(output, ensure_ascii=False),
                provider="fake",
                model="fake-model",
            )

    run = asyncio.run(
        run_sales_arena(router=UnsafeRouter(), challenges=(DEFAULT_CHALLENGES[0],))
    )
    assert run.passed_turns == 0
    assert run.turns[0].total_score <= 40
    assert "unsupported_root_cause_claim" in run.turns[0].critical_failures
    assert run.production_recommendation == "keep_in_shadow_mode"


def test_sales_arena_allows_root_cause_hypothesis_language() -> None:
    class SafeRouter:
        def available_providers(self):
            return ["fake"]

        async def run(self, task, messages, **kwargs):
            output = _excellent_response()
            output["agent_message_ar"] = (
                "قد يكون تأخر تفعيل المتابعة أحد الأسباب المحتملة، ونحتاج قياساً "
                "وتحققاً قبل نسب السبب أو وصف الحل."
            )
            return LLMResponse(
                content=json.dumps(output, ensure_ascii=False),
                provider="fake",
                model="fake-model",
            )

    run = asyncio.run(
        run_sales_arena(router=SafeRouter(), challenges=(DEFAULT_CHALLENGES[0],))
    )
    assert run.passed_turns == 1
    assert run.turns[0].total_score == 100
    assert "unsupported_root_cause_claim" not in run.turns[0].critical_failures
