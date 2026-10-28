# Live Codex Cloud runbook

Use only if learners have access to a connected GitHub repository and a published Codex Cloud environment. Product availability, settings, permissions, and labels may vary by account. The local runbook is a complete alternative.

## Before class

1. Connect only the training repositories. Keep them free of secrets and personal data.
2. Prepare the environment with the project runtime, Git, and test command; test it with a fresh task.
3. Confirm learners can view the selected repository and can create a branch/PR if that is part of the exercise.
4. Explain exactly which repositories, files, setup scripts, and network destinations are available to the cloud task. A cloud task does not automatically inherit a learner's local files, local running services, browser login, or VPN access.
5. Use a disposable training repo. Do not merge the exercise PRs into a production repository.

## Instructor demonstration: observe, don't trust the summary

Start a task on the `cart_service` repository and paste:

> Implement CART-01, CART-02, and CART-03 from `learner/brief.md`. First inspect the repository's current public API, tests, and project instructions. Before coding, report the design choices you believe are settled and list any blocking ambiguity. Do not invent the rounding policy. Do not change the public `calculate_total(items)` signature or add dependencies. If no approved rounding policy exists, stop and ask. If it is documented in `learner/design_note.md`, implement only the scoped change, add tests for every acceptance case, run the documented test command, and report changed files, exact commands/results, requirement IDs, and remaining risks. Do not merge or open a PR until I review the plan.

Pause before approving implementation. Ask learners: What repository context can it actually see? Which context is missing? What has been delegated, and what remains your responsibility?

## Parallel delegation exercise

Once both task cards are approved, start one cloud task for each independent repository. Name the tasks by requirement IDs. Have learners capture:
- the selected environment and repositories;
- what is in the task workspace;
- the plan and files changed;
- exact checks and outcomes;
- what still needs human validation;
- the PR links and revision identifiers.

Do not assume separate tasks are automatically independent if they share a contract, database, or file. Here they are separated by repo and interface, but the requirement/design review is shared work that must happen first.

## Review and merge gate

Open each PR. Review the latest diff and checks. Ask Codex Code Review or `@codex review` if enabled. Treat this as another signal. Security Review (where available) is a separate security-focused pass, not a substitute for correctness review. Record findings in the rubric; inspect each finding in the source diff. The human reviewer decides. A training task should stop at draft PR unless the instructor explicitly chooses to demonstrate merge controls.
