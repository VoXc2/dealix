"""Live integration smoke test: ingest company + opportunity + verify priority view."""
import asyncio, os, sys, uuid
sys.path.insert(0, "/opt/dealix/ai_cro/opportunity_graph")
from graph_api import OpportunityGraph

async def main():
    dsn = os.getenv("DATABASE_URL", "postgresql://dealix:dealix_local_dev_2026@127.0.0.1:5432/dealix")
    g = OpportunityGraph(dsn=dsn)
    await g.connect()
    try:
        # unique CR per run for repeatability
        cr = f"70{uuid.uuid4().int % 10**8:08d}"
        cid = await g.upsert_company(
            name_ar="شركة الأهلية للعقارات",
            cr_number=cr,
            sector="real_estate",
            region="الرياض",
            size_employees=180,
            source="integration_test",
        )
        print(f"company_id = {cid}")

        oid = await g.create_opportunity(
            company_id=cid,
            title_ar="صفقة مجمع سكني الملك فهد",
            expected_value_sar=2_500_000,
            win_probability=0.62,
            supporting_signal_ids=[],
            suggested_action="مكالمة اكتشاف مع مدير التطوير",
            evidence_summary="بحث السوق + إشارات تمويل حديثة من SAMA",
            owner_approval_required=False,
            created_by_agent="discovery_agent",
        )
        print(f"opportunity_id = {oid}")

        # query priority view directly
        async with g.pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT id, title_ar, company_name, stage, weighted_value "
                "FROM v_priority_opportunities ORDER BY weighted_value DESC NULLS LAST LIMIT 5"
            )
        print(f"\npriority view returned {len(rows)} row(s):")
        for r in rows:
            print(f"  [{r['stage']:10s}] {r['company_name']} — {r['title_ar']} "
                  f"(weighted: {r['weighted_value']})")

        print("\n✅ Live integration test PASSED")
    finally:
        await g.close()

if __name__ == "__main__":
    asyncio.run(main())
