---
name: plan-issue
description: "Plan an issue/ticket end-to-end: fetch the issue, explore the codebase, grill the user to produce a self-contained spec."
disable-model-invocation: true
---

Takes an issue/ticket URL as an argument and produces an approved spec on disk, ready for a fresh `/implement` session.

Currently scoped to work with linear, however same approach applies across all task managemeng platforms.

## Hard requirements

- **Linear MCP must be connected.** If it isn't, stop immediately with: "Linear MCP is not connected — check your MCP config."

## Steps

### 1. Fetch and orient

- Fetch the ticket. Read the full body and any comments.
- Explore the codebase(s) to understand the area the ticket touches.
- Create and checkout a git branch using the branch name Linear provides for the ticket.

**Done when:** you have the ticket content, a working understanding of the relevant codebase area, and are on the correct branch.

### 2. Grill

Run `/grill-me` to drive a back-and-forth with the user. The grilling must cover:

- What does success look like? (observable outcomes — not implementation steps)
- What is explicitly out of scope?
- Any constraints, risks, or unknowns that surfaced during codebase exploration
- Proposed test seams — present these as suggestions derived from the success criteria, not mandates

**Done when:** every open question is resolved and you could hand the outcome to a proficient, but new engineer who knows nothing about this conversation.

### 3. Write the spec

Write the spec to `docs/specs/<ticket-id>.md` on the current branch, using [`SPEC_TEMPLATE.md`](SPEC_TEMPLATE.md) as the template.

**Done when:** every decision from the grilling is captured, success criteria are checkable pass/fail, and the file is committed to the branch.

### 4. Post draft to Linear

Post the full spec content as a comment on the Linear ticket, prefixed with `> **[DRAFT — pending approval]**`.

**Done when:** the comment is visible on the ticket.

### 5. Compact your conversation

After posting the spec, the user will take somet time to review. Run the `/compact` command explicitly stating that the user may want to come back and ask more questions, make modifications to the plan.

### 6. Get approval

Show the user the spec and ask for explicit approval. Do not proceed to implementation.

Once the user approves:
- Update the Linear comment prefix to `> **[APPROVED]**`
- Record the approval in the spec file under a `## Approval` heading with the timestamp

Start a fresh agent session yourself with instructions to implement, invoking the `implement` skill directly if possible, or giving clear instructions to invoke the skill to implement.

**Done when:** the Linear comment is marked approved and the spec file reflects it.

