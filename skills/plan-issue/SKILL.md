---
name: plan-issue
description: Plan an issue completely, invokes other skills to ensure comprehensive and agreed upon understanding, spec creation, sub-ticket creation.
disable-model-invocation: true
---

# Plan Issue

Work collaboratively with the user to completely plan out an issue.

Start by reading the `grill-and-record` and running a grilling session with the user. During this grilling session you should ask the user whether this will be implemented in a single PR, or implemented across more PRs and thus requiring sub-tickets.

After a comprehensive shared understanding is reached, confirm with the user that there's nothing more to discuss and then invoke the `to-spec-with-tech-detail` skill to make the spec.

Usually the spec is written directly to the linear ticket, but if one does not exist then the local .agents/<ticket-id-or-name>/spec.md is where it should live.

Finally, once the spec is created, if the user wants more than 1 PR, then invoke the `to-tickets`, making sub-tickets under the primary linear issue given to you.

After this is all complete - confirm with the user next steps, don't begin implementation at all.
