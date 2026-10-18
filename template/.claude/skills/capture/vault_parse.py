"""Shared parser for the vault's own tools: check.py and build_index.py.

One parser, so the check and the builder cannot drift apart. Standard library only, no network, so it runs in every
place capture runs.
"""
import os
import re

SKIP_DIRS = {".git", ".obsidian", ".claude", ".trash", "archive"}
ROOT_FILES = {"README.md", "index.md", "catalog.md", "log.md", "CLAUDE.md", "AGENTS.md"}

KEY = re.compile(r"^([A-Za-z_]+):[ \t]*(.*)$")
ITEM = re.compile(r"^\s+-\s+(.*)$")
LINK = re.compile(r"\[\[([^\]|#]+)")
CODE = re.compile(r"```.*?```|`[^`\n]+`", re.S)
FOOTNOTE_DEF = re.compile(r"^\[\^([^\]]+)\]:[ \t]*(.*)$", re.M)
FOOTNOTE_REF = re.compile(r"\[\^([^\]]+)\](?!:)")

FOLDER_TYPES = {
    "People": "person", "Organizations": "organization", "Places": "place", "Events": "event", "Concepts": "concept",
    "Tools": "tool", "Creative works": "creative work", "Hobbies": "hobby", "Animals": "animal", "Pets": "pet",
    "Goals": "goal", "Preferences": "preference", "Sources": "source", "Reviews": "review",
}


def notes(root):
    """Every .md file under the root, as a sorted list of '/'-separated relative paths, skipping tool folders."""
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.endswith(".md"):
                out.append(os.path.relpath(os.path.join(dirpath, name), root).replace("\\", "/"))
    return sorted(out)


def is_article(rel):
    """An article: one folder deep, .md, not in a skipped or hidden folder."""
    parts = rel.split("/")
    return len(parts) == 2 and parts[1].endswith(".md") and parts[0] not in SKIP_DIRS and not parts[0].startswith(".")


def read(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as fh:
        return fh.read()


def unquote(s):
    s = s.strip()
    return s[1:-1] if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'" else s


def frontmatter(text):
    """(fields, body). A field holds a string, or a list when list items follow it. CRLF reads the same as LF."""
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end < 0:
        return {}, text
    data, key = {}, None
    for line in text[4:end].split("\n"):
        m = KEY.match(line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            data[key] = unquote(val) if val else []
        elif key and ITEM.match(line):
            if not isinstance(data[key], list):
                data[key] = [data[key]] if data[key] else []
            data[key].append(unquote(ITEM.match(line).group(1)))
    return data, text[end + 4:]


parse_frontmatter = frontmatter   # the name build_index.py imports


def links(value):
    """Wikilink targets in a frontmatter value, whether it holds a string or a list."""
    v = value or []
    return [l.strip() for x in ([v] if isinstance(v, str) else v) for l in LINK.findall(x)]


def wikilinks(text):
    """Wikilink targets in text, skipping code spans and blocks, where links are examples."""
    return [l.strip() for l in LINK.findall(CODE.sub("", text))]


def footnotes(body):
    """(reference ids in order, {definition id: text})."""
    defs = dict(FOOTNOTE_DEF.findall(body))
    refs = [m.group(1) for m in FOOTNOTE_REF.finditer(body) if not body[m.end():m.end() + 1] == ":"]
    return refs, defs


def clean(line):
    """A body line as display text: no footnote markers, no bullet."""
    return re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", re.sub(r"\[\^[^\]]+\](?!:)", "", line)).strip()


def summary_line(body):
    """The first paragraph line after the article's H1, or None if a heading comes first."""
    lines = body.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            for nxt in lines[i + 1:]:
                if nxt.strip():
                    return None if nxt.startswith("#") else clean(nxt)
    return None


def folder_type(rel):
    """The `type` an article's folder implies, or None for a folder the README does not define."""
    return FOLDER_TYPES.get(rel.split("/")[0]) if "/" in rel else None
