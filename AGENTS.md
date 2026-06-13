# AGENTS.md

This contains generic instructions for agents to follow when working.

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

### Code is self-documenting

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
