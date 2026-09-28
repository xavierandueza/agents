---
name: fleet-implement
description: Orchestrate agents to implement a body of work, carrying the work through to full completion including drafting PRs.
disable-model-invocation: true
---

# Fleet Implement

Invoke the `orchestrate-agents` skill to understand how to manage the fleet of agents that you will be coordinating to implement the work.

For each individual task, if the task is a coding task it is ONLY considered completed upon drafting a Github Pull-Request - ensure that sub-agents use the `draft-pr` skill to do this.

