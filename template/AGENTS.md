# Instructions for agents

This repo is a personal knowledge vault. It is the canonical context about its owner, named in `README.md`, for every agent and harness they use.

At the start of every session:

1. Pull: `git -C "<vault>" pull --ff-only`. If it fails, continue with what is on disk.
2. Load the always-on context. In Claude Code a SessionStart hook has already printed it (it begins "Personal knowledge vault at"). Anywhere else, run `python .claude/hooks/pref_loader.py session` in this repo and read the output. It holds the rules digest, the topic hubs, the Preferences that always apply, and the titles of the rest.
3. The other Preferences load on demand. In Claude Code, hooks inject them when a prompt or tool call matches, and announce "Preferences loaded: ...". Without hooks, open the matching article in `Preferences/` yourself before the task it governs. Each Preference lists its triggers in its own frontmatter. Responses stay grounded either way: cite sources and label inference.
4. Before writing to the vault, read `README.md`. Open other articles, hubs, and `catalog.md` (the duplicate-check list) only when the conversation needs them.

Capture is always on. Whenever the conversation surfaces something durable, follow `.claude/skills/capture/SKILL.md` right away. If that procedure and `README.md` disagree, the README wins. Commit and push straight to `main` as the owner, using the identity in the README's Commit identity rule, never to a side branch, and never force-push. Never write facts about the owner to a harness's private memory instead of this vault.
