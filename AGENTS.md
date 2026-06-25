# AGENTS.md

This contains generic instructions for agents to follow when working.

## pix — spawning sub-agents

`pix` is a shell utility that spawns a named pi sub-agent in a new tmux window.

**Invocation:**
```
pix <window-name> "<message>"
```

**When to use it:**
- Delegating a parallel workstream to a specialised sub-agent (e.g. reviewer, planner, implementer)
- Kicking off a long-running task without blocking your current window
- Composing multi-agent workflows where each agent has a distinct role

**Behaviour:**
- Creates a new tmux window named `<window-name>` in the current session
- Starts `pi` in that window with the current directory as the working directory
- Seeds the message (or `/skill:<skill-name>` slash command) into the pi TUI automatically
- Runs fully in the background — your current window is unaffected
- If `<window-name>` is already taken, auto-suffixes (`-2`, `-3`, ...)

**Window naming convention:** use role-descriptive names.
```
pix implementer "/skill:implement the auth middleware as per the plan at .agents/rm-100/plan.md"
pix reviewer "/skill:thermo-nuclear-code-quality-review review the changes made in PR-100"
```

**Notes:**
- No flag passthrough — `pi` is always invoked with defaults
- Skill invocations (e.g. `/tdd`, `/grill-me`) work natively via tmux send-keys into the TUI - but note that you MUST start the message with `/skill:<skill-name>` for this to work, following text instructions can go after.

## Response format

This user prefers to have responses that are:
* Not overly verbose
* Goes into detail
* Doesn't format in large paragraphs

### No sycophancy

This user does not appreciate compliments, and prefers for you to be direct. They appreciate being challenged and being pushed back on.

Any ideas that have holes in them should be identified, and it is completely fine to disagree with this user when there are valid alternatives that, in your opinion, would be better.

## Code

These are generic coding principals that MUST be followed at all times when generating any code.

### Commenting

All code is self-documenting. Do NOT provide useless comments that just explain WHAT the code is doing when it is obvious what the code is doing.

<bad-example>
```ts
# Fetch the user from the database
user = db.get("user", id);
```
</bad-example>

<good-example>
```
user = db.get("user", id);
```
</good-example>

It's fine to explain the WHAT when its not immediately clear from the code - regex is a good example where a what comment is helpful, since it is difficult to parse the regex.

#### Comment Depth

Comments should always be succinct - typically a line is usually suffice.

NEVER reference any linear tickets, PRs, GH issues in ANY tickets - that's something that gets old extremely quickly.

### Don't abstract away for simple checks

If an abstraction would only be a single line, UNLESS that abstraction is used a LOT then don't abstract into a function, and just do the check inline:

<bad-example>
```ts
function isMale(user: User): boolean {
  return user.sex === 'male';
}
```
</bad-example>

<good-example>
```ts
  if (user.sex === 'male') {
    // rest of code
  }
```

</good-example>

### If the user asks a question

NEVER just assume that when the user asks a question that they want you to actually update code.

Just answer the user's question and DON'T ask whether the user wants changes - they will tell you to update things when they tell you to. 

DON'T autonomously decide to go and make changes UNLESS you receive express permission to do so.

### The user cares DEEPLY about best practice

This user always wants to know about best practice standards, patterns and more. When answerint their questions - always mention what is best-practice for the topic/task at hand. This is particularly when there are other methods that may work better than what they may be proposing/asking for feedback on.

