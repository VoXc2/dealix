# Final Repository Structure

The doctrine proposes a canonical numbered docs tree and a canonical code tree. The repository already realizes that structure under **named folders**. This document maps each numbered slot to where it lives today, so the doctrine and the repo stay aligned without forcing a destructive rename.

## 1. Proposed numbered docs → realized location

| Proposed | Realized |
| --- | --- |
| `docs/00_constitution/` | `docs/endgame/ENDGAME_OPERATING_DOCTRINE.md` and the rest of `docs/endgame/` |
| `docs/01_method/` | `docs/operating_manual/` (this layer) |
| `docs/02_core_os/` | `docs/global_grade/CORE_OS_GLOBAL.md` |
| `docs/03_data_os/` | `docs/sovereignty/DATA_SOVEREIGNTY_STANDARD.md`, `docs/sovereignty/SOURCE_PASSPORT_STANDARD.md` |
| `docs/04_governance/` | `docs/endgame/RUNTIME_GOVERNANCE_PRODUCT.md`, `docs/global_grade/RUNTIME_GOVERNANCE_PRODUCT.md`, `docs/command_control/GOVERNANCE_COMMAND.md` |
| `docs/05_llm_gateway/` | `docs/sovereignty/MODEL_ROUTER_STRATEGY.md` |
| `docs/06_services/` | `docs/endgame/PRODUCTIZED_OFFER_STACK.md`, `docs/strategic_control/PRODUCT_LINES_V2.md` |
| `docs/07_proof/` | `docs/endgame/PROOF_ECONOMY.md`, `docs/sovereignty/PROOF_SOVEREIGNTY.md`, `docs/command_control/PROOF_COMMAND.md`, `docs/operating_manual/PROOF_TO_RETAINER_SYSTEM.md` |
| `docs/08_capital/` | `docs/endgame/CAPITAL_LEDGER_STRATEGY.md`, `docs/sovereignty/CAPITAL_SOVEREIGNTY.md`, `docs/command_control/CAPITAL_COMMAND.md` |
| `docs/09_intelligence/` | `docs/endgame/INTELLIGENCE_OS.md` |
| `docs/10_command/` | `docs/command_control/` (entire folder) |
| `docs/11_business_units/` | `docs/endgame/BUSINESS_UNITS.md`, `docs/global_grade/BUSINESS_UNITS.md`, `docs/command_control/BUSINESS_UNIT_COMMAND.md` |
| `docs/12_market_power/` | `docs/endgame/MARKET_POWER.md`, `docs/global_grade/MARKET_POWER_SCORE.md`, `docs/command_control/MARKET_COMMAND.md`, `docs/sovereignty/MARKET_SOVEREIGNTY.md`, `docs/strategic_control/MARKET_COMMAND_DASHBOARD.md` |
| `docs/13_standards/` | `docs/strategic_control/MARKET_LEADERSHIP_STACK.md`, plus per-standard docs across the layers |
| `docs/14_academy/` | `docs/endgame/ACADEMY_STRATEGY.md`, `docs/global_grade/ACADEMY_PARTNERS.md` |
| `docs/15_partners/` | `docs/global_grade/ACADEMY_PARTNERS.md`, `docs/sovereignty/DISTRIBUTION_SOVEREIGNTY.md` |
| `docs/16_ventures/` | `docs/endgame/VENTURE_FACTORY.md` |
| `docs/17_investment/` | `docs/endgame/CAPITAL_LEDGER_STRATEGY.md` (capital allocation), plus the venture factory |
| `docs/18_sovereignty/` | `docs/sovereignty/` (entire folder) |

## 2. Proposed code → realized location

| Proposed package | Realized package(s) |
| --- | --- |
| `core_os/` | existing pre-doctrine modules + `endgame_os/operating_chain.py` |
| `data_os/` | existing pre-doctrine modules + `global_grade_os/enterprise_trust.py`, `sovereignty_os/source_passport_standard.py` |
| `governance_os/` | existing pre-doctrine modules + `endgame_os/governance_product.py`, `global_grade_os/runtime_governance_product.py`, `command_control_os/governance_command.py` |
| `llm_gateway/` | existing pre-doctrine modules + `sovereignty_os/model_router_strategy.py` |
| `revenue_os/` | existing pre-doctrine modules + `endgame_os/business_units.py` |
| `brain_os/` | existing pre-doctrine modules |
| `operations_os/` | existing pre-doctrine modules |
| `reporting_os/` | existing pre-doctrine modules + `command_control_os/proof_command.py`, `operating_manual_os/proof_to_retainer.py` |
| `capital_os/` | existing pre-doctrine modules + `command_control_os/capital_command.py`, `sovereignty_os/capital_sovereignty.py` |
| `intelligence_os/` | existing pre-doctrine modules + `endgame_os/`, `strategic_control_os/control_metrics.py` |
| `command_os/` | existing pre-doctrine modules + `command_control_os/command_center.py` |
| `business_units/` | `endgame_os/business_units.py`, `command_control_os/`, `global_grade_os/` |
| `market_power_os/` | `endgame_os/market_power.py`, `global_grade_os/market_power_score.py`, `strategic_control_os/market_command_dashboard.py` |
| `venture_os/` | `endgame_os/venture_factory.py` |

## 3. Why named folders, not numbers

- Renaming destroys git history and breaks imports across the repo.
- The numbered slots are an **organizational ideal**; named folders are the **operational reality**.
- The mapping above is the canonical resolution between the two.
- New layers continue to land under named folders; the mapping is updated.

## 4. The principle

> A canonical layout is useful only when it does not require destructive moves. The map is the layout.
