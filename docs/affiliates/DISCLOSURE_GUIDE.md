# Disclosure Guide — دليل الإفصاح

Every affiliate post that promotes Dealix must disclose the affiliate
relationship. This is a condition of the program and a requirement of fair
advertising practice.

## The required disclosure

Approved affiliate assets carry the disclosure text automatically — it is
appended by `affiliate_os/asset_registry.review_asset_copy()` from
`affiliate_rules.yaml`:

**English**

> Affiliate disclosure: I earn a commission if you purchase via my link.
> Estimated outcomes are not guaranteed outcomes.

**العربية**

> إفصاح الشراكة: أحصل على عمولة عند الشراء عبر رابطي. النتائج التقديرية ليست
> نتائج مضمونة.

## How to disclose well

- Place the disclosure where the reader sees it **before** they act on the
  link — not buried at the end.
- Use the affiliate's own voice, but keep both elements: (1) you earn a
  commission, (2) outcomes are estimates, not guarantees.
- On short-form channels, the disclosure still appears in full — there is no
  short version.

## Where the text comes from

The canonical disclosure copy is `disclosure_text` in
`affiliate_os/config/affiliate_rules.yaml`. Update it there; approved assets
pick up the current text at review time. `get_disclosure_text(locale)` returns
it programmatically.
