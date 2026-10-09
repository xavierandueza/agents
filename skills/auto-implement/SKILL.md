---
name: auto-implement
description: Autonomously take an approved request or ticket through spec creation, iterative spec roasting, implementation, and a verified draft PR. Use when the user requests auto-implementation or a fleet ticket is assigned for it.
---

# Auto-implement

Own the request through to a draft PR. Explicit invocation or the user's approval of auto-implementation authorizes routine planning, implementation, checks, commits, pushing the task branch, and opening the draft PR. A question or a request to plan alone is not approval.

Use the current worktree unless assigned another. For a separate ticket worktree, use `fleet-implement`; ordinary assistance uses internal Pi subagents.

## 1. Establish scope

Read the request and any ticket, including its description, comments, linked spec, and dependencies. Inspect the repository instructions, current branch, base branch, and existing changes. Preserve unrelated work and use a task branch rather than committing to the base branch.

Resolve technical questions through investigation. Ask the user only when a material product decision, scope change, destructive operation, production action, security-sensitive change, or missing authorization cannot be resolved from the supplied context. Check that predecessor work is available before building on it.

If the internal `subagent` tool is unavailable, report the missing package and stop; do not substitute Herdr agents for the review loop.

**Complete when:** the scope, execution location, dependencies, and approval boundaries are understood.

## 2. Make the spec

Load [`to-spec-with-tech-detail`](../to-spec-with-tech-detail/SKILL.md) with the existing auto-implementation approval. Synthesize the supplied context and codebase findings instead of running an interview.

Use the ticket ID, or a short task name when there is no ticket. Keep the working spec at `.agents/<ticket-id-or-name>/spec.md`, including the intended approach, acceptance criteria, test strategy, and out-of-scope work. Reuse an existing spec where it is already sufficient. Keep material assumptions explicit.

During the roast loop, revise this local spec. Publish the agreed version to the existing ticket afterward; do not create a ticket solely to satisfy this workflow.

**Complete when:** the critic can understand the problem, proposed approach, and intended behavior from the spec and original request.

## 3. Roast and revise

Start an internal `subagent` with:

- `subagent_type: "Plan"`;
- an explicit model selected using `AGENTS.md`;
- `inherit_context: false`;
- a short `description`;
- a prompt containing the original request, ticket context, constraints, repository location, and absolute paths to the spec and [`roast-spec`](../roast-spec/SKILL.md).

Tell the critic to read that skill and spec, investigate the codebase, and return its critique without modifying the implementation. Keep its returned agent ID.

Evaluate the critique, investigate disputed claims, and revise the spec. Call `subagent` again with the same type and explicit model, `resume` set to that agent ID, and the revisions, decisions, and rationale in its prompt. Continue until both you and the critic agree that the approach is valid and the spec is good enough to implement. Small disagreements are fine so long as they are not major ones.

If a major disagreement stops making progress, bring the decision and both positions to the user. If the reviewer session is unavailable, start a replacement with the current spec and prior critique/decisions, and disclose the loss of continuity.

**Complete when:** both agents agree to proceed, with no major disagreements remaining.

## 4. Implement

Implement the agreed spec, using internal subagents wherever useful. Coordinate shared changes and integration directly through their conversations; no Markdown assignment/result protocol is required.

Use the project's testing conventions and `tdd` where suitable. Run focused checks while implementing and relevant broader tests, typechecking, and linting before publishing. Diagnose failures; report checks blocked by the environment rather than treating them as passes.

Keep the spec faithful to the agreed scope. Material design changes go back to the critic; product or scope changes require user approval. Commit only task changes and push the task branch.

**Complete when:** the agreed behavior is implemented and the task commits are pushed, with required checks passing or remaining failures/blockers explicitly reported.

## 5. Publish and verify

Load [`draft-pr`](../draft-pr/SKILL.md), supplying the ticket ID or task name, agreed spec path, and correct PR base. Follow its post-publication spec verification and review workflow, including repairing implementation gaps when authorized.

Finish with the draft PR URL, check results, spec verification outcome, and remaining blockers. Keep the PR in draft state; merging is outside this workflow.

**Complete when:** the draft PR exists and its current head has passed spec verification. If verification or required checks fail or are blocked, report the draft PR as incomplete rather than claiming the task is finished.
