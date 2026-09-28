# Claude personal vault

Build your own personal knowledge vault that Claude and your other agents can read and grow: a private, git-backed Obsidian vault of the people, projects, preferences, and ideas in your life, linked together and cited.

Claude walks you through the whole build in Claude Code, one step and one question at a time.

## Start

Open Claude Code and paste:

```text
Build my personal vault using https://github.com/delharp231/claude-personal-vault. Clone it, read SETUP.md, and walk me through it step by step.
```

## What you get

- **A private GitHub repo that is also an Obsidian vault.** Browse it in Obsidian; every change is in git history and can be rolled back.
- **Your own design.** Claude interviews you to settle the article template, the kinds of things you track, how they link, and what stays out.
- **A seeded vault**, built from what already exists: your Claude memory, your Claude Code and Cowork conversations, your GitHub repos, and a short interview. Every fact is cited to where it came from.
- **Always-on capture.** When something worth remembering comes up in any Claude Code session, on your desktop or in the Claude app's Code tab on your phone, Claude saves it to the vault on its own and tells you only about new articles, connections across different areas of your life, and conflicting information.
- **Context in every session.** On your computer, each new Claude Code session syncs the vault and starts with its index loaded, then opens full articles only when the conversation needs them.
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
| `template/` | Starting files for your vault, including the capture skill and check script |
| `reference/` | The research the design is based on: personal knowledge management, ontologies, and agent-readable markdown |
| `tools/extract_messages.py` | Pulls your own messages out of Claude transcripts for seeding |

## Privacy

Your vault is private and lives in your own GitHub account. Nothing from it comes back to this repo. The build asks before saving anything sensitive, such as health, family, or finances, and helps you set firm rules for anything that must never go in, like your employer's internal details.

## License

MIT. See `LICENSE`.
