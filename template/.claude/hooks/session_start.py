"""SessionStart hook: refresh the vault, then load the small always-on context.

Claude Code adds whatever this prints to the start of the session. pref_loader.session_text()
prints the rules digest, the topic hubs, and the core Preferences; the rest of the Preferences
load on demand through the UserPromptSubmit and PreToolUse hooks (see pref_loader.py). Agents
open individual articles only when the conversation needs them.

Safe by design: the pull is fast-forward only, so it never merges, rebases, or leaves
a conflict behind. Any failure (offline, local commits not yet pushed) is skipped and
the session starts with whatever is on disk. If the loader fails, the fallback is to print
the root index and ask for every Preference to be read.
"""
import pathlib
import subprocess
import sys

VAULT = pathlib.Path(__file__).resolve().parents[2]

try:
    subprocess.run(
        ["git", "-C", str(VAULT), "pull", "--ff-only", "-q"],
        capture_output=True, timeout=15,
    )
except Exception:
    pass

sys.stdout.reconfigure(encoding="utf-8")
try:
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import pref_loader

    text = pref_loader.session_text()
    print(f"Personal knowledge vault at {VAULT} (synced at session start).\n")
    print(text)
except Exception:
    index = VAULT / "index.md"
    if index.exists():
        print(f"Personal knowledge vault at {VAULT}. Read every article in Preferences/ before acting.\n")
        print(index.read_text(encoding="utf-8"))
