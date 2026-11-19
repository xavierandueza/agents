---
name: t0-isolated-stack
description: Isolated t0 stack (t0_backend + t0_frontend) with its own Supabase, API, admin, queue, Metro and Android emulator, beside the default dev stack. Use when t0 work needs running services to validate, or several agents work on t0 on one machine.
---

# t0 isolated stacks

An isolated stack is a whole t0 environment defined by one env file, its **stack file**: a Supabase project, the engine API, the admin, the Cloud Tasks emulator, and (when the work touches the app) Metro plus an Android emulator running Expo Go. Its ports, Supabase project, data directory and virtual device are its own. Each repo runs against it with `ISOLATED_ENV=<stack file>` on any `make` target; `make start-isolated` starts its part.

A machine runs a **pool** of stacks under `~/isolated-t0/`, each with its own lock, next to the developer's default dev stack. An agent acquires a free stack, validates on it, and releases it. Stacks take a lot of memory, so check for spare memory before acquiring (step 3).

`scripts/slot` in this skill's directory locks and stops one stack; `scripts/slot --help` has the full protocol. Below, `$SLOT` is that script's absolute path. It acts on the stack named by three variables, all required:

```sh
stack="$HOME/isolated-t0/<name>"
export VALIDATION_SLOT_ENV="$stack/stack.env" VALIDATION_LOCK_DIR="$stack/lock" VALIDATION_LOCK_LOG="$stack/lock.log"
```

Set them in every shell you run `$SLOT` from. `$ENV` below is the stack file, `$VALIDATION_SLOT_ENV`.

## Rules

- **Your stack only.** Use only the ports, URLs, Supabase project and device in your stack file. Start services only with `make start-isolated ISOLATED_ENV="$ENV"`. Stop them only with Ctrl+C in their own terminals, or with `"$SLOT" stop` / `"$SLOT" release`. Everything else belongs to someone else: leave it running and untouched. That includes other stacks (readme's in `~/isolated/` too) and the default dev stack: Supabase project `t0_backend` (54320–54324, 54327, 54329), API 8080, admin 3000, queue 8123/8124, Metro 8081, edge inspector 8083, `emulator-5554` and the AVD `t0`, and the adb server on 5037.
- **Holder only.** Start, reset or use a stack only while you hold its lock. Leave a held stack's file as it is.
- **Stale-lock rule.** When `"$SLOT" acquire` says the stack is taken:
  - **Not overdue:** try another stack, wait and retry, or do other work. Leave the lock alone.
  - **Overdue:** run or follow its `check:` line. If the owner is alive, ask them to release or extend, then wait. If the owner is gone, run `"$SLOT" break --reason "<why you know they're gone>" --by "<you>"`.
  - **`owner: human`:** ask that person. Use `--force` only with their agreement.
  - If status says a human must inspect the lock, stop and tell the user.

## 1. Set up the stacks (once per machine)

For each stack, create `$HOME/isolated-t0/<name>/` and copy [`stack.env.example`](stack.env.example) to `stack.env` in it. Give the stack values no other stack uses: every `ISOLATED_*_PORT`, `ISOLATED_DATA_DIR`, `ISOLATED_COMPOSE_PROJECT` and `ISOLATED_AVD`.

- This matters because stop kills whatever listens on the stack's ports and removes its project's containers, and reset wipes its Supabase volumes, data directory and AVD. A value two stacks share lets one destroy the other.
- A pattern that works: stack `sN` adds `1000 × N` to the example's Supabase ports (s2: 56321, 56322, 56320, 56324), `100 × (N − 1)` to the other ports (s2: 8280, 3210, 8323, 8324, 8281), and `2 × (N − 1)` to the emulator port (s2: 5572). Use `/home/<you>/isolated-t0/sN/data`, `t0-sN` and `t0-sN`.
- Write `ISOLATED_DATA_DIR` as an absolute path; the Makefiles `include` the file, so `$HOME` and `~` don't expand.

Both repos validate the file and refuse default dev ports, the project `t0_backend` and the AVD `t0`.

**Done when:** each stack's directory has a `stack.env`, and no port, data directory, project or AVD is shared with another stack or the default dev stack.

## 2. Prepare a worktree per repo

You need a `t0_backend` worktree, and a `t0_frontend` worktree when any AC touches the app. Backend-only work runs the backend half alone.

- **A repo you changed:** use the worktree you're working in.
- **A repo without changes:** `git -C <clone> fetch origin`, then `git -C <clone> worktree add --detach <path> origin/main`.

Install dependencies before acquiring, so you don't hold a lock while installing:

- Backend: `make setup`. Copy `.env.local` (the Anthropic and Langfuse keys) from the main clone; without it, Agent Coach runs fail.
- Frontend: run everything inside the flake's dev shell (`direnv allow`, or prefix `direnv exec <worktree>`), then `npm ci`.

**Done when:** each worktree you need is at the commit you intend to test, with dependencies installed. You have each one's branch, SHA and path.

## 3. Acquire a stack

First check the machine has spare memory: `free -g` shows at least 10 GiB available for a full stack, or 4 GiB for backend only. A full stack uses about 7 GiB (the emulator alone about 3.6 GiB). If it doesn't, don't acquire a free stack: wait until a held stack is released (its lock dir disappears), check memory again, then acquire that one.

Then set the three variables for a stack and acquire it:

```sh
"$SLOT" acquire --owner "<unique name for you or your session>" \
  --check "<how someone can tell you're alive, e.g. 'herdr agent get <name>'>" \
  --ticket "<ticket-id>" --objective "<what you're validating>" --expected-end +90m \
  --repo "backend:<branch>:<sha>:<path>" --repo "frontend:<branch>:<sha>:<path>"
```

- **Any free stack:** with spare memory, try each stack in `$HOME/isolated-t0/` in turn until one acquires. Acquire is an atomic `mkdir`, so two agents can never hold the same stack.
- **Every stack taken:** follow the stale-lock rule.
- **People:** a person holding a stack uses `--owner human`.
- **Detached worktree:** use `origin/main` as `<branch>`.

Acquire prints a lock id. Pass it as `--id <lock id>` to every `stop` and `release`, so a late call can't stop or free the next holder's stack.

**Done when:** the memory check passed, acquire prints `slot: acquired`, and you've recorded the lock id and the stack's three variables.

## 4. Reset

Run `make reset-isolated ISOLATED_ENV="$ENV"` in the backend worktree, and in the frontend worktree when you use it. The backend's wipes the Supabase project's volumes, the queue and `backend.env`; the frontend's deletes the stack's AVD and frontend logs. Together they clear what the previous holder left: their accounts, data and app state.

**Done when:** each target exits 0.

## 5. Start the backend, then the frontend

Run `make start-isolated ISOLATED_ENV="$ENV"` in the backend worktree, then (if you need the app) in the frontend worktree, each in its own terminal; each stays in the foreground. Before starting the next, wait until the output matches this extended regex, with `<svc>` as `backend` or `frontend`:

```
\[ready\] isolated stack: <svc> ready|\[failed\] isolated stack: <svc>
```

- The backend prints its ready line once the API's `/health` and the admin answer. After a reset it starts Supabase, applies the migrations and seeds every persona first, which takes several minutes.
- The frontend needs the backend's `backend.env`, so it starts second. It boots the stack's emulator headless (a cold boot, about a minute; the first start also creates the AVD), installs Expo Go, starts Metro with only the stack's settings, opens the app, then prints its ready line.
- A `[failed]` line means the target failed or wasn't ready in time (`READY_TIMEOUT`, in seconds): stop, report its output, and don't start the next.

If a target reports one of your stack's ports already in use, run `"$SLOT" stop --id <lock id>` to clear the previous holder's leftovers, then start again. If the port is still taken, stop and report the port and PID.

**Done when:** each half you need printed its ready line.

## 6. Validate

Your stack's endpoints, with the ports from `$ENV`:

- Supabase API: `http://127.0.0.1:$ISOLATED_SUPABASE_API_PORT`; Postgres: `postgresql://postgres:postgres@127.0.0.1:$ISOLATED_SUPABASE_DB_PORT/postgres`, or `docker exec supabase_db_$ISOLATED_COMPOSE_PROJECT psql -U postgres`
- engine API: `http://127.0.0.1:$ISOLATED_API_PORT`; admin: `http://127.0.0.1:$ISOLATED_ADMIN_PORT`; mail catcher: `http://127.0.0.1:$ISOLATED_SUPABASE_INBUCKET_PORT`
- device: `emulator-$ISOLATED_EMULATOR_PORT`; Metro: `exp://127.0.0.1:$ISOLATED_METRO_PORT`

Every `make` target takes the stack: `make test ISOLATED_ENV="$ENV"`, `make seed ...`, `make e2e ...` (the admin's Playwright) in the backend; `make e2e ...`, `make doctor ...`, `make snap ...` in the frontend. A stack file value can't be overridden on the command line, so pass only target options (`FLOWS=`, `NAME=`).

- **App:** use the frontend's `verify-android` skill, following its "Isolated stack" section: `export ANDROID_SERIAL=emulator-$ISOLATED_EMULATOR_PORT`, and drive with the Maestro CLI, always with `--device "$ANDROID_SERIAL"` and `-e METRO_PORT=$ISOLATED_METRO_PORT`. The Maestro MCP drives only the default emulator.
- **Admin:** browsers share cookies across ports, so give each stack its own browser context or profile.
- **Data:** the personas are seeded with the default password; create fresh accounts for anything that mutates data. The engine API is real on a stack: the app's block generation calls it, and Agent Coach runs call the model and cost a little.
- **Flake:** a Maestro run can fail with `device offline` right after an emulator boots. Rerun it once.

If you need more time, run `"$SLOT" extend +30m` before `expected_end` passes.

**Done when:** every acceptance criterion has an observed result.

## 7. Save evidence

Save evidence in your verification evidence directory, in your worktree of the repo under test (usually `.agents/<ticket-id>/verification/vNN/`). Copy any logs you need from `$ISOLATED_DATA_DIR` first, because the next holder's reset wipes them. Record in the report which stack you used, its ports, and each repo's branch and SHA.

**Done when:** the evidence and logs are saved outside `$ISOLATED_DATA_DIR`.

## 8. Release

Press Ctrl+C in the frontend's terminal, then the backend's. Then run `"$SLOT" release --id <lock id>`, which removes the stack's containers (Supabase and the queue; volumes kept until the next reset), kills its listeners including its emulator, and frees the lock. Release even when validation failed or you're giving up.

If release fails, it keeps the lock. Fix what it reports and run it again. If you can't fix it, run `"$SLOT" release --id <lock id> --force`, which frees the lock and logs what was left running, and report what it listed.

**Done when:** release prints `slot: released`.
