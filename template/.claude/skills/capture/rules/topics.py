"""Topic rules and the generated index.

Every article except hubs and reviews names 1 to 3 hubs in `topics`; hubs take no topics; `in_scheme` is exactly
"[[Vault topics]]"; the scheme article exists; index.md and catalog.md match what build_index.py would write; and the
root stays inside its character budget.
"""
import os
import tempfile

import build_index
from rules import rule

SCHEME = build_index.SCHEME


def _view(ctx):
    """The builder's view of the vault, loaded once per check run."""
    if not hasattr(ctx, "_topics_view"):
        ctx._topics_view = build_index.load(ctx.root)["articles"]
    return ctx._topics_view


def _rel(title, a):
    return f"{a['folder']}/{title}.md"


@rule("topics-scheme")
def scheme_exists(ctx):
    if SCHEME not in _view(ctx):
        yield "", f"{SCHEME}.md is missing: the topic scheme article must exist"


@rule("topics-in-scheme")
def in_scheme_value(ctx):
    for title, a in sorted(_view(ctx).items()):
        if a["in_scheme"] and a["in_scheme"] != [SCHEME]:
            yield _rel(title, a), f'{_rel(title, a)}: in_scheme must be exactly "[[{SCHEME}]]"'


@rule("topics-hub-topics")
def hub_has_no_topics(ctx):
    arts = _view(ctx)
    for title in build_index.hubs(arts):
        if arts[title]["topics"]:
            yield _rel(title, arts[title]), f"{_rel(title, arts[title])}: a hub takes no topics"


@rule("topics-count")
def topic_count(ctx):
    arts = _view(ctx)
    hubs = set(build_index.hubs(arts))
    for title, a in sorted(arts.items()):
        if a["review"] or title in hubs:
            continue
        if not 1 <= len(a["topics"]) <= 3:
            yield _rel(title, a), (f"{_rel(title, a)}: needs 1 to 3 topics (has {len(a['topics'])}); "
                                   "pick hubs from the Topics list in index.md")


@rule("topics-not-hub")
def topics_are_hubs(ctx):
    arts = _view(ctx)
    hubs = set(build_index.hubs(arts))
    for title, a in sorted(arts.items()):
        if a["review"] or title in hubs:
            continue
        for t in a["topics"]:
            if t not in hubs:
                yield _rel(title, a), f"{_rel(title, a)}: topics value [[{t}]] is not a hub"


@rule("index-stale")
def generated_current(ctx):
    stale, _ = build_index.build(ctx.root, check=True)
    for name in stale:
        yield name, f"{name}: out of date; run build_index.py"


@rule("index-budget")
def root_budget(ctx):
    _, out = build_index.build(ctx.root, check=True)
    n = len(out["index.md"])
    if n > build_index.ROOT_BUDGET:
        yield "index.md", (f"index.md: {n} characters, over the {build_index.ROOT_BUDGET} budget; "
                           "merge hubs, shorten summaries, or turn on nesting")


HUB = '---\ntype: goal\nin_scheme: "[[Vault topics]]"\n---\n\n# Hub A\n\nThe first hub.\n'
SCHEME_ART = '---\ntype: creative work\ntopics:\n  - "[[Hub A]]"\n---\n\n# Vault topics\n\nThe list.\n'
NOTE = '---\ntype: concept\ntopics:\n  - "[[Hub A]]"\n---\n\n# Note\n\nA note.\n'
PREF = '---\ntype: preference\ntopics:\n  - "[[Hub A]]"\n---\n\n# Pref\n\nA rule.\n'
BASE = {"log.md": "# Log\n", "Goals/Hub A.md": HUB, "Creative works/Vault topics.md": SCHEME_ART,
        "Concepts/Note.md": NOTE, "Preferences/Pref.md": PREF}


def _generated(files):
    """The files plus the index.md and catalog.md the builder writes for them, so a fixture is otherwise current."""
    with tempfile.TemporaryDirectory() as tmp:
        for rel, text in files.items():
            p = os.path.join(tmp, *rel.split("/"))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8", newline="") as fh:
                fh.write(text)
        _, out = build_index.build(tmp)
    return {**files, **out}


def _many_prefs(n):
    return {f"Preferences/A deliberately long preference title for the budget test number {i:03d}.md": PREF for i in range(n)}


FIXTURES = [
    ("clean vault", _generated(BASE), set()),
    ("generated files missing", BASE, {"index-stale"}),
    ("scheme article missing", _generated({k: v for k, v in BASE.items() if k != "Creative works/Vault topics.md"}), {"topics-scheme"}),
    ("in_scheme with another value", _generated({**BASE, "Concepts/Note.md": NOTE.replace("type: concept\n", 'type: concept\nin_scheme: "[[Other]]"\n')}), {"topics-in-scheme"}),
    ("hub with topics", _generated({**BASE, "Goals/Hub A.md": HUB.replace("---\n\n#", 'topics:\n  - "[[Hub A]]"\n---\n\n#', 1)}), {"topics-hub-topics"}),
    ("article without topics", _generated({**BASE, "Concepts/Note.md": NOTE.replace('topics:\n  - "[[Hub A]]"\n', "")}), {"topics-count"}),
    ("topic that is not a hub", _generated({**BASE, "Preferences/Pref.md": PREF.replace("[[Hub A]]", "[[Note]]")}), {"topics-not-hub"}),
    ("root over budget", _generated({**BASE, **_many_prefs(120)}), {"index-budget"}),
]
