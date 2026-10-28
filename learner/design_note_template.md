# Design note: [change name]

## Context and user outcome
What user or operational problem are we solving? Which requirements apply?

## Existing system: reuse before build
- Existing API/function/interface inspected:
- Existing tests and conventions inspected:
- Existing libraries/components considered:
- What we will reuse:
- What we will add or change:
- Why this is the smallest compatible change:

## Decision record
For each decision, include options, selected option, reason, and consequence.

| Decision | Options | Selected | Reason | Consequence / tradeoff |
|---|---|---|---|---|
| Coupon rounding |  |  |  |  |
| Timezone validation |  |  |  |  |
| Retryable error class |  |  |  |  |

## Architecture sketch
`caller -> existing contract -> new behavior -> result`

Name the files/modules at each step. What remains untouched?

## Failure behavior and edge cases
List invalid inputs, exact boundaries, transient/permanent failures, and behavior after exhaustion.

## Test strategy
Map requirement IDs to examples and edge cases. State what the test does not prove.

## Risks and unresolved questions
Include risk, likelihood/impact, mitigation, owner, and status.

## Human checkpoints
- Before implementation:
- Before PR approval:
- Before merge:
