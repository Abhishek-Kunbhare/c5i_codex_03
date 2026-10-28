# Delegation plan

| Task ID | Requirement IDs | Repo | Files in scope | Deliverable | Tests/evidence | Depends on | Human checkpoint |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

## Parallelism decision
- Why are these tasks independent?
- Which shared decisions must be settled first?
- What could conflict if both agents edit the same files?
- How many PRs can the review team responsibly handle at once?
- What is the stop condition if Codex discovers a new architectural need?

## Delegation prompt skeleton

> Implement only task [ID] for requirements [IDs] in [repo]. First inspect the existing interface, tests, and local guidance. Reuse existing project patterns before introducing a new abstraction or dependency. Do not change [out-of-scope items]. If [named ambiguity] blocks correct behavior, stop and ask rather than choosing silently. Add deterministic tests for [cases]. Run [commands]. Report requirement IDs, files changed, tests and exact outcomes, assumptions, and risks. Do not merge.
