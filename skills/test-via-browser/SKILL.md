---
name: test-via-browser
description: Browser-test a ticket and produce an evidence-backed acceptance test report.
disable-model-invocation: true
---

# Browser acceptance testing

Validate an implemented web ticket against its acceptance criteria. Establish facts and preserve evidence; do not treat testing as permission to change code.

Use the `playwright-cli` skill for browser interactions.

## Artifacts

Store artifacts under `.agents/<ticket-id>/`:

- `testing-plan.md` contains test cases and expected outcomes.
- `testing-reports/<session>.md` contains one agent's execution results.
- `testing-report.md` consolidates completed session reports when a coordinator is used.
- `evidence/<session>/` contains that agent's screenshots, snapshots, traces, and other browser evidence.

Keep the plan separate from execution history. Each agent writes only to its own session report and evidence directory; do not overwrite previous runs or concurrently edit the consolidated report.

## Browser session isolation

Every agent must create and exclusively use a unique named browser session. Never use the unnamed default session, reuse another agent's session name, or route a command without `-s="$SESSION"`.

Assign each worker a role and one-based ordinal from the testing plan. Resolve [`scripts/browser-worker.sh`](scripts/browser-worker.sh) relative to this `SKILL.md`, but keep the working directory at the project root. Run it to derive the worker's session, test email, password-variable name, report, and evidence directory:

```bash
WORKER_HELPER="<skill-directory>/scripts/browser-worker.sh"
eval "$("$WORKER_HELPER" RM-17884 admin 1)"
mkdir -p "$WORKER_EVIDENCE_DIR" "$(dirname "$WORKER_REPORT")"

playwright-cli -s="$WORKER_SESSION" open --browser=firefox
playwright-cli -s="$WORKER_SESSION" screenshot \
  --filename="$WORKER_EVIDENCE_DIR/homepage.png"
```

The helper produces identities such as `rm-17884-admin1-<pi-session-id>` and `rm-17884-admin1-<pi-session-id>@e2e.test`. The ticket separates work across tickets, the role and ordinal separate workers within one agent, and `PI_SESSION_ID` separates concurrent agents. Running the same inputs in the same Pi session is intentionally idempotent.

Route every subsequent browser command to `WORKER_SESSION` and finish with:

```bash
playwright-cli -s="$WORKER_SESSION" close
```

Never delete session data owned by another agent.

A named browser session isolates browser state, not application data. Consider this when you are using the local setup provided to you w.r.t. the details of accounts you have access to.

## The Project

You are working on ReadMe's full-stack web application.

It has:
- The "dash": `http://dash.readme.local:3000/` -> This is the dashboard where users can see all of the projects they have access to.
- The "hub": links here end with .readme.local:3000 but start with the given subdomain. With -> `http://<subdomin>.readme.local:3000/`
- Enterprise projects: These have a parent project, where to access the homepage of the parent project you visit same as above: who has the root the same as the hub - so "my-enterprise" subdomain gets: `http://<parent-subdomin>.readme.local:3000/` -> BUT this points to a basic page that just shows the child projects that are available.
  - Enterprise children are found under a sub-page of the parent's domain. For a child project we get `http://<parent-subdomain>.readme.local:3000/<child-subdomain>/`
  - The majority of settings for an enterprise parent are located at the "Enterprise Dashboard" which canbe found, for the above project, at: http://readme.local:3000/group/<parent-subdomain>/settings
  - Child project settings can be found at the normal location too - but some of these will just show that it's disabled and you should navigate to the parent page.

## Login details

Read test-account environment variables from the gitignored `.env.e2e.local`. These will typically have:

- Admins -> these have full ownership over given projects
- Editors -> These just have edit access over projects, no admin powers

Often times you will need to test from the perspective of a signed out user - just navigate to any published local docs site for this with a non-signed in session to do so.

## 1. Establish the test target

Derive the ticket ID from the active branch, then inspect its ticket, acceptance criteria, `.agents/<ticket-id>/` artifacts, changed code, and project documentation. If the ticket cannot be resolved after inspecting those sources, ask the user for it.

Record the following in the report run:

- ticket ID
- Git SHA and whether the worktree is dirty
- worker username (its an email)
- per-session evidence paths
- relevant configuration and feature flags
- test account and test-data assumptions, without recording secrets

This step is complete when the acceptance criteria are known, the application is reachable, and the tested revision, environment, unique session, and per-session artifact paths are recorded. Otherwise, record the run as blocked with the missing prerequisite.

## 2. Build or validate the browser test plan

If `testing-plan.md` exists, read its browser-testing decision and reconcile the browser cases with the current acceptance criteria, changed code, and identified risks. Do not assume an existing plan is current, and do not execute its code-based test cases through the browser.

If the plan says browser testing is not required and its rationale remains valid, record that browser testing is not applicable and stop after finalising the report. If implementation changes invalidate the decision, update it and explain why.

When browser testing is required but browser cases are missing, add them. Give every browser case an ID and include:

- acceptance criterion or risk covered
- preconditions and test data
- actions
- expected observable result
- evidence to capture

Cover relevant happy paths, negative paths, boundaries, state transitions, permissions, and regressions without duplicating behaviour fully established by lower-level tests. Scope responsive and cross-browser coverage to the project's supported targets.

This step is complete when every acceptance criterion or risk assigned to browser validation maps to at least one browser case, with intentionally excluded browser coverage documented.

## 3. Execute every browser test case

Verify `playwright-cli` and the required browser are available, then execute the cases one at a time. Isolate or reset test state where practical.

For every case, append to the current report run:

- status: `pass`, `fail`, or `blocked`
- actual result
- evidence path or captured observation

Match evidence to the assertion:

- snapshots or visible state for DOM behaviour
- screenshots for visual behaviour
- console output for client errors
- request and response details for network behaviour
- URL or storage state for navigation and session behaviour

Inspect console errors and failed network requests when relevant. Capture evidence for important passes as well as failures.

This step is complete when every planned browser case has a terminal status and evidence sufficient for another agent to verify the conclusion.

## 4. Diagnose failures

For every failure, record:

- reproducible steps
- expected and actual behaviour
- evidence
- likely code-level cause and affected area
- related cases that may also be at risk

Continue executing unaffected cases. Do not modify code unless the user explicitly requested fixes as part of this run or authorises them after the failure is reported. Do not commit changes unless requested.

After an authorised fix, rerun the original failing case, related boundary cases, and relevant regression cases. Preserve the initial failure and append the fix summary and retest results; never rewrite a failure as an initial pass.

This step is complete when every failure is actionable, fixed and retested, or explicitly blocked.

## 5. Finalise the report

Write the summary to this agent's `testing-reports/<session>.md`. Only a coordinating agent may consolidate completed session reports into `testing-report.md`, after workers have stopped writing.

Summarise:

- acceptance criteria and test coverage
- passed, failed, and blocked counts
- fixes and retest outcomes, if authorised
- untested areas and residual risks
- final tested Git SHA and dirty-worktree state

Close only this agent's named browser session, even when the run fails or is blocked.

The run is complete only when every planned browser case is accounted for, every failure has reproducible evidence, all authorised fixes have relevant regression results, and the report states exactly what was and was not validated.
