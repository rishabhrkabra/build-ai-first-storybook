#!/usr/bin/env python3
"""Validate a scoped DS decision and dependency receipt against local artifacts.

This consumes measured exports; it neither collects Figma nor certifies approval,
inventory completeness or visual judgment. See references/change-completion.md.
"""
import hashlib
import json
from pathlib import Path
import re
import sys


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def indexed(rows, label):
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"{label}: nonempty list required")
    result = {}
    for row in rows:
        key = row.get("id")
        if not isinstance(key, str) or not key.strip() or key in result:
            raise ValueError(f"{label}: missing or duplicate id {key!r}")
        result[key] = row
    return result


def required_text(row, names):
    for name in names:
        if not isinstance(row.get(name), str) or not row[name].strip():
            raise ValueError(f"{name}: nonempty text required")


def pointer(value, path):
    if path == "":
        return value
    if not isinstance(path, str) or not path.startswith("/"):
        raise ValueError("invalid JSON pointer")
    for part in path[1:].split("/"):
        if re.search(r"~(?![01])", part):
            raise ValueError("invalid JSON pointer escape")
        part = part.replace("~1", "/").replace("~0", "~")
        if isinstance(value, list):
            if not re.fullmatch(r"0|[1-9][0-9]*", part):
                raise ValueError("invalid array index")
            value = value[int(part)]
        elif isinstance(value, dict):
            value = value[part]
        else:
            raise ValueError("pointer traverses a scalar")
    return value


def validate(data, base):
    errors = []
    try:
        if data.get("schemaVersion") != 1:
            raise ValueError("unsupported schemaVersion")
        change = data["change"]
        required_text(change, ("id", "decision", "approvalSource"))
        surfaces = indexed(data["surfaces"], "surfaces")
        checks = indexed(data["checks"], "checks")
        requirements = indexed(data["requirements"], "requirements")
        coverage = indexed(data["coverage"], "coverage")
        roots = change["roots"]
        if not isinstance(roots, list) or not roots or len(set(roots)) != len(roots):
            raise ValueError("roots: unique nonempty list required")
        if set(roots) - surfaces.keys():
            raise ValueError("roots: unknown surface")

        contents, hashes = {}, {}
        for sid, surface in surfaces.items():
            required_text(surface, ("source", "path", "sha256"))
            deps = surface["dependsOn"]
            if not isinstance(deps, list) or len(set(deps)) != len(deps):
                raise ValueError(f"{sid}: invalid dependsOn")
            if set(deps) - surfaces.keys():
                raise ValueError(f"{sid}: unknown dependency")
            if not isinstance(surface.get("visual"), bool):
                raise ValueError(f"{sid}: visual must be boolean")
            path = base / surface["path"]
            hashes[sid] = digest(path)
            if hashes[sid] != surface["sha256"]:
                errors.append(f"{sid}: stale artifact digest")
            raw = path.read_text(encoding="utf-8")
            contents[sid] = json.loads(raw) if path.suffix.lower() == ".json" else raw

        visited, active = set(), set()
        def visit(sid):
            if sid in active:
                raise ValueError(f"dependency cycle at {sid}")
            if sid not in visited:
                active.add(sid)
                for dep in surfaces[sid]["dependsOn"]:
                    visit(dep)
                active.remove(sid)
                visited.add(sid)
        for sid in surfaces:
            visit(sid)

        affected = set(roots)
        while True:
            expanded = affected | {sid for sid, s in surfaces.items()
                                   if affected.intersection(s["dependsOn"])}
            if expanded == affected:
                break
            affected = expanded
        for sid in sorted(affected - coverage.keys()):
            errors.append(f"{sid}: affected surface has no coverage")
        if coverage.keys() - surfaces.keys():
            raise ValueError("coverage: unknown surface")

        def read_ref(ref):
            return pointer(contents[ref["surface"]], ref["pointer"])

        check_refs = {}
        for cid, check in checks.items():
            try:
                actual = read_ref(check["actual"])
                refs = {check["actual"]["surface"]}
                if ("expected" in check) == ("expectedFrom" in check):
                    raise ValueError("exactly one expected or expectedFrom required")
                if "expectedFrom" in check:
                    if check["actual"] == check["expectedFrom"]:
                        raise ValueError("self-comparison cannot prove parity")
                    expected = read_ref(check["expectedFrom"])
                    refs.add(check["expectedFrom"]["surface"])
                else:
                    expected = check["expected"]
                check_refs[cid] = refs
                op = check["op"]
                if op == "equals":
                    passed = type(actual) is type(expected) and actual == expected
                elif op in ("contains", "not_contains"):
                    if not isinstance(actual, (str, list, dict)):
                        raise ValueError("contains requires text, list or object")
                    passed = expected in actual
                    if op == "not_contains":
                        passed = not passed
                elif op == "every_match":
                    passed = (isinstance(actual, list) and bool(actual)
                              and isinstance(expected, str)
                              and all(isinstance(v, str) and re.fullmatch(expected, v)
                                      for v in actual))
                else:
                    raise ValueError(f"unsupported operation {op}")
                if not passed:
                    errors.append(f"{cid}: decision assertion failed")
            except (KeyError, IndexError, TypeError, ValueError, re.error) as exc:
                errors.append(f"{cid}: invalid assertion: {exc}")

        def check_ids(row, label):
            ids = row.get("checks")
            if not isinstance(ids, list) or not ids or set(ids) - checks.keys():
                raise ValueError(f"{label}: nonempty known checks required")
            return ids

        for rid, req in requirements.items():
            required_text(req, ("statement",))
            check_ids(req, rid)
        for sid, record in coverage.items():
            required_text(record, ("reason",))
            inputs = {dep: hashes[dep] for dep in surfaces[sid]["dependsOn"]}
            if record.get("inputs") != inputs:
                errors.append(f"{sid}: stale or missing upstream evidence")
            status = record.get("status")
            if status == "historical-preserved":
                if record.get("beforeSha256") != hashes[sid]:
                    errors.append(f"{sid}: history not preserved")
                if sid in roots:
                    errors.append(f"{sid}: changed root cannot be exempt history")
                continue
            if status not in ("verified", "unaffected"):
                errors.append(f"{sid}: unresolved status {status!r}")
                continue
            ids = check_ids(record, sid)
            if not any(sid in check_refs.get(cid, set()) for cid in ids):
                errors.append(f"{sid}: checks do not inspect this surface")
            if surfaces[sid]["visual"]:
                review = record.get("review", {})
                required_text(review, ("reviewer", "notes"))
                if review.get("result") != "pass" or review.get("sourceSha256") != hashes[sid]:
                    errors.append(f"{sid}: missing or stale visual review")
                capture = review["capture"]
                if digest(base / capture["path"]) != capture["sha256"]:
                    errors.append(f"{sid}: stale visual capture")
    except (OSError, KeyError, IndexError, TypeError, ValueError, AttributeError, RecursionError) as exc:
        errors.append(f"invalid receipt or artifact: {exc}")
    return errors


def main():
    if len(sys.argv) != 2:
        print("usage: validate_change_sync.py RECEIPT.json", file=sys.stderr)
        return 2
    path = Path(sys.argv[1]).resolve()
    try:
        errors = validate(json.loads(path.read_text()), path.parent)
    except (OSError, ValueError) as exc:
        errors = [f"cannot read receipt: {exc}"]
    print(json.dumps({"ok": not errors, "errors": errors,
                      "scope": "registered local artifacts and decision assertions; not live collection or visual certification"}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
