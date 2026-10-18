---
name: capture
description: Start every session by reading the vault's AGENTS.md. Silently save durable information into the owner's personal ontology vault as it comes up in any conversation, search, or research. Use whenever a conversation surfaces something likely to matter a month from now (a person, pet, place, preference, decision, goal, project, possession, plan, event, or sourced research finding), and whenever the owner says "remember this", "save this", "add to the vault", or "/capture". Updates an existing article when one exists, creates one when not, keeps every citation, commits and pushes, and stays silent except for new articles, cross-domain connections, and real disagreements.
---

# Capture

Keep the owner's vault current without interrupting them. Capture as soon as something durable comes up, not at the end of the session: a missed capture costs more than a small correction later.

## Find the vault

- Read the vault's `AGENTS.md` at the start of a session, before anything else. It sets the load order this skill assumes: pull, load the always-on context, then read `README.md` before the first capture.
- In a cloud or phone session opened on the vault repo, the vault is the repo root.
- Otherwise, use the vault path named in the instruction that loaded this skill (the owner's global instruction file, such as `~/.claude/CLAUDE.md` for Claude Code or `~/.codex/AGENTS.md` for Codex CLI).
- The vault root holds `README.md`, `index.md`, `log.md`, and `.claude/skills/capture/check.py`.

**Read the vault's `README.md` before your first capture in a session.** It holds every rule this skill follows: scope, types and folders, the article template, relationships, life areas, and conflict handling. If this skill and the README disagree, the README wins.

## Decide whether to capture

Capture if the information is durable as the README defines it and allowed by its Scope section. Skip passing task chatter, anything out of scope, and all credentials. When unsure whether something is in scope, leave it out and mention it to the owner in one line.

## Capture, step by step

1. **Pull first.** `git -C "<vault>" pull --rebase --autostash`.
2. **Search before writing.** Check `index.md` (recent changes and topics), `catalog.md` (every article by topic), file names, and `aliases` for the subject, for example `grep -ril "<name>" "<vault>"`. Prefer updating an existing article over creating a new one.
3. **Write.**
   - Updating: add the new claim to the right section, give it a footnote, and change `updated`.
   - Creating: use the README template, the right folder and `type`, a one-line summary, at least one sourced fact, and `topics:` with 1 to 3 hubs from the Topics list in `index.md`, primary first. If no hub fits, file it under the closest one and say so (see below). Never add or remove `in_scheme`; only the owner approves a new hub.
   - A thought the owner gives about a source goes on that source's article as `- Owner's take (YYYY-MM-DD): ...`, as the README's Creating and updating articles section says.
   - Every claim gets a footnote naming its source and date. For something said in conversation, cite the owner, the surface, and the date, for example `[^w]: Owner, Claude Code conversation, 2026-09-26.` For outside material, cite the author, title, date, and URL.
   - Link to existing articles, with relationship fields in frontmatter (in quotes) and wikilinks in the body. Store each relationship in one direction only.
   - Something mentioned but not yet known stays an unresolved `[[link]]`. Do not create an empty article for it.
4. **Handle conflicts** as the README says: keep both claims with dates and never delete the older one. Corrections and changes over time are silent. A real disagreement gets flagged.
5. **Log, then rebuild the index.** Append one line to `log.md` in the form `YYYY-MM-DD | capture | <Article title>: what changed`, starting with the article's title. Then run `python "<vault>/.claude/skills/capture/build_index.py" "<vault>"`. Never edit `index.md` or `catalog.md` by hand; they are generated.
6. **Check.** Run `python "<vault>/.claude/skills/capture/check.py" "<vault>"`. If it fails, fix every problem it lists and run it again. Never commit while it fails. Lines under `Warnings:` don't block a commit. If `check.py` itself crashes (a Python error instead of a list of problems), run it again with `--legacy-only`, which runs only the original checks, and tell the owner in one line.
7. **Commit and push to `main`.**
   - Set the commit identity from the README's Commit identity rule if it is not already set. Commits authored by anyone else can block future pushes to `main` from cloud sessions.
   - `git -C "<vault>" add -A`
   - `git -C "<vault>" commit -m "capture: <short summary>"`
   - `git -C "<vault>" pull --rebase --autostash`
   - `git -C "<vault>" push origin HEAD:main`
   - If the rebase conflicts only in `index.md` or `catalog.md`, run the builder again, then `git -C "<vault>" add index.md catalog.md` and `git -C "<vault>" -c core.editor=true rebase --continue`. Generated files never need a person to merge them.
   - If the rebase conflicts in anything else, run `git -C "<vault>" rebase --abort`, leave the change uncommitted, and flag it to the owner. Never force-push.

## Tell the owner, or don't

Stay silent unless one of these happened. When one did, end your reply with a single line per event:

- New article: `Vault: new article [[Title]]`
- Cross-domain connection, meaning a new link between articles in different life areas from the README: `Vault: connected [[A]] (area) to [[B]] (area)`
- Real disagreement: `Vault: conflict in [[Title]]: <the two claims, briefly>`
- No topic fits a new article: `Vault: no topic fits [[X]]; filed under [[Y]]. New hub?` If the owner says yes, set `in_scheme: "[[Vault topics]]"` on the article they name, refile the members they agree to, and rebuild.
- Blocked capture (a failed rebase or an unclear scope): `Vault: not saved: <reason>`

Do not report ordinary updates, same-area links, or routine index and log changes.

## Keep it light

A capture should take a few tool calls and should never take over the owner's actual task. Batch several facts from the same moment into one commit. If the vault cannot be reached (no clone, no network, no permission), keep working on the task and end with `Vault: not saved: <reason>`.
