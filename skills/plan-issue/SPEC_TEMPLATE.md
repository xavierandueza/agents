# <Ticket ID>: <Ticket Title>

## Problem

What the ticket is solving, from a user perspective.

## Success criteria

A numbered list of observable, pass/fail outcomes that define done. Tests must be derivable from these — not the other way around.

## Out of scope

What this ticket deliberately does not address.

## Implementation decisions

### Decision 1

Decisions made during the grilling: modules touched, interfaces changed, schema changes, API contracts, architectural choices. No file paths or code snippets unless a snippet encodes a decision more precisely than prose can.

**Relevant Files**

- `packages/api-contracts/src/constants/import.ts`
- `packages/backend/models/project/types.ts`
- `packages/dash/controllers/import.ts`
- `packages/dash/controllers/lib/import.ts`

## Proposed test seams

Where the implementation can be verified. These are suggestions — the implementing agent may adjust. Each seam should trace back to a success criterion.

## Further notes

Anything else relevant to implementation that doesn't fit above.
