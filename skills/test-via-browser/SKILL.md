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
- `testing-report.md` contains timestamped execution results.
- `evidence/` contains screenshots, snapshots, traces, or other saved browser evidence.

Keep the plan separate from execution history. Do not overwrite previous report runs.

## Login Details

You will find signin details for features via the `.env.e2e.local` environment variables. Note that if you're not in a monorepo/frontend repo then you'll need to find the details from the monorepo/frontend repository.

## 1. Establish the test target

Derive the ticket ID from the active branch, then inspect its ticket, acceptance criteria, `.agents/<ticket-id>/` artifacts, changed code, and project documentation. If the ticket cannot be resolved after inspecting those sources, ask the user for it.

Discover how to start or connect to the application. Determine required authentication, fixtures, seed data, feature flags, browser, and viewport from the project rather than assuming defaults.

Record the following in the report run:

- ticket ID
- Git SHA and whether the worktree is dirty
- base URL
- browser and viewport
- relevant configuration and feature flags
- test account and test-data assumptions, without recording secrets

This step is complete when the acceptance criteria are known, the application is reachable, and the tested revision and environment are recorded. Otherwise, record the run as blocked with the missing prerequisite.

## 2. Build or validate the test plan

If `testing-plan.md` exists, reconcile it with the current acceptance criteria, changed code, and identified risks. Do not assume an existing plan is current.

Otherwise, create it. Give every case an ID and include:

- acceptance criterion or risk covered
- preconditions and test data
- actions
- expected observable result

Cover each acceptance criterion and relevant happy paths, negative paths, boundaries, state transitions, permissions, and regressions. Scope responsive and cross-browser coverage to the project's supported targets.

This step is complete when every acceptance criterion and identified risk maps to at least one test case, with any intentionally excluded coverage documented.

## 3. Execute every test case

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

This step is complete when every planned case has a terminal status and evidence sufficient for another agent to verify the conclusion.

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

Summarise:

- acceptance criteria and test coverage
- passed, failed, and blocked counts
- fixes and retest outcomes, if authorised
- untested areas and residual risks
- final tested Git SHA and dirty-worktree state

Close browser sessions even when the run fails or is blocked.

The run is complete only when every planned case is accounted for, every failure has reproducible evidence, all authorised fixes have relevant regression results, and the report states exactly what was and was not validated.
