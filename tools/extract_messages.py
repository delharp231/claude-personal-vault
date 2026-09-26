"""Extract only the owner's own typed messages from Claude Code and Cowork transcripts.

Usage: python extract_messages.py <output-folder> [--cap 1500] [--skip <session-id> ...]

Writes one markdown file per surface (claude-code, cowork), sessions sorted by date,
each with the owner's messages in order. Skips scheduled-task runs, tool results,
system wrappers, and subagent sidechains. Messages longer than --cap characters
(usually pasted documents) are cut to their first 600 characters so the output
stays small enough to read. Standard library only.
"""
import argparse
import glob
import json
import os
import re

SOURCES = {
    "claude-code": os.path.expanduser("~/.claude/projects/*/*.jsonl"),
    "cowork": os.path.join(os.environ.get("APPDATA", os.path.expanduser("~/Library/Application Support")),
                           "Claude", "local-agent-mode-sessions", "**", "*.jsonl"),
}
SKIP_PREFIXES = ("<scheduled-task", "<command-", "<local-command", "Caveat:")


def text_of(content):
    if isinstance(content, str):
        return content
    return "\n".join(c.get("text", "") for c in content or [] if isinstance(c, dict) and c.get("type") == "text")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--cap", type=int, default=1500)
    ap.add_argument("--skip", nargs="*", default=[], help="session IDs to leave out")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    for surface, pattern in SOURCES.items():
        sessions = []
        for path in glob.glob(pattern, recursive=True):
            sid = os.path.splitext(os.path.basename(path))[0]
            if sid in args.skip or "subagents" in path.replace("\\", "/"):
                continue
            msgs, first_ts, seen = [], None, set()
            with open(path, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    try:
                        r = json.loads(line)
                    except ValueError:
                        continue
                    if r.get("type") != "user" or r.get("isSidechain"):
                        continue
                    if (r.get("origin") or {}).get("kind") not in (None, "human"):
                        continue
                    t = text_of((r.get("message") or {}).get("content")).strip()
                    t = re.sub(r"<system-reminder>.*?</system-reminder>", "", t, flags=re.S).strip()
                    if not t or t.startswith(SKIP_PREFIXES) or "tool_use_id" in t or t in seen:
                        continue
                    seen.add(t)
                    if len(t) > args.cap:
                        t = t[:600] + f" [...cut, {len(t)} characters total]"
                    first_ts = first_ts or r.get("timestamp", "")
                    msgs.append(t)
            if msgs:
                sessions.append((first_ts[:10], sid, msgs))
        sessions.sort()
        out = os.path.join(args.out, f"messages_{surface}.md")
        with open(out, "w", encoding="utf-8") as fh:
            for date, sid, msgs in sessions:
                fh.write(f"\n## {date} | {sid}\n\n")
                for m in msgs:
                    fh.write("- " + m.replace("\n", "\n  ") + "\n")
        print(f"{surface}: {len(sessions)} sessions, {sum(len(s[2]) for s in sessions)} messages -> {out}")


if __name__ == "__main__":
    main()
