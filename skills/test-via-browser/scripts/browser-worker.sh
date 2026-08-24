#!/usr/bin/env bash

set -euo pipefail

usage() {
  printf 'Usage: %s <ticket-id> <role> [ordinal]\n' "${0##*/}" >&2
}

if [[ $# -lt 2 || $# -gt 3 ]]; then
  usage
  exit 2
fi

if [[ -z ${PI_SESSION_ID:-} ]]; then
  printf 'PI_SESSION_ID is required. Run this helper from a Pi agent session.\n' >&2
  exit 1
fi

ticket_id=$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')
role=$(printf '%s' "$2" | tr '[:upper:]' '[:lower:]')
ordinal=${3:-1}
session_id=$(printf '%s' "$PI_SESSION_ID" | tr '[:upper:]' '[:lower:]')

if [[ ! $ticket_id =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  printf 'Ticket ID must contain only letters, numbers, and single hyphens: %s\n' "$1" >&2
  exit 2
fi

if [[ ! $role =~ ^[a-z][a-z0-9-]*$ ]]; then
  printf 'Role must start with a letter and contain only letters, numbers, and hyphens: %s\n' "$2" >&2
  exit 2
fi

if [[ ! $ordinal =~ ^[1-9][0-9]*$ ]]; then
  printf 'Ordinal must be a positive integer: %s\n' "$ordinal" >&2
  exit 2
fi

if [[ ! $session_id =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  printf 'PI_SESSION_ID contains unsupported characters.\n' >&2
  exit 1
fi

worker_id="${role}${ordinal}"
identity="${ticket_id}-${worker_id}-${session_id}"

if (( ${#identity} > 64 )); then
  printf 'Worker identity exceeds the 64-character email local-part limit: %s\n' "$identity" >&2
  exit 2
fi

password_role=$(printf '%s' "$role" | tr '[:lower:]-' '[:upper:]_')

printf "WORKER_ID='%s'\n" "$worker_id"
printf "WORKER_ROLE='%s'\n" "$role"
printf "WORKER_SESSION='%s'\n" "$identity"
printf "WORKER_EMAIL='%s@e2e.test'\n" "$identity"
printf "WORKER_PASSWORD_ENV='E2E_%s_PASSWORD'\n" "$password_role"
printf "WORKER_REPORT='.agents/%s/testing-reports/%s.md'\n" "$ticket_id" "$identity"
printf "WORKER_EVIDENCE_DIR='.agents/%s/evidence/%s'\n" "$ticket_id" "$identity"
