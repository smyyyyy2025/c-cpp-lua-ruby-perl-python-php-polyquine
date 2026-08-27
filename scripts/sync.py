#!/usr/bin/env python3
"""Copy 413-byte variant 0 to the six main files without changing its bytes."""
import sys
from verify import ROOT, MAIN_FILES, VARIANT_FILES, format_errors


def main():
    source_path = ROOT / VARIANT_FILES[0]
    try:
        source = source_path.read_bytes()
    except OSError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    errors = format_errors(VARIANT_FILES[0], source)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    for name in MAIN_FILES:
        target = ROOT / name
        if not target.exists() or target.read_bytes() != source:
            target.write_bytes(source)
        print("%s: %d bytes" % (name, len(source)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
