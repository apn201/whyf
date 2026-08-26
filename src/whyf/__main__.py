"""Terminal entry point. `python -m whyf "paste a row here"`."""
import sys

from . import render
from .pipeline import Pipeline


def main(argv=None):
    # Cards price things in euro symbols and the Windows console defaults to a
    # codepage that cannot print one. Reconfigure rather than degrade the card.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass

    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print('usage: python -m whyf "one row from a questionnaire"')
        return 2
    pipeline = Pipeline()
    print(render.to_text(pipeline.resolve(" ".join(argv))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
