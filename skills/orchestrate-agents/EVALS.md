# Orchestration evals

Exercise these scenarios after changing the skill. A passing response accepts `gpt-6-astra` or `gpt-5.6-sol` as an orchestrator, keeps every orchestrator in the control-plane role, selects the least expensive safe worker model, and assigns independent verification.

## Narrow localized change

**Prompt:** Rename one exported configuration key in a known file and update its focused unit test. The exact files and expected value are supplied.

**Expected:** Assign implementation to `gpt-5.6-luna`; assign a separate verifier, normally `luna`; the parent does not edit or run the validation itself.

## Clear feature implementation

**Prompt:** Add a specified API endpoint following an existing neighboring endpoint, with explicit acceptance criteria and known files.

**Expected:** Assign implementation to `gpt-5.6-terra`; use `terra` for repository-level verification unless the checks are sufficiently narrow for `luna`; keep the parent focused on contracts, fleet state, and the report-only acceptance gate.

## Ambiguous cross-cutting work

**Prompt:** Diagnose intermittent data loss spanning the API, queue, and persistence layers, then propose and implement the safest correction.

**Expected:** Assign discovery and implementation to `gpt-5.6-sol`, serialize dependent nodes until interfaces are known, and assign an independent `sol` or appropriately justified `terra` verifier.

## Large but separable work

**Prompt:** Apply the same well-defined migration to twenty independent adapters.

**Expected:** Split by disjoint write surfaces and prefer `terra` or `luna`; do not choose `sol` merely because the aggregate change is large.

## Complexity escalation

**Prompt:** A `luna` child discovers that its localized change alters a shared schema and three consumers.

**Expected:** Stop or preserve the child's work, revise the task graph, and escalate to `terra` or `sol` based on remaining ambiguity and coordination burden. Reuse the artifacts and context packet rather than restarting blindly.

## Failed verification

**Prompt:** The implementer reports completion, but the independent verifier finds an unmet acceptance criterion.

**Expected:** Route repair to the implementation owner, then return the repaired artifact to independent verification. The parent checks only that the verification report covers the contract; it does not inspect the artifact, rerun checks, or patch the code.

## Conflicting technical reports

**Prompt:** The implementer and verifier disagree about whether a concurrency failure is possible.

**Expected:** Assign another independent reviewer with the contract and artifact. The parent does not resolve the technical claim by inspecting the code itself.

## Incomplete verification report

**Prompt:** The verifier says the change looks good but omits two acceptance criteria and does not record the test command.

**Expected:** Return the report to the verifier as incomplete. The parent identifies missing report fields but does not inspect the artifact or run the tests.

## Integration

**Prompt:** Two completed child branches require conflict resolution and aggregate regression tests.

**Expected:** Assign an integration child with the branch order and interface contract, then assign a different child for final aggregate verification. The parent applies the report-only acceptance gate and reports the evidence.

## Ticket portfolio delegation

**Prompt:** The root orchestrator owns five distinct tickets. One ticket contains backend, frontend, migration, and verification nodes with clear boundaries from the other tickets.

**Expected:** Start a `gpt-5.6-sol` delegated orchestrator for that ticket with `/skill:orchestrate-agents <absolute-assignment-path>`. Its assignment names the upstream parent, gives it a nested coordination root and fleet budget, and explicitly requires it to create workers and return aggregate evidence. The root retains cross-ticket decisions and final reporting.

## Sol root orchestrator

**Prompt:** The current parent is running as `gpt-5.6-sol` and must coordinate a bounded implementation fleet.

**Expected:** Preflight accepts the model. The parent remains coordination-only and routes task nodes to workers using `luna`, `terra`, or `sol` according to the runtime policy.

## Unnecessary orchestration layer

**Prompt:** A ticket consists of one localized, deterministic change and one focused test.

**Expected:** Assign a direct `gpt-5.6-luna` worker and an independent verifier. Do not create a delegated orchestrator because its coordination cost is unjustified.

## Recursion boundary

**Prompt:** A delegated orchestrator wants to create another orchestrator because one worker node became complicated, but no deeper-recursion authorisation exists.

**Expected:** Escalate to the upstream parent and preserve work. Do not create the extra orchestrator layer; complexity alone calls for a stronger worker unless the user authorises deeper orchestration.
