"""Pre-commit check for a personal ontology vault.

Run from anywhere: python check.py [vault_root]
Exits 1 and prints every problem if the vault breaks a rule; exits 0 when clean.
Standard library only, so it runs on any machine or cloud session.
"""
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "..", ".."))
SKIP_DIRS = {".git", ".obsidian", ".claude", ".trash"}
SPECIAL = {"README.md", "index.md", "log.md", "CLAUDE.md"}
FIELD = re.compile(r"^[a-z_]+:( .*)?$")
ITEM = re.compile(r"^  - .+$")
problems = []


def notes():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.endswith(".md"):
                yield os.path.relpath(os.path.join(dirpath, name), ROOT).replace("\\", "/")


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def check_frontmatter(rel, text):
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        problems.append(f"{rel}: missing frontmatter")
        return
    lines = text.splitlines()
    try:
        end = lines.index("---", 1)
    except ValueError:
        problems.append(f"{rel}: frontmatter is never closed with ---")
        return
    for n, line in enumerate(lines[1:end], start=2):
        if not (FIELD.match(line) or ITEM.match(line)):
            problems.append(f"{rel}:{n}: frontmatter line is not 'field: value' or '  - item': {line!r}")
        if "[[" in line and not re.search(r'"\[\[[^\]]+\]\]"', line):
            problems.append(f"{rel}:{n}: wikilink in frontmatter must be in quotes")
    if not any(l.startswith("type:") for l in lines[1:end]):
        problems.append(f"{rel}: frontmatter has no type field")


def load_scope():
    path = os.path.join(ROOT, ".claude", "scope.txt")
    rules = []
    if os.path.exists(path):
        for line in read(".claude/scope.txt").splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            term, _, allowed = line.partition("|")
            rules.append((term.strip().lower(), {a.strip() for a in allowed.split(",") if a.strip()}))
    return rules


all_notes = sorted(notes())
titles = {os.path.splitext(os.path.basename(r))[0] for r in all_notes}
index = read("index.md") if "index.md" in all_notes else ""
scope = load_scope()

for rel in all_notes:
    text = read(rel)
    if "—" in text or "–" in text:
        problems.append(f"{rel}: contains an em or en dash")
    lower = text.lower()
    for term, allowed in scope:
        if term in lower and rel not in allowed:
            problems.append(f"{rel}: mentions scope term '{term}' outside its allowed files")
    name = os.path.basename(rel)
    if "/" in rel and name not in SPECIAL:
        check_frontmatter(rel, text)
        title = os.path.splitext(name)[0]
        if f"[[{title}]]" not in index:
            problems.append(f"{rel}: not listed in index.md")

if problems:
    print("Vault check FAILED:")
    for p in problems:
        print(" -", p)
    sys.exit(1)
print(f"Vault check passed: {len(all_notes)} notes.")
