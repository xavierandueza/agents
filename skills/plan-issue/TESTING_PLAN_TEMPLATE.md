# <Ticket ID>: Testing Plan

## Scope

- **Spec:** [`spec.md`](spec.md)
- **Revision or branch:** <target revision>
- **Relevant risks:** <behaviour or boundaries most likely to regress>

## Test environment and data

Describe required fixtures, seed data, feature flags, services, test-account roles, and environment assumptions. Reference credential environment-variable names only; never include secret values.

## Browser-testing decision

- **Required:** <Yes | No>
- **Rationale:** <why browser validation does or does not add meaningful confidence>
- **Targets:** <browser and viewport requirements, or Not applicable>

## Automated code tests

If no code-based tests are applicable, state why instead of manufacturing cases.

| ID | Success criterion or risk | Level | Target | Scenario | Expected result |
|---|---|---|---|---|---|
| A-01 | <criterion or risk> | <unit, integration, contract, etc.> | <module or interface> | <setup and action> | <observable assertion> |

## Browser acceptance tests

If browser testing is not required, write `Not required` and remove the table. Otherwise, `/test-via-browser` will execute these cases.

| ID | Success criterion or risk | Preconditions and test data | Actions | Expected observable result | Evidence to capture |
|---|---|---|---|---|---|
| B-01 | <criterion or risk> | <starting state> | <user-visible actions> | <pass/fail outcome> | <snapshot, screenshot, console, network, URL, or storage evidence> |

## Excluded coverage and residual risks

Document intentionally excluded scenarios, why they are excluded, and any remaining risk.
