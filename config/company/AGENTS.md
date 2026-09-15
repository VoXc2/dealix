# Dealix company-config agent precedence

This scoped file applies to `config/company/**` and refines the root `AGENTS.md`.

Machine-readable company configuration is authority-sensitive. Do not create parallel registries, duplicate commercial truth, second schedulers, second model routers, or independent approval/proof/economic stores.

Canonical architecture is Omega V3:
`Holding -> Control Plane -> Sector Companies -> Arm Pods -> Specialist Logical Agents -> ResourceGovernor-bounded runtime workers`.

Rules for config changes:
- Fixed-five lists are legacy executor aliases only, never current logical-agent count authority.
- Arm/sector counts are inventory snapshots, not permanent architecture constraints.
- Historical `deep_wip_max=3` must never be interpreted as a global runtime worker ceiling. Runtime capacity belongs to ResourceGovernor/Session Factory; business Top-3 may remain explicit economic prioritization where clearly labelled.
- Automatic model policy is provider-neutral local/free-first and fail-closed: deterministic/no-model -> adequate local/private -> eligible verified-free -> trusted-current included capacity -> HOLD. DeepSeek is eligible only through the canonical broker when explicit-free or trusted included evidence passes cost/data/privacy gates. Provider namespaces, worker env, caller args and self-authored refs do not prove cost/privacy authority. Legacy direct-provider no-DeepSeek guards remain compatibility isolation for legacy/direct runtime, not global canonical model policy.
- Paid spill is disabled by default; exceptional paid use is separate exact action-bound authority.
- Public commercial truth is free diagnostic -> qualified discovery -> customer-specific quote; no fixed public price/duration authority.
- Config migrations must preserve compatibility/provenance explicitly and add validation tests that reject re-promotion of legacy values into current authority.
- Never add raw secrets, credentials or provider tokens to repository config.

Production/DNS/DB/provider/billing mutation is not authorized by changing repository config; those remain separate exact L5 effects.
