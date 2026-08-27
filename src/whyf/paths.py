"""Finding the knowledge base, in a way that survives being repackaged.

This existed as `parent.parent.parent` in three modules, and it was wrong in
the only environment that matters. In the repo the package sits under src/, so
three levels up is the repo root. In the Lambda bundle the package sits at the
root, so three levels up is somewhere above the bundle entirely, and every
lookup silently returned nothing.

Silently is the problem. An empty cards directory is not an error anywhere: the
index builds fine with no documents, the shortlist comes back empty, and the
agent politely declines every question in eleven milliseconds. It looks like a
working deployment with an unlucky knowledge base.

So: search upward for the directory instead of counting levels, and raise if it
is genuinely absent rather than continuing with nothing.
"""
import os
from pathlib import Path


def find_knowledge(start=None):
    """The knowledge directory, found by looking for it.

    WHYF_KNOWLEDGE overrides, for anyone who wants to point the agent at a
    different card set without moving files around.
    """
    override = os.environ.get("WHYF_KNOWLEDGE")
    if override:
        return Path(override)

    here = Path(start or __file__).resolve()
    for parent in [here] + list(here.parents):
        candidate = parent / "knowledge"
        # `concepts` is what distinguishes the knowledge base from the
        # whyf.knowledge python package, which is also called knowledge and is
        # also on this path.
        if (candidate / "concepts").is_dir():
            return candidate

    raise RuntimeError(
        "no knowledge/concepts directory found above {}. The agent has no "
        "cards and would decline every question.".format(here))
