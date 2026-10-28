# Bounded task cards

## CART-T1: coupon calculation

- Repo: `cart_service`
- Requirements: CART-01, CART-02, CART-03
- Scope: add coupon calculation while preserving `calculate_total(items)` and numeric output.
- Before edit: inspect current contract; confirm approved rounding/timezone decision and the inclusive one-hour grace cutoff in the design note.
- Required evidence: valid code; case-insensitive match; activation boundary; exact expiry; within the grace period; exact one-hour cutoff and just after; percentage bounds; cap; zero floor; regression on old API; no dependency change.
- Stop condition: approved rounding or timestamp policy absent, grace cutoff ambiguous, or implementation requires changing the existing public contract. The approved policies for this checkout are recorded in `design_note.md`.
- Out of scope: tax, shipping, UI, database, payment provider.

## NOTIF-T1: bounded transient retry

- Repo: `notification_service`
- Requirements: NOTIF-01, NOTIF-02, NOTIF-03
- Scope: retry only the approved temporary exception, maximum three total sends, waits of one and two seconds between attempts.
- Required evidence: immediate success; temporary then success; three temporary failures; permanent 4xx once; exact delays; fake sender/sleeper; unchanged interface.
- Stop condition: error classification is not explicit or retry behavior would change the public sender contract.
- Out of scope: provider integration, persistence, production sending, distributed delivery guarantees.

## Independence check

These can run in parallel after requirements and cross-cutting review rules are agreed because they use separate repositories and do not modify a shared interface. If both tasks need a shared library, schema, or contract change, resolve that dependency first or serialize the work.
