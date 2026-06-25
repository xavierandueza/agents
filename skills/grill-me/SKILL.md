---
name: grill-me
description: Interview the user relentlessly about a plan or design. Use when the user wants to stress-test a plan before building.
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a question can be answered by exploring the codebase, explore the codebase instead.

After you're done with the grilling - you should use `/handoff` with the interaction and all of the Qs + As that you just did. Put the grilling information into the `.agents/<ticket_number>/grilling.md`. 

If this grilling session relates to an issue - the `/handoff` agent should use `/plan-issue` to create the plan based off of the information you've gathered.

If no ticket is specified, still make the handoff document and start another agent, but instruct the agent to await further instructions.
