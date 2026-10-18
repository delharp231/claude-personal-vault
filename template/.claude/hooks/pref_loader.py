"""On-demand Preference loader. Plain Python, standard library only.

Modes (hook protocol: JSON on stdin, JSON on stdout):
  python pref_loader.py session   SessionStart: print the small always-loaded context
  python pref_loader.py prompt    UserPromptSubmit: inject Preferences whose triggers match the prompt
  python pref_loader.py tool      PreToolUse: inject Preferences tied to a tool call or file path

Each Preference in Preferences/ says how it loads in its own frontmatter, so this script holds nothing personal:

  tier: core | pinned | ondemand      core: always loaded; pinned: one line always; ondemand: title only (default)
  full: true                          core only: load the whole article every session instead of a digest
  digest:                             core only: bullet lines loaded every session
    - A short rule.
  line: One sentence.                 pinned only: the line loaded every session
  section: ## Rules                   load only this section of the article when a trigger fires
  trigger_prompt: \\b(word|other)\\b    regex; the article loads when a prompt matches it (case-insensitive)
  trigger_tool_names: ^SomeTool$      regex on the tool name
  trigger_path: regex                 regex on the file path a tool touches
  trigger_cwd: regex                  regex on the working directory
  trigger_path_ext: \\.(md|html)$      with trigger_path_must: Write/Edit of a file whose path matches both
  trigger_path_must: regex
  trigger_path_not: regex             paths that never trigger

Regexes are written raw, with no quotes. check.py validates these fields (rules/preferences.py).

Every injection carries a systemMessage ("Preferences loaded: ...") so the user can see it, and is appended to the
injection log. A flag file named pref_loader.off next to this script disables the hooks, and the SessionStart mode
then prints a pointer to read every Preference. Any error fails open.
"""
import json
import re
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
VAULT = HERE.parent.parent
PREFS = VAULT / "Preferences"
LOG = HERE / "pref_injections.log"
CAP = 12000  # max characters injected by one hook call

sys.dont_write_bytecode = True
sys.path.insert(0, str(VAULT / ".claude" / "skills" / "capture"))
try:
    from vault_parse import frontmatter
except Exception:   # fail open: no Preferences load, but the session still starts
    frontmatter = None

TIERS = ("core", "pinned", "ondemand")
TOOL_FIELDS = {"names": "trigger_tool_names", "path_ext": "trigger_path_ext", "path_must": "trigger_path_must",
               "path_not": "trigger_path_not", "path": "trigger_path", "cwd": "trigger_cwd"}


def as_list(v):
    return v if isinstance(v, list) else ([v] if v else [])


def load_config():
    """{title: config} read from every article in Preferences/."""
    config = {}
    if frontmatter is None or not PREFS.is_dir():
        return config
    for p in sorted(PREFS.glob("*.md")):
        fm, _ = frontmatter(p.read_text(encoding="utf-8"))
        tool = {k: fm[field] for k, field in TOOL_FIELDS.items() if isinstance(fm.get(field), str) and fm.get(field)}
        c = {"tier": fm["tier"] if fm.get("tier") in TIERS else "ondemand",
             "full": str(fm.get("full", "")).lower() == "true",
             "digest": [d for d in as_list(fm.get("digest")) if isinstance(d, str)],
             "line": fm["line"] if isinstance(fm.get("line"), str) else "",
             "section": fm["section"] if isinstance(fm.get("section"), str) else "",
             "prompt": fm["trigger_prompt"] if isinstance(fm.get("trigger_prompt"), str) else "",
             "tool": tool}
        config[p.stem] = c
    return config


def rules_digest():
    out = [f"Vault: {VAULT} (the owner's canonical context). Preferences load on demand by hook; titles below.",
           "- Responses stay grounded: state only what a source, file, or tool result supports, cite it, and label inference as inference.",
           "- Writing to the vault: read README.md first and follow the capture skill. Every claim gets a footnote citation, record only what a source says, no em dashes, search before creating.",
           "- Navigation: hubs -> articles. index.md lists hubs; catalog.md is the duplicate-check list. Open only what the task needs."]
    readme = VAULT / "README.md"
    if readme.exists():
        m = re.search(r"^- \*\*Out, always:\*\*\s*(.+)$", readme.read_text(encoding="utf-8"), flags=re.M)
        if m and not m.group(1).lstrip().startswith("<"):   # skip the template's unfilled placeholder
            out.insert(1, "- Out of scope, always: " + re.sub(r"\s+", " ", m.group(1)).strip()[:500])
    return "\n".join(out)


def strip(text, section=None):
    """Frontmatter, Sources footnotes, and [^x] markers removed; optionally one section only."""
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    text = re.split(r"\n## Sources\b", text)[0]
    if section:
        m = re.search(rf"^{re.escape(section)}\n(.*?)(?=^## |\Z)", text, flags=re.S | re.M)
        if m:
            title = re.search(r"^# .*$", text, flags=re.M)
            text = (title.group(0) + "\n\n" if title else "") + m.group(0)
    text = re.sub(r"\[\^[^\]]+\]", "", text)
    return text.strip()


def read_pref(name, section=None):
    return strip((PREFS / f"{name}.md").read_text(encoding="utf-8"), section)


def hub_lines():
    out = []
    idx = VAULT / "index.md"
    if not idx.exists():
        return out
    m = re.search(r"^## Topics\n\n(.*?)\n\n## ", idx.read_text(encoding="utf-8").replace("\r\n", "\n"), flags=re.S | re.M)
    for line in (m.group(1).splitlines() if m else []):
        mm = re.match(r"- \[\[(.+?)\]\] \((\d+)\): (.*)", line)
        if mm:
            out.append(f"{mm.group(1)} ({mm.group(2)})")
    return out


def session_text(config=None):
    if (HERE / "pref_loader.off").exists():
        return f"Vault: {VAULT}. Read README.md, index.md, and every article in Preferences/ before acting for the owner."
    config = load_config() if config is None else config
    L = [rules_digest(), "", "Topic hubs:"] + [f"- {h}" for h in hub_lines()]
    L += ["", "Preferences always in force:"]
    for name, c in config.items():
        if c["tier"] == "core":
            if c["full"]:
                L += ["", f"[{name}]", read_pref(name)]
            elif c["digest"]:
                L += [f"[{name}]"] + [f"- {d}" for d in c["digest"]]
    pinned = [c["line"] for c in config.values() if c["tier"] == "pinned" and c["line"]]
    if pinned:
        L += ["", "Pinned rules:"] + [f"- {x}" for x in pinned]
    od = [n for n, c in config.items() if c["tier"] in ("ondemand", "pinned") or (c["tier"] == "core" and c["prompt"])]
    if od:
        L += ["", "Loaded automatically when relevant (open the article yourself if a hook did not and the task fits): " + "; ".join(od) + "."]
    if not config:
        L += ["", "(No Preferences yet. When the owner states how they want things done, capture it as an article in Preferences/.)"]
    return "\n".join(L)


def match_prompt(prompt, config):
    return [name for name, c in config.items() if c["prompt"] and re.search(c["prompt"], prompt, flags=re.I)]


def match_tool(tool_name, tool_input, cwd, config):
    hits = []
    path = ""
    if isinstance(tool_input, dict):
        path = str(tool_input.get("file_path") or tool_input.get("path") or tool_input.get("notebook_path") or "")
    for name, c in config.items():
        t = c["tool"]
        if not t:
            continue
        ok = False
        if t.get("names") and re.search(t["names"], tool_name or ""):
            ok = True
        if not ok and t.get("path_ext") and tool_name in ("Write", "Edit", "NotebookEdit") and path:
            if (re.search(t["path_ext"], path, flags=re.I) and re.search(t.get("path_must", ""), path, flags=re.I)
                    and not re.search(t.get("path_not", r"$^"), path, flags=re.I)):
                ok = True
        if not ok and t.get("path") and path and re.search(t["path"], path, flags=re.I) \
                and not re.search(t.get("path_not", r"$^"), path, flags=re.I):
            ok = True
        if not ok and t.get("cwd") and cwd and re.search(t["cwd"], cwd, flags=re.I) \
                and not re.search(t.get("path_not", r"$^"), cwd, flags=re.I):
            ok = True
        if ok:
            hits.append(name)
    return hits


def body_for(name, c):
    if c["tier"] in ("core", "pinned") and not c["section"]:
        return read_pref(name)  # the whole article; a core digest is already loaded
    return read_pref(name, c["section"] or None)


def state_path(session_id):
    return Path(tempfile.gettempdir()) / f"pref_loader_{re.sub(r'[^A-Za-z0-9_-]', '_', session_id or 'nosession')}.json"


def inject(event, names, session_id, config):
    seen = []
    sp = state_path(session_id)
    try:
        seen = json.loads(sp.read_text())
    except Exception:
        pass
    new = [n for n in names if n not in seen]
    if not new:
        return None
    parts, used = [], 0
    for n in new:
        text = f"[Preference: {n}]\n{body_for(n, config[n])}"
        if used + len(text) > CAP:
            break
        parts.append(text)
        used += len(text)
        seen.append(n)
    try:
        sp.write_text(json.dumps(seen))
        with LOG.open("a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')}\t{event}\t{session_id}\t{', '.join(new)}\t{used}\n")
    except Exception:
        pass
    loaded = ", ".join(n for n in new if any(p.startswith(f"[Preference: {n}]") for p in parts))
    return {
        "systemMessage": f"Preferences loaded: {loaded}",
        "hookSpecificOutput": {"hookEventName": event, "additionalContext": "\n\n".join(parts)},
    }


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except Exception:
        data = {}
    try:
        if mode == "session":
            print(session_text())
        elif (HERE / "pref_loader.off").exists():
            return
        elif mode == "prompt":
            config = load_config()
            out = inject("UserPromptSubmit", match_prompt(data.get("prompt", ""), config), data.get("session_id"), config)
            if out:
                print(json.dumps(out))
        elif mode == "tool":
            config = load_config()
            hits = match_tool(data.get("tool_name", ""), data.get("tool_input", {}), data.get("cwd", ""), config)
            out = inject("PreToolUse", hits, data.get("session_id"), config)
            if out:
                print(json.dumps(out))
    except Exception as e:  # fail open
        sys.stderr.write(f"pref_loader error: {e}\n")


if __name__ == "__main__":
    main()
