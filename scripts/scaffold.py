#!/usr/bin/env python3
"""Create a framework-neutral AI design-system contract without overwriting files."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys


SKILL_ROOT = pathlib.Path(__file__).resolve().parent.parent
STARTER = SKILL_ROOT / "assets" / "starter"


def git_revision(target: pathlib.Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=target,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "uncommitted"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, help="Repository root")
    parser.add_argument("--name", required=True, help="Human-facing design-system name")
    parser.add_argument("--version", default="0.1.0")
    parser.add_argument("--storybook-url", default="")
    parser.add_argument("--directory", default="ai-design-system")
    args = parser.parse_args()

    target = pathlib.Path(args.target).expanduser().resolve()
    if not target.is_dir():
        print(f"Target repository does not exist: {target}", file=sys.stderr)
        return 2

    destination = target / args.directory
    if destination.exists():
        print(f"Refusing to overwrite existing contract: {destination}", file=sys.stderr)
        return 3

    shutil.copytree(STARTER, destination)
    replacements = {
        "__DESIGN_SYSTEM_NAME__": args.name,
        "__VERSION__": args.version,
        "__REVISION__": git_revision(target),
        "__RELEASED_AT__": dt.datetime.now(dt.timezone.utc).isoformat(),
        "__STORYBOOK_URL__": args.storybook_url,
    }

    for path in destination.rglob("*"):
        if not path.is_file() or path.suffix not in {".json", ".md", ".txt"}:
            continue
        content = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            content = content.replace(old, new)
        path.write_text(content, encoding="utf-8")

    release_path = destination / "release.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    release["checksums"] = {
        path.relative_to(destination).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(destination.rglob("*"))
        if path.is_file() and path != release_path
    }
    release_path.write_text(json.dumps(release, indent=2) + "\n", encoding="utf-8")

    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
