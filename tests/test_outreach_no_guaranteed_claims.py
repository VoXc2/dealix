"""No forbidden/guaranteed claim appears in any OUTBOUND artifact (drafts,
content ideas). The forbidden list and policy docs are intentionally excluded —
they cite examples as data, not as outbound copy."""
import _loaders as L


def test_drafts_have_no_forbidden_claims():
    fb = L.forbidden()
    for d in L.load_jsonl("data/outreach/drafts.jsonl"):
        hits = L.find_forbidden(d.get("subject", "") + " " + d.get("body", ""), fb)
        assert not hits, f"draft {d['draft_id']} contains forbidden claim(s): {hits}"


def test_content_ideas_have_no_forbidden_claims():
    fb = L.forbidden()
    for post in L.load_jsonl("data/content/post_ideas.jsonl"):
        hits = L.find_forbidden(post.get("hook", ""), fb)
        assert not hits, f"post {post['idea_id']} contains forbidden claim(s): {hits}"


def test_forbidden_list_is_populated():
    fb = L.forbidden()
    # Sanity: the block-list itself must be non-trivial, else the scan is vacuous.
    assert len(fb["phrases"]) >= 10
    assert "10x" in " ".join(fb["phrases"])
