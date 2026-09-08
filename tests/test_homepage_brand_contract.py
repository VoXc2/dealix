from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "apps" / "web" / "components" / "landing" / "InteractiveHome.tsx"
CSS = ROOT / "apps" / "web" / "app" / "interactive-home.css"
LAYOUT = ROOT / "apps" / "web" / "app" / "layout.tsx"
LOGO = ROOT / "apps" / "web" / "public" / "dealix-logo.svg"
MARK = ROOT / "apps" / "web" / "public" / "dealix-mark.svg"
OG = ROOT / "apps" / "web" / "public" / "dealix-og.svg"


def test_interactive_home_uses_canonical_brand_assets():
    home = HOME.read_text(encoding="utf-8")
    layout = LAYOUT.read_text(encoding="utf-8")

    assert LOGO.exists()
    assert MARK.exists()
    assert OG.exists()
    assert 'src="/dealix-logo.svg"' in home
    assert 'src="/dealix-mark.svg"' in home
    assert "/dealix-og.svg" in layout
    assert "/og-image.png" not in layout


def test_interactive_home_preserves_current_positioning_and_path():
    home = HOME.read_text(encoding="utf-8")

    for required in [
        "AI Business Operating System",
        "Revenue + Proof + Command",
        "Execution Diagnostic",
        "Qualified Discovery",
        "Customer-Specific Outcome Sprint",
        "Proof Review",
        "Dealix Runtime",
        "Research",
        "Relationship",
        "Public contact",
        "Consent",
        "Draft",
        "Sent",
        "Invoice",
        "Payment",
        "Customer Proof",
    ]:
        assert required in home


def test_interactive_home_rejects_stale_or_forbidden_claims():
    home = HOME.read_text(encoding="utf-8")

    for stale_or_forbidden in [
        "8 AI Agents",
        "v3.1",
        "Production Ready",
        "guaranteed revenue",
        "first Saudi AI Business Operating System",
        "first in Saudi Arabia",
    ]:
        assert stale_or_forbidden not in home


def test_interactive_home_keeps_accessible_motion_contract():
    css = CSS.read_text(encoding="utf-8")

    assert "prefers-reduced-motion: reduce" in css
    assert "animation-duration: .001ms" in css
    assert ".dx-nav-links a:hover, .dx-nav-links a:focus-visible" in css


def test_interactive_pointer_effect_is_bounded_to_mouse_animation_frames():
    home = HOME.read_text(encoding="utf-8")

    assert 'event.pointerType !== "mouse"' in home
    assert "window.requestAnimationFrame" in home
    assert "window.cancelAnimationFrame" in home
    assert 'fetchPriority="high"' in home


def test_below_fold_sections_use_dependency_free_render_containment():
    home = HOME.read_text(encoding="utf-8")

    assert 'contentVisibility: "auto"' in home
    assert 'containIntrinsicSize: "auto 720px"' in home
    assert home.count("style={deferredSectionStyle}") >= 4
