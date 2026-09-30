# Instructions for agents

This repo is a personal knowledge vault. It is the canonical context about its owner, named in `README.md`, for every agent and harness they use.

At the start of every session:

1. Pull: `git -C "<vault>" pull --ff-only`. If it fails, continue with what is on disk.
2. Read `README.md` for the rules, then `index.md` to see what exists.
3. Read every article in `Preferences/` before doing anything for the owner.
4. Open other articles only when the conversation needs them.

Capture is always on. Whenever the conversation surfaces something durable, follow `.claude/skills/capture/SKILL.md` right away. If that procedure and `README.md` disagree, the README wins. Commit and push straight to `main` as the owner, using the identity in the README's Commit identity rule, never to a side branch, and never force-push. Never write facts about the owner to a harness's private memory instead of this vault.
