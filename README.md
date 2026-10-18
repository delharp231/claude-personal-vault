# Claude personal vault

Build your own personal knowledge vault that Claude and your other agents can read and grow: a private, git-backed Obsidian vault of the people, projects, preferences, and ideas in your life, linked together and cited.

Your agent walks you through the whole build, one step and one question at a time. Setup is wired for Claude Code. Codex CLI and Gemini CLI can read the finished vault through its `AGENTS.md`.

**Agents:** if a person gave you this link, they want you to build their vault. Clone this repo, read `SETUP.md`, and follow it.

## Start

Open your agent and paste this link:

```text
https://github.com/delharp231/claude-personal-vault
```

If your agent doesn't act on the link alone, paste this instead:

```text
Build my personal vault using https://github.com/delharp231/claude-personal-vault. Clone it, read SETUP.md, and walk me through it step by step.
```

## What you get

- **A private GitHub repo that is also an Obsidian vault.** Browse it in Obsidian; every change is in git history and can be rolled back.
- **Your own design.** Claude interviews you to settle the article template, the kinds of things you track, how they link, and what stays out.
- **A seeded vault**, built from what already exists: your Claude memory, memory from other AI assistants, your Claude Code and Cowork conversations, your GitHub repos, and a short interview. Every fact is cited to where it came from, and the memory you seeded from is kept as a read-only archive so those citations keep working.
- **Always-on capture.** When something worth remembering comes up in any Claude Code session, on your desktop or in the Claude app's Code tab on your phone, Claude saves it to the vault on its own and tells you only about new articles, connections across different areas of your life, and conflicting information.
- **Context in every session.** On your computer, each new Claude Code session syncs the vault and loads a short always-on context: a rules digest, your topic list, and your core preferences. Other preferences load when a prompt or tool call matches their triggers. Full articles open only when the conversation needs them.
- **A generated index.** `index.md` and `catalog.md` are built from your articles' topics, so they never drift from the vault. Agents find things through topic hubs, not by scanning everything.
- **One home for what your agents know about you.** The vault replaces your assistant's private memory, and its instructions live in a plain `AGENTS.md` that other agent tools, such as Codex CLI or Gemini CLI, can read too. Switch models or tools and your context comes with you.
- **A safety check** that runs before every commit and blocks broken formatting or anything you have ruled out of scope.

## What you need

- A GitHub account, with the GitHub CLI (`gh`) installed and signed in
- Git
- [Obsidian](https://obsidian.md)
- Claude Code on a plan that includes cloud sessions, if you want to capture from your phone. Phone sessions must be opened on your vault repo.

Plan for a few hours, spread across as many sittings as you like. Each step ends with a checkpoint for your approval.

## What's in this repo

| Path | What it is |
| --- | --- |
| `SETUP.md` | The step-by-step guide Claude follows |
| `template/` | Starting files for your vault, including the capture skill, check engine, index builder, and preference loader |
| `reference/` | The research the design is based on: personal knowledge management, ontologies, and agent-readable markdown |
| `tools/extract_messages.py` | Pulls your own messages out of Claude transcripts for seeding |

## Privacy

Your vault is private and lives in your own GitHub account. Nothing from it comes back to this repo. The build asks before saving anything sensitive, such as health, family, or finances, and helps you set firm rules for anything that must never go in, like your employer's internal details.

## License

MIT. See `LICENSE`.
