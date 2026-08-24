---
name: test-via-browser
description: "Test a ticket via web interactions. Ensure no bugs/issues and that the feature works as intended"
disable-model-invocation: false
---

Test out the changes made in a ticket, ensuring that all edge cases are captured and validated.

## Hard Requirements

That the `playwright-cli` is installed and that it has a browser installed (default firefox).

You may or may not have a testing plan contained in a `testing-plan.md` file under the `.agents/<ticket-id>/` folder.

## Steps

### 1. Ensure test plan existence

Under the `.agents/<ticket-id>/` folder (where the ticket id should be in the active branch) there may or may not be a `testing-plan.md` file.

If one exists, leverage that testing plan to go through your test cases. If one does not, read the spec/plan from that, read the ticket, and make the plan.

### 2. Run through the test cases

Run through the test-cases one-by-one and record the results into the `testing-plan.md` file:

- If its a success, record why it is and provide evidence (if visual a screenshot is always helpful)
- If it is not, then analyze WHY that test was not successful in the code, and attempt to implement a fix for the issue.
  - Retest this, and record the initial results, fix concept, what was done (including commit hashes) and the results in the `testing-plan.md`.
  - Use the `handoff` skill to spin out other agents to diagnoze, retest, and fix issues where necessary.
