# Web verification

Drive the browser with `playwright-cli`; load its skill for the command reference. If it isn't installed, stop and ask.

- Run it from the `verification/` directory so its `.playwright-cli/` logs stay out of the repo.
- Use a named, in-memory session per run (`-s=<name>`), so it starts signed out and doesn't clash with other sessions. `playwright-cli list` first and close a stale one.
- Read element refs from a fresh `snapshot` on each page; they change between pages.
- Sign-in and setup stay out of the video unless sign-in is what you're testing. Save storage state to `private/` if you need to reuse it.

## Evidence

- Screenshot the end state of each AC: `screenshot --filename="$RUN/01-<what>.png"`.
- Record a video of the main flow (`video-start` / `video-stop`) when the AC is about interaction, not just a final state.
- Cover mobile (`resize 390 844`) and dark mode (`run-code "async page => page.emulateMedia({ colorScheme: 'dark' })"`) when the change affects layout or styling. Suffix those shots `-mobile` / `-dark`.

## Secrets

`playwright-cli` echoes the page URL after most commands. When a URL carries a token or code (magic links, OAuth callbacks), pipe output through a `sed` redaction, and keep the raw URL in a `private/` file.

Close every session you opened with `playwright-cli -s=<name> close`.
