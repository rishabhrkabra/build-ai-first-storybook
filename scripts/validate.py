#!/usr/bin/env python3
"""Validate the portable AI-first Storybook contract using only Python stdlib."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
from typing import Any


ALLOWED_LIFECYCLE = {"current", "legacy", "deprecated", "internal", "unknown"}
ALLOWED_PUBLICATION = {"public", "internal", "documentation-only", "hidden"}
ALLOWED_READINESS = {"ready", "review", "inventory-only", "blocked"}
BAD_NAME = re.compile(r"^(component|frame|group|variant|icon|button|checkbox|tooltip)[ _-]*\d+$", re.I)


class ContractError(Exception):
    pass


def load_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file():
        raise ContractError(f"Missing file: {path}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ContractError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError(f"Expected object in {path}")
    return value


def require(obj: dict[str, Any], keys: list[str], label: str) -> None:
    missing = [key for key in keys if key not in obj or obj[key] in (None, "")]
    if missing:
        raise ContractError(f"{label} missing: {', '.join(missing)}")


def unique(records: list[dict[str, Any]], field: str, label: str) -> None:
    values = [record.get(field) for record in records]
    duplicates = sorted({value for value in values if value is not None and values.count(value) > 1})
    if duplicates:
        raise ContractError(f"Duplicate {label} {field}: {duplicates}")


def validate_ready(component: dict[str, Any], root: pathlib.Path) -> None:
    label = f"ready component {component.get('id', '<unknown>')}"
    require(
        component,
        ["id", "name", "status", "importPath", "contextFile", "source", "storyIds", "docs", "tests", "authority", "contract"],
        label,
    )
    for field in ("source", "storyIds", "tests", "authority"):
        if not isinstance(component[field], list) or not component[field]:
            raise ContractError(f"{label} requires non-empty {field}")
    if not isinstance(component["docs"], str):
        raise ContractError(f"{label} docs must be a path")
    for relative in [*component["source"], component["docs"], component["contextFile"]]:
        if not (root / relative).is_file():
            raise ContractError(f"{label} references missing file: {relative}")
    contract = component["contract"]
    if not isinstance(contract, dict):
        raise ContractError(f"{label} contract must be an object")
    for field in ("states", "behavior", "responsive", "accessibility", "composition"):
        if not isinstance(contract.get(field), list) or not contract[field]:
            raise ContractError(f"{label} contract requires non-empty {field}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, help="Repository root")
    parser.add_argument("--directory", default="ai-design-system")
    args = parser.parse_args()

    root = pathlib.Path(args.root).expanduser().resolve()
    directory = root / args.directory
    try:
        manifest = load_json(directory / "manifest.json")
        require(manifest, ["schemaVersion", "name", "version", "authority", "artifacts", "requirements"], "manifest")
        if manifest["schemaVersion"] != 1:
            raise ContractError("Unsupported manifest schemaVersion")
        if not all(manifest["requirements"].values()):
            raise ContractError("All AI-first requirements must be enabled")

        artifacts = manifest["artifacts"]
        require(
            artifacts,
            ["inventory", "publicApi", "contextIndex", "tokens", "rules", "migrations", "recipes", "decisions", "release"],
            "manifest artifacts",
        )
        inventory = load_json(directory / artifacts["inventory"])
        public_api = load_json(directory / artifacts["publicApi"])
        context_index = load_json(directory / artifacts["contextIndex"])
        tokens = load_json(directory / artifacts["tokens"])
        rules = load_json(directory / artifacts["rules"])
        content_path = artifacts.get("content")
        content = load_json(directory / content_path) if content_path else {
            "schemaVersion": 1,
            "version": manifest["version"],
            "entries": [],
        }
        migrations = load_json(directory / artifacts["migrations"])
        recipes = load_json(directory / artifacts["recipes"])
        decisions = load_json(directory / artifacts["decisions"])
        release = load_json(directory / artifacts["release"])

        families = inventory.get("families")
        components = public_api.get("components")
        contexts = context_index.get("components")
        content_entries = content.get("entries")
        if not isinstance(families, list) or not all(isinstance(item, dict) for item in families):
            raise ContractError("inventory families must be an array of objects")
        if not isinstance(components, list) or not all(isinstance(item, dict) for item in components):
            raise ContractError("public API components must be an array of objects")
        if not isinstance(contexts, list) or not all(isinstance(item, dict) for item in contexts):
            raise ContractError("context index components must be an array of objects")
        if not isinstance(content_entries, list) or not all(isinstance(item, dict) for item in content_entries):
            raise ContractError("content entries must be an array of objects")

        unique(families, "id", "inventory")
        unique(families, "name", "inventory")
        unique(components, "id", "public API")
        unique(components, "name", "public API")
        unique(contexts, "id", "context index")
        unique(content_entries, "id", "content")
        context_by_id = {item.get("id"): item for item in contexts}
        story_ids: list[str] = []

        family_by_id = {}
        for family in families:
            require(family, ["id", "name", "sourceName", "lifecycle", "publication", "readiness", "source"], "inventory family")
            if BAD_NAME.match(family["name"]):
                raise ContractError(f"Raw or numbered authoring name used as canonical name: {family['name']}")
            if family["lifecycle"] not in ALLOWED_LIFECYCLE:
                raise ContractError(f"Invalid lifecycle for {family['id']}")
            if family["publication"] not in ALLOWED_PUBLICATION:
                raise ContractError(f"Invalid publication for {family['id']}")
            if family["readiness"] not in ALLOWED_READINESS:
                raise ContractError(f"Invalid readiness for {family['id']}")
            family_by_id[family["id"]] = family

        ready_ids = set()
        for component in components:
            require(component, ["id", "name", "status"], "public API component")
            if component["id"] not in family_by_id:
                raise ContractError(f"Public API component missing from inventory: {component['id']}")
            if component["id"] not in context_by_id:
                raise ContractError(f"Public API component missing from context index: {component['id']}")
            if component["status"] not in {"ready", "review"}:
                raise ContractError(f"Invalid public API status for {component['id']}")
            family = family_by_id[component["id"]]
            if family["publication"] != "public":
                raise ContractError(f"Non-public family appears in public API: {component['id']}")
            if component["status"] == "ready":
                if family["lifecycle"] != "current" or family["readiness"] != "ready":
                    raise ContractError(f"Ready selection conflicts with inventory lifecycle/readiness: {component['id']}")
                validate_ready(component, root)
                if context_by_id[component["id"]].get("contextFile") != component["contextFile"]:
                    raise ContractError(f"Context path mismatch for {component['id']}")
                ready_ids.add(component["id"])
            story_ids.extend(component.get("storyIds", []))

        if len(story_ids) != len(set(story_ids)):
            raise ContractError("Duplicate Storybook story IDs in public API")

        for entry in content_entries:
            require(entry, ["id", "context", "intent", "tone", "requires", "forbids", "examples"], "content entry")
            for field in ("tone", "requires", "forbids", "examples"):
                if not isinstance(entry[field], list):
                    raise ContractError(f"content entry {entry['id']} {field} must be an array")

        require(release, ["schemaVersion", "name", "version", "revision", "releasedAt", "checksums"], "release")
        versioned = [release, public_api, context_index, tokens, recipes]
        if content_path:
            versioned.append(content)
        if "version" in rules:
            versioned.append(rules)
        if any(item.get("version") != manifest["version"] for item in versioned) or migrations.get("currentVersion") != manifest["version"]:
            raise ContractError("Version mismatch across manifest and machine-readable artifacts")
        rule_records = rules.get("rules")
        exceptions = rules.get("exceptions", [])
        if not isinstance(rule_records, list) or not all(isinstance(item, dict) for item in rule_records):
            raise ContractError("Rules must contain an array of objects")
        if not isinstance(exceptions, list) or not all(isinstance(item, dict) for item in exceptions):
            raise ContractError("Rule exceptions must be an array of objects")
        if not isinstance(tokens.get("tokens"), list):
            raise ContractError("Rules and tokens must contain arrays")
        unique(rule_records, "id", "rules")
        unique(exceptions, "id", "rule exceptions")
        rule_ids = {item.get("id") for item in rule_records}
        for rule in rule_records:
            require(rule, ["id", "principle", "appliesWhen", "requires", "forbids", "rationale", "severity", "evidence"], "rule")
        for exception in exceptions:
            require(exception, ["id", "ruleId", "reason", "owner", "expiresAt", "status"], "rule exception")
            if exception["ruleId"] not in rule_ids:
                raise ContractError(f"Rule exception references unknown rule: {exception['id']}")
        if not isinstance(release["checksums"], dict) or not release["checksums"]:
            raise ContractError("Release requires artifact checksums")
        for relative, expected in release["checksums"].items():
            path = directory / relative
            if not path.is_file():
                raise ContractError(f"Checksum references missing file: {relative}")
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != expected:
                raise ContractError(f"Checksum mismatch: {relative}")

        for decision in decisions.get("decisions", []):
            if decision.get("status") == "open" and not decision.get("owner"):
                raise ContractError(f"Open decision lacks owner: {decision.get('id', '<unknown>')}")

        for recipe in recipes.get("recipes", []):
            require(recipe, ["id", "name", "status", "componentIds", "responsive"], "recipe")
            if recipe["status"] == "ready":
                unavailable = sorted(set(recipe["componentIds"]) - ready_ids)
                if unavailable:
                    raise ContractError(f"Ready recipe uses non-ready components: {recipe['id']} -> {unavailable}")
                if not recipe["responsive"]:
                    raise ContractError(f"Ready recipe lacks responsive contract: {recipe['id']}")

        print(
            json.dumps(
                {
                    "valid": True,
                    "version": manifest["version"],
                    "inventory": len(families),
                    "ready": len(ready_ids),
                    "review": len(components) - len(ready_ids),
                    "recipes": len(recipes.get("recipes", [])),
                    "contentEntries": len(content_entries),
                    "ruleExceptions": len(exceptions),
                    "openDecisions": sum(1 for item in decisions.get("decisions", []) if item.get("status") == "open"),
                },
                indent=2,
            )
        )
        return 0
    except ContractError as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
