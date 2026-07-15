#!/usr/bin/python3

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def main() -> int:
    errors: list[str] = []
    for document in sorted(ROOT.rglob("*.md")):
        if any(part.startswith(".") for part in document.relative_to(ROOT).parts):
            continue
        text = document.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path_text = target.split("#", 1)[0]
            if not path_text:
                continue
            destination = (document.parent / path_text).resolve()
            if not destination.exists():
                errors.append(
                    f"{document.relative_to(ROOT)}: missing link target {target}"
                )
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("documentation links are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
