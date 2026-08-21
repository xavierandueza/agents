#!/usr/bin/env bash

set -euo pipefail

usage() {
  printf 'Usage: %s <ticket-id> <pr-url>\n' "${0##*/}" >&2
}

if [[ $# -ne 2 ]]; then
  usage
  exit 2
fi

ticket_id=$1
pr_url=$2

for command_name in git herdr jq loops; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    printf 'Required command not found: %s\n' "$command_name" >&2
    exit 1
  fi
done

if [[ -z ${HERDR_WORKSPACE_ID:-} ]]; then
  printf 'HERDR_WORKSPACE_ID is required; run this command inside a Herdr workspace.\n' >&2
  exit 1
fi

repo_root=$(git rev-parse --show-toplevel)
tab_label="loops-$ticket_id"
tab_id=''

cleanup_failed_tab() {
  status=$?
  if [[ $status -ne 0 && -n $tab_id ]]; then
    herdr tab close "$tab_id" >/dev/null 2>&1 || true
  fi
  exit "$status"
}
trap cleanup_failed_tab EXIT

tab_response=$(herdr tab create \
  --workspace "$HERDR_WORKSPACE_ID" \
  --cwd "$repo_root" \
  --label "$tab_label" \
  --no-focus)

tab_id=$(printf '%s' "$tab_response" | jq -er '.result.tab.tab_id | select(type == "string" and length > 0)')
pane_id=$(printf '%s' "$tab_response" | jq -er '.result.root_pane.pane_id | select(type == "string" and length > 0)')

herdr pane run "$pane_id" loops pr-watch "$pr_url" >/dev/null

trap - EXIT
printf 'Started loops watcher in Herdr tab "%s" (tab: %s, pane: %s).\n' \
  "$tab_label" "$tab_id" "$pane_id"
