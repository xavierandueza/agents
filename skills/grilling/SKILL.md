---
name: grilling
description: Interview the user relentlessly about a plan or design. Use when the user wants to stress-test a plan before building, or uses any 'grill' trigger phrases.
---

## Main session
Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a question can be answered by exploring the codebase, explore the codebase instead.

## After grilling completion
After the grilling is complete use the `/handoff` skill to create a document that contains the details of this interaction. See the `./GRILLING_RESULT_TEMPLATE` for what this should include.
The agent you hand off to can either:
* Directly invoke the `/plan-issue` skill if the grilling session was done clearly for the implementation of a ticket/issue.
* Not actually invoke a new agent if next steps are not clear, and tell the user that the artifact was created and where to find it, and ask for next steps to perform and whether that should be done in a new agent session.

