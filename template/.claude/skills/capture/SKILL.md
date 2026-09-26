---
name: capture
description: Silently save durable information into the owner's personal ontology vault as it comes up in any conversation, search, or research. Use whenever a conversation surfaces something likely to matter a month from now (a person, pet, place, preference, decision, goal, project, possession, plan, event, or sourced research finding), and whenever the owner says "remember this", "save this", "add to the vault", or "/capture". Updates an existing article when one exists, creates one when not, keeps every citation, commits and pushes, and stays silent except for new articles, cross-domain connections, and real disagreements.
---

# Capture

Keep the owner's vault current without interrupting them. Capture as soon as something durable comes up, not at the end of the session: a missed capture costs more than a small correction later.

## Find the vault

- In a cloud or phone session opened on the vault repo, the vault is the repo root.
- Otherwise, use the vault path named in the instruction that loaded this skill (the owner's global `CLAUDE.md`).
- The vault root holds `README.md`, `index.md`, `log.md`, and `.claude/skills/capture/check.py`.

**Read the vault's `README.md` before your first capture in a session.** It holds every rule this skill follows: scope, types and folders, the article template, relationships, life areas, and conflict handling. If this skill and the README disagree, the README wins.

## Decide whether to capture

Capture if the information is durable as the README defines it and allowed by its Scope section. Skip passing task chatter, anything out of scope, and all credentials. When unsure whether something is in scope, leave it out and mention it to the owner in one line.

## Capture, step by step

1. **Pull first.** `git -C "<vault>" pull --rebase --autostash`.
2. **Search before writing.** Check `index.md`, file names, and `aliases` for the subject, for example `grep -ril "<name>" "<vault>"`. Prefer updating an existing article over creating a new one.
3. **Write.**
   - Updating: add the new claim to the right section, give it a footnote, and change `updated`.
   - Creating: use the README template, the right folder and `type`, a one-line summary, and at least one sourced fact.
   - Every claim gets a footnote naming its source and date. For something said in conversation, cite the owner, the surface, and the date, for example `[^w]: Owner, Claude Code conversation, 2026-09-26.` For outside material, cite the author, title, date, and URL.
   - Link to existing articles, with relationship fields in frontmatter (in quotes) and wikilinks in the body. Store each relationship in one direction only.
   - Something mentioned but not yet known stays an unresolved `[[link]]`. Do not create an empty article for it.
4. **Handle conflicts** as the README says: keep both claims with dates and never delete the older one. Corrections and changes over time are silent. A real disagreement gets flagged.
5. **Keep the index and log current.** Add or update the article's line in `index.md`, and append one line to `log.md` in the form `YYYY-MM-DD | capture | what changed`.
6. **Check.** Run `python "<vault>/.claude/skills/capture/check.py" "<vault>"`. If it fails, fix every problem it lists and run it again. Never commit while it fails.
7. **Commit and push to `main`.**
   - Set the commit identity from the README's Commit identity rule if it is not already set. Commits authored by anyone else can block future pushes to `main` from cloud sessions.
   - `git -C "<vault>" add -A`
   - `git -C "<vault>" commit -m "capture: <short summary>"`
   - `git -C "<vault>" pull --rebase --autostash`
   - `git -C "<vault>" push origin HEAD:main`
   - If the rebase conflicts, run `git -C "<vault>" rebase --abort`, leave the change uncommitted, and flag it to the owner. Never force-push.
8. **Clean up a cloud session's side branch.** Cloud sessions may also push their own `claude/...` branch. After the push to `main` succeeds, delete that one branch, and only if `main` already contains all of its commits:
   - `git -C "<vault>" fetch origin`
   - If `git -C "<vault>" rev-list --count origin/main..origin/<branch>` prints `0`, run `git -C "<vault>" push origin --delete <branch>`.
   - Never delete a branch that has commits missing from `main`, and never delete any branch this session did not create.

## Tell the owner, or don't

Stay silent unless one of these happened. When one did, end your reply with a single line per event:

- New article: `Vault: new article [[Title]]`
- Cross-domain connection, meaning a new link between articles in different life areas from the README: `Vault: connected [[A]] (area) to [[B]] (area)`
- Real disagreement: `Vault: conflict in [[Title]]: <the two claims, briefly>`
- Blocked capture (a failed rebase or an unclear scope): `Vault: not saved: <reason>`

Do not report ordinary updates, same-area links, or routine index and log changes.

## Keep it light

A capture should take a few tool calls and should never take over the owner's actual task. Batch several facts from the same moment into one commit. If the vault cannot be reached (no clone, no network, no permission), keep working on the task and end with `Vault: not saved: <reason>`.
