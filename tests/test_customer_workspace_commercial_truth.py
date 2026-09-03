from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LIVE_SURFACES = [
    ROOT / "scripts" / "create_customer_workspace.py",
    ROOT / "scripts" / "run_dealix_e2e_dry_run.py",
    *sorted((ROOT / "customers" / "_template").glob("*.md")),
]


def joined() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in LIVE_SURFACES)


def test_live_customer_workspace_has_canonical_pilot_path() -> None:
    text = joined()
    assert "Free Mini Diagnostic" in text
    assert "Qualified Discovery" in text
    assert "30-Day Revenue Command Pilot" in text
    assert "STOP / EXPAND / REDESIGN" in text


def test_live_customer_workspace_has_no_retired_fixed_price_authority() -> None:
    text = joined()
    for forbidden in (
        "499 SAR",
        "4,999 SAR",
        "Indicative price (SAR)",
        "State the fixed sprint price",
        "Paid Sprint Simulation",
    ):
        assert forbidden not in text


def test_customer_next_action_board_is_agent_owned() -> None:
    board = (ROOT / "customers" / "_template" / "07_next_action_board.md").read_text(encoding="utf-8")
    assert "`dealix-sales`" in board
    assert "`dealix-delivery`" in board
    assert "`dealix-pm`" in board
    assert "`dealix-content`" in board
    assert "all tasks | founder" not in board.lower()


def test_proof_pack_separates_material_truth_states() -> None:
    proof = (ROOT / "customers" / "_template" / "10_proof_pack.md").read_text(encoding="utf-8")
    for required in (
        "Delivery evidence",
        "Payment evidence",
        "Customer value",
        "Publication permission",
    ):
        assert required in proof


def test_expansion_file_cannot_auto_upsell() -> None:
    review = (ROOT / "customers" / "_template" / "11_upsell_recommendation.md").read_text(encoding="utf-8")
    assert "not an automatic upsell surface" in review
    assert "No automatic renewal/upsell" in review
    assert "Indicative price" not in review
