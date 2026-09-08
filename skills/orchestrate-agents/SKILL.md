---
name: orchestrate-agents
description: Orchestrate Pi child agents through Herdr for software tasks. Use when delegating implementation, running independent workstreams, coordinating worktrees or stacked PRs, or supervising child agents to completion.
disable-model-invocation: false
---

# Orchestrate agents

Act as the **control plane**. Retain ownership of the user contract, task graph, approvals, validation, integration, and final response. Children perform bounded work and return evidence; they do not take over the user conversation.

## Runtime policy

- Parent model: `gpt-6-astra`
- Child model: `openai-codex/gpt-5.6-sol`
- Child protocol: `/skill:child-agent`
- Agent kind: Pi
- Delegation depth: one level
- Concurrency: one child unless independent ready work justifies more

Children must not create or manage other agents unless the user explicitly authorises recursive delegation.

## 1. Preflight

1. Confirm `HERDR_ENV=1`. If it is absent, stop and tell the user this workflow must run inside Herdr.
2. Confirm `PI_MODEL=gpt-6-astra`.
3. Load the `herdr` skill.
4. Establish the repository, task identifier, base branch, current worktree state, requested outcome, and final deliverable.
5. Identify operations that require human approval: credentials, destructive actions, production changes, security policy, material spending, or scope expansion.

**Completion criterion:** environment, authority, repository state, outcome, and approval boundaries are explicit.

## 2. Build the task graph

Describe each candidate node with:

- one outcome and observable acceptance criteria;
- predecessors and required inputs;
- expected files, modules, or interfaces it may change;
- deliverable type and validation commands;
- risk, approval requirements, and owner.

A node is **ready** only when all predecessor artifacts and decisions exist. Use model reasoning to propose and revise the graph; keep the graph itself as execution truth.

Use the parent checkout as the canonical coordination root. For every run, maintain:

```text
.agents/<task-id>/
  orchestration.md
  decisions.md
  children/
    <child-id>/
      assignment.md
      result.md
      artifacts/
```

The parent owns `orchestration.md`, `decisions.md`, and every `assignment.md`. Each child owns only its `result.md` and artifact directory. Pi conversations hold routine progress and questions; do not create duplicate status or message files.

Record node, owner, Herdr target, worktree/branch, dependencies, and state in `orchestration.md`. Children must not edit it.

**Completion criterion:** every node has a checkable contract, every dependency is represented, and ready nodes are identifiable.

## 3. Choose boundaries

Keep three decisions separate:

1. **Task unit:** what one child owns.
2. **Worktree:** isolation for a concurrent writer.
3. **PR:** an independently reviewable and mergeable product change.

A worktree does not imply a separate PR. The parent may integrate multiple child branches into one cohesive feature PR.

Use the smallest **functional unit** that is independently useful, testable, reviewable, and safe to merge or revert. Split by behavior, not architecture layer. Keep backend and frontend changes together when both are required to deliver one behavior. A dependent read-only capability and later mutation capability may be stacked changes only when the first is useful and complete by itself.

Run nodes in parallel only when all are true:

- every predecessor is complete;
- each child can work from an independent context packet;
- write surfaces are disjoint and isolated;
- one child's design decisions cannot invalidate another's work;
- expected latency savings exceed coordination and integration cost.

Otherwise serialize them. Shared schemas, migrations, lockfiles, generated code, central configuration, and unresolved interfaces default to one owner at a time.

If multiple defensible PR boundaries remain and the choice affects review, rollout, or product scope, recommend one option with tradeoffs and ask the user one focused question.

**Completion criterion:** each node has an execution location, branch/PR strategy, and justified scheduling decision.

## 4. Provision children

- Use a new window in the current checkout for read-only research, planning, diagnosis, or testing.
- Use `herdr worktree create` for every concurrent code-writing child.
- Use a stable, role-based, unique agent name. If you can use a distinct ticket/issue id, use it.
- Preserve user focus.
- Start only Pi children with the configured child model:

```sh
herdr agent start <name> --kind pi --pane <pane-id> -- \
  --provider openai-codex --model gpt-5.6-sol
```

One child owns each code-writing branch. The parent and other children must not concurrently edit that worktree.

**Completion criterion:** every ready node has one named owner, the required isolation, and a recorded Herdr target.

## 5. Write and dispatch the assignment

Before prompting a child:

1. Read the matching branch in [`DELIVERABLE-CONTRACTS.md`](DELIVERABLE-CONTRACTS.md).
2. Read [`../child-agent/ASSIGNMENT-TEMPLATE.md`](../child-agent/ASSIGNMENT-TEMPLATE.md).
3. Create `.agents/<task-id>/children/<child-id>/assignment.md` in the parent checkout and create its `artifacts/` directory.
4. Fill every template field with concrete values. Paste the matching deliverable requirements into the assignment.
5. Use absolute paths for the coordination root, assignment, result, artifacts, repository, and worktree. An ignored `.agents/` directory in the parent checkout is not present at the same relative path in a linked worktree.
6. Record the child name, Herdr target, assignment path, worktree, and branch in `orchestration.md`.

Seed the idle child with exactly this skill invocation:

```text
/skill:child-agent <absolute-assignment-path>
```

The invocation must be the start of the Herdr prompt so Pi treats it as a skill command. Do not duplicate the assignment in the prompt. The child skill provides the stable worker protocol; `assignment.md` provides task-specific context.

Fresh children do not inherit the parent's conversation or previously read files. The assignment must carry every fact needed to execute and prove the node complete.

**Completion criterion:** the assignment exists in the canonical parent coordination directory, all paths and contracts are concrete, and the child has started `/skill:child-agent` with its absolute path.

## 6. Handle child input requests

Require children to return a normal response with this shape, then stop work when blocking:

```text
PARENT_INPUT_REQUIRED
Blocking: yes|no
Decision needed:
Evidence:
Options:
Recommendation:
Work preserved at:
```

Answer from established context only when the decision is already determined. Route product choices, approval dialogs, credentials, destructive operations, production actions, security policy, spending, and scope expansion to the user.

Read the request from the child's Pi conversation through Herdr. After resolving it, record only durable cross-child decisions in `.agents/<task-id>/decisions.md`; do not mirror routine conversation into Markdown. Prompt the same child with the answer or the absolute decision path and have it resume from preserved work. Do not replace it or restart from scratch unless its state is unrecoverable.

**Completion criterion:** every request is answered or escalated, and preserved work has a clear resume path.

## 7. Supervise execution

Prefer Herdr's semantic waits over busy polling:

- use `agent prompt --wait` for an initial bounded turn;
- use `agent wait` for later lifecycle changes;
- inspect `agent get` and `agent read --source recent-unwrapped` after timeout, stall, `blocked`, or `unknown`;
- use recorded names or IDs, never UI position or inferred IDs.

Track task state separately from Herdr lifecycle state:

```text
planned -> ready -> starting -> working -> input-required -> validating -> completed
                                      \-> failed | canceled
```

`idle` and `done` mean ready for input, not that the task contract passed. `unknown`, silence, and timeout are not completion or failure. Inspect evidence before retrying. Never blindly resubmit a prompt after a timeout.

Use bounded retries only for classified transient failures. Reuse the same task ID, attempt number, branch, worktree, and existing artifacts where safe. Deterministic test failures, permission denial, ambiguous partial writes, and scope conflicts require diagnosis or escalation rather than automatic retry.

**Completion criterion:** every active node has a known task state, preserved work, and an appropriate next action.

## 8. Accept completion

A child must write its assigned `result.md` and return:

```text
CHILD_COMPLETE
Result: <absolute-result-path>
Outcome: <one-line summary>
```

Read `result.md`, then inspect the actual artifact, diff, commit, or PR and verify the reported checks. A self-reported completion, result file alone, or settled Herdr state is insufficient.

Send repair work to the owning child when practical. For high-risk changes, use a separate reviewer after implementation; the reviewer receives the acceptance contract and changed artifact, not the implementer's conclusions.

**Completion criterion:** every acceptance criterion maps to verified evidence and every residual risk is explicit.

## 9. Integrate

1. Compare assumptions and public interfaces across completed nodes.
2. Integrate in topological order.
3. Resolve conflicts with semantic knowledge rather than choosing hunks mechanically.
4. Run repository-level checks after integration.
5. Confirm each PR is independently coherent, or combine internal branches into the intended functional PR.
6. Preserve failed or unintegrated worktrees until the outcome is classified.

**Completion criterion:** the integrated result satisfies the user contract, aggregate checks pass or failures are reported, and PR dependencies are explicit.

## 10. Finish

Report:

- completed nodes and owners;
- artifacts, commits, branches, prototypes, or PR URLs;
- validation performed;
- dependency and merge order;
- unresolved risks or blocked work;
- Herdr resources intentionally left running;
- cleanup that remains.

Remove only resources this parent created, and only after useful work is integrated or the user explicitly discards it. Do not delete branches as an incidental part of worktree cleanup.

**Completion criterion:** the user can locate every result, understand its status and order, and act on remaining work.

When changing this skill, exercise the scenarios in [`EVALS.md`](EVALS.md).
