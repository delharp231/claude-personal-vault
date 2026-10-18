"""The basic structure checks: placeholders, empty notes, root notes, dashes, scope terms, and frontmatter shape.

index.md and catalog.md are generated, so rules/topics.py checks them instead of this module. A crash in one of
these rules is an error, not a warning.
"""
import os
import re

from rules import rule

SPECIAL = {"README.md", "index.md", "catalog.md", "log.md", "CLAUDE.md", "AGENTS.md"}
FIELD = re.compile(r"^[a-z_]+:( .*)?$")
ITEM = re.compile(r"^  - .+$")
PLACEHOLDER = re.compile(r"<[A-Z][A-Z ]{3,}|<!-- Setup:")


def _subfolder_notes(ctx):
    """Notes in a folder whose name is not one of the root files: the ones that get frontmatter and index checks."""
    return [r for r in ctx.filled if "/" in r and os.path.basename(r) not in SPECIAL]


def _frontmatter_lines(text):
    """(lines, end) of the frontmatter, or None when it is missing or never closed."""
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return None
    lines = text.splitlines()
    try:
        return lines, lines.index("---", 1)
    except ValueError:
        return None


@rule("legacy-placeholder", dimension="legacy")
def placeholder(ctx):
    for rel in ("README.md", "CLAUDE.md"):
        if rel in ctx.notes:
            for n, line in enumerate(ctx.read(rel).splitlines(), start=1):
                if PLACEHOLDER.search(line):
                    yield rel, f"{rel}:{n}: unfilled setup placeholder: {line.strip()[:80]}", n


@rule("legacy-empty", dimension="legacy")
def empty(ctx):
    for rel in ctx.notes:
        if not ctx.read(rel).strip():
            yield rel, f"{rel}: empty note (often made by clicking an unresolved link in Obsidian)"


@rule("legacy-root", dimension="legacy")
def root_note(ctx):
    for rel in ctx.filled:
        if "/" not in rel and rel not in SPECIAL:
            yield rel, f"{rel}: note in the vault root; move it into its type folder"


@rule("legacy-dash", dimension="legacy")
def dash(ctx):
    for rel in ctx.filled:
        text = ctx.read(rel)
        if "—" in text or "–" in text:
            yield rel, f"{rel}: contains an em or en dash"


@rule("legacy-scope", dimension="legacy")
def scope(ctx):
    for rel in ctx.filled:
        lower = ctx.read(rel).lower()
        for term, allowed in ctx.scope:
            if term in lower and rel not in allowed:
                yield rel, f"{rel}: mentions scope term '{term}' outside its allowed files"


@rule("legacy-frontmatter", dimension="legacy")
def frontmatter_shape(ctx):
    for rel in _subfolder_notes(ctx):
        text = ctx.read(rel)
        if not text.startswith("---\n") and not text.startswith("---\r\n"):
            yield rel, f"{rel}: missing frontmatter"
            continue
        fm = _frontmatter_lines(text)
        if fm is None:
            yield rel, f"{rel}: frontmatter is never closed with ---"
            continue
        lines, end = fm
        for n, line in enumerate(lines[1:end], start=2):
            if not (FIELD.match(line) or ITEM.match(line)):
                yield rel, f"{rel}:{n}: frontmatter line is not 'field: value' or '  - item': {line!r}", n


@rule("legacy-quoted-link", dimension="legacy")
def quoted_link(ctx):
    for rel in _subfolder_notes(ctx):
        fm = _frontmatter_lines(ctx.read(rel))
        if fm:
            lines, end = fm
            for n, line in enumerate(lines[1:end], start=2):
                if "[[" in line and not re.search(r'"\[\[[^\]]+\]\]"', line):
                    yield rel, f"{rel}:{n}: wikilink in frontmatter must be in quotes", n


@rule("legacy-type", dimension="legacy")
def has_type(ctx):
    for rel in _subfolder_notes(ctx):
        fm = _frontmatter_lines(ctx.read(rel))
        if fm:
            lines, end = fm
            if not any(l.startswith("type:") for l in lines[1:end]):
                yield rel, f"{rel}: frontmatter has no type field"


ARTICLE = "---\ntype: person\ncaptured_from: test\n---\n\n# A\n\nA person.[^1]\n\n[^1]: test.\n"
BASE = {"index.md": "# Index\n\n- [[A]]\n", "People/A.md": ARTICLE}

FIXTURES = [
    ("clean vault", BASE, set()),
    ("setup placeholder in README", {**BASE, "README.md": "Owner: <YOUR NAME>\n"}, {"legacy-placeholder"}),
    ("empty note", {**BASE, "People/E.md": "   \n"}, {"legacy-empty"}),
    ("note in the root", {**BASE, "Stray.md": "# Stray\n"}, {"legacy-root"}),
    ("em dash", {**BASE, "People/A.md": ARTICLE.replace("A person.", "A person — here.")}, {"legacy-dash"}),
    ("scope term", {**BASE, ".claude/scope.txt": "secretco |\n", "People/A.md": ARTICLE.replace("A person.", "Works at SecretCo.")}, {"legacy-scope"}),
    ("missing frontmatter", {**BASE, "People/A.md": "# A\n\nNo frontmatter.\n"}, {"legacy-frontmatter"}),
    ("bad frontmatter line", {**BASE, "People/A.md": ARTICLE.replace("captured_from: test", "Captured From: test")}, {"legacy-frontmatter"}),
    ("unquoted frontmatter link", {**BASE, "People/A.md": ARTICLE.replace("captured_from: test", "related: [[B]]")}, {"legacy-quoted-link"}),
    ("no type field", {**BASE, "People/A.md": ARTICLE.replace("type: person\n", "")}, {"legacy-type"}),
    ("catalog.md is a root file", {**BASE, "catalog.md": "# Catalog\n"}, set()),
]
