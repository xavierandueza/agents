---
name: draft-pr
disable-model-invocation: false
description: Open a draft PR, verify its implementation against the agreed spec with a fresh internal subagent, and start PR reviews. Pass the ticket ID or task name.
---

# Draft PR

## Steps

### 1. Resolve the task and base

Use the invocation's ticket ID (e.g. `RM-123`), or infer it from the branch. For ticketless work, use the supplied task name or a short branch-derived name without inventing a ticket ID.

Establish the intended PR base from the supplied context; for a stacked PR, use the predecessor branch. Otherwise use the repository's default branch. Confirm task changes are committed and pushed, preserving unrelated changes.

**Completion criterion:** task identifier, ticket presence, and PR base are known; the task branch is pushed.

### 2. Gather context

Read relevant plans, notes, and specs under `.agents/<ticket-id-or-name>/`, when present, and the existing ticket. Resolve the agreed spec from the supplied path, local working spec, or ticket requirements. If none exists, ask for the intended requirements before publishing; do not reverse-engineer a spec from the implementation.

Inspect the changes against the actual PR base:

```sh
git diff <base-ref>...HEAD
```

Use the agreed spec and diff to understand what was done and why. Keep the spec source available for the independent verifier.

**Completion criterion:** the agreed spec is identified and you understand the change well enough to write a brief, accurate summary.

### 3. Detect PR template

Check in this order:

1. `.github/PULL_REQUEST_TEMPLATE.md`
2. `.github/pull_request_template.md`
3. `docs/pull_request_template.md`

If none found, use [`DEFAULT_TEMPLATE.md`](DEFAULT_TEMPLATE.md) from this skill folder.

**Completion criterion:** template source is known.

### 4. Write the title

Format:

```
<type>(<scope>): <ticket-id> <short summary>
```

- **type**: `feat` / `fix` / `chore` / `docs` / `refactor`
- **scope**: the affected area (e.g. `agent-chat`, `auth`, `billing`)
- **summary**: for fixes, describe the _problem_, not the solution
- For ticketless work, omit the ticket ID from the title.

Examples:
```
fix(agent-chat): RM-100 Resend button hidden for some users
feat(agent-chat): RM-101 Add model selector
```

**Completion criterion:** title follows the format exactly, type and scope chosen deliberately.

### 5. Fill the PR body

Populate the template from step 3:

- **Resolves**: the ticket ID; omit this entry when there is no ticket
- **Changes**: high-level _what_, never _how_. Dot points only. Never describe files or code internals — reviewers can read the diff. For fixes, include a concise BEFORE / AFTER.
- **QA & Testing**: how a human can verified it's complete - NOTE that added tests/current tests passing are obvious from CI. Don't add that information. Otherwise, instruct the user on what they need to test to ensure that its working as intended, including edge cases.

Leave the recording/images line as-is — the human fills that in.

**Completion criterion:** body is brief, accurate, and free of implementation detail.

### 6. Open the draft PR

If this branch already has the intended PR, reuse it rather than creating a duplicate; keep it in draft state. Otherwise create it:

```sh
ASSIGNEE=$(gh api user --jq '.login')

gh pr create \
  --draft \
  --assignee "$ASSIGNEE" \
  --base "<base-branch>" \
  --title "<title>" \
  --body "<body>"
```

Capture the PR URL from the output.

**Completion criterion:** PR is open in draft state, URL captured.

### 7. Verify the PR against the spec

Start a fresh `subagent`, independent of the implementers and spec critic. Supply the original request, agreed spec path or ticket requirements, repository location, and PR URL. This verification is required for every repository, regardless of its other review automation.

Ask the verifier to:

- Read the agreed spec and inspect the actual PR diff and head, not just the PR description or implementation report. Identify the exact head commit being verified.
- Map each requirement and acceptance criterion to implementation and test evidence, reporting what is met, missing, incorrect, or blocked.
- Investigate relevant code at the PR head. Run checks where possible; if the local checkout does not match that head, inspect fetched PR files and report checks that cannot be safely run against it.
- Report scope deviations, untested requirements, and remaining risks. Review only; leave implementation changes to the task owner.

Wait for the result and save the returned report at `.agents/<ticket-id-or-name>/spec-verification.md`, including the PR URL and verified head SHA.

During approved auto-implementation, fix in-scope gaps, rerun relevant checks, push, and resume this verifier against the updated PR. Otherwise report the gaps and obtain authorization for changes. Resolve product ambiguities with the user; preserve the agreed spec rather than weakening it to fit the implementation.

If the PR head changes after verification, reverify the new head before reporting completion. If the subagent tool, spec, or checks are unavailable, report verification as blocked; an open draft PR alone is not a verified implementation.

**Completion criterion:** the verifier confirms that the current PR head implements the agreed spec, or the PR is explicitly reported as incomplete with its gaps or blockers.

### 8. Start a `loops` session on the draft PR

The custom `loops` CLI watches PRs for comments and spins out an agent to analyze, fix, and respond to them.

Run the bundled script, resolving its path relative to this `SKILL.md`:

```sh
scripts/start-pr-loop.sh <ticket-id-or-name> <pr-url>
```

The script creates a dedicated **Herdr tab** (the Herdr equivalent of a window) in the current workspace, roots it at the repository, and starts `loops pr-watch` without stealing focus. The process runs until manually stopped.

If the script fails, report its error. Do not run the watcher in the current pane, append `&`, or otherwise bypass the script.

**Completion criterion:** the watcher is running in a dedicated, labelled Herdr tab for this ticket, and the current agent pane remains available.

### 9. (Optional) Add review label(s)

On the `readme` and `ai` repositories, you must add the `anand-review` label to the pull request.

This triggers an AI review of the pull request using project standards and more, and will leave comments that the `loops` session will pickup and auto-resolve.

