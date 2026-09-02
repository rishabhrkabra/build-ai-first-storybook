#!/usr/bin/env python3
"""Refresh integrity hashes for a scaffolded AI design-system contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="Repository root")
    parser.add_argument("--directory", default="ai-design-system")
    args = parser.parse_args()

    directory = pathlib.Path(args.root).expanduser().resolve() / args.directory
    release_path = directory / "release.json"
    if not release_path.is_file():
        print(f"Missing release file: {release_path}", file=sys.stderr)
        return 2

    release = json.loads(release_path.read_text(encoding="utf-8"))
    release["checksums"] = {
        path.relative_to(directory).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.rglob("*"))
        if path.is_file() and path != release_path
    }
    release_path.write_text(json.dumps(release, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"updated": len(release["checksums"]), "release": str(release_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
