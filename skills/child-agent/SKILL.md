---
name: child-agent
description: Execute one parent-assigned task using a durable Markdown assignment and report back through Pi. Pass the absolute assignment.md path.
disable-model-invocation: true
argument-hint: "<absolute assignment.md path>"
---

# Child agent

Act as a bounded **worker**. The parent owns orchestration, product decisions, integration, and the final user response. Complete the assigned task and preserve its result; do not widen the task.

## 1. Load the assignment

Read the absolute `assignment.md` path supplied in the invocation arguments. A relative path is invalid because the assignment lives in the parent checkout while this agent may run in another worktree.

Confirm the assignment provides:

- issue and child identifiers;
- absolute coordination, assignment, and result paths;
- repository, worktree, branch, base, and starting revision;
- role, objective, and intent;
- inputs and completed dependencies;
- allowed scope and non-goals;
- acceptance criteria and validation;
- deliverable contract;
- escalation and approval boundaries.

Inspect the actual repository and Git state. If required information is missing or the worktree does not match the assignment, report `PARENT_INPUT_REQUIRED` rather than guessing.

Treat `assignment.md`, the issue-level `orchestration.md`, and `decisions.md` as parent-owned. Read them when directed; do not edit them.

**Completion criterion:** the task, authority, paths, starting state, and proof required for completion are unambiguous.

## 2. Execute the bounded task

Load any task-specific skills named by the assignment, then work through the task to its deliverable contract.

- Change only the assigned worktree and allowed scope.
- Preserve unrelated and pre-existing changes.
- Use predecessor artifacts and issue decisions by their supplied paths and revisions.
- Validate incrementally instead of postponing all checks until the end.
- Keep code in the assigned branch or worktree; do not copy patches into `.agents/`.
- Store requested reports, evidence, and non-code artifacts under the assigned child directory.
- Keep credentials, tokens, and other secrets out of `.agents/`.
- Do not create, start, prompt, or manage another agent.

Pi's persisted conversation is the progress record. Do not create a duplicate status file or mirror routine progress into Markdown.

**Completion criterion:** the scoped outcome is implemented or produced, and every assigned acceptance criterion has evidence.

## 3. Request parent input

Ask only when missing information or authority affects correctness, including conflicting acceptance criteria, public-interface changes, unavailable dependencies, scope conflicts, credentials, destructive actions, production changes, security policy, or exhausted retry bounds.

Return a normal Pi response with this exact structure:

```text
PARENT_INPUT_REQUIRED
Blocking: yes|no
Decision needed:
Evidence:
Options:
Recommendation:
Work preserved at:
```

For a blocking request, stop after preserving useful work in the assigned branch, commit, report, or artifact path. The parent reads this conversation through Herdr and records durable cross-child decisions in the issue-level `decisions.md` when needed.

When the parent resumes the task, read the supplied answer or decision path, confirm its effect on scope, and continue from preserved work. Do not restart completed work unless the decision invalidates it.

**Completion criterion:** the parent has enough evidence and options to decide, and the child can resume without reconstructing lost work.

## 4. Publish the result

Before claiming completion, write `result.md` to the absolute result path from the assignment. It must contain:

```md
# Result

## Outcome

## Branch, commit, PR, or artifact

## Acceptance evidence

## Validation

## Assumptions

## Residual risks
```

Include exact commands and outcomes under validation. Reference large artifacts by path, branch, commit SHA, or PR URL rather than embedding them. Write the result only after its referenced artifacts are complete.

Then return:

```text
CHILD_COMPLETE
Result: <absolute-result-path>
Outcome: <one-line summary>
```

A settled Pi or Herdr state is not completion without `result.md` and this response.

**Completion criterion:** `result.md` exists, references verifiable outputs, accounts for every acceptance criterion, and the parent has received its absolute path.
