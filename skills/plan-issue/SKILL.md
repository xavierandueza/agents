---
name: plan-issue
description: "Plan an issue end-to-end and produce an approved spec and testing plan."
disable-model-invocation: true
---

Takes an issue/ticket URL as an argument and produces an approved spec and testing plan on disk, ready for a fresh `/implement` session.

Currently scoped to Linear, although the same approach applies across task-management platforms.

## Hard requirements

- **Linear MCP must be connected.** Search the MCP gateway for Linear tools before concluding it is unavailable. If it is not connected, stop with: "Linear MCP is not connected — check your MCP config."

## Steps

### 1. Fetch and orient

- Fetch the ticket. Read the full body and any comments.
- Explore the codebase(s) to understand the area the ticket touches.
- If you're not already on the right branch (check first you often will be) create and checkout a git branch using the branch name Linear provides for the ticket.
  - Note - linear likes to use <name>/xx-11111-name-of-ticket style but I like git flow style branch names with fix/feature/chore/docs instead so go for those instead of using names.

**Done when:** you have the ticket content, a working understanding of the relevant codebase area, and are on the correct branch.

### 2. Grill

Run `/grill-with-docs` to drive a back-and-forth with the user. The grilling must cover:

- What does success look like? (observable outcomes — not implementation steps)
- What is explicitly out of scope?
- Any constraints, risks, or unknowns that surfaced during codebase exploration
- The most appropriate verification layer for every success criterion: unit, integration, contract, browser acceptance, or another project-specific layer
- Whether browser acceptance testing adds meaningful confidence

Use judgement rather than requiring browser tests because the project has a web interface. Browser testing is usually warranted when success depends on rendering, interaction, client-side state, navigation, browser APIs, authentication flows, or integration across system boundaries. It is usually unnecessary when lower-level tests fully verify an internal, backend-only, documentation, configuration, or non-UI change.

**Done when:** every open question is resolved, every success criterion has a proposed verification method, and the browser-testing decision has a clear rationale.

### 3. Write the spec and testing plan

Write these gitignored artifacts under `.agents/<ticket-id>/`:

- `spec.md`, using [`SPEC_TEMPLATE.md`](SPEC_TEMPLATE.md)
- `testing-plan.md`, using [`TESTING_PLAN_TEMPLATE.md`](TESTING_PLAN_TEMPLATE.md)

If there is no ticket ID, use an appropriate brief folder name.

The spec must let an engineer unfamiliar with this area implement the work. Include relevant files when they would otherwise be difficult to discover.

The testing plan must map every success criterion and identified risk to an appropriate verification method. Include applicable code-based tests regardless of the browser-testing decision, and document when none apply. Record an explicit `Yes` or `No` browser-testing decision and its rationale. When browser testing is required, define cases that the user can later execute with `/test-via-browser`; when it is not required, do not manufacture browser cases. Assign each browser worker a role and one-based ordinal, identify cases that can run concurrently, and serialize cases that mutate shared application state.

Keep credentials out of the plan. Reference test-account roles and environment-variable names, never secret values.

**Done when:** every planning decision is captured, success criteria are checkable pass/fail, every criterion has test coverage or a documented exclusion, and both files are stored under `.agents/<ticket-id>/`.

### 4. Post draft to Linear

Post the full spec and testing plan as a comment on the Linear ticket, prefixed with `> **[DRAFT — pending approval]**`.

**Done when:** both artifacts are visible on the ticket.

### 5. Compact your conversation

After posting the spec and testing plan, the user will take some time to review. Run the `/compact` command explicitly stating that the user may return with questions or modifications to either artifact.

### 6. Get approval

Show the user the spec and testing plan and ask for explicit approval. Do not proceed to implementation.

Once the user approves:
- Update the Linear comment prefix to `> **[APPROVED]**`
- Record the approval in the spec file under a `## Approval` heading with the timestamp

Start a fresh agent session with instructions to implement from both artifacts, invoking the `implement` skill directly if possible or giving clear instructions to invoke it. If the approved testing plan requires browser acceptance testing, tell the user to run `/test-via-browser` after implementation; do not invoke that user-invoked skill on their behalf.

**Done when:** the Linear comment is marked approved, the spec records approval, and the implementation handoff references both artifacts.

