# Personal ontology vault

<OWNER NAME>'s personal knowledge base. It is shared, persistent context for their Claude sessions and any agents they build. It lives in Obsidian and in the private GitHub repo `<GITHUB USER>/<REPO>`.

**Agents: read this file, then `index.md`, before reading or writing anything else.**

<!-- Setup: replace every <PLACEHOLDER>, adjust the defaults below to the owner's approved decisions, then delete this comment. -->

## Scope

- **In:** anything personal and durable. <LIST WHAT THE OWNER WANTS IN, for example people, pets, hobbies, ideas, research, goals, preferences, side projects.>
- **Out, always:** <THE OWNER'S BRIGHT LINES, for example: internal details of their employer. The vault may hold the company's name and the owner's job title, and nothing else about it.> When a source mixes allowed and excluded material, take only the allowed part.

## Where to start

| File | Purpose |
| --- | --- |
| `README.md` | These rules |
| `index.md` | Every article, grouped by type, with a one-line description. Read it first to find what exists. |
| `log.md` | Append-only record of changes, newest at the bottom |
| `CLAUDE.md` | Short instructions any Claude session in this repo loads automatically |
| `.claude/skills/capture/SKILL.md` | The capture procedure |
| `.claude/skills/capture/check.py` | Pre-commit check. Run `python .claude/skills/capture/check.py .` and never commit while it fails |
| `.claude/scope.txt` | Terms the check watches for, and where each may appear |

## Folders and types

One folder per type. No subfolders. The `type` field repeats the folder so queries can filter on it.

**Folder names are exact, including capital letters.** Never create a new top-level folder. Windows treats `People` and `people` as the same folder, but GitHub treats them as two, so a wrong case from another surface splits a folder in the repo.

<!-- Default types. Keep, rename, add, or drop to match the owner's approved list. -->

| Folder | `type` | What goes here |
| --- | --- | --- |
| `People/` | `person` | Anyone worth remembering, including the owner |
| `Organizations/` | `organization` | Companies, communities, groups |
| `Places/` | `place` | Physical locations that matter. Smaller places link to larger ones with `part_of`. |
| `Events/` | `event` | Something that happened, or is planned, at a point in time |
| `Concepts/` | `concept` | Ideas, frameworks, mental models, research syntheses |
| `Tools/` | `tool` | Software and physical tools the owner uses |
| `Creative works/` | `creative work` | Things the owner makes: posts, sites, apps, projects |
| `Hobbies/` | `hobby` | Things the owner does for fun |
| `Animals/` | `animal` | Species or breed research |
| `Pets/` | `pet` | Animals owned by the owner or their family. Say whose in the summary. Link each to its Animal with `is_a`. |
| `Goals/` | `goal` | What the owner is working toward. Each has a `## Plan` section. |
| `Preferences/` | `preference` | How the owner wants things done. Check these before acting for them. |
| `Sources/` | `source` | Anything made by someone else that earns its own page: a book, article, video, paper, or game |

## Article template

```markdown
---
type: pet
aliases:
  - Other name
part_of: "[[Larger thing]]"
related:
  - "[[Another article]]"
captured_from: conversation, Claude Code, 2026-01-01
created: 2026-01-01
updated: 2026-01-01
---

# Title

One or two sentences saying what this is.

## Details

- A claim.[^1]

## Sources

[^1]: Who or what said it, date, and a URL or file path.
```

- **Summary line:** say what the thing is. An agent should be able to stop reading here.
- **Details:** long articles may split this into several `##` sections.
- **Footnotes:** every claim gets one. Put the citation on the claim, not only at the end.
- **`captured_from`:** how the article entered the vault (research, conversation, seed), which surface, and the date.
- **`updated`:** change it whenever the article changes.

## Relationships

Relationships are frontmatter fields. Values are wikilinks **in quotes** (`"[[Name]]"`), single or a list.

| Field | Meaning | Example |
| --- | --- | --- |
| `is_a` | Instance or kind of | Pet → Animal |
| `part_of` | A piece of a larger thing | A neighborhood → its city |
| `supports` | Moves a goal forward | A project → a Goal |
| `made_by` | Who created it | A source → its author |
| `about` | What a work is about | A book → a Concept |
| `affiliated_with` | A person's tie to an organization | A person → a company |
| `applies_to` | What a preference governs | A preference → a creative work |
| `related` | Connected, when nothing more specific fits | Anything |

Rules:

- **Store one direction only.** Write the field on the article named first in the table's meaning. Obsidian backlinks show the reverse. Never add inverse fields like `has_part`.
- **Field names are snake_case.**
- **Relationships between people go in the body as prose,** not as fields.

## Naming and linking

- Titles are unique across the whole vault, because wikilinks match by name. On a clash, add a qualifier: `Magic (card game)`.
- Put other names in `aliases` so searches and links find the article.
- Link by title, not by path.
- Avoid dots in titles (`Acme`, not `Acme.io`). Obsidian can read the part after the dot as a file extension. Put the dotted name in `aliases`.

## Creating and updating articles

- **Search before creating.** Check `index.md`, titles, and aliases. Update an existing article rather than making a duplicate.
- **An article needs at least one sourced fact.** Anything mentioned but not yet known stays an unresolved `[[link]]`, which marks a gap to fill later.
- **Record only what a source says.** Never write an inference as a fact.
- **After any change,** update `index.md` if an article was added, renamed, or removed, and add a line to `log.md`.
- **Conflicting information:** keep both claims, each with its date and footnote. Never delete the older claim.
  - A **correction** (the owner says an earlier fact was wrong) or a **change over time** (both were true at their dates): mark which is current and continue silently.
  - A **real disagreement** (two sources the owner would have to settle): keep both and flag it to the owner.
- **No em dashes** in anything written to this vault. <DELETE THIS RULE IF THE OWNER DOES NOT WANT IT.>

## Life areas

Used to decide whether a new link is a cross-domain connection worth telling the owner about. Judge each article's area from what it is about.

<!-- Replace with the owner's approved list. -->

- Work and career
- Family and home
- Health and fitness
- Hobbies
- Learning and ideas

## Capture

Agents capture durable information into this vault as it comes up, using the `capture` skill in `.claude/skills/capture/`. The skill holds the procedure. This README holds the rules it follows.

- **Durable** means likely to still be true or useful a month from now: people, pets, places, preferences, decisions, goals, projects, possessions, plans, events, and research findings with sources.
- **Not durable:** passing task chatter, anything the Scope section excludes, and credentials of any kind.
- **Tell the owner** with one line at the end of the reply, and only for: a new article, a cross-domain connection (a new link between articles in different life areas), or a real disagreement. Everything else is silent.
- **Scope terms** that the check script watches for, and the files allowed to mention them, are in `.claude/scope.txt`.
- **Commit identity:** every commit must be authored as the owner, or cloud sessions lose the right to push to `main`. Before committing, if `git config user.email` is not the address below, set it for this repo:
  - `git config user.name "<OWNER GIT NAME>"`
  - `git config user.email "<OWNER GITHUB NOREPLY EMAIL>"`
- **Cloud and phone sessions:** open them on this repo. A cloud session only sees the repo it was opened on and can only push to that repo, so a session opened on any other repo can't read or save to the vault. Laptop sessions find the vault through the global `CLAUDE.md` wherever they're opened.

## Maintenance

Capture adds facts as they come up, so the vault drifts. When the owner asks for a lint pass, check for and fix:

- claims with no footnote, including summary lines
- research that may be out of date (check the source's date and look for newer information)
- conflicting claims that were never flagged
- orphan articles that nothing links to
- unresolved links that now have enough sourced facts to become articles
- anything the Scope section excludes
- leftover `claude/...` branches on GitHub from cloud sessions. Delete a branch only if `git rev-list --count origin/main..origin/<branch>` prints `0`, meaning `main` already has all its commits. Cloud sessions can't delete these themselves.

Report what changed with one line per article, and stay silent on anything that was already fine.

## Sync

The Obsidian Git plugin pulls on startup, and pulls, commits, and pushes every 10 minutes. Agents writing outside Obsidian pull with rebase right before committing, run the check script, then push straight to `main`. If a rebase conflicts, stop and flag it rather than forcing it.
