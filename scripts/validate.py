#!/usr/bin/env python3
"""Validate the portable AI-first Storybook contract using only Python stdlib."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import datetime as dt
from typing import Any
from contract_io import (ContractError, safe_path, relative_path, timestamp, evidence,
                         authoring_hashes, REQUIREMENTS, REQUIRED_ARTIFACTS)


ALLOWED_LIFECYCLE = {"current", "legacy", "deprecated", "internal", "unknown"}
ALLOWED_PUBLICATION = {"public", "internal", "documentation-only", "hidden"}
ALLOWED_READINESS = {"ready", "review", "inventory-only", "blocked"}
ALLOWED_CANDIDATE_STATUS = {"draft", "review", "rejected"}
BAD_NAME = re.compile(r"^(component|frame|group|variant|icon|button|checkbox|tooltip)[ _-]*\d+$", re.I)

REQUIRED_AUTOMATION_DENIALS = {
    "promote",
    "deprecate",
    "delete",
    "accept-visual-baseline",
    "merge",
    "deploy",
    "rewrite-approval",
}


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
    if not isinstance(obj, dict):
        raise ContractError(f'{label} must be an object')
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
        ["id", "name", "status", "importPath", "framework", "contextFile", "source", "storyIds", "docs", "tests", "authority", "contract", "styles", "types", "verification"],
        label,
    )
    for field in ("source", "storyIds", "tests", "authority"):
        if not isinstance(component[field], list) or not component[field]:
            raise ContractError(f"{label} requires non-empty {field}")
    if not isinstance(component["docs"], str):
        raise ContractError(f"{label} docs must be a path")
    for field in ('styles', 'types'):
        if not isinstance(component[field], list):
            raise ContractError(f'{label} {field} must be an array (empty only when not needed)')
    for relative in [*component["source"], *component['styles'], *component['types'],
                     *component['tests'], component["docs"], component["contextFile"]]:
        if not safe_path(root, relative).is_file():
            raise ContractError(f"{label} references missing file: {relative}")
    evidence(root, component['authority'], label + ' authority')
    verification = component['verification']
    require(verification, ['revision', 'artifactSha256', 'checks'], label + ' verification')
    if not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', verification['revision']):
        raise ContractError(f'{label} verification requires immutable revision')
    if not re.fullmatch(r'[0-9a-f]{64}', verification['artifactSha256']):
        raise ContractError(f'{label} requires artifact SHA256')
    checks = verification['checks']
    required_checks = {'build', 'interaction', 'accessibility', 'responsive', 'visual', 'consumer'}
    if not isinstance(checks, dict) or not required_checks.issubset(checks):
        raise ContractError(f'{label} verification lacks required check receipts')
    for name in required_checks:
        check = checks[name]
        require(check, ['status', 'evidence'], label + ' ' + name)
        if check['status'] != 'passed':
            raise ContractError(f'{label}: required {name} check did not pass')
        evidence(root, check['evidence'], label + ' ' + name)
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
    parser.add_argument('--base-ref', help='Full immutable SHA chosen by protected CI, not the change under review')
    args = parser.parse_args()

    root = pathlib.Path(args.root).expanduser().resolve()
    try:
        directory = safe_path(root, args.directory)
        manifest = load_json(directory / "manifest.json")
        require(manifest, ["schemaVersion", "name", "version", "authority", "artifacts", "requirements"], "manifest")
        if type(manifest['schemaVersion']) is not int or manifest['schemaVersion'] != 2:
            raise ContractError('Unsupported schemaVersion; migrate v1 explicitly using portable-contract.md')
        if not isinstance(manifest['requirements'], dict) or any(manifest['requirements'].get(k) is not True for k in REQUIREMENTS):
            raise ContractError('Missing or disabled required AI-first safeguards')
        require(manifest, ['distribution', 'frameworks', 'repositoryPolicy'], 'v2 manifest')
        if not isinstance(manifest['frameworks'], list):
            raise ContractError('frameworks must be an array')
        distribution = manifest['distribution']
        require(distribution, ['access', 'basePath', 'files'], 'distribution')
        if distribution['access'] not in {'local-only', 'authenticated', 'public'}:
            raise ContractError('Invalid distribution access mode')
        if not re.fullmatch(r'/(?:[A-Za-z0-9_-]+/)*[A-Za-z0-9_-]+', distribution['basePath']):
            raise ContractError('distribution basePath must be a normalized absolute URL path without trailing slash')
        if not isinstance(distribution['files'], list):
            raise ContractError('distribution files must be an explicit array')

        artifacts = manifest["artifacts"]
        for key in REQUIRED_ARTIFACTS:
            if key not in artifacts:
                raise ContractError(f'Missing required artifact: {key}')
            safe_path(directory, artifacts[key])
        require(
            artifacts,
            [
                "inventory",
                "publicApi",
                "componentCandidates",
                "componentLifecycle",
                "contextIndex",
                "tokens",
                "rules",
                "migrations",
                "recipes",
                "decisions",
                "release",
            ],
            "manifest artifacts",
        )
        inventory = load_json(directory / artifacts["inventory"])
        public_api = load_json(directory / artifacts["publicApi"])
        candidates = load_json(directory / artifacts["componentCandidates"])
        lifecycle = load_json(directory / artifacts["componentLifecycle"])
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
        for artifact_name, relative in artifacts.items():
            document = load_json(safe_path(directory, relative))
            if type(document.get('schemaVersion')) is not int or document['schemaVersion'] != 2:
                raise ContractError(f'{artifact_name} requires schemaVersion 2')
        for stale in ('catalog.json', 'current.json', 'context/index.json', 'foundation-migration.json'):
            if (directory / stale).exists():
                raise ContractError(f'Competing v1 artifact found: {stale}; reconcile using portable-contract.md')

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

        require(candidates, ["schemaVersion", "publication", "selectable", "selectionPolicy", "reviewThreshold", "candidates"], "component candidates")
        if candidates["publication"] != "private" or candidates["selectable"] is not False:
            raise ContractError("Component candidates must remain private and non-selectable")
        threshold = candidates["reviewThreshold"]
        if not isinstance(threshold, dict):
            raise ContractError("Component candidate reviewThreshold must be an object")
        require(threshold, ["occurrences", "independentModules"], "component candidate reviewThreshold")
        if any(type(threshold[field]) is not int or threshold[field] < 1 for field in ("occurrences", "independentModules")):
            raise ContractError("Component candidate review thresholds must be positive integers")
        candidate_records = candidates["candidates"]
        if not isinstance(candidate_records, list) or not all(isinstance(item, dict) for item in candidate_records):
            raise ContractError("Component candidates must be an array of objects")
        unique(candidate_records, "id", "component candidates")
        candidate_ids = set()
        for candidate in candidate_records:
            require(
                candidate,
                [
                    "id",
                    "status",
                    "occurrences",
                    "semanticPurpose",
                    "nonGoals",
                    "behaviorDifferences",
                    "responsive",
                    "accessibility",
                    "appLogicBoundary",
                    "owner",
                    "decisionNeeded",
                ],
                "component candidate",
            )
            if candidate["status"] not in ALLOWED_CANDIDATE_STATUS:
                raise ContractError(f"Invalid component candidate status: {candidate['id']}")
            for field in ("occurrences", "nonGoals", "behaviorDifferences", "responsive", "accessibility"):
                if not isinstance(candidate[field], list):
                    raise ContractError(f"component candidate {candidate['id']} {field} must be an array")
            for occurrence in candidate["occurrences"]:
                if not isinstance(occurrence, dict):
                    raise ContractError(f"component candidate {candidate['id']} occurrences must contain objects")
                require(occurrence, ["module", "path"], f"component candidate {candidate['id']} occurrence")
            candidate_ids.add(candidate["id"])

        require(
            lifecycle,
            [
                "schemaVersion",
                "baselineMeaning",
                "policy",
                "freezeLine",
                "promotionApprovals",
                "sharedPlacementApprovals",
                "retirementApprovals",
            ],
            "component lifecycle",
        )
        policy = lifecycle["policy"]
        if not isinstance(policy, dict):
            raise ContractError("Component lifecycle policy must be an object")
        for field in ("featureLocalByDefault", "recurrenceOpensReviewOnly", "zeroConsumersOpensRetirementReviewOnly"):
            if policy.get(field) is not True:
                raise ContractError(f"Component lifecycle policy must enable {field}")
        automation_denials = policy.get("automationMayNot")
        if not isinstance(automation_denials, list) or not REQUIRED_AUTOMATION_DENIALS.issubset(automation_denials):
            missing = sorted(REQUIRED_AUTOMATION_DENIALS - set(automation_denials or []))
            raise ContractError(f"Component lifecycle automationMayNot missing: {missing}")
        if not isinstance(policy.get("automationMay"), list):
            raise ContractError("Component lifecycle automationMay must be an array")
        if set(policy['automationMay']) & set(automation_denials):
            raise ContractError('Automation policy both allows and forbids the same action')

        freeze_line = lifecycle["freezeLine"]
        if not isinstance(freeze_line, dict):
            raise ContractError("Component lifecycle freezeLine must be an object")
        require(freeze_line, ["capturedAt", "publicComponentIds", "sharedPlacementPaths", "publishedStoryIds"], "component lifecycle freezeLine")
        for field in ("publicComponentIds", "sharedPlacementPaths", "publishedStoryIds"):
            if not isinstance(freeze_line[field], list) or len(freeze_line[field]) != len(set(freeze_line[field])):
                raise ContractError(f"Component lifecycle freezeLine {field} must be a unique array")

        approval_specs = {
            "promotionApprovals": ["id", "componentId", "candidateId", "owner", "approvedAt", "evidence", "candidateSnapshot"],
            "sharedPlacementApprovals": ["id", "path", "owner", "approvedAt", "semanticScope", "evidence"],
            "retirementApprovals": ["id", "componentId", "owner", "approvedAt", "consumerEvidence", "decision"],
            'deprecationApprovals': ['id', 'componentId', 'owner', 'approvedAt', 'evidence', 'decision'],
            'storyApprovals': ['id', 'path', 'storyIds', 'owner', 'approvedAt', 'evidence', 'decision'],
            'contractApprovals': ['id', 'componentId', 'owner', 'approvedAt', 'evidence', 'contractSha256', 'decision'],
        }
        approvals = {}
        for collection, fields in approval_specs.items():
            records = lifecycle.get(collection)
            if not isinstance(records, list) or not all(isinstance(item, dict) for item in records):
                raise ContractError(f"Component lifecycle {collection} must be an array of objects")
            unique(records, "id", collection)
            for record in records:
                require(record, fields, f"component lifecycle {collection} record")
                for field in ('id', 'owner'):
                    if not isinstance(record[field], str) or not record[field].strip():
                        raise ContractError(f'{collection} requires nonempty {field}')
                timestamp(record['approvedAt'], collection + ' approvedAt')
                evidence(root, record['consumerEvidence' if collection == 'retirementApprovals' else 'evidence'], collection)
                expected_decision = {'retirementApprovals': 'retire', 'deprecationApprovals': 'deprecate',
                                     'storyApprovals': 'publish-story', 'contractApprovals': 'change-contract'}.get(collection)
                if expected_decision and record['decision'] != expected_decision:
                    raise ContractError(f'{collection} requires decision={expected_decision}')
                if collection in {'sharedPlacementApprovals', 'storyApprovals'}:
                    relative_path(record['path'])
                if collection == 'storyApprovals' and (not isinstance(record['storyIds'], list) or not record['storyIds']):
                    raise ContractError('Story approval requires explicit nonempty storyIds')
                if collection == 'contractApprovals' and not re.fullmatch(r'[0-9a-f]{64}', record['contractSha256']):
                    raise ContractError('Contract approval requires SHA256 digest')
                if collection == 'promotionApprovals':
                    current_candidate = next((c for c in candidate_records if c['id'] == record['candidateId']), None)
                    if not current_candidate or current_candidate['status'] != 'review' or record['candidateSnapshot'] != current_candidate:
                        raise ContractError('Promotion requires exact review-status candidate snapshot; supersede rejected decisions explicitly')
            approvals[collection] = records

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
                if component.get('framework') not in manifest['frameworks']:
                    raise ContractError('Ready component framework is not declared supported')
                if family["lifecycle"] != "current" or family["readiness"] != "ready":
                    raise ContractError(f"Ready selection conflicts with inventory lifecycle/readiness: {component['id']}")
                validate_ready(component, root)
                if component['verification']['revision'] != release.get('revision'):
                    raise ContractError('Ready component verification is for another release revision')
                story_index_path = manifest['repositoryPolicy'].get('storyIndex')
                if not story_index_path:
                    raise ContractError('Ready record requires actual built Storybook index')
                story_index = load_json(safe_path(root, story_index_path))
                if not set(component['storyIds']).issubset(story_index.get('entries', {})):
                    raise ContractError(f"Ready component references nonexistent story: {component['id']}")
                if context_by_id[component["id"]].get("contextFile") != component["contextFile"]:
                    raise ContractError(f"Context path mismatch for {component['id']}")
                ready_ids.add(component["id"])
            story_ids.extend(component.get("storyIds", []))

        public_ids = {component["id"] for component in components}
        promotion_by_component = {record["componentId"]: record for record in approvals["promotionApprovals"]}
        retirement_by_component = {record["componentId"]: record for record in approvals["retirementApprovals"]}
        frozen_public_ids = set(freeze_line["publicComponentIds"])
        for component_id in sorted(public_ids - frozen_public_ids):
            approval = promotion_by_component.get(component_id)
            if not approval:
                raise ContractError(f"New public component lacks promotion approval: {component_id}")
            if approval["candidateId"] not in candidate_ids:
                raise ContractError(f"Promotion approval references unknown private candidate: {component_id}")
        for component_id in sorted(frozen_public_ids - public_ids):
            if component_id not in retirement_by_component:
                raise ContractError(f"Frozen public component was removed without retirement approval: {component_id}")

        leaked_candidate_ids = candidate_ids.intersection(context_by_id).difference(public_ids)
        if leaked_candidate_ids:
            raise ContractError(f"Private candidates leaked into public agent context: {sorted(leaked_candidate_ids)}")
        if set(context_by_id) != public_ids:
            raise ContractError('Context index must match public API records exactly')

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
            expiry = timestamp(exception['expiresAt'], 'exception expiry', future=True)
            if exception['status'] not in {'active', 'resolved'}:
                raise ContractError('Exception status must be active or resolved')
            if exception['status'] == 'active' and expiry <= dt.datetime.now(dt.timezone.utc):
                raise ContractError(f"Expired active exception: {exception['id']}")
        if not isinstance(release["checksums"], dict) or not release["checksums"]:
            raise ContractError("Release requires artifact checksums")
        if release['checksums'] != authoring_hashes(directory, manifest):
            raise ContractError('Authoring checksum coverage or content mismatch; refresh exact required artifacts')

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

        if args.base_ref:
            from policy import check_policy
            check_policy(root, args.directory, args.base_ref, manifest, lifecycle, public_api, inventory)
        print(
            json.dumps(
                {
                    'schemaValid': True,
                    'repositoryPolicy': 'configured-scope-passed' if args.base_ref else 'not-run',
                    'approvalAuthenticity': 'requires-protected-review',
                    'runtimeAndVisualAcceptance': 'not-executed-by-this-checker',
                    "version": manifest["version"],
                    "inventory": len(families),
                    "declaredReady": len(ready_ids),
                    "review": len(components) - len(ready_ids),
                    "componentCandidates": len(candidate_records),
                    "promotionApprovals": len(approvals["promotionApprovals"]),
                    "sharedPlacementApprovals": len(approvals["sharedPlacementApprovals"]),
                    "retirementApprovals": len(approvals["retirementApprovals"]),
                    "recipes": len(recipes.get("recipes", [])),
                    "contentEntries": len(content_entries),
                    "ruleExceptions": len(exceptions),
                    "openDecisions": sum(1 for item in decisions.get("decisions", []) if item.get("status") == "open"),
                },
                indent=2,
            )
        )
        return 0
    except (ContractError, KeyError, TypeError, ValueError, OSError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
