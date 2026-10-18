# Maintaining this template

For the person who keeps this repo current with their own working vault. Agents building a vault do not need this file.

The tooling in `template/.claude/` is a generic copy of what runs in a working vault. When the working vault learns something, port it here by hand.

## What to port

| Template file | Source in a working vault | Notes |
| --- | --- | --- |
| `skills/capture/build_index.py`, `vault_parse.py`, `check.py`, `rules/legacy.py`, `rules/topics.py`, `rules/__init__.py` | Same names | Copy, then scrub docstrings of private repo names, spec paths, and commit ids. |
| `skills/capture/rules/preferences.py` | Template only | Validates the Preference frontmatter the loader reads. |
| `skills/capture/SKILL.md` | Same | Replace the owner's name with "the owner". |
| `hooks/pref_loader.py` | Template only | Reads each Preference's tier and triggers from its frontmatter. A working vault may keep them in code, so port behavior changes by hand. |
| `hooks/session_start.py` | Same | Already generic. |
| `AGENTS.md`, `README.md` | Same | Keep owner-specific rules out. Placeholders stay unfilled. |

## Before you push

1. Run from `template/`: `python .claude/skills/capture/build_index.py . --check` and `python .claude/skills/capture/check.py --selftest`. Both must pass.
2. Run `python .claude/skills/capture/check.py .`. The only errors left should be the unfilled README placeholders.
3. Simulate an owner: copy `template/` to a scratch folder, fill the placeholders, add one article and two Preferences with triggers, rebuild the index, and run `session_start.py` and `pref_loader.py` in all three modes. The check must pass.
4. Scrub. Search the working tree and every commit's added lines for your name, your employer's name, your private repo names, your email, and local paths. Keep that term list in your own notes, not in this repo. Check that the search finds hits in your working vault, so you know it works.
5. Read the diff. Push to a branch first and run SETUP from that branch's link in a fresh agent session before merging to `main`.

## Releases

Tag a release after each merged change, such as `v1`. A link to `main` moves under people who use it later, so point the README's prompt at a tag once one exists.
