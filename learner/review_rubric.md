# Pull request review rubric

Score each dimension 0, 1, or 2. A high total does not override a critical defect.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Requirement trace | No IDs or unclear scope | IDs partly mapped | Each requirement maps to changed code and evidence |
| Business behavior | Wrong/undefined behavior | Main path works; boundary gaps remain | Normal, boundary, and failure cases match approved spec |
| Contract compatibility | Breaking or unexamined | Compatibility partly checked | Existing API/interface deliberately preserved or approved |
| Test quality | Missing or misleading | Some relevant cases | Deterministic tests prove claims and include boundaries |
| Architecture/reuse | Duplicates or unexplained dependency | Reuse considered superficially | Existing patterns inspected and minimal compatible choice justified |
| Security/privacy | Unsafe network, secrets, or data handling | Risk not fully bounded | Scope, error paths, network/data behavior explicitly checked |
| Diff scope | Unrelated work mixed in | Some scope creep | Small coherent patch with clear ownership |
| Evidence integrity | No test evidence or stale | Results incomplete | Exact commands/results tied to current revision |
| Review governance | No accountable decision | Reviewer listed but no reasoning | Named human decision, checklist, branch checks satisfied |

### Review order
1. Read the business requirement and acceptance criteria.
2. Read the PR summary, changed-file list, and dependency changes.
3. Read the diff; trace from entry point to behavior.
4. Inspect tests and run/inspect checks on the exact revision.
5. Ask “what important behavior is not covered?”
6. Consider automated review findings, verify each against the diff.
7. Make and record the human decision. If changed, review the new revision again.
