
---
name: grill-and-record
description: A grilling session to sharpen a plan or design that records findings into a markdown file
disable-model-invocation: true
---

Invoke the `grill-with-docs` skill and grill the user as according to the skill.

You must record the grilling session into a local markdown file under `.agents/<ticket-id>/grilling.md` as you go.

This should have a format:

```md
# Grilling: <ticket-id-or-description>

## Questions

### Q1
**Question: <question>**

Shared understanding reached:
<shared-understanding-reached>

...

## Additional Context

Here, any additional context/research etc that has been discussed, but isn't relevant to specific questions should be recorded.

This may include references to other artifacts created as you go.
```

This should contain sufficient information such that a colleague with knowledge of the system, but not of this task could pick this work up and carry forward this work.

Do not attempt to implement anything at the end of the grilling session and merely ask for further instructions when complete.
