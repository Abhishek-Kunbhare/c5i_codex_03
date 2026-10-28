# Local Codex runbook

This path works without a cloud environment or GitHub integration. It demonstrates delegation discipline and review gates locally; state plainly that a local task is not a cloud task and does not demonstrate a real hosted PR review.

## Prepare the two repos

In Terminal, from the lab folder:

```bash
cd learner/starter/cart_service
python3 -m unittest discover -s tests -v
```

In another terminal:

```bash
cd learner/starter/notification_service
python3 -m unittest discover -s tests -v
```

For realistic PR separation, copy each starter directory into its own training repository and initialize Git. Or create two branches in one class repo and make the two change sets separate commits. Do not make both tasks write the same files.

## Inspect first

Ask Codex in the cart repo:

> Inspect this repository for the current public contract, tests, and relevant design patterns. Do not edit files. Summarize what must stay compatible, what behavior is missing, and what question blocks implementation. Cite filenames and function names.

Then do the same for notifications. Compare what it reports with the actual code. The goal is to teach learners to verify context, not to accept a confident summary.

## Implement only after approval

Use the delegation prompt skeleton from `task_plan_template.md`, with the approved design decision recorded in a file. Ask Codex for a plan first; inspect it; then authorize implementation. Run the tests yourself or inspect the exact recorded output. Keep a clean diff and prepare a PR-like description with the supplied template.

## Review the seeded patch

Read `review_packet/seeded_pr.diff` and `review_packet/review_agent_prompt.md`. The review-agent prompt is intentionally constrained to one automated pass. The instructor answer key is under `instructor/` and should not be shown until debrief.
