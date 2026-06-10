# DEALIX PROMPT TEMPLATES v3.0
# Copy into Aider for maximum results

## Template 1: Daily Refactoring (Gear 1)
Task: Refactor [FILE_PATH] for clarity and maintainability.
Requirements:
- Follow PEP 8 strictly
- Add type hints to all functions
- Keep functions under 40 lines
- Use Pydantic v2 models for data structures
- Run pytest and ensure all pass
- Do NOT change business logic, only structure
Output: SEARCH/REPLACE blocks for modified files.

## Template 2: New Feature (Gear 2)
Task: Implement [FEATURE_NAME] in Dealix.
Context:
- Read dealix/llm/engine.py first
- Must fit the 5-plane architecture (Decision/Execution/Trust/Data/Operating)
- Use DecisionOutput with Approval/Risk/Sensitivity classes
- Add bilingual AR/EN support where user-facing
- Write pytest tests with >80% coverage
- Update .env.example if new env vars needed
Output:
1. New file content (complete)
2. Test file
3. Integration steps

## Template 3: Architecture Decision (Gear 3)
Task: Design [SYSTEM_COMPONENT] for Dealix.
Requirements:
- Must comply with PDPL Art. 5/13/14/18/21
- ZATCA Phase 2 compatible where financial
- Include PolicyEvaluator integration (A2+ approval required)
- Evidence pack required: sources, alternatives, risks
- Bilingual board-grade memo (AR/EN)
Output:
1. Design document (markdown)
2. Implementation plan with phases
3. Skeleton code with TODOs
4. Risk register entries

## Template 4: Bug Fix (Gear 2)
Task: Fix bug in [AREA].
Evidence:
- Error message: [PASTE]
- Expected behavior: [DESCRIBE]
- Actual behavior: [DESCRIBE]
Steps:
1. Add logging to isolate root cause
2. Write minimal reproduction test
3. Fix with tests passing
4. Update evidence pack if Trust Plane involved
Output: Root cause (1 sentence) + fix + test.

## Template 5: Compliance Audit (Gear 3)
Task: Audit [MODULE] for Saudi compliance.
Checklist:
- PDPL lawful basis documented
- Data retention schedule defined
- Cross-border transfer posture assessed
- NCA ECC 2-2024 controls mapped
- No hardcoded secrets (bandit/gitleaks clean)
Output: Compliance report + remediation plan.

## Template 6: Performance Optimization (Gear 1 or 2)
Task: Optimize [COMPONENT] for speed/memory.
Metrics:
- Baseline: [CURRENT_MS or MB]
- Target: [GOAL]
- Constraints: Must not break API contracts
Steps:
1. Profile with py-spy or cProfile
2. Identify bottleneck
3. Optimize (caching, async, query batching)
4. Validate with pytest
Output: Before/after metrics + code changes.

## Template 7: Agent Wiring (Gear 2)
Task: Connect new agent to Trust Plane.
Requirements:
- Agent outputs DecisionOutput
- PolicyEvaluator returns ALLOW/DENY/ESCALATE
- ApprovalRequest created for A1+ actions
- Audit trail written to AuditSink
- Tool calls verified via ToolVerificationLedger
Output: Agent code + Trust Plane integration + tests.

## Template 8: Credit-Safe Mode (Auto-Gear 1)
Task: [ANY_TASK] but minimize token usage.
Rules:
- Use Gear 1 (DeepSeek) only
- Keep responses under 2000 tokens
- No unnecessary explanations
- Focus on the exact change needed
- Skip tests if already covered
Output: Minimal SEARCH/REPLACE blocks only.
