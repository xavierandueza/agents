---
name: draft-pr
disable-model-invocation: false
description: Prepare and open a draft PR. Pass the ticket ID as the argument (e.g. /draft-pr RM-123).
---

# Draft PR

## Steps

### 1. Resolve ticket ID

The ticket ID comes from the invocation argument (e.g. `RM-123`). If not provided, check what git branch you're on now and use the ticket id from that.

**Completion criterion:** ticket ID confirmed.

### 2. Gather context

Read every file under `.agents/<ticket-id>/` — plans, notes, specs. Then run:

```sh
git diff origin/main...HEAD
```

Use both to understand what was done and why.

**Completion criterion:** you understand the scope and intent of the change well enough to write a brief, accurate summary.

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

Examples:
```
fix(agent-chat): RM-100 Resend button hidden for some users
feat(agent-chat): RM-101 Add model selector
```

**Completion criterion:** title follows the format exactly, type and scope chosen deliberately.

### 5. Fill the PR body

Populate the template from step 3:

- **Resolves**: the ticket ID
- **Changes**: high-level _what_, never _how_. Dot points only. Never describe files or code internals — reviewers can read the diff. For fixes, include a concise BEFORE / AFTER.
- **QA & Testing**: how you verified it's complete - NOTE that added tests are obvious and don't need to be included, don't add that information. Otherwise, instruct the user on what they need to test to ensure that its working as intended, including edge cases.

Leave the recording/images line as-is — the human fills that in.

**Completion criterion:** body is brief, accurate, and free of implementation detail.

### 6. Open the draft PR

```sh
ASSIGNEE=$(gh api user --jq '.login')

gh pr create \
  --draft \
  --assignee "$ASSIGNEE" \
  --title "<title>" \
  --body "<body>"
```

Capture the PR URL from the output.

**Completion criterion:** PR is open in draft state, URL captured.

### 7. Start a `loops` session on the draft PR

The custom `loops` CLI watches PRs for comments and spins out an agent to analyze, fix, and respond to them.

Run the bundled script, resolving its path relative to this `SKILL.md`:

```sh
scripts/start-pr-loop.sh <ticket-id> <pr-url>
```

The script creates a dedicated **Herdr tab** (the Herdr equivalent of a window) in the current workspace, roots it at the repository, and starts `loops pr-watch` without stealing focus. The process runs until manually stopped.

If the script fails, report its error. Do not run the watcher in the current pane, append `&`, use tmux, or otherwise bypass the script.

**Completion criterion:** the watcher is running in a dedicated, labelled Herdr tab for this ticket, and the current agent pane remains available.

### 8. Trigger Review Agents

There are 2x ways that you should do this, depending on the repository that you are in.

1. For the `ai` and `readme` repositories: Trigger by adding the `anand-review` label to the pull request.
2. For any other repository trigger another agent with the `/thermo-nuclear-code-quality-review` skill passing:
  - `ticketId`: the ticket ID from step 1
  - `prUrl`: the GitHub PR URL from step 6
