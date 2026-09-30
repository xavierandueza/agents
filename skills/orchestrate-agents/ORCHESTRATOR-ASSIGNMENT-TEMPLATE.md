# Delegated orchestrator assignment

## Identity

- Portfolio: `<root-task-id>`
- Delegated task: `<delegated-task-id>`
- Orchestrator: `<orchestrator-id>`
- Model: `gpt-6.1-sol`

## Hierarchy

- Role: subordinate orchestrator
- Upstream parent: `<parent-agent-name-or-id>`
- Upstream Herdr target: `<parent-agent-name-or-pane-id>`
- Orchestration depth: `<current-depth>`
- Maximum authorised depth: `<maximum-depth>`
- May create worker agents: `yes`
- May create another orchestrator layer: `no`, unless explicit user authorisation is recorded below

You report to the upstream parent. Build and manage the worker fleet needed to complete this delegated task. Return aggregate evidence to the result path; do not take over the portfolio or user conversation.

## Locations

- Parent coordination root: `<absolute-parent-coordination-root>`
- Delegated coordination root: `<absolute-parent-coordination-root>/delegations/<orchestrator-id>`
- Assignment: `<absolute-delegated-coordination-root>/assignment.md`
- Aggregate result: `<absolute-delegated-coordination-root>/result.md`
- Repository: `<absolute-repository-path>`
- Base branch: `<base-ref>`
- Starting revision: `<sha>`

## Outcome

`<one independently verifiable ticket or program outcome>`

## Intent

`<user-visible or architectural reason>`

## Inputs and dependencies

- `<specifications, decisions, predecessor artifacts, shared interfaces, and sibling dependencies>`

## Delegated authority

- `<decisions this orchestrator may make without escalation>`

## Boundaries

- `<owned repositories, files, modules, branches, and actions>`
- `<explicit exclusions and decisions retained by the upstream parent>`

## Fleet budget

- Maximum concurrent workers: `<count>`
- Maximum total workers: `<count>`
- Allowed worker models: `<gpt-6-luna, gpt-6.1-sol>`
- Worktree and branch constraints: `<constraints>`

## Acceptance criteria

- [ ] `<observable aggregate criterion>`
- [ ] Implementation and integration evidence is present.
- [ ] Verification was performed by agents independent of the implementation.

## Validation

- `<required aggregate commands and evidence>`

## Deliverable

`<integrated branch, commits, draft PRs, reports, or other aggregate result>`

Write `<absolute-delegated-coordination-root>/result.md` with completed nodes, worker names and models, verification ownership, artifacts, validation evidence, dependency order, residual risks, and preserved resources.

## Escalate to the upstream parent when

- the delegated outcome or boundaries must change;
- a sibling ticket, shared interface, or portfolio decision is affected;
- the fleet or recursion budget is insufficient;
- credentials, destructive actions, production changes, security policy, spending, or user approval are required;
- acceptance criteria conflict or cannot be proven;
- another orchestrator layer appears necessary.

## Explicit deeper-recursion authorisation

`<user-authorised scope and limit, or none>`
