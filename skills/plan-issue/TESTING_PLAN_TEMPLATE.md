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

### A-01: <Test name>

#### Coverage

- **Success criterion or risk:** <criterion or risk>
- **Level:** <unit, integration, contract, etc.>
- **Target:** <module or interface>

#### Scenario

<Setup and action>

#### Expected result

<Observable assertion>

## Browser acceptance tests

If browser testing is not required, write `Not required` and remove the example case. Otherwise, `/test-via-browser` will execute these cases.

### B-01: <Test name>

#### Coverage

<Success criterion or risk>

#### Preconditions and test data

<Required starting state>

#### Actions

1. <User-visible action>
2. <User-visible action>

#### Expected result

<Observable pass/fail outcome>

#### Evidence

<Snapshot, screenshot, console, network, URL, or storage evidence to capture>

## Browser workers and execution groups

Assign each worker a role and one-based ordinal. `/test-via-browser` combines these with the ticket and executing Pi session ID to derive unique browser sessions, `@e2e.test` identities, reports, and evidence paths.

Identify workers that may run concurrently and workers that must be serialized because they share fixtures or mutable server-side state.

### admin1

- **Role:** admin
- **Ordinal:** 1
- **Assigned cases:** <B-01, B-02>
- **Execution:** <parallel-safe or serial>
- **Isolation requirements:** <distinct fixture or other constraint>

### user1

- **Role:** user
- **Ordinal:** 1
- **Assigned cases:** <B-03>
- **Execution:** <parallel-safe or serial>
- **Isolation requirements:** <distinct fixture or other constraint>

## Excluded coverage and residual risks

Document intentionally excluded scenarios, why they are excluded, and any remaining risk.
