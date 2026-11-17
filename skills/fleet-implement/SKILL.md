---
name: fleet-implement
description: Implement multiple tickets in separate worktrees.
disable-model-invocation: true
---

# Fleet implement

Own ticket scheduling and supervision. Each ticket agent owns its spec, implementation, checks, and draft PR through `auto-implement`.

## 1. Resolve the tickets

Read the supplied tickets or the parent ticket and its subtickets. Establish the repository, requested outcomes, dependencies, and branch/PR bases. Use one worktree and one Herdr Pi agent per implementation ticket; a parent ticket need not get another implementation agent when its subtickets cover the work.

Launch independent ready tickets in parallel. Dependent tickets wait until their prerequisites are verified and available on a pushed branch or merged base. For stacked PRs, identify the predecessor branch as the base and preserve the merge order. Resolve shared interfaces before launching tickets whose designs depend on them.

## 2. Place tickets on machines

List machines with `herdr machine list`. Each one runs its own Herdr server, so every command for a remote machine takes `--machine <label>`, and pane IDs and agent names are per machine. Check free memory and CPU on each machine, keep about a quarter of RAM free, and don't count on swap.

Each machine has one validation slot (`verify`'s [`SLOT.md`](../verify/SLOT.md)), and tickets whose ACs need running services queue for it. Spread those tickets across machines. Tickets that only need unit-level checks go wherever there's capacity.

Before launching, on every machine you'll use:
- `~/validation-slot/slot.env` exists. If it's missing, tell the user and point them at `slot.env.example` in the `validation-slot` skill.
- `slot status` runs.
- Each tool the agents need works there: the ticket tracker MCP, the Node toolchain, `gh` auth. Where one doesn't, give agents the ticket text in a file on that machine, apply tracker updates yourself, and put machine quirks in their prompts.

**Complete when:** every ready ticket has a machine, and every machine you'll use has a working slot.

## 3. Start ticket agents

Confirm `HERDR_ENV=1` and load `herdr` for the installed CLI's semantics. Preserve user focus.

For each ready ticket, create its worktree:

```sh
herdr worktree create --cwd <repository> --branch <ticket-branch> --base <base-ref> --label <ticket-id> --no-focus
```

Reuse an existing ticket worktree and agent when present rather than duplicating them. Read the workspace and available shell pane from the command response or discover them through Herdr. Start one uniquely named Pi agent there, selecting the model according to `AGENTS.md`:

```sh
herdr agent start <ticket-agent-name> --kind pi --pane <pane-id> -- --provider <provider> --model <model-id>
```

Resolve the absolute path to [`auto-implement`](../auto-implement/SKILL.md). Start the prompt with `/skill:auto-implement <ticket-id>`. Include the machine, repository/worktree, base branch, prerequisite branches/PRs, relevant user decisions, and approval to perform auto-implementation. Say that ACs needing running services go through that machine's validation slot. Tell the agent to read the ticket for its full requirements. If the skill command is unavailable, have the same agent read the absolute skill path and execute it; do not create another agent.

Keep ticket-to-agent, worktree, branch, dependency, and PR information in the parent conversation. No assignment or result files are required.

## 4. Supervise to completion

Use `herdr agent wait`, then inspect the agent's response with `herdr agent read`. An idle or done lifecycle state alone does not mean the ticket is complete. After a timeout or blocked state, inspect the transcript before retrying; do not blindly resubmit work.

Answer from established context and route unresolved product decisions or approval requests to the user. Resume the same ticket agent for fixes and follow-up. Start newly ready tickets as prerequisites become available.

Watch each machine's slot with `slot status`. When a lock is past `expected_end`, check its owner with `herdr [--machine <label>] agent get <owner>`. If the owner has stopped, resume that agent so it releases the slot. If it's gone, break the lock with the reason.

When an agent reports `NOT VERIFIED` because no environment was available, arrange the slot for it (on another machine if that one is free) and resume it. The ticket isn't done until that's resolved, unless the user waives it.

A coding ticket is complete only when its draft PR exists, required checks pass, and `draft-pr` reports successful spec verification of the current PR head. Unit tests alone don't count as spec verification for an AC that needs running services. Report blocked work as incomplete, preserving its worktree and progress.

Finish with PR URLs, verification/check results, outstanding blockers, and dependency/merge order. Leave ticket worktrees, agents, and PR watchers available for user review; cleanup is a separate action.
