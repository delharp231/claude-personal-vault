# Setup guide for Claude

You are helping the owner build a personal ontology vault: a private, git-backed Obsidian vault that gives their Claude sessions and other agents shared, persistent, relational context about their life. Follow this guide step by step.

## How to work with the owner

- **Interview before building.** Ask one question at a time. Ask the owner early whether they prefer open questions or multiple choice, and use their answer for the rest of the build.
- **Get explicit approval for every key decision before building it.** Summarize what was decided before moving on.
- **Explain what you are doing and why.** Many owners are doing this to learn.
- **Keep it lean.** Build only what an approved decision calls for.
- **Make no assumptions.** If something is unclear or unverified, ask or check. Never write an inference into the vault as a fact: "drives to a town to look after a relative's pets" does not mean "the relative lives there."
- **Each step ends with a gate.** Do not start the next step until the owner approves.

## Safety rules for the whole build

- Never force-push, delete files, delete branches, or rewrite git history without the owner's explicit approval for that specific action.
- Never write credentials, passwords, API keys, or tokens into the vault.
- Before the owner installs any Obsidian plugin besides Git, check what it writes inside the vault folder. The Git plugin auto-commits everything that isn't ignored, including a plugin's settings file (which may hold an access token) and any program files it downloads. Add those paths to `.gitignore` before the next auto-commit, and remove the lines if the plugin is uninstalled.
- Ask before capturing sensitive categories: health, family members, finances, and anything about the owner's employer.
- If the owner has an employer, agree early on a bright line (for example, "company name and job title only, no internal details") and write it into the vault's Scope section. The check script's word list (`.claude/scope.txt`) can only enforce rules about names and terms. A rule that needs judgment, like "nothing confidential," lives only in the Scope section, and agents apply it by reading.

## Files in this repo

| Path | Use |
| --- | --- |
| `template/` | Starting files for the owner's vault. Copy, then fill in. |
| `template/AGENTS.md` | Session-start steps any agent tool can read. The vault's `CLAUDE.md` imports it, so Claude reads the same file and the two can't drift. |
| `template/.claude/skills/capture/` | The capture skill, its check engine (`check.py` and `rules/`), and the index builder (`build_index.py`). Generic: they read every owner-specific rule from the vault's README. |
| `template/.claude/hooks/` | `session_start.py` pulls the vault and prints the always-on context. `pref_loader.py` loads each Preference when its triggers match. Neither holds anything personal: the Preferences carry their own tier and triggers. |
| `template/Preferences/` | Two default Preferences about how the vault works, not about the owner: "Stay grounded" and "Reference the vault selectively". |
| `template/Creative works/` | The `Vault topics` scheme article and one starter hub. Step 2 replaces the hub with the owner's own topics. |
| `reference/` | Three research articles behind the design. Use them in Step 2 instead of redoing the research. |
| `tools/extract_messages.py` | Pulls only the owner's own typed messages out of Claude Code and Cowork transcripts, for seeding. |

## Step 0: Preflight

Check, do not assume:

- `git --version`
- `gh --version` and `gh auth status`. The owner needs a GitHub account and `gh` signed in with the `repo` scope.
- Obsidian installed. If not, have the owner install it from obsidian.md.
- The operating system, because commands differ between Windows and macOS or Linux.
- `git config --global user.email`. Suggest the owner's GitHub noreply address if it is unset or a placeholder.

## Step 1: Repo and vault

1. Ask the owner for a vault name and a location.
2. Create the folder, run `git init -b main`, then `gh repo create <name> --private --source . --remote origin`.
3. Have the owner open the folder in Obsidian with **Open folder as vault**. Then look at what Obsidian wrote in `.obsidian/`.
4. Copy `template/.gitignore` into the vault. It ignores Obsidian's constantly changing UI state (`workspace.json`), the trash, and OS clutter. Explain the rule: track content and settings, ignore anything that changes from clicking around.
5. Make the first commit and push it.
6. Sync: have the owner install the community plugin **Git** (by Vinzent) through Obsidian's plugin browser, then set auto commit-and-sync to 10 minutes, auto pull to 10 minutes, and pull on startup.
7. Test the plugin: the owner runs **Git: Commit-and-sync** from the command palette. Warn them first: **close the Settings window before running commands**, or the command silently does nothing. Confirm the commit reached GitHub.
8. Watch for accidental stub notes. The Daily note and Bases icons create files with one click. Ask before deleting any.

**Gate:** the repo exists and is private, the vault opens in Obsidian, and a commit from the plugin has pushed.

## Step 2: Design decisions

Read the three articles in `reference/` and summarize them for the owner. Then settle these decisions one at a time, each with explicit approval:

1. **Article template.** Ask what an agent should be able to tell at a glance. The template in `template/README.md` is a tested default.
2. **Entity types.** Build the list from the owner's own life, using schema.org's top level as a checklist. Flag questionable items and let the owner decide.
3. **Goals.** If goals are one of the types, ask whether they are fixed targets or directions.
   - **Fixed targets** (the default): each goal has a `## Plan` section. Delete the optional "Goals are directions" section from `README.md`.
   - **Directions:** the goal may drift. The summary line names the direction, and a `## Current bets` section lists the concrete moves the owner is making now, each dated, with old bets kept when they change. Deadlines and stated preferences inside a goal stay firm. This suits owners whose goals shift as they learn. Keep the "Goals are directions" section in `README.md`, and change the Goals row in its folder table to: "Directions the owner is moving in, not fixed targets. Each has a `## Current bets` section: the concrete moves they are making now."
4. **Relationship types.** Start from the default set in `template/README.md`. Store each relationship in one direction only, and let backlinks show the reverse.
5. **Folders.** One folder per type, flat inside, is the tested default. Folders are the only structure visible on GitHub from a phone.
6. **Life areas.** Used to decide which new links are worth telling the owner about.
7. **Scope.** Employer rule, sensitive categories, anything the owner wants kept out.
8. **Topics.** The index groups articles under hubs listed in `Vault topics`. Ask what the owner looks for in their own life and propose a starting list. A hub needs at least 3 articles to earn its place, so start short and let the list grow with the owner's approval. Replace the starter hub, `Personal ontology vault`, with the approved list. Each hub is an article with `in_scheme: "[[Vault topics]]"`.
9. **Seeding sources.** What material exists to seed from (see Step 3).

Then copy everything in `template/`, including `AGENTS.md`, the hidden `.claude` folder, `Preferences/`, and `Creative works/`, into the vault, and fill in `README.md` with these decisions. If the owner renamed the preferences type, change `Preferences/` in `AGENTS.md`, `.claude/hooks/pref_loader.py`, `.claude/skills/capture/build_index.py`, and `.claude/skills/capture/vault_parse.py` to match. Fill in `.claude/scope.txt` with the terms the check script should police. Copy the three reference articles into the vault's concepts folder with `topics:` naming a hub. Run `python .claude/skills/capture/build_index.py .` to write `index.md` and `catalog.md`, then `python .claude/skills/capture/check.py .` and keep going until it passes. The check fails on any placeholder left in `README.md` or `CLAUDE.md`, which is how you know setup is finished.

**Gate:** the owner approves every decision, and the README states them.

## Step 3: Seed the vault

Seed from material that already exists, citing every fact to its source. Ask the owner which of these to use:

- **Claude memory files**, in `~/.claude/projects/*/memory/`.
- **Memory from other AI assistants** the owner has used, exported or pasted in.
- **Claude Code and Cowork transcripts.** Run `python tools/extract_messages.py <output-folder>`, then read only the output. It keeps the owner's own typed messages and cuts tool output and long pastes. Never quote transcripts into the vault wholesale.
- **GitHub repos**: `gh repo list <user>` and each repo's README.
- **Project folders** on disk.
- **Direct interview** for things no file holds, such as pets, family, and hobbies.

Rules while seeding:

- **Archive memory before seeding from it.** Copy each memory source into the vault's `archive/` as a dated snapshot, for example `archive/claude-memory-<date>/` for Claude's memory folder and `archive/<assistant>-memory-<date>.md` for a pasted export. Cite the archived copy, not the original, so citations still resolve on another machine or after the original is gone. Have the owner add `archive/` under Obsidian's **Settings > Files and links > Excluded files**, so the snapshots stay out of search and the graph.
- Memory from different assistants often disagrees. Keep both claims with their dates, and ask the owner to settle each real disagreement, per the README's conflict rule.
- Build the owner's own article first as the hub, then preferences and goals, then everything else.
- Work in batches. Stop after each batch for the owner to review in Obsidian.
- An article needs at least one sourced fact. Leave unknowns as unresolved `[[links]]`.
- Apply the Scope section to every fact. Check every source for employer details before writing.
- Give every article `topics:` naming 1 to 3 hubs, primary first. Run `build_index.py`, then `check.py`, before every commit.
- When the owner states how they want things done, write it as a Preference with a tier and triggers (see the README's Preferences section). Keep the core ones few and short, since they load at every session start.
- If the owner asks you to delete any record of something, remove it from the vault and from your working files, and tell them how to delete the original themselves.

**Retire the old memory.** Once the vault holds what the memory files held, ask the owner whether to trim them. Otherwise two versions of the owner drift apart, and agents can't tell which is current. With approval, back the memory folder up, then move out (don't delete) every file that holds facts about the owner. Keep only notes about the harness itself, plus one note saying that facts about the owner live in the vault.

**Gate:** the owner browses the seeded vault and confirms it reads well and the links work.

## Step 4: Capture skill

1. **Commit identity.** Write the owner's git name and noreply email into the README's Commit identity rule. Cloud sessions that commit as anyone else lose the right to push to `main`.
2. **Desktop.** Link the vault's `.claude/skills/capture` folder into `~/.claude/skills/capture` so every Claude Code session finds it:
   - Windows: `New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\capture" -Target "<vault>\.claude\skills\capture"`
   - macOS or Linux: `ln -s "<vault>/.claude/skills/capture" ~/.claude/skills/capture`
3. **Always-on trigger.** Append to the owner's global `~/.claude/CLAUDE.md` a short section naming the vault path and saying: at the start of every session, follow the vault's `AGENTS.md` (pull, then load the always-on context); the session-start hook prints that context, and elsewhere the agent runs `python <vault>/.claude/hooks/pref_loader.py session`; other Preferences load on demand, by hook in Claude Code and by opening the matching article in `Preferences/` elsewhere; responses stay grounded, so cite sources and label inference; read the vault's `README.md` before writing to it, and open other articles, hubs, or `catalog.md` only when the conversation needs them; capture is always on, use the `capture` skill, and stay silent except for its one-line notices; write durable facts about the owner to the vault, never to a harness's private memory. The vault's own `AGENTS.md`, which its `CLAUDE.md` imports, covers sessions opened on the repo.
4. **Hooks.** Register three hooks in the owner's `~/.claude/settings.json`. `session_start.py` pulls the vault at the start of every session on this computer (fast-forward only, so it never merges or leaves a conflict, and it skips quietly when offline) and prints the always-on context. `pref_loader.py prompt` and `pref_loader.py tool` inject a Preference when its triggers match a prompt or a tool call. Sessions then start current even when Obsidian is closed, and the capture skill is always the latest version.
   - Back up `settings.json` first, then merge this in without removing existing settings: `{"hooks": {"SessionStart": [{"hooks": [{"type": "command", "command": "python \"<vault>/.claude/hooks/session_start.py\"", "timeout": 30}]}], "UserPromptSubmit": [{"hooks": [{"type": "command", "command": "python \"<vault>/.claude/hooks/pref_loader.py\" prompt", "timeout": 10}]}], "PreToolUse": [{"matcher": "Write|Edit|NotebookEdit|mcp__.*", "hooks": [{"type": "command", "command": "python \"<vault>/.claude/hooks/pref_loader.py\" tool", "timeout": 10}]}]}}`. Use forward slashes in the path, and `python3` if that is the owner's Python command. Widen the `PreToolUse` matcher only if a Preference needs another tool.
   - Test it by running `session_start.py` once by hand: it should print a one-line header, the rules digest, the topic hubs, and the core Preferences. Then pipe a prompt that matches a trigger into `pref_loader.py prompt` and confirm it prints a "Preferences loaded" message.
   - To turn the loader off, create an empty file named `pref_loader.off` next to the script. The session hook then tells the agent to read every Preference.
5. **Other agent tools.** Ask whether the owner uses, or may switch to, other agent tools such as Codex CLI or Gemini CLI. If so, set them up the same way, so the vault survives a change of model or tool:
   - Keep one canonical copy of the global section from item 3 in a file the owner versions, such as a private repo, and write it to each tool's global instruction file: `~/.claude/CLAUDE.md` for Claude Code, `~/.codex/AGENTS.md` for Codex CLI, and `~/.gemini/GEMINI.md` for Gemini CLI. Confirm each path in the tool's current docs.
   - Offer a small script that copies the canonical file to every target, run at logon or on a schedule, so the copies never drift. Mark each copy as generated, so nobody edits it by hand.
   - If a tool loads skills, link the vault's capture folder into the folder that tool scans, as in item 2.
   - If a tool offers a session-start hook, point it at the same `session_start.py`. Otherwise, steps 1 and 2 of `AGENTS.md` have the agent pull first, then run `pref_loader.py session` and read the output. Without prompt and tool hooks, the agent opens the matching Preference itself before the task it governs.
6. **Phone.** The Claude app's **Code** tab runs cloud Claude Code sessions that can clone the repo and push. Regular app chats cannot write to GitHub. Have the owner install the Claude GitHub App (github.com/apps/claude) on the vault repo. Tell the owner to always open phone and cloud sessions on the vault repo: a cloud session only reaches the repo it was opened on and never sees the laptop's global `CLAUDE.md`.
7. **Branch cleanup.** Cloud sessions leave `claude/...` branches on GitHub and can't delete them. Copy `template/.github/workflows/cleanup-claude-branches.yml` into the vault. This GitHub Action deletes a `claude/` branch only when `main` already has every commit on it, on each push and once a day. Test it: push a throwaway `claude/test` branch at `main`'s commit and confirm the Action deletes it.
8. **Test both surfaces with real captures.** After the phone test, check on GitHub that the commit landed on `main`, is authored as the owner, and passed the check.

**Gate:** one real capture from each surface, confirmed in Obsidian.

## Step 5: Verify

1. Have the owner open a brand-new Claude Code session **on this computer**, in a folder other than the vault, and ask questions only the vault can answer. Every answer should cite a vault file. Don't run this test in a cloud session opened on a different repo: cloud sessions only see the repo they are opened on and never read the computer's global `CLAUDE.md`, so they can't find the vault.
2. If the owner set up another agent tool in Step 4, repeat the test there. The agent should find the vault and read its preferences without being told where it is.
3. Run `python .claude/skills/capture/check.py --selftest` and confirm it prints `SELFTEST OK`.
4. In the new session, give a prompt that matches one Preference's trigger and confirm a "Preferences loaded: <name>" message appears. If none does, check the three hooks in `settings.json`.
5. Review the README with the owner. It should let a future agent work in the vault with no other context.

**Gate:** the owner signs off.

## If git history ever needs rewriting

For example, when something out of scope was committed and pushed. Get explicit approval first, then:

1. Make a backup with `git bundle create <backup-file> --all`.
2. **Pause sync.** Have the owner quit Obsidian and keep it closed until you say so. On startup the Git plugin pulls and will merge the old history straight back in. Do not rely on the app staying closed: check before pushing.
3. Rewrite with `git filter-repo`, or with `git filter-branch` if filter-repo is not installed.
4. Delete `refs/original/`, expire the reflog, and run `git gc --prune=now`.
5. Verify with `git log --all -G "<text>"` that the text is in no commit.
6. Run `git push --force-with-lease`, then confirm the remote matches.
7. Tell the owner that GitHub may still serve the old commits by their exact ID until its own cleanup runs.

## Maintenance

After setup, the owner can ask any session for a lint pass. The vault README defines it.

When the owner later builds routines, skills, or agents on the vault, follow the README's "Building on the vault" rule: each model step reads only the part of the vault its task needs.

Not included: logging which articles cloud sessions read. It is only worth building together with a weekly rollup that counts the reads, since cloud sessions leave no transcript on the owner's computer.
