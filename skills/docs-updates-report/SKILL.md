---
name: docs-updates-report
description: Generate a merged-PR docs updates report from ReadMe bot comments.
disable-model-invocation: true
argument-hint: "Start date and end date, e.g. 2026-06-01 2026-06-30"
---

# Docs Updates Report

Create a concise markdown report of docs updates found on merged PRs in these repositories:

- `readmeio/readme`
- `readmeio/ai`
- `readmeio/gitto`

The source of truth is the latest `readme-ai-writer` bot comment on each PR that contains a `View all changes in ReadMe` link.

## Steps

### 1. Resolve the date range

Use the invocation arguments as the inclusive merged date range. If either date is missing or ambiguous, ask for exact `YYYY-MM-DD` dates before running anything.

**Done when:** start and end dates are confirmed in `YYYY-MM-DD` form.

### 2. Scrape candidate PRs

Run the bundled scraper:

```sh
python3 skills/docs-updates-report/bin/collect-docs-updates.py \
  --start-date YYYY-MM-DD \
  --end-date YYYY-MM-DD \
  --output .agents/docs-updates-YYYY-MM-DD-to-YYYY-MM-DD/raw.json
```

The scraper uses `gh`, detects the active GitHub user, logs progress to the console, searches only merged PRs authored by that user in the target repositories, keeps only PRs with docs-review links from `readme-ai-writer`, and orders results newest-first by merge date.

If GitHub authentication fails, stop and tell the user to run `gh auth login` or refresh their token. To scan another user's PRs, pass `--author github-login`.

**Done when:** `raw.json` exists and every entry has `title`, `mergedAt`, `prUrl`, `headRefName`, `docsReviewUrl`, and `botCommentBody`.

### 3. Write the markdown report

Create `.agents/docs-updates-YYYY-MM-DD-to-YYYY-MM-DD/report.md`.

For each raw entry, write exactly this shape:

```md
## [PR Name (date merged)](https://github.com/owner/repo/pull/123)
* one liner on docs changes

[docs review link](https://docs.readme.com/.../review)
```

Rules:

- Do not include PRs without docs changes.
- Use the PR URL in the heading link.
- Use the `docsReviewUrl` as the docs review link.
- The one-liner should summarise the docs change from the bot comment, not the engineering change from the PR title.
- Keep the newest-first order from `raw.json`; do not resort it.
- Keep the report clean: no metadata table, no raw bot comments, no repository grouping unless the user asks.

**Done when:** every raw entry appears once in `report.md`, every section has a one-line bullet and docs review link, and no extra PRs are present.
