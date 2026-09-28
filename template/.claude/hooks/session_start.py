"""SessionStart hook: refresh the vault, then load its index as session context.

Claude Code adds whatever this prints to the start of the session. The index is the
"basics": a one-line map of every article. Agents open individual articles only when
the conversation needs them.

Safe by design: the pull is fast-forward only, so it never merges, rebases, or leaves
a conflict behind. Any failure (offline, local commits not yet pushed) is skipped and
the session starts with whatever is on disk.
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

index = VAULT / "index.md"
if index.exists():
    sys.stdout.reconfigure(encoding="utf-8")
    print(
        f"Personal knowledge vault at {VAULT} (synced at session start). "
        "Below is its index: a one-line summary of every article. Use it to decide "
        "which articles to open, and read an article only when the conversation needs "
        "it. Rules for writing are in the vault's README.md.\n"
    )
    print(index.read_text(encoding="utf-8"))
