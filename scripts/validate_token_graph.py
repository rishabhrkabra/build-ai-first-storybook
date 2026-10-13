"""Validate a normalized design-token export; never writes to its authority."""
import argparse
import json
import math
import re
import sys
from pathlib import Path


def validate(data):
    errors, by_id, names, edges = [], {}, set(), {}
    tokens = data.get("tokens")
    if not isinstance(tokens, list) or not tokens:
        return ["tokens must be a non-empty array"]
    role = re.compile(r"(?:^|[/_-])(heading|surface|action|border|nav|navigation|avatar|disabled|selected|primary|secondary|placeholder)(?:$|[/_-])")
    statuses = {"observed", "observed-value", "draft", "review", "approved", "approved-scoped", "accepted-exception", "deprecated"}
    for t in tokens:
        if not isinstance(t, dict):
            errors.append("token must be an object")
            continue
        key, name, tier = t.get("id"), t.get("name", ""), t.get("tier")
        if not isinstance(key, str) or not key or key in by_id:
            errors.append(f"duplicate or missing id: {key}")
            continue
        by_id[key] = t
        if not isinstance(name, str) or not name:
            errors.append(f"{key}: missing name")
            name = ""
        if (tier, name) in names:
            errors.append(f"{key}: duplicate tier/name")
        names.add((tier, name))
        if tier not in {"primitive", "semantic", "component"}:
            errors.append(f"{key}: invalid tier")
        if "merge" in name.lower():
            errors.append(f"{key}: unresolved merge marker")
        if not t.get("purpose") or not t.get("source"):
            errors.append(f"{key}: missing purpose/source")
        if not isinstance(t.get("permittedUses"), list) or not t["permittedUses"]:
            errors.append(f"{key}: missing permitted uses")
        if t.get("status") not in statuses:
            errors.append(f"{key}: missing/unknown status")
        if tier == "component" and (not t.get("owner") or not name.startswith(t["owner"] + "/")):
            errors.append(f"{key}: component owner/name mismatch")
        if tier == "primitive":
            if role.search(name):
                errors.append(f"{key}: usage role in primitive name")
            if t.get("type") == "COLOR" and data.get("policy", {}).get("numberedColorPrimitives") and not re.fullmatch(r"color/[a-z][a-z-]*/\d+", name):
                errors.append(f"{key}: expected numbered colour primitive")
        values = t.get("values")
        if not isinstance(values, dict) or not values:
            errors.append(f"{key}: missing mode values")
            continue
        edges[key] = []
        for mode, value in values.items():
            if isinstance(value, dict) and value.get("type") == "VARIABLE_ALIAS":
                if tier == "primitive":
                    errors.append(f"{key}: primitive must contain raw values")
                edges[key].append(value.get("id"))
                continue
            if tier != "primitive":
                errors.append(f"{key}/{mode}: raw value outside primitive tier")
                continue
            kind = t.get("type")
            num = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
            valid = ((kind == "FLOAT" and num(value)) or
                     (kind == "STRING" and isinstance(value, str)) or
                     (kind == "BOOLEAN" and isinstance(value, bool)) or
                     (kind == "COLOR" and isinstance(value, dict) and all(num(value.get(k)) and 0 <= value[k] <= 1 for k in ["r", "g", "b"]) and num(value.get("a", 1)) and 0 <= value.get("a", 1) <= 1))
            if not valid:
                errors.append(f"{key}/{mode}: invalid raw value for {kind}")
            if kind == "FLOAT" and re.match(r"^(space|dimension|radius|opacity)/", name):
                step = name.split("/")[-1].replace("minus-", "-")
                try:
                    if not math.isclose(float(step), float(value), abs_tol=1e-6):
                        errors.append(f"{key}: numeric scale name differs from value")
                except (ValueError, TypeError):
                    errors.append(f"{key}: numeric primitive has non-numeric name")
    for key, refs in edges.items():
        t = by_id[key]
        for ref in refs:
            target = by_id.get(ref)
            if target is None:
                errors.append(f"{key}: missing alias {ref}")
                continue
            if target.get("type") != t.get("type"):
                errors.append(f"{key}: alias type mismatch")
            if t.get("tier") == "semantic" and target.get("tier") == "component":
                errors.append(f"{key}: semantic depends on component")
            if t.get("tier") == "component":
                if t.get("type") == "COLOR" and target.get("tier") == "primitive":
                    errors.append(f"{key}: component colour bypasses semantic role")
                if target.get("tier") == "component" and target.get("owner") != t.get("owner"):
                    errors.append(f"{key}: cross-owner component dependency")
    visiting, done = set(), set()

    def visit(key):
        if key in visiting:
            errors.append(f"{key}: alias cycle")
            return
        if key in done:
            return
        visiting.add(key)
        for ref in edges.get(key, []):
            if ref in by_id:
                visit(ref)
        visiting.remove(key)
        done.add(key)

    for key in by_id:
        visit(key)
    for b in data.get("bindings", []):
        t = by_id.get(b.get("tokenId"))
        if not t:
            errors.append(f"{b.get('nodeId')}: missing bound token")
        elif t.get("tier") == "primitive" and b.get("context") != "foundation":
            errors.append(f"{b.get('nodeId')}: direct primitive binding")
        elif t.get("tier") == "component" and b.get("context") != "foundation" and b.get("owner") != t.get("owner"):
            errors.append(f"{b.get('nodeId')}: wrong component-token owner")
    return sorted(set(errors))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    data = {}
    try:
        data = json.loads(args.manifest.read_text())
        errors = validate(data)
    except (OSError, ValueError, TypeError, AttributeError, RecursionError) as exc:
        errors = [f"Invalid manifest: {exc}"]
    print(json.dumps({"ok": not errors, "tokensChecked": len(data.get("tokens", [])) if isinstance(data, dict) else 0, "bindingsChecked": len(data.get("bindings", [])) if isinstance(data, dict) else 0, "errors": errors}, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
