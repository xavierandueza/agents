# Child assignment

## Identity

- Issue: `<issue-id>`
- Child: `<child-id>`
- Parent orchestrator: `<parent-agent-name-or-id>`
- Parent Herdr target: `<parent-agent-name-or-pane-id>`

## Locations

- Coordination root: `<absolute-coordination-root>`
- Decisions: `<absolute-coordination-root>/decisions.md`
- Assignment: `<absolute-coordination-root>/children/<child-id>/assignment.md`
- Result: `<absolute-coordination-root>/children/<child-id>/result.md`
- Artifacts: `<absolute-coordination-root>/children/<child-id>/artifacts`
- Repository: `<absolute-repository-path>`
- Worktree: `<absolute-worktree-path>`
- Branch: `<branch>`
- Base: `<base-ref>`
- Starting revision: `<sha>`

## Role

- Mode: `<implementation | integration | diagnosis | research | review | verification>`
- Specialty and decision authority: `<bounded role>`
- Subject artifact or revision: `<path, branch, commit, PR, or not applicable>`

## Objective

`<one outcome>`

## Intent

`<user-visible or architectural reason>`

## Inputs and dependencies

- `<paths, commits, specifications, decisions, and predecessor artifacts>`

## Scope

- `<allowed files, modules, and actions>`

## Non-goals

- `<explicit exclusions>`

## Acceptance criteria

- [ ] `<observable criterion>`

## Validation

- `<required commands and evidence>`

## Deliverable

`<draft PR, integration-ready branch or commit, runnable prototype, research report, diagnosis, or verification report>`

`<paste the matching completion requirements from the parent's deliverable contracts>`

## Escalate when

- required context or dependencies are missing;
- acceptance criteria conflict;
- assigned scope or another worker's ownership must change;
- a public interface must change outside the assignment;
- credentials, destructive actions, production changes, security policy, or additional spending require approval;
- bounded retries cannot resolve a failure.

## Task-specific skills

- `<skill names to load, or none>`
