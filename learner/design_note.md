# Design note: coupon calculation with one-hour grace period

## Context and outcome

Implement CART-01, CART-02, and CART-03. A matching coupon may be redeemed from its activation time through one hour after its stated expiration time, inclusive. Preserve the existing unadjusted total calculation for callers that do not use coupons.

## Existing system and reuse

- `cart_service/src/cart.py` exposes `calculate_total(items)` and has no coupon function.
- `cart_service/tests/test_cart.py` checks the existing numeric total and empty cart.
- Reuse `calculate_total(items)` for the subtotal. Use only Python standard-library `datetime` and `decimal` utilities; no dependency is added.
- Add `calculate_total_with_coupon(items, coupon, code, now)` as a separate function so the original signature and behavior stay intact. `now` is supplied by the caller for deterministic tests.

## Decisions

| Decision | Selected policy | Reason and consequence |
| --- | --- | --- |
| Grace period | `active_from <= now <= expires_at + timedelta(hours=1)` | The exact one-hour mark is valid; any later instant is invalid. The hour is 60 elapsed minutes in UTC. |
| Coupon rounding | Calculate with `Decimal`, then round the final discounted total to two decimal places using `ROUND_HALF_UP` | Approved by the user. The coupon-aware result is a numeric `float`; the original function's return behavior is unchanged. |
| Timezone validation | Require timezone-aware datetimes with UTC offset zero for `active_from`, `expires_at`, and `now`; reject naive or nonzero-offset values | Approved by the user. Invalid timestamps and reversed activation/expiration order raise `ValueError`. |
| Invalid percentage | Require a finite numeric value from 0 through 100 inclusive; reject invalid values with `ValueError` | Prevents silently applying an invalid coupon configuration. |
| Missing coupon or code | Return the unadjusted total | Keeps the coupon optional for the new function. |

## Flow and boundaries

`caller -> calculate_total_with_coupon -> calculate_total -> validate coupon -> check code and UTC window -> cap discount at 50 -> floor at zero -> round final total`

The coupon dictionary uses `code`, `active_from`, `expires_at`, and `percent`. Code comparison uses `casefold()`. A nonmatching code or a time outside the allowed window returns the unadjusted total. Invalid coupon data raises an error. The notification starter is unaffected.

## Tests and limitations

The cart tests cover the old API, case matching, activation boundary, exact expiry, time inside the grace period, exact one-hour cutoff, just after cutoff, percentage bounds, cap, zero floor, rounding, missing coupon/code, and timestamp validation. The tests use fixed timestamps and no network calls.

The training service has no persistent coupon use tracking or provider integration. The coupon-aware function accepts the starter's numeric item values; it does not introduce validation of item prices or quantities beyond the existing contract.

## Human review

Review the latest diff against CART-01 through CART-03 and the test output. In particular, verify the inclusive one-hour cutoff and the approved rounding/timezone policies before approval.
