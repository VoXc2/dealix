"""Third-party integration clients used outside of /integrations/ legacy code.

The older `/integrations/` package (top-level) hosts the legacy provider
SDKs (HubSpot, WhatsApp, ZATCA). This `dealix.integrations` package is
where new commercial SaaS integrations live — Plain, Knock, BetterStack,
Apollo, Clearbit, Wathq, Loops, Lago, Infisical.

Each module exposes a single client class, prefers feature-flag
configuration via env, and falls back silently when its key is absent.
"""

from __future__ import annotations
