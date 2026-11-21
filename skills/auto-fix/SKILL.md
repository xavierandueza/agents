---
name: auto-fix
description: Autonomously verify the issue by replicating, and implement a fix.
---

# Auto-fix

Own the fix for an issue through to a draft PR.

Use the current worktree unless assigned another.

## 1. Replicate the issue

Read the request and any ticket, including its description, comments, images, etc. and replicate the issue.

You MUST be able to replicate the issue, and record evidence of the issue in the given (states) using the [`verify`](../verify/SKILL.md) skill.

If you cannot replicate the issue - you must stop and ask for further instructions. NEVER implement a fix for something that you cannot verify - since there's no way to know if you actually resolved the issue.

## 2. Auto-implement the solution

Call the [`auto-implement`](../auto-implement/SKILL.md) skill to design and then draft the solution to the problem. Put up the draft-pr as the skill suggests, but ensure that the evidence on the PR includes the clear BEFORE + AFTER in tables for the exact issue.
