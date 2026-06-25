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
- **QA & Testing**: how you verified it's complete

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

### 7. Self-review

Scan the diff for anything out-of-scope of the ticket — opportunistic refactors, incidental fixes, structural changes. For each one a reviewer would benefit from knowing about, post a line-level comment via the gh cli in an open review, explaining _why_ it's there (not what it does):

```sh
gh pr view <url> --json headRepository,number \
  --jq '[.headRepository.owner.login, .headRepository.name, .number]'

gh api repos/<owner>/<repo>/pulls/<number>/comments \
  --method POST \
  --field body="<explanation>" \
  --field commit_id="$(git rev-parse HEAD)" \
  --field path="<file>" \
  --field line=<line-number> \
  --field side="RIGHT"
```

Only comment on OOS changes that would otherwise look like noise to a reviewer. Don't over-comment.

**Completion criterion:** every meaningful OOS change has a comment and that review is submitted, or there are none.

### 8. Handoff

Trigger `/handoff` to a new agent for the thermo-nuclear code quality review, passing:

- `ticketId`: the ticket ID from step 1
- `prUrl`: the GitHub PR URL from step 6
