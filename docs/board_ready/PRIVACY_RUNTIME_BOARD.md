# Privacy Runtime Board

A live view of runtime privacy posture.

## 1. Indicators

- PII detected
- Redactions applied
- Policy decisions
- Blocked disclosures
- External-use attempts
- Source passports missing
- Approval required
- Approval completed

## 2. Derived

- **Open approvals** = required − completed.
- **Has open risks** = `passports_missing > 0 OR open_approvals > 0 OR blocked_disclosures > 0`.

## 3. Typed surface

`board_ready_os.privacy_runtime_board.PrivacyRuntimeBoardSnapshot`.

## 4. The principle

> Privacy posture is operated, not declared.
