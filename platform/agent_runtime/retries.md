# Retry Strategy

## Retry Classes

- transient: network/provider timeout
- recoverable: temporary dependency outage
- terminal: policy rejection / invalid contract

## Policy

- exponential backoff
- max attempts per class
- idempotency key required
- persist retry reason and outcome

## Escalation Trigger

عند exhaustion:

- stop autonomous retries
- notify approval/escalation path
- attach run evidence for human review
