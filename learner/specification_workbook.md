# Specification workbook

Complete this before implementation. Work in pairs. One person plays product owner; one plays technical lead. The product owner may clarify business outcomes but must not silently make technical decisions.

## Part A: Rewrite one vague sentence

Original: “Coupons should work and notifications should retry.”

For each behavior, write an observable condition, a boundary, a failure response, and a test that could prove it.

| Behavior | Given | When | Then | Boundary to test | Requirement ID |
|---|---|---|---|---|---|
| Coupon active window |  |  |  |  |  |
| Coupon expiry and one-hour grace |  |  |  | Exact expiry, within grace, exact one-hour cutoff, just after cutoff | CART-01 |
| Temporary notification error |  |  |  |  |  |
| Permanent client error |  |  |  |  |  |

## Part B: Split facts, decisions, assumptions, questions

- Fact stated in the brief:
- Decision required before implementation:
- Assumption we must not hide:
- Question to ask the product owner:
- What happens if two people interpret this differently?

## Part C: Design note

Use `design_note_template.md`. The reuse-before-build section must identify the current public function/interface, existing dependency choices, tests, and relevant neighboring code. State whether to reuse, extend, or replace and explain why.

## Part D: Requirement-to-task trace

| Requirement ID | Task | Likely files | Test evidence | Human checkpoint |
|---|---|---|---|---|
| CART-01 |  |  |  |  |
| CART-02 |  |  |  |  |
| CART-03 |  |  |  |  |
| NOTIF-01 |  |  |  |  |
| NOTIF-02 |  |  |  |  |
| NOTIF-03 |  |  |  |  |

## Part E: Ready-to-delegate check

Mark each item only after you can point to the evidence:

- [ ] Expected behavior is testable, not just aspirational.
- [ ] Boundary cases are named.
- [ ] Ambiguities are answered or explicitly blocked pending an answer.
- [ ] Reuse-before-build investigation is recorded.
- [ ] Public contracts and non-goals are explicit.
- [ ] Task has one owner, one repo, bounded files, and a reviewable outcome.
- [ ] Human checkpoint is placed before costly or risky work.
