"""Preference frontmatter rules: the fields .claude/hooks/pref_loader.py reads must be well formed.

A mistyped tier or a regex that does not compile would make the loader skip a Preference without a sound, so the check
catches it before the commit.
"""
import re

from rules import rule
from vault_parse import frontmatter

TIERS = {"core", "pinned", "ondemand"}
TRIGGERS = {"trigger_prompt", "trigger_tool_names", "trigger_path", "trigger_cwd",
            "trigger_path_ext", "trigger_path_must", "trigger_path_not"}


def _prefs(ctx):
    for rel in ctx.filled:
        if rel.startswith("Preferences/") and rel.count("/") == 1:
            fm, _ = frontmatter(ctx.read(rel))
            yield rel, fm


@rule("pref-tier")
def tier_value(ctx):
    for rel, fm in _prefs(ctx):
        if "tier" in fm and fm["tier"] not in TIERS:
            yield rel, f"{rel}: tier must be one of core, pinned, ondemand (got {fm['tier']!r})"


@rule("pref-core-empty")
def core_loads_something(ctx):
    for rel, fm in _prefs(ctx):
        if fm.get("tier") == "core" and not fm.get("digest") and str(fm.get("full", "")).lower() != "true":
            yield rel, f"{rel}: a core Preference needs `full: true` or a `digest:` list, or it loads nothing every session"


@rule("pref-pinned-line")
def pinned_has_line(ctx):
    for rel, fm in _prefs(ctx):
        if fm.get("tier") == "pinned" and not (isinstance(fm.get("line"), str) and fm.get("line")):
            yield rel, f"{rel}: a pinned Preference needs a `line:` field"


@rule("pref-trigger-key")
def known_trigger_keys(ctx):
    for rel, fm in _prefs(ctx):
        for key in fm:
            if key.startswith("trigger_") and key not in TRIGGERS:
                yield rel, f"{rel}: unknown field {key}; the loader reads {', '.join(sorted(TRIGGERS))}"


@rule("pref-regex")
def regexes_compile(ctx):
    for rel, fm in _prefs(ctx):
        for key in sorted(TRIGGERS & set(fm)):
            value = fm[key]
            if not isinstance(value, str):
                yield rel, f"{rel}: {key} must be one regex on one line"
                continue
            try:
                re.compile(value)
            except re.error as e:
                yield rel, f"{rel}: {key} is not a valid regex: {e}"


def _pref(*lines):
    return "---\ntype: preference\n" + "".join(l + "\n" for l in lines) + "---\n\n# Pref\n\nA rule.\n"


FIXTURES = [
    ("clean preferences", {
        "Preferences/A.md": _pref("tier: core", "digest:", "  - A short rule."),
        "Preferences/B.md": _pref("tier: core", "full: true"),
        "Preferences/C.md": _pref("tier: pinned", "line: One sentence."),
        "Preferences/D.md": _pref("tier: ondemand", r"trigger_prompt: \b(recipes?|dinner)\b", r"trigger_tool_names: ^mcp__x__",
                                  r"trigger_path_ext: \.(md|txt)$", "trigger_path_must: (post|email)"),
        "Preferences/E.md": _pref("topics:", '  - "[[Hub A]]"'),
    }, set()),
    ("unknown tier", {"Preferences/A.md": _pref("tier: always")}, {"pref-tier"}),
    ("core loads nothing", {"Preferences/A.md": _pref("tier: core")}, {"pref-core-empty"}),
    ("pinned without a line", {"Preferences/A.md": _pref("tier: pinned")}, {"pref-pinned-line"}),
    ("mistyped trigger field", {"Preferences/A.md": _pref("trigger_promt: \\bfood\\b")}, {"pref-trigger-key"}),
    ("regex that does not compile", {"Preferences/A.md": _pref("trigger_prompt: \\b(food")}, {"pref-regex"}),
]
