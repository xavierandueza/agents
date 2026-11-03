---
name: verify
disable-model-invocation: false
description: Verify a change end to end in the running app or CLI and leave an evidence run. Use when asked to verify, validate, or gather evidence for a change.
---

# Verify

Prove the change works the way a user would meet it: the running web app, or the built CLI. Test suites are CI's job; this is final validation.

## Rules

- Layout, with each attempt in the next unused `vNN`. Earlier runs are history: leave them untouched.
  ```text
  .agents/<ticket-id-or-name>/verification/
    vNN/       shareable: report.md, *.png, *.webm, *.txt
    private/   secrets: tokens, sign-in URLs, storage state, config snapshots
  ```
- Secrets live only in `private/`. Pass them by file or variable so they stay out of `vNN/` and your messages.
- Status is exactly one of `VERIFIED`, `FAILED`, `NOT VERIFIED`. Only something you observed is `VERIFIED`. A `FAILED` AC is a finding: record it and carry on.
- If the environment isn't ready (server down, wrong branch, missing tool), stop and report what's missing. Workarounds produce evidence nobody can trust.
- Clean up what you created (sessions, panes, scratch dirs, test accounts), even after a failure. Touch nothing else.

## 1. Derive acceptance criteria

Read the spec, ticket, and diff. Write `AC1`, `AC2`, … each with one observable outcome and how to reach it (route, click path, or command).

**Done when:** every changed behaviour maps to at least one AC.

## 2. Exercise each AC

Record the tested SHA (`git rev-parse HEAD`) and whether the tree is dirty. Then capture evidence per surface:

- Web UI: [`WEB.md`](WEB.md)
- CLI, TUI, or other terminal output: [`CLI.md`](CLI.md)

Name evidence `NN-<what>.<ext>`, where `NN` follows the AC order. `$RUN` below means the absolute path to this run's `vNN/`.

**Done when:** every AC has evidence in `vNN/`, or a one-line reason it couldn't be observed.

## 3. Write the report

Write `vNN/report.md`, kept to tables and links so a reviewer can scan it:

```markdown
# <Change name>

| Field       | Value             |
| ----------- | ----------------- |
| Tested SHA  | `<sha>`           |
| Run         | `vNN`             |
| Environment | local             |

## AC1: <short title>

**Status:** VERIFIED

- [01-<what>.png](01-<what>.png)

## AC2: <short title>

<One sentence, only when the status or evidence needs explaining.>

**Status:** FAILED

- [02-<what>.txt](02-<what>.txt)
```

Before finishing, open every screenshot and grep `vNN/` for tokens, credentials, and sign-in URLs. Retake or redact anything that leaks.

**Done when:** every AC has a status and linked evidence that exists, and `vNN/` holds nothing secret.

Report the run directory and per-AC status to the user.
