---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. If currently on a branch that has a ticket id, save to `.agents/<ticket-id>/` directory - otherwise save to `.agents/<new-folder-name>` directory, where the folder name is based on the details of the interaction. Keep that folder name brief, and the resulting .md document name brief too. Follow naming conventions of other issues/folders.

Include a "suggested skills" section in the document, which suggests skills that the agent should invoke. If there are instructions to invoke a specific skill in the next agent directly, make that clear.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path, id, or URL instead.

If arguments were passed, treat them as a description of what the next session will focus on and tailor the doc accordingly.
