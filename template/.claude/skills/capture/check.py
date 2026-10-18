"""Pre-commit check for a personal ontology vault: a rule engine over rules/.

Usage: python check.py [vault_root] [--json] [--all] [--changed RANGE|staged] [--rule ID] [--legacy-only] [--selftest]

Prints "Vault check passed: N notes." or "Vault check FAILED:" first, as it always has, then the errors, then any
warnings. Exits 1 only when an error survives exceptions.txt. A rule on probation reports every finding as a warning.
A rule that crashes becomes a rule-crashed warning, except a legacy rule, whose crash is an error.
Emergency escape: --legacy-only runs only the checks that existed before the engine.
Standard library only, so it runs on any machine or cloud session.
"""
import argparse
import importlib
import json
import os
import pkgutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True   # no __pycache__ folders in the vault for Obsidian Git to commit

import rules  # noqa: E402
import vault_parse  # noqa: E402
from rules import REGISTRY, Finding  # noqa: E402

EXCEPTIONS = os.path.join(HERE, "exceptions.txt")


def load_rules():
    """Import every module in rules/, so each registers its rules. Returns {module name: module}."""
    mods = {}
    for info in pkgutil.iter_modules(rules.__path__):
        mods[info.name] = importlib.import_module(f"rules.{info.name}")
    return mods


class Context:
    """What every rule reads: the notes, their text (read once), and the scope terms."""

    def __init__(self, root):
        self.root = os.path.abspath(root)
        self.notes = vault_parse.notes(self.root)
        self._text = {}
        self.filled = [r for r in self.notes if self.read(r).strip()]
        self.scope = self._scope()

    def read(self, rel):
        if rel not in self._text:
            self._text[rel] = vault_parse.read(self.root, rel)
        return self._text[rel]

    def _scope(self):
        path = os.path.join(self.root, ".claude", "scope.txt")
        out = []
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                for line in fh.read().splitlines():
                    if not line.strip() or line.lstrip().startswith("#"):
                        continue
                    term, _, allowed = line.partition("|")
                    out.append((term.strip().lower(), {a.strip() for a in allowed.split(",") if a.strip()}))
        return out


def parse_exceptions(text):
    """[(rule, path, reason, added, line number)] from 'rule | path | reason | added' lines; '#' starts a comment."""
    out = []
    for n, line in enumerate(text.splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        parts += [""] * (4 - len(parts))
        out.append((parts[0], parts[1], parts[2], parts[3], n))
    return out


def run(root, selected, exceptions_text="", changed=None):
    """Run the selected rules on the vault at root. Returns (errors, warnings, note count)."""
    ctx = Context(root)
    findings = []
    for r in selected:
        try:
            for item in r.fn(ctx) or []:
                file, message = item[0], item[1]
                line = item[2] if len(item) > 2 else None
                severity = "warn" if r.stage == "probation" else r.severity
                findings.append(Finding(r.id, severity, file, message, line))
        except Exception as e:   # one broken rule must not hide the rest
            sev = "error" if r.module == "legacy" else "warn"
            findings.append(Finding("rule-crashed", sev, "", f"rule {r.id} crashed: {type(e).__name__}: {e}"))
    used = set()
    kept = []
    excs = parse_exceptions(exceptions_text)
    for f in findings:
        hit = next((e for e in excs if e[0] == f.rule and e[1] == f.file and e[2]), None)
        if hit:
            used.add(hit[4])
        else:
            kept.append(f)
    for rule_id, path, reason, _, n in excs:
        if not reason:
            kept.append(Finding("exception-no-reason", "error", "exceptions.txt", f"exceptions.txt:{n}: exception for {rule_id} on {path} gives no reason", n))
        elif n not in used:
            kept.append(Finding("exception-unused", "warn", "exceptions.txt", f"exceptions.txt:{n}: exception for {rule_id} on {path} suppresses nothing", n))
    errors = [f for f in kept if f.severity == "error"]
    warnings = [f for f in kept if f.severity != "error" and (changed is None or f.file in changed)]
    return errors, warnings, len(ctx.notes)


def changed_files(root, spec):
    """Vault-relative paths touched by a git range, or by what is staged."""
    args = ["diff", "--name-only", "--cached"] if spec == "staged" else ["diff", "--name-only", spec]
    out = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True, encoding="utf-8")
    return {l.strip() for l in out.stdout.splitlines() if l.strip()}


def report(errors, warnings, n, as_json=False):
    if as_json:
        print(json.dumps({"passed": not errors, "notes": n,
                          "findings": [dict(f.__dict__, fingerprint=f.fingerprint) for f in errors + warnings]}, ensure_ascii=False))
        return
    if errors:
        print("Vault check FAILED:")
        for f in errors:
            print(" -", f.message)
    else:
        print(f"Vault check passed: {n} notes.")
    if warnings:
        print("Warnings:")
        for f in warnings:
            print(f" - [{f.rule}] {f.message}")


def selftest(mods):
    """Every rule module's FIXTURES must give exactly their expected rule ids; a rule with no fixture fails."""
    count, failures = 0, []
    for name, mod in sorted(mods.items()):
        own = [r for r in REGISTRY if r.module == name]
        covered = set()
        for fname, files, expected in getattr(mod, "FIXTURES", []):
            with tempfile.TemporaryDirectory() as tmp:
                for rel, text in files.items():
                    p = os.path.join(tmp, *rel.split("/"))
                    os.makedirs(os.path.dirname(p), exist_ok=True)
                    with open(p, "w", encoding="utf-8", newline="") as fh:
                        fh.write(text)
                errs, warns, _ = run(tmp, own)
                got = {f.rule for f in errs + warns}
            count += 1
            covered |= set(expected)
            if got != set(expected):
                failures.append(f"{name}: {fname}: expected {sorted(expected)}, got {sorted(got)}")
        for r in own:
            if r.id not in covered:
                failures.append(f"{name}: rule {r.id} has no fixture that expects it")
    if failures:
        print("SELFTEST FAILED:")
        for f in failures:
            print(" -", f)
        return 1
    print(f"SELFTEST OK {count} fixtures")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check a personal ontology vault.")
    ap.add_argument("root", nargs="?", default=os.path.join(HERE, "..", "..", ".."))
    ap.add_argument("--json", action="store_true", help="print findings as JSON")
    ap.add_argument("--all", action="store_true", help="check every note (the default)")
    ap.add_argument("--changed", help="report warnings only for files in this git range, or 'staged'; errors anywhere")
    ap.add_argument("--rule", help="run only this rule id")
    ap.add_argument("--legacy-only", action="store_true", help="run only the checks that existed before the engine")
    ap.add_argument("--selftest", action="store_true", help="run every rule's fixtures and exit")
    args = ap.parse_args(argv)
    mods = load_rules()
    if args.selftest:
        return selftest(mods)
    selected = [r for r in REGISTRY if (not args.legacy_only or r.module == "legacy") and (not args.rule or r.id == args.rule)]
    exceptions_text = ""
    if os.path.exists(EXCEPTIONS):
        with open(EXCEPTIONS, encoding="utf-8") as fh:
            exceptions_text = fh.read()
    root = os.path.abspath(args.root)
    changed = changed_files(root, args.changed) if args.changed else None
    errors, warnings, n = run(root, selected, exceptions_text, changed)
    report(errors, warnings, n, args.json)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
