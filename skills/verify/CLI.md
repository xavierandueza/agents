# CLI verification

Run the real binary or entrypoint the user would run, not a test harness.

## Transcripts

Save each AC as a `.txt` transcript holding the command, its output, and its exit code:

```bash
{ echo "\$ mytool sync --dry-run"; mytool sync --dry-run; echo "[exit $?]"; } > "$RUN/01-dry-run.txt" 2>&1
```

When the AC is about a side effect (files written, config changed, a row inserted), capture the check that proves it in the same transcript, e.g. `cat` the file or query the row.

## Screenshots

For visual evidence, render with [`freeze`](https://github.com/charmbracelet/freeze), which runs the command in a PTY and keeps colour:

```bash
freeze --execute "mytool sync --dry-run" -o "$RUN/01-dry-run.png"
```

## Interactive and long-running commands

Drive TUIs, prompts, and servers in a Herdr pane (load the `herdr` skill): `pane run`, `wait-output`, `send-keys`, then `pane read` into a `.txt` transcript. Use one pane per long-running process, and close the tab when done.

## Isolation

- If the tool writes to the working directory, run it in a scratch dir (`mktemp -d`) outside the repo.
- If it writes global state (`~/.config`, a user's config file), snapshot that state into `private/` first, then diff it after cleanup to prove nothing was left behind.
- Redact tokens from output with `sed` before it reaches `vNN/`.
