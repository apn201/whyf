"""The curated knowledge, loaded once and held in memory.

This module is also the anti-hallucination layer. Every framework, incident,
pattern and already-have reference the agent emits is checked against the id
sets built here, and anything unknown is dropped before it reaches a user. The
model is never in a position to invent a control number or a dollar figure,
because it does not write either: it selects an id, and the id either resolves
or disappears.

Cards marked `skeleton` are treated as absent. An unfinished card is worse than
no card, because the agent would render its TODOs at somebody.
"""
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from ..paths import find_knowledge

KNOWLEDGE = find_knowledge(__file__)

SHIPPABLE = {"draft", "done"}


@dataclass
class Library:
    concepts: dict = field(default_factory=dict)
    frameworks: dict = field(default_factory=dict)   # control id -> description
    incidents: dict = field(default_factory=dict)
    patterns: dict = field(default_factory=dict)
    already_have: dict = field(default_factory=dict)

    # ---- lookup ----------------------------------------------------------

    def concept(self, concept_id):
        return self.concepts.get(concept_id)

    def ids(self):
        return {
            "frameworks": set(self.frameworks),
            "incidents": set(self.incidents),
            "patterns": set(self.patterns),
            "already_have": set(self.already_have),
        }

    def validate_references(self, refs):
        """Split a model's proposed references into the ones that exist and the
        ones it invented. The caller renders the first and logs the second.

        `refs` is {"frameworks": [...], "incidents": [...], ...}."""
        known = self.ids()
        kept, dropped = {}, {}
        for field_name, values in (refs or {}).items():
            valid = known.get(field_name, set())
            kept[field_name] = [v for v in (values or []) if v in valid]
            invented = [v for v in (values or []) if v not in valid]
            if invented:
                dropped[field_name] = invented
        return kept, dropped

    def describe(self, field_name, ref_id):
        """Human-readable text for a reference, straight from the library. The
        model never writes these."""
        if field_name == "frameworks":
            return self.frameworks.get(ref_id)
        source = getattr(self, field_name, {})
        item = source.get(ref_id) or {}
        if field_name == "incidents":
            return self._describe_incident(item)
        return item.get("name") or item.get("title") or item.get("claim")

    @staticmethod
    def _describe_incident(item):
        """An incident is worth more than its name.

        Every record that reaches this point is status: done, which means the
        cost figure behind it has a primary source attached. Carrying the
        figure into the reference is the difference between naming a breach
        and making an argument with it.
        """
        name = item.get("name") or item.get("id")
        year = item.get("year")
        label = "{} ({})".format(name, year) if year else name
        figure = (item.get("what_it_cost") or {}).get("figure")
        return "{}, {}".format(label, figure) if figure else label

    def summary(self):
        by_class = {}
        for card in self.concepts.values():
            by_class[card.get("class", "?")] = by_class.get(card.get("class", "?"), 0) + 1
        return {
            "concepts": len(self.concepts),
            "by_class": by_class,
            "frameworks": len(self.frameworks),
            "incidents": len(self.incidents),
            "patterns": len(self.patterns),
            "already_have": len(self.already_have),
        }


def _load_dir(path, shippable_only=True):
    import yaml
    out = {}
    if not path.exists():
        return out
    for f in sorted(path.glob("*.yaml")):
        data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        if shippable_only and data.get("status") not in SHIPPABLE:
            continue
        out[data.get("id") or f.stem] = data
    return out


@lru_cache(maxsize=2)
def load(path=None, shippable_only=True) -> Library:
    """Read the corpus off disk. Cached, because in a Lambda this happens once
    at cold start and then never again."""
    import yaml
    base = Path(path or KNOWLEDGE)

    frameworks = {}
    for f in sorted((base / "frameworks").glob("*.yaml")):
        data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        for control in (data.get("controls") or []):
            if isinstance(control, dict) and control.get("id"):
                frameworks[control["id"]] = control.get("title") or control["id"]

    return Library(
        concepts=_load_dir(base / "concepts", shippable_only),
        frameworks=frameworks,
        incidents=_load_dir(base / "incidents", shippable_only),
        patterns=_load_dir(base / "patterns", shippable_only),
        already_have=_load_dir(base / "already-have", shippable_only),
    )
