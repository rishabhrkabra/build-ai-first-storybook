#!/usr/bin/env python3
"""Refresh integrity hashes for a scaffolded AI design-system contract."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from contract_io import ContractError, safe_path, load_json, authoring_hashes, dump


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="Repository root")
    parser.add_argument("--directory", default="ai-design-system")
    args = parser.parse_args()

    try:
        directory = safe_path(pathlib.Path(args.root).expanduser().resolve(), args.directory)
    except ContractError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    try:
        manifest = load_json(directory / 'manifest.json')
        if manifest.get('schemaVersion') != 2:
            raise ContractError('Migrate v1 explicitly; see references/portable-contract.md')
        release_path = safe_path(directory, manifest['artifacts']['release'])
        release = load_json(release_path)
        release['checksums'] = authoring_hashes(directory, manifest)
        dump(release_path, release)
    except (ContractError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps({"updated": len(release["checksums"]), "release": str(release_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
