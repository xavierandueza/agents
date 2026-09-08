# Deliverable contracts

Read only the section matching the child node's deliverable. Copy its requirements into the child's `assignment.md`. The child records the required details in `result.md` and returns the common `CHILD_COMPLETE` response from `SKILL.md`.

## Draft pull request

The child owns the branch through a draft PR.

Complete when:

- the scoped behavior and tests are implemented;
- required validation has run;
- commits contain only the owned functional unit;
- the branch is pushed and the draft PR exists;
- the PR base reflects the dependency graph;
- `result.md` records the PR URL, head/base branches, commit SHA, checks, and residual risks.

A draft PR is not complete merely because it opens. Its implementation and validation contract must already be satisfied.

## Integration-ready branch or commit

The child produces work for the parent to combine into another branch or PR.

Complete when:

- the scoped behavior and tests are implemented;
- required validation has run;
- changes are committed on the assigned branch;
- `result.md` records the branch, commit SHA or ordered SHA range, integration instructions, checks, and residual risks.

The child does not open a PR unless the parent changes the contract.

## Runnable prototype

The child produces a disposable artifact that answers a named design question.

Complete when:

- the prototype exercises the target interaction or state model;
- setup and run commands work from a clean stated starting point;
- sample data or prerequisites are documented without secrets;
- limitations and deliberately omitted production concerns are explicit;
- `result.md` records the artifact path, run instructions, observations, and unresolved design decisions.

Polish, migration safety, and production hardening are outside scope unless the work packet includes them.

## Research or design report

The child produces a durable Markdown artifact.

Complete when:

- every research question or design decision is addressed;
- factual claims cite primary sources or repository evidence;
- recommendations distinguish evidence from judgment;
- alternatives, tradeoffs, and unresolved questions are recorded;
- `result.md` records the artifact path and a concise findings summary.

## Diagnosis

The child establishes a cause before proposing implementation work.

Complete when:

- the failure is reproduced or the inability to reproduce is evidenced;
- observations distinguish facts from hypotheses;
- the likely cause is supported by a minimal failing case, trace, log, or code path;
- affected scope and confidence are stated;
- `result.md` records evidence paths, reproduction steps, and recommended next action.

Diagnosis does not grant permission to change code.

## Test report

The child validates a named revision against acceptance criteria without owning implementation.

Complete when:

- the revision and environment are recorded;
- every assigned case is `pass`, `fail`, or `blocked`;
- actual results and evidence accompany each case;
- failures include reproducible steps and expected versus actual behavior;
- `result.md` records the report path, counts, evidence locations, and residual coverage gaps.
