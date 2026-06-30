#!/usr/bin/env python3

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

DEFAULT_REPOS = ("readmeio/readme", "readmeio/ai", "readmeio/gitto")
DEFAULT_BOT_LOGINS = ("readme-ai-writer", "readme-ai-writer[bot]")
DOCS_REVIEW_RE = re.compile(
    r"\[\s*View all changes in ReadMe\s*\]\(([^)]+)\)|"
    r"<a\s+[^>]*href=[\"']([^\"']+)[\"'][^>]*>\s*View all changes in ReadMe\s*</a>",
    re.IGNORECASE,
)

SEARCH_QUERY = """
query($searchQuery: String!, $cursor: String) {
  search(type: ISSUE, query: $searchQuery, first: 100, after: $cursor) {
    nodes {
      ... on PullRequest {
        number
        title
        url
        mergedAt
        headRefName
        repository { nameWithOwner }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""


def run_gh(args: list[str]) -> Any:
    command = ["gh", *args]
    completed = subprocess.run(command, text=True, capture_output=True)
    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"gh command failed: {' '.join(command)}\n{message}")
    output = completed.stdout.strip()
    return json.loads(output) if output else None


def parse_date(value: str) -> dt.date:
    try:
        return dt.date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"expected YYYY-MM-DD, got {value!r}") from exc


def current_gh_login() -> str:
    user = run_gh(["api", "user"])
    login = user.get("login")
    if not login:
        raise RuntimeError("Could not determine current GitHub login from gh api user")
    return login


def search_merged_prs(repo: str, start_date: dt.date, end_date: dt.date, author: str) -> list[dict[str, Any]]:
    query = f"repo:{repo} is:pr is:merged author:{author} merged:{start_date.isoformat()}..{end_date.isoformat()}"
    prs: list[dict[str, Any]] = []
    cursor = None

    while True:
        args = ["api", "graphql", "-f", f"query={SEARCH_QUERY}", "-F", f"searchQuery={query}"]
        if cursor:
            args.extend(["-F", f"cursor={cursor}"])

        payload = run_gh(args)
        search = payload["data"]["search"]
        prs.extend(node for node in search["nodes"] if node)

        page_info = search["pageInfo"]
        if not page_info["hasNextPage"]:
            break
        cursor = page_info["endCursor"]

    return prs


def paged_rest(path: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    page = 1

    while True:
        payload = run_gh(["api", "--method", "GET", path, "-F", "per_page=100", "-F", f"page={page}"])
        if not payload:
            break

        items.extend(payload)
        if len(payload) < 100:
            break
        page += 1

    return items


def bot_comments(repo: str, number: int, bot_logins: set[str]) -> list[dict[str, Any]]:
    issue_comments = paged_rest(f"repos/{repo}/issues/{number}/comments")
    review_comments = paged_rest(f"repos/{repo}/pulls/{number}/comments")
    comments = [*issue_comments, *review_comments]

    return [
        comment
        for comment in comments
        if comment.get("user", {}).get("login") in bot_logins
    ]


def docs_review_url(body: str) -> str | None:
    match = DOCS_REVIEW_RE.search(body or "")
    if not match:
        return None
    return match.group(1) or match.group(2)


def first_summary_line(body: str) -> str | None:
    lines = body.replace("\r\n", "\n").split("\n")

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if "View all changes in ReadMe" in stripped:
            continue
        if stripped.startswith(("#", "---")):
            continue

        stripped = re.sub(r"^[-*•]\s*", "", stripped)
        stripped = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", stripped)
        stripped = re.sub(r"https?://\S+", "", stripped).strip()
        if stripped:
            return stripped

    return None


def latest_docs_comment(comments: list[dict[str, Any]]) -> dict[str, Any] | None:
    docs_comments = []

    for comment in comments:
        url = docs_review_url(comment.get("body") or "")
        if not url:
            continue
        docs_comments.append({**comment, "docsReviewUrl": url})

    if not docs_comments:
        return None

    return sorted(docs_comments, key=lambda comment: comment.get("created_at") or "")[-1]


def log(message: str) -> None:
    timestamp = dt.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}", file=sys.stderr, flush=True)


def collect(repos: list[str], start_date: dt.date, end_date: dt.date, bot_logins: set[str], author: str, quiet: bool) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []

    if not quiet:
        log(f"Scanning {len(repos)} repos for merged PRs authored by {author} from {start_date} to {end_date}")

    for repo_index, repo in enumerate(repos, start=1):
        if not quiet:
            log(f"[{repo_index}/{len(repos)}] Searching {repo}")

        prs = search_merged_prs(repo, start_date, end_date, author)
        if not quiet:
            log(f"[{repo_index}/{len(repos)}] Found {len(prs)} merged PRs in {repo}")

        for pr_index, pr in enumerate(prs, start=1):
            label = f"{repo}#{pr['number']}"
            if not quiet:
                log(f"[{repo_index}/{len(repos)} {pr_index}/{len(prs)}] Checking {label}: {pr['title']}")

            comment = latest_docs_comment(bot_comments(repo, int(pr["number"]), bot_logins))
            if not comment:
                if not quiet:
                    log(f"[{repo_index}/{len(repos)} {pr_index}/{len(prs)}] No docs update for {label}")
                continue

            if not quiet:
                log(f"[{repo_index}/{len(repos)} {pr_index}/{len(prs)}] Docs update found for {label}")

            entries.append(
                {
                    "repo": pr["repository"]["nameWithOwner"],
                    "number": pr["number"],
                    "title": pr["title"],
                    "prUrl": pr["url"],
                    "mergedAt": pr["mergedAt"],
                    "headRefName": pr["headRefName"],
                    "docsReviewUrl": comment["docsReviewUrl"],
                    "botCommentCreatedAt": comment.get("created_at"),
                    "suggestedSummary": first_summary_line(comment.get("body") or ""),
                    "botCommentBody": comment.get("body") or "",
                }
            )

    if not quiet:
        log(f"Collected {len(entries)} PRs with docs updates")

    return sorted(entries, key=lambda entry: (entry["mergedAt"], entry["repo"], entry["number"]), reverse=True)


def write_markdown(entries: list[dict[str, Any]], path: Path) -> None:
    sections = []

    for entry in entries:
        merged_date = entry["mergedAt"][:10]
        summary = entry.get("suggestedSummary") or "TODO: summarise docs changes from botCommentBody"
        sections.append(
            f"## [{entry['title']} ({merged_date})]({entry['prUrl']})\n"
            f"* {summary}\n\n"
            f"[docs review link]({entry['docsReviewUrl']})"
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n\n".join(sections) + ("\n" if sections else ""), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect merged PRs with ReadMe docs-update bot comments.")
    parser.add_argument("--start-date", required=True, type=parse_date)
    parser.add_argument("--end-date", required=True, type=parse_date)
    parser.add_argument("--output", required=True, type=Path, help="JSON output path")
    parser.add_argument("--markdown-output", type=Path, help="Optional rough markdown output path")
    parser.add_argument("--repo", action="append", dest="repos", help="Repository to scan. Repeat to override defaults.")
    parser.add_argument("--bot-login", action="append", dest="bot_logins", help="Bot login to accept. Repeat to override defaults.")
    parser.add_argument("--author", help="GitHub login whose PRs should be scanned. Defaults to the active gh user.")
    parser.add_argument("--quiet", action="store_true", help="Only print final output messages.")
    args = parser.parse_args()

    if args.start_date > args.end_date:
        parser.error("--start-date must be before or equal to --end-date")

    repos = args.repos or list(DEFAULT_REPOS)
    bot_logins = set(args.bot_logins or DEFAULT_BOT_LOGINS)

    try:
        author = args.author or current_gh_login()
        if not args.quiet and not args.author:
            log(f"Using active gh user as author: {author}")
        entries = collect(repos, args.start_date, args.end_date, bot_logins, author, args.quiet)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if args.markdown_output:
        write_markdown(entries, args.markdown_output)

    print(f"Wrote {len(entries)} PR docs update entr{'y' if len(entries) == 1 else 'ies'} to {args.output}")
    if args.markdown_output:
        print(f"Wrote rough markdown to {args.markdown_output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
