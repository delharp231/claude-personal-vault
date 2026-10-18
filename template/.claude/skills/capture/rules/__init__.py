"""The rule registry behind check.py.

A rule is a function of the check's context that returns findings. Each rule has an id, a severity (error or warn), a
stage (enforced, or probation, which reports every finding as a warning), and a dimension. Rule modules register with
the @rule decorator and expose FIXTURES for check.py --selftest: (name, {path: text}, {expected rule ids}).
"""
import hashlib
import re
from dataclasses import dataclass, field
from typing import Callable, Optional

REGISTRY = []


@dataclass
class Finding:
    rule: str
    severity: str
    file: str
    message: str
    line: Optional[int] = None

    @property
    def fingerprint(self):
        return fingerprint(self.rule, self.file, self.message)


@dataclass
class Rule:
    id: str
    severity: str
    stage: str
    dimension: str
    fn: Callable = field(repr=False)
    module: str = ""


def fingerprint(rule_id, where, message):
    """Ten hex digits naming a finding, with numbers blurred so a count that moves is the same finding."""
    return hashlib.sha1(f"{rule_id}|{where}|{re.sub(r'[0-9]+', 'N', message)}".encode("utf-8")).hexdigest()[:10]


def rule(rule_id, severity="error", stage="enforced", dimension="structure"):
    """Register a rule function fn(ctx) -> iterable of (file, message) or (file, message, line)."""
    def register(fn):
        REGISTRY.append(Rule(rule_id, severity, stage, dimension, fn, fn.__module__.rsplit(".", 1)[-1]))
        return fn
    return register
