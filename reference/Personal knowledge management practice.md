---
type: concept
aliases:
  - PKM
  - Second brain
related:
  - "[[Formal ontologies and knowledge graphs]]"
  - "[[Agent-readable markdown conventions]]"
captured_from: research, Claude Code, 2026-09-26
created: 2026-09-26
updated: 2026-09-26
---

# Personal knowledge management practice

The main traditions for organizing personal notes (PARA, Zettelkasten, evergreen notes, Maps of Content), researched to design this vault.

## Summary

Three traditions dominate personal knowledge management (PKM). They disagree mainly on one question: what should decide where a note lives?

- **Building a Second Brain and PARA** (Tiago Forte) organize by *actionability*: what you are working on now.
- **Zettelkasten** (Niklas Luhmann, as documented by zettelkasten.de) organizes by *connection*: small notes, each with a fixed address, linked to each other.
- **Evergreen notes** (Andy Matuschak) and **Maps of Content** (Nick Milo) sit closer to Zettelkasten: notes built around concepts, densely linked, with hub notes for navigation.

## Building a Second Brain and PARA

Forte defines a second brain as an "external, centralized, digital repository for the things you learn."[^basb] His premise is that "our brains are for having ideas, not storing them."[^basb]

The method is CODE:[^basb]

1. **Capture:** keep what resonates rather than everything.
2. **Organize:** sort by actionability using PARA.
3. **Distill:** summarize in layers so a future read takes seconds.
4. **Express:** turn what you collected into output.

PARA has four buckets:[^para]

| Bucket | Forte's definition |
| --- | --- |
| Projects | "short-term efforts ... that you take on with a certain goal in mind" |
| Areas | "important parts of your work and life that require ongoing attention" |
| Resources | topics you are interested in and learning about |
| Archives | "anything from the previous three categories that is no longer active" |

Items move over time. A finished project goes to Archives, and so does an area you no longer tend.[^para]

## Zettelkasten

zettelkasten.de describes the method as "a personal tool for thinking and writing" with "hypertextual features to make a web of thoughts possible."[^zk] Its core principles:

- **Unique identifiers.** Every note has a fixed address. Luhmann used branching numbers (1, 1a, 1a1). Digital systems often use timestamps.[^zk]
- **Atomicity.** "One knowledge building block per note."[^zk]
- **Connections over collection.** Links carry context, and knowledge grows from the relationships between notes.[^zk]
- **Structure notes.** Hub notes that act as entry points into a cluster.[^zk]

## Evergreen notes and Maps of Content

Matuschak's evergreen notes are atomic, concept-oriented, densely linked, and "associative over hierarchical."[^evergreen] Their purpose is better thinking, not better filing.[^evergreen]

Milo's Map of Content (MOC) is "a special type of note" that helps you "gather, develop, and navigate your ideas."[^moc] In practice an MOC is mostly a list of links to the notes in one cluster. It works like a table of contents that you keep current.

## Where the traditions agree and disagree

| Question | PARA | Zettelkasten / evergreen / MOC |
| --- | --- | --- |
| What decides placement? | Current goals | Meaning and links |
| Main structure | Folders | Links and hub notes |
| Unit of note | Whatever a project needs | One idea per note |
| Changes over time | Items move to Archives | Notes stay put; links grow |

## What this means for the vault

These are options for the design decisions, not conclusions:

- **PARA answers a different question than this vault asks.** PARA serves a person deciding what to act on. This vault serves agents looking up what is true about the owner's life. Actionability is a poor fit for facts about a pet or a hobby, which never become "done."
- **Atomicity and fixed addresses matter more for agents than for people.** An agent can only link reliably to a note whose name will not change.
- **Hub notes map directly to what agents need.** An MOC is an index an agent can read first. Karpathy's LLM wiki uses the same idea with an `index.md` (see [[Agent-readable markdown conventions]]).
- **Distill fits the capture skill.** Layered summaries let an agent read the top of an article and stop there.

## Sources

[^basb]: Tiago Forte, "Building a Second Brain: The Definitive Introductory Guide," Forte Labs, May 1, 2023 (updated November 23, 2023). https://fortelabs.com/blog/basboverview/ (accessed 2026-09-26).
[^para]: Tiago Forte, "The PARA Method: The Simple System for Organizing Your Digital Life in Seconds," Forte Labs, February 24, 2023. https://fortelabs.com/blog/para/ (accessed 2026-09-26).
[^zk]: Sascha Fast, "Introduction to the Zettelkasten Method," zettelkasten.de, October 27, 2020. https://zettelkasten.de/introduction/ (accessed 2026-09-26).
[^evergreen]: Andy Matuschak, "Evergreen notes," Andy's working notes. https://notes.andymatuschak.org/Evergreen_notes (accessed 2026-09-26).
[^moc]: Nick Milo, "Maps," LYT Blog (Linking Your Thinking). https://blog.linkingyourthinking.com/maps/ (accessed 2026-09-26).
