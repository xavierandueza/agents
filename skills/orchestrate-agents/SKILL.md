---
name: orchestrate-agents
description: Orchestrate Pi child agents through Herdr for software tasks. Use when delegating implementation, running independent workstreams, coordinating worktrees or stacked PRs, or supervising child agents to completion.
disable-model-invocation: false
---

# Orchestrate agents

Act as the **control plane**. Retain ownership of the user contract, task graph, approvals, fleet state, integration order, and final response. Children execute the work and return evidence; they do not take over the user conversation.

The orchestrator is coordination-only: decomposition, model and owner selection, assignment, Herdr control, decision routing, fleet state, acceptance, and reporting. Agents own artifact-producing and artifact-checking work, including repository investigation, implementation, diagnosis, review, testing, verification, and integration. The orchestrator controls flow from assignments and agent reports; acceptance requires a complete independent verification record.

## Runtime policy

- Orchestrator models: `gpt-6-astra` or `gpt-5.6-sol`
- Delegated orchestrator model: `gpt-5.6-sol`
- Worker models: `gpt-5.6-luna`, `gpt-5.6-terra`, or `gpt-5.6-sol`
- Default worker model: `gpt-5.6-terra`
- Worker protocol: `/skill:child-agent`
- Delegated orchestrator protocol: `/skill:orchestrate-agents`
- Agent kind: Pi
- Default hierarchy: root orchestrator -> delegated orchestrator -> workers
- Concurrency: one direct child unless independent ready work justifies more

Select the least expensive model that safely fits the node, based on ambiguity, coupling, risk, and coordination burden rather than task size alone:

- `gpt-5.6-luna`: narrow, low-risk, well-defined work with a self-contained context packet and deterministic acceptance criteria. Prefer it for small localized changes, focused research, mechanical updates, and targeted verification.
- `gpt-5.6-terra`: the default workhorse for clearly scoped implementation, diagnosis, review, and testing that needs normal repository reasoning but limited cross-node coordination.
- `gpt-5.6-sol`: difficult, high-risk, cross-cutting, or poorly defined work that requires discovery, architectural judgment, broad context, complex debugging, or coordination across interfaces and completed nodes.

Split large separable work instead of selecting `sol` only because a task is large. Escalate from `luna` to `terra`, or from `terra` to `sol`, when the child discovers ambiguity, coupling, or risk beyond its assignment; preserve the existing artifacts and context packet for the replacement child.

Worker children must not create or manage agents. A delegated orchestrator may create workers within its assigned scope and budget. Keep recursion bounded to the default hierarchy; only the user may authorise another orchestrator layer.

## Delegated orchestration

Delegate a whole ticket or self-contained program to a `gpt-5.6-sol` orchestrator when it has sufficient complexity. Usually if its implementing a full ticket then that will have sufficient complexity. Sufficient complexity means that it contains multiple task nodes, benefits from its own implementation and verification fleet, and can be given a clear outcome boundary. Use a direct worker for a single bounded node.

The upstream parent retains the portfolio contract, cross-ticket dependencies, shared decisions, approval routing, and final reporting. The delegated orchestrator owns its assigned task graph, workers, verification, integration, and aggregate result. Every agent has exactly one accountable orchestrator, and escalations flow upward through that chain.

When this skill is invoked with an assignment path:

1. Read the assignment before planning or creating agents.
2. Treat the declared upstream parent, delegated scope, authority, budget, coordination root, and result path as binding.
3. Operate explicitly as a subordinate orchestrator: report to the named parent, manage a worker fleet, and return aggregate evidence rather than taking over the portfolio or user conversation.
4. Do not create another orchestrator layer unless the assignment records explicit user authorisation.

**Completion criterion:** the subordinate knows who its parent is, what fleet it may create, where its authority ends, and how it returns results.

## 1. Preflight

1. Confirm `HERDR_ENV=1`. If it is absent, stop and tell the user this workflow must run inside Herdr.
2. Confirm `PI_MODEL` is `gpt-6-astra` or `gpt-5.6-sol`.
3. Load the `herdr` skill.
4. If invoked with an assignment path, read it and establish the upstream parent and delegated authority before continuing.
5. Establish the repository, task identifier, base branch, current worktree state, requested outcome, and final deliverable.
6. Identify operations that require human approval: credentials, destructive actions, production changes, security policy, material spending, or scope expansion.

**Completion criterion:** environment, authority, repository state, outcome, and approval boundaries are explicit.

## 2. Build the task graph

Describe each candidate node with:

- one outcome and observable acceptance criteria;
- predecessors and required inputs;
- expected files, modules, or interfaces it may change;
- deliverable type and validation commands;
- risk, approval requirements, owner, selected child model, and model-selection rationale;
- an independent verification node with its own acceptance contract.

A node is **ready** only when all predecessor artifacts and decisions exist. Use model reasoning to propose and revise the graph; keep the graph itself as execution truth.

Use the parent checkout as the canonical coordination root. For every run, maintain:

```text
.agents/<task-id>/
  orchestration.md
  decisions.md
  children/
    <worker-id>/
      assignment.md
      result.md
      artifacts/
  delegations/
    <orchestrator-id>/
      assignment.md
      result.md
      orchestration.md
      decisions.md
      children/
        <worker-id>/
          assignment.md
          result.md
          artifacts/
```

Within each orchestration scope, that orchestrator owns `orchestration.md`, `decisions.md`, and every worker `assignment.md`. Workers own only their `result.md` and artifact directory. The upstream parent owns each delegated orchestrator's `assignment.md`; the delegated orchestrator owns its aggregate `result.md` and nested coordination files. Pi conversations hold routine progress and questions; do not create duplicate status or message files.

Record node, owner, selected model, upstream parent, Herdr target, worktree/branch, dependencies, and state in the applicable `orchestration.md`. Workers must not edit orchestration state.

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
- Start only Pi agents.

Start workers with the model selected for their node:

```sh
herdr agent start <name> --kind pi --pane <pane-id> -- \
  --provider openai-codex --model <gpt-5.6-luna|gpt-5.6-terra|gpt-5.6-sol>
```

Start delegated orchestrators with `gpt-5.6-sol`:

```sh
herdr agent start <name> --kind pi --pane <pane-id> -- \
  --provider openai-codex --model gpt-5.6-sol
```

One agent owns each code-writing branch. An orchestrator and its other agents must not concurrently edit that worktree.

**Completion criterion:** every ready node has one named owner, the required isolation, a recorded Herdr target, and the model appropriate to its worker or orchestrator role.

## 5. Write and dispatch the assignment

For a worker:

1. Read the matching branch in [`DELIVERABLE-CONTRACTS.md`](DELIVERABLE-CONTRACTS.md).
2. Read [`../child-agent/ASSIGNMENT-TEMPLATE.md`](../child-agent/ASSIGNMENT-TEMPLATE.md).
3. Create `children/<worker-id>/assignment.md` under the current coordination root and create its `artifacts/` directory.
4. Fill every template field with concrete values and paste the matching deliverable requirements into the assignment.
5. Seed the idle worker with `/skill:child-agent <absolute-assignment-path>`.

For a delegated orchestrator:

1. Read [`ORCHESTRATOR-ASSIGNMENT-TEMPLATE.md`](ORCHESTRATOR-ASSIGNMENT-TEMPLATE.md).
2. Create `delegations/<orchestrator-id>/assignment.md` under the current coordination root.
3. Fill every hierarchy, authority, budget, outcome, and reporting field. State explicitly that it is a subordinate orchestrator reporting to the named upstream parent and is expected to create and manage workers.
4. Seed the idle orchestrator with `/skill:orchestrate-agents <absolute-assignment-path>`.

Use absolute paths for every coordination root, assignment, result, artifact, repository, and worktree. An ignored `.agents/` directory in one checkout is not present at the same relative path in a linked worktree. Record the child name, role, selected model and rationale, upstream parent, Herdr target, assignment path, worktree, and branch in `orchestration.md`.

The skill invocation must start the Herdr prompt so Pi treats it as a skill command. Do not duplicate the assignment in the prompt. Fresh agents do not inherit the parent's conversation or previously read files; the assignment must carry every fact needed to execute and prove the delegated contract complete.

**Completion criterion:** the assignment exists in the canonical coordination directory, hierarchy and contracts are concrete, and the child has started the role-appropriate skill with its absolute assignment path.

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

`idle` and `done` mean ready for input, not that the task contract passed. `unknown`, silence, and timeout are not completion or failure. Inspect Herdr lifecycle state and transcript evidence before retrying. Never blindly resubmit a prompt after a timeout.

Use bounded retries only for classified transient failures. Reuse the same task ID, attempt number, branch, worktree, and existing artifacts where safe. Deterministic test failures, permission denial, ambiguous partial writes, and scope conflicts require diagnosis or escalation rather than automatic retry.

**Completion criterion:** every active node has a known task state, preserved work, and an appropriate next action.

## 8. Verify and accept

A worker must write its assigned `result.md`. Dispatch an independent verifier after the implementation result exists. Give the verifier the original acceptance contract and direct access to the artifact, diff, commit, or PR; the implementation report is context, not proof. Select the verifier model with the runtime policy: `luna` for narrow deterministic checks, `terra` for normal repository-level review, and `sol` for broad or high-risk verification.

The verifier owns technical validation. It must inspect the actual work, run or confirm every required check, map each acceptance criterion to evidence, record residual risks, and write its own `result.md`.

The orchestrator owns the **acceptance gate**, a protocol check limited to the reports:

- the implementation and verification results exist;
- the verifier is independent of the implementation owner;
- every acceptance criterion has an explicit status and evidence location;
- required checks have commands, outcomes, and relevant failure details;
- residual risks and skipped checks are explicit.

The orchestrator does not inspect product artifacts, run validation commands, or decide between conflicting technical claims. Return incomplete evidence to the verifier. Route failed criteria to the implementation owner and then back to verification. Assign another independent reviewer to resolve a technical disagreement.

One verifier may batch closely related low-risk nodes when each node retains explicit evidence.

**Completion criterion:** the independent verifier has validated the actual work, and the orchestrator's report-only acceptance gate is complete.

## 9. Integrate

Treat integration as child work whenever it requires merging, cherry-picking, conflict resolution, product edits, or repository-level checks. The parent owns the order and dispatches an integration node with the completed branches, interface assumptions, and target acceptance contract.

The integration child must:

1. Compare assumptions and public interfaces across completed nodes.
2. Integrate in topological order.
3. Resolve conflicts semantically rather than choosing hunks mechanically.
4. Run repository-level checks after integration.
5. Confirm each PR is independently coherent, or combine internal branches into the intended functional PR.
6. Preserve failed or unintegrated worktrees until the outcome is classified.

After integration, dispatch an independent final verifier against the aggregate user contract. Apply the report-only acceptance gate, then route any failed criteria to the owning agent.

**Completion criterion:** an integration child produced the integrated result, an independent child verified the aggregate contract, checks pass or failures are reported, and PR dependencies are explicit.

## 10. Finish

Report:

- completed nodes, hierarchy, owners, selected models, and independent verifiers;
- artifacts, commits, branches, prototypes, or PR URLs;
- validation performed;
- dependency and merge order;
- unresolved risks or blocked work;
- Herdr resources intentionally left running;
- cleanup that remains.

Remove only resources this parent created, and only after useful work is integrated or the user explicitly discards it. Do not delete branches as an incidental part of worktree cleanup.

**Completion criterion:** the user can locate every result, understand its status and order, and act on remaining work.

When changing this skill, exercise the scenarios in [`EVALS.md`](EVALS.md).
