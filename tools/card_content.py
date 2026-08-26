"""All eighty cards' content, merged from tools/content/*.py.

Split into parts only so each file stays editable. Nothing here depends on
which part a concept lives in.
"""
import importlib
import pkgutil

import content as _pkg

CONTENT = {}
for _mod in sorted(m.name for m in pkgutil.iter_modules(_pkg.__path__)):
    CONTENT.update(importlib.import_module("content." + _mod).CARDS)
