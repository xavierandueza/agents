---
name: test-via-browser
description: Browser-test a ticket and produce an evidence-backed acceptance test report.
disable-model-invocation: true
---

# Browser acceptance testing

Validate an implemented web ticket against its acceptance criteria. Establish facts and preserve evidence; do not treat testing as permission to change code.

Use the `playwright-cli` skill for browser interactions.

Store results under `.agents/<ticket-id>/testing/xxx` when a ticket id exists.

## Browser session isolation

Every agent must create and exclusively use a unique named browser session. Never use the unnamed default session, reuse another agent's session name, or route a command without `-s="$SESSION"`.

Doing so may lead to clashes and interferences that aren't desired for multiple agents working on things. Ie:

```bash
playwright-cli -s="$WORKER_SESSION" close
```

Never delete session data owned by another agent.

A named browser session isolates browser state, not application data. Consider this when you are using the local setup provided to you w.r.t. the details of accounts you have access to. So, usually you want to make your own data however is needed.

## The Project

You are working on ReadMe's full-stack web application.

It has:
- The "dash": `http://dash.readme.local:3000/` -> This is the dashboard where users can see all of the projects they have access to.
- The "hub": links here end with .readme.local:3000 but start with the given subdomain. With -> `http://<subdomain>.readme.local:3000/`
- Enterprise projects: These have a parent project, where to access the homepage of the parent project you visit same as above: who has the root the same as the hub - so "my-enterprise" subdomain gets: `http://<parent-subdomin>.readme.local:3000/` -> BUT this points to a basic page that just shows the child projects that are available.
  - Enterprise children are found under a sub-page of the parent's domain. For a child project we get `http://<parent-subdomain>.readme.local:3000/<child-subdomain>/`
  - The majority of settings for an enterprise parent are located at the "Enterprise Dashboard" which canbe found, for the above project, at: http://readme.local:3000/group/<parent-subdomain>/settings
  - Child project settings can be found at the normal location too - but some of these will just show that it's disabled and you should navigate to the parent page.

## Login details

Read test-account environment variables from the gitignored `.env.e2e.local`. These will typically have:

- Admins -> these have full ownership over given projects
- Editors -> These just have edit access over projects, no admin powers

Often times you will need to test from the perspective of a signed out user - just navigate to any published local docs site for this with a non-signed in session to do so.

Verify `playwright-cli` and the required browser are available, then execute the testing

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

## Diagnose failures

For every failure, record:

- reproducible steps
- expected and actual behaviour
- evidence
- likely code-level cause and affected area
- related cases that may also be at risk

Continue executing unaffected cases. Do not modify code unless the user explicitly requested fixes as part of this run or authorises them after the failure is reported. Do not commit changes unless requested.

After an authorised fix, rerun the original failing case, related boundary cases, and relevant regression cases. Preserve the initial failure and append the fix summary and retest results; never rewrite a failure as an initial pass.

This step is complete when every failure is actionable, fixed and retested, or explicitly blocked.
