# Running services: the validation slot

Each machine has one **validation slot**: a full stack on its own ports and data, guarded by a lock. Load the `validation-slot` skill. It owns the protocol: the env file, the `slot` script, start order, reset and release. This file adds how to run it under Herdr. If that skill isn't installed, stop and ask the user.

The slot is yours alone while you hold the lock: start, stop, rebuild and reset anything in it. The default dev stack and everything outside the slot belong to the user and other agents.

## 1. Book it last

Finish the code, checks and push first. Then hold the slot only while you exercise ACs.

Run `slot status`. If someone else holds it:
- Keep doing other work, and check again every few minutes.
- Once the lock is past `expected_end`, run its `check:` line, then read the owner's transcript with `herdr agent read <owner> --source recent-unwrapped --lines 80`.
- Break the lock (`slot break --reason "<what you saw>"`) only when the owner is idle or done and has stopped working on the slot.
- A `human` owner is the user's: ask them.

**Done when:** you hold the lock.

## 2. Acquire

- `--owner`: your Herdr agent name.
- `--check`: `herdr agent get <your-agent-name>`. The lock lives on the machine where you run, so a plain `herdr` command there reaches you.
- `--ticket` and `--objective`: the ticket ID and the ACs you're about to exercise.
- `--repo`: one per repo you run, as `name:branch:sha:path`.
- `--expected-end`: an honest estimate. Run `slot extend` before you overrun it.

Keep the lock id `acquire` prints, and pass `--id <lock id>` to every `slot stop` and `slot release`. It's what stops a late call from tearing down the next holder's stack.

## 3. Run the stack

- Run each repo from a worktree of the branch under test:
  - your own worktree for your repo;
  - an existing worktree on the needed branch;
  - otherwise `herdr worktree create --cwd ~/projects/<repo> --branch <branch> --base <ref> --no-focus`.

  The user's main checkouts stay untouched.
- Create one tab for the slot: `herdr tab create --workspace <your-workspace> --cwd <worktree> --label slot --no-focus`. Then split one pane per repo.
- Reset first (the slot skill's reset step), then start in the order given if one is provided from the `validation-slot` skill. Use `herdr pane run <pane> 'make start-isolated ENV_FILE="<env file>"'` from that repo's worktree, with the env file path from the `validation-slot` skill. Wait for each service's ready line (`herdr pane wait-output <pane> --regex <the skill's ready regex>`) before starting the next. Never match a banner: it prints before the service is ready.
- Exercise the ACs as `verify` describes. Browsers use an isolated named session.

**Done when:** every AC that needs running services has evidence in `vNN/`.

## 4. Release

Release even when ACs fail or you're blocked:
1. Copy logs or evidence you need into `vNN/`.
2. Run `slot release --id <lock id>`. It stops everything on the slot's ports.
3. Close the tab you created (`herdr tab close <tab-id>`).

**Done when:** `slot status` shows the slot free and your slot tab is gone.
