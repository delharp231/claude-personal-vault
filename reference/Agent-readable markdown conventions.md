---
type: concept
aliases:
  - LLM wiki
related:
  - "[[Personal knowledge management practice]]"
  - "[[Formal ontologies and knowledge graphs]]"
captured_from: research, Claude Code, 2026-09-26
created: 2026-09-26
updated: 2026-09-26
---

# Agent-readable markdown conventions

How to structure markdown so agents can navigate it: frontmatter, wikilinks, index notes, and Karpathy's LLM Wiki pattern.

## Summary

An agent reading this vault faces the same problem a new person would: where do I start, and how do I find the right note without reading everything? The sources below agree on the answer:

- plain markdown,
- a small amount of structured metadata at the top of each file,
- names and links that stay stable,
- an index to read first.

## Frontmatter (Obsidian properties)

Obsidian stores structured fields as YAML frontmatter between `---` lines at the top of a note, written as `name: value`.[^props] It supports six types: text, list, number, checkbox, date, and date & time.[^props]

Details that matter for an agent-written vault:[^props]

- Built-in properties are `tags`, `aliases`, and `cssclasses`. `aliases` lets one note answer to several names.
- Properties can hold links, but "internal links in text properties must be surrounded with quotes": `related: "[[Some note]]"`. An agent that forgets the quotes produces a broken link.
- Nested properties are not supported in the normal view. Obsidian says properties "are meant for small, atomic bits of information." That argues for a flat set of fields.

## Wikilinks and backlinks

A wikilink, `[[Note name]]`, links notes by title. Obsidian shows the reverse direction automatically as backlinks, so a link written once is visible from both ends. For an agent this has a cost: renaming a note breaks links written by any tool that is not Obsidian. That is one reason [[Personal knowledge management practice]] stresses fixed note addresses.

## Index notes

Karpathy's LLM Wiki pattern (April 2026) is the closest match to what this vault is trying to be.[^karpathy] Its structure:

- **Raw sources**, kept unchanged, as the source of truth.
- **The wiki:** markdown pages the LLM writes and maintains (summaries, entity pages, concept pages).
- **A schema file** (like `CLAUDE.md`) that "tells the LLM how the wiki is structured."
- **`index.md`:** a catalog of every page, updated on each change. The agent reads it first to find relevant pages.
- **`log.md`:** an append-only record of what changed and when.

It also has three operations:

- **ingest:** a new source typically touches 10 to 15 pages.
- **query:** answers cite wiki pages, and good answers become new pages.
- **lint:** a periodic check for contradictions, stale claims, orphan pages, and missing links.

Karpathy's key observation is that the tedious part of keeping a knowledge base is not the reading or the thinking. It is the bookkeeping, and LLMs are good at bookkeeping.[^karpathy]

The llms.txt proposal (Jeremy Howard, 2024) makes the same bet for websites. It holds that "the most widely and easily understood format for language models is Markdown" and proposes a single index file: an H1 name, a one-paragraph summary, then lists of links with short descriptions.[^llmstxt]

## How agents actually use files

Anthropic's context-engineering guidance explains why these conventions work.[^context] Agents keep "lightweight identifiers (file paths, stored queries, web links, etc.)" and load content only when they need it. Folder names, file names, and timestamps act as signals about what a file is for. Agents also work by "progressive disclosure": each file read tells them what to read next.[^context]

The same article describes "structured note-taking," where "the agent regularly writes notes persisted to memory outside of the context window."[^context] A vault capture skill is this pattern made permanent and shared.

## What this means for the vault

These are options for the design decisions, not conclusions:

- **An index note is the entry point every source recommends.** For an agent, it is the difference between reading one file and reading everything.
- **A schema or README file tells agents the rules.** Karpathy's pattern suggests writing it early, because a capture skill will need it.
- **A change log gives agents recent context cheaply.** Git history holds the same information, but a log note is readable from the phone without git.
- **Frontmatter should stay flat and small.** Links in properties need quotes.
- **A periodic lint pass is the maintenance answer** for contradictions and orphan notes, which also covers how to handle conflicting information.
- **Karpathy's model makes one choice worth questioning.** He keeps raw sources as separate, unchanged files. The alternative is keeping citations inside each article. That is a real choice for the seeding decision.

## Sources

[^props]: Obsidian, "Properties," Obsidian Help. https://obsidian.md/help/properties (accessed 2026-09-26).
[^karpathy]: Andrej Karpathy, "llm-wiki," GitHub Gist, April 4, 2026. https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f (accessed 2026-09-26).
[^llmstxt]: Jeremy Howard, "The /llms.txt file," llmstxt.org, September 3, 2024. https://llmstxt.org/ (accessed 2026-09-26).
[^context]: Anthropic Applied AI team, "Effective context engineering for AI agents," Anthropic Engineering, September 29, 2025. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (accessed 2026-09-26).
