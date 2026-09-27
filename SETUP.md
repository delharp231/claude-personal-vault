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
- If the owner has an employer, agree early on a bright line (for example, "company name and job title only, no internal details") and write it into the vault's Scope section.

## Files in this repo

| Path | Use |
| --- | --- |
| `template/` | Starting files for the owner's vault. Copy, then fill in. |
| `template/.claude/skills/capture/` | The capture skill and its check script. Generic: they read every owner-specific rule from the vault's README. |
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
3. **Relationship types.** Start from the default set in `template/README.md`. Store each relationship in one direction only, and let backlinks show the reverse.
4. **Folders.** One folder per type, flat inside, is the tested default. Folders are the only structure visible on GitHub from a phone.
5. **Life areas.** Used to decide which new links are worth telling the owner about.
6. **Scope.** Employer rule, sensitive categories, anything the owner wants kept out.
7. **Seeding sources.** What material exists to seed from (see Step 3).

Then copy everything in `template/`, including the hidden `.claude` folder, into the vault, and fill in `README.md` with these decisions. Fill in `.claude/scope.txt` with the terms the check script should police. Copy the three reference articles into the vault's concepts folder and list them in `index.md`, adding a section per type. Run `python .claude/skills/capture/check.py .` and keep going until it passes. It fails on any placeholder left in `README.md` or `CLAUDE.md`, which is how you know setup is finished.

**Gate:** the owner approves every decision, and the README states them.

## Step 3: Seed the vault

Seed from material that already exists, citing every fact to its source. Ask the owner which of these to use:

- **Claude memory files**, in `~/.claude/projects/*/memory/`.
- **Claude Code and Cowork transcripts.** Run `python tools/extract_messages.py <output-folder>`, then read only the output. It keeps the owner's own typed messages and cuts tool output and long pastes. Never quote transcripts into the vault wholesale.
- **GitHub repos**: `gh repo list <user>` and each repo's README.
- **Project folders** on disk.
- **Direct interview** for things no file holds, such as pets, family, and hobbies.

Rules while seeding:

- Build the owner's own article first as the hub, then preferences and goals, then everything else.
- Work in batches. Stop after each batch for the owner to review in Obsidian.
- An article needs at least one sourced fact. Leave unknowns as unresolved `[[links]]`.
- Apply the Scope section to every fact. Check every source for employer details before writing.
- Run `python .claude/skills/capture/check.py .` before every commit.
- If the owner asks you to delete any record of something, remove it from the vault and from your working files, and tell them how to delete the original themselves.

**Gate:** the owner browses the seeded vault and confirms it reads well and the links work.

## Step 4: Capture skill

1. **Commit identity.** Write the owner's git name and noreply email into the README's Commit identity rule. Cloud sessions that commit as anyone else lose the right to push to `main`.
2. **Desktop.** Link the vault's `.claude/skills/capture` folder into `~/.claude/skills/capture` so every Claude Code session finds it:
   - Windows: `New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\skills\capture" -Target "<vault>\.claude\skills\capture"`
   - macOS or Linux: `ln -s "<vault>/.claude/skills/capture" ~/.claude/skills/capture`
3. **Always-on trigger.** Append to the owner's global `~/.claude/CLAUDE.md` a short section naming the vault path and saying: capture is always on, use the `capture` skill, and stay silent except for its one-line notices. The vault's own `CLAUDE.md` from the template covers sessions opened on the repo.
4. **Phone.** The Claude app's **Code** tab runs cloud Claude Code sessions that can clone the repo and push. Regular app chats cannot write to GitHub. Have the owner install the Claude GitHub App (github.com/apps/claude) on the vault repo. Tell the owner to always open phone and cloud sessions on the vault repo: a cloud session only reaches the repo it was opened on and never sees the laptop's global `CLAUDE.md`.
5. **Test both surfaces with real captures.** After the phone test, check on GitHub that the commit landed on `main`, is authored as the owner, and passed the check.

**Gate:** one real capture from each surface, confirmed in Obsidian.

## Step 5: Verify

1. Have the owner open a brand-new Claude Code session **on this computer**, in a folder other than the vault, and ask questions only the vault can answer. Every answer should cite a vault file. Don't run this test in a cloud session opened on a different repo: cloud sessions only see the repo they are opened on and never read the computer's global `CLAUDE.md`, so they can't find the vault.
2. Review the README with the owner. It should let a future agent work in the vault with no other context.

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
