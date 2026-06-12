# AGENTS.md

This contains generic instructions for agents to follow when working.

## Response format

This user prefers to have responses that are:
* Not overly verbose
* Goes into detail
* Doesn't format in large paragraphs

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
