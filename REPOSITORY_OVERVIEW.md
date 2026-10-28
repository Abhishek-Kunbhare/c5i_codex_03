# Repository overview

## Purpose

This repository is a training lab for specifying, delegating, implementing, and reviewing small software changes. Its example business is an online shop with two needs: coupon discounts at checkout and reliable order confirmations when a notification provider fails temporarily.

The repository contains deliberately small Python starter modules, a business brief, learner worksheets, task cards, runbooks, and review materials. It is not a deployed shop or a complete production service. The learning goal is to turn business outcomes into testable requirements, preserve existing contracts, verify implementation claims, and keep a human responsible for the final review decision.

The brief describes checkout and notifications as separately owned services in separate repositories. In this checkout, both starters are directories inside one Git repository. The local runbook suggests copying each starter into its own training repository, or using separate branches and commits, when practicing separate pull requests.

## What exists today

| Starter | Public function | Current behavior | Existing tests |
| --- | --- | --- | --- |
| `learner/starter/cart_service` | `calculate_total(items)` and `calculate_total_with_coupon(items, coupon, code, now)` in `src/cart.py` | The original function sums `price * quantity`. The new function applies an eligible coupon through one hour after expiry. | Existing contract and coupon behavior, including exact time boundaries. |
| `learner/starter/notification_service` | `send_order_confirmation(sender, order)` in `src/notifications.py` | Calls the injected sender's `send(order)` method once and returns its result. | A fake sender receives one order and returns `"sent"`. |

The cart starter implements coupons; the notification starter does not yet implement retries. There is no user interface, database, real payment integration, or real notification provider in this exercise.

The current suites contain 9 cart tests and 1 notification test. The notification test verifies the starting contract; it does not prove the proposed retry behavior.

## Business requirements

The authoritative requirements and acceptance evidence are in [`learner/brief.md`](learner/brief.md).

### Coupon calculation

| ID | Required behavior | Evidence expected |
| --- | --- | --- |
| CART-01 | Match coupon codes without case sensitivity. Apply a coupon when `active_from <= now <= expires_at + 1 hour`, using UTC timestamps. | Tests for matching and different case, activation, expiry, grace period, exact one-hour cutoff, and immediately after. |
| CART-02 | Accept discount percentages from 0 through 100 inclusive. Cap the discount at 50 currency units and keep the final total at or above zero. | Tests for 0%, 100%, values outside the allowed range, the cap, and the zero floor. |
| CART-03 | Keep `calculate_total(items)` callable with the same signature and a numeric return value. Add no third-party package. | Regression tests for the existing caller and no dependency change. |

The one-hour grace cutoff is inclusive: a coupon expiring at 12:00 UTC remains valid at 13:00 UTC and becomes invalid immediately afterward. The coupon-aware API is `calculate_total_with_coupon(items, coupon, code, now)`; the old `calculate_total(items)` contract remains intact.

### Notification retry

| ID | Required behavior | Evidence expected |
| --- | --- | --- |
| NOTIF-01 | Retry an approved temporary failure for at most three **total** send attempts. Wait 1 second before attempt 2 and 2 seconds before attempt 3. | Deterministic tests using a fake sender and an injected sleeper, including success and retry exhaustion. |
| NOTIF-02 | Do not retry permanent 4xx client errors. | One send attempt and no wait for a fake 4xx failure. |
| NOTIF-03 | Preserve the sender interface and avoid real network calls in unit tests. | Fake sender tests with no credentials or provider endpoint. |

“Three attempts” means the first send plus up to two retries. Waits occur only between retryable attempts; there is no wait after the final failure.

### Review and governance

| ID | Required behavior |
| --- | --- |
| GOV-01 | The PR description identifies requirement IDs, changed files, tests run, and unresolved risks. |
| GOV-02 | A named human reviewer checks the business boundaries and latest revision, then records the merge decision. |

The brief's definition of done is **ready for human review**, not automatically approved or merged. The diff should be focused, evidence should belong to the latest revision, and unresolved risks should be visible.

## Design decisions and remaining questions

The lab deliberately leaves some details unresolved:

- **Coupon rounding:** The approved policy is to round the final discounted total to two decimal places, half up.
- **Timezone handling:** The approved policy requires timezone-aware UTC datetimes and rejects naive or nonzero-offset timestamps.
- **Retryable failure classification:** “Temporary failure” needs an explicit error type or status classification. Retrying every exception would not meet the requirement.
- **Contract design:** Any added coupon or retry behavior must preserve the existing public function or sender interface. A required new public contract should be reviewed before coding.

The cart decisions are recorded in [`learner/design_note.md`](learner/design_note.md). Retry classification remains an unresolved notification task decision.

## Intended learning workflow

1. **Specify:** Read the business brief and fill in [`learner/specification_workbook.md`](learner/specification_workbook.md). Turn vague statements into given/when/then cases, boundaries, failure responses, and tests.
2. **Inspect and design:** Read the starter functions, existing tests, dependencies, and neighboring code. Use [`learner/design_note_template.md`](learner/design_note_template.md) to record reuse choices, decisions, edge cases, risks, and human checkpoints.
3. **Plan bounded work:** Use [`learner/task_cards.md`](learner/task_cards.md) and [`learner/task_plan_template.md`](learner/task_plan_template.md) to assign one scoped cart task and one scoped notification task. They can proceed independently once shared decisions and review rules are settled.
4. **Implement in a training environment:** Follow [`learner/local_runbook.md`](learner/local_runbook.md) or, when a connected training repository and environment are available, [`learner/live_cloud_runbook.md`](learner/live_cloud_runbook.md). Add deterministic acceptance tests and run the documented test commands.
5. **Review:** Prepare the description using [`learner/pull_request_template.md`](learner/pull_request_template.md). Use [`learner/review_rubric.md`](learner/review_rubric.md) to trace requirements to changed lines and current test evidence. Automated review can help identify issues, but a human records the decision.

To run the baseline tests from each starter directory:

```text
python -m unittest discover -s tests -v
```

Run this command once from `learner/starter/cart_service` and once from `learner/starter/notification_service`. The runbooks show the same command as `python3` for environments where that executable name is used.

## Seeded review exercise

[`learner/review_packet/seeded_pr.diff`](learner/review_packet/seeded_pr.diff) is a historical proposed patch supplied for review; it is **not applied** to the starter source. Its coupon expiry check uses `now > expires_at`, so it would reject coupons during the newly required one-hour grace period. It also does not implement the approved rounding and timestamp validation policies. The accompanying [`review_agent_prompt.md`](learner/review_packet/review_agent_prompt.md) asks for concrete, evidence-based findings and warns against treating passing old tests as proof of all requirements.

## Scope and limitations

Taxes, shipping, persistence, queueing, UI, payment providers, real message sending, production deployment, and distributed exactly-once delivery are outside this exercise. The coupon feature and its design note are present; notification retries and PRs are not. The local runbook mentions an instructor answer key under `instructor/`, but that directory is absent from this checkout.

In short, the code is the small starting point; most of the repository teaches the process of defining and reviewing the changes safely.
