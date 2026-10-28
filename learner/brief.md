# Business brief: safer checkout and more reliable order notifications

## The situation

A small online shop has two separately owned services. Checkout is maintained in one repository and notification delivery in another. Product wants to reduce checkout friction with coupons. Operations wants order confirmation messages to survive temporary provider failures. A coding agent can implement quickly, but two independent changes can create two pull requests at once. The team needs a way to specify, delegate, and review that work without confusing speed with correctness.

## The business outcomes

1. A valid coupon changes the checkout total predictably and preserves the existing caller contract.
2. A temporary notification failure gets a bounded retry, while a permanent client error stops promptly.
3. No real payment, email, or network provider is contacted by this exercise.
4. Every implementation claim can be traced to a requirement, a changed line, and evidence.
5. A named human reviewer makes the final merge decision.

## Requirements and acceptance evidence

| ID | Requirement | Evidence expected |
|---|---|---|
| CART-01 | Match a coupon code without case sensitivity. Apply it when UTC `active_from <= now <= expires_at + 1 hour`. The grace period is 60 elapsed minutes. | Tests for matching case, different case, just before activation, exact activation, just before expiry, exact expiry, within the grace period, exact one-hour cutoff, and just after the cutoff. |
| CART-02 | Accept percentages from 0 through 100 inclusive; cap the discount at 50 currency units; total must not fall below zero. | Tests for 0%, 100%, invalid below/above range, capped discount, zero floor. |
| CART-03 | Keep `calculate_total(items)` callable with the same signature and numeric return type. Add no third-party package. | Existing caller remains valid; regression test; dependency file unchanged. |
| NOTIF-01 | Retry a temporary failure for at most three total send attempts. Wait 1 second before attempt 2 and 2 seconds before attempt 3. | Deterministic tests using an injected sleeper and fake sender. |
| NOTIF-02 | Do not retry permanent 4xx client errors. | A 4xx fake failure produces exactly one attempt and no wait. |
| NOTIF-03 | Preserve the sender interface and avoid real network calls in unit tests. | Fake sender tests; no credentials or provider endpoint. |
| GOV-01 | PR description names requirement IDs, changed files, tests run, and unresolved risks. | Completed PR template. |
| GOV-02 | Human reviewer checks business boundaries and latest revision before merge. | Named reviewer and explicit decision in the review record. |

## Explicit assumptions to challenge

- Coupon timestamps must be timezone-aware UTC datetimes. Naive or nonzero-offset timestamps are rejected.
- A coupon remains usable for one hour after `expires_at`, including the exact one-hour cutoff. After that cutoff it is invalid.
- “Three attempts” counts the first send plus two retries, not three retries after the first.
- Waits happen only between retryable attempts: 1 second, then 2 seconds. There is no wait after the final failure.
- Round the final coupon-adjusted total to two decimal places using half-up rounding, as recorded in `design_note.md`.
- “Temporary failure” must have an explicit type or status classification. Do not retry every exception indiscriminately.

## Out of scope

Taxes, shipping, persistence, queueing, user interface, payment provider, real message sending, production deployment, distributed exactly-once semantics, and broad refactoring.

## Definition of done

A change is ready for human review when it is small, requirement IDs appear in the plan and PR, contract tests pass, relevant edge cases are tested, the diff is focused, reported test evidence was run on the latest revision, and unresolved risks are visible. “Ready for review” is not the same as “approved” or “merged.”
