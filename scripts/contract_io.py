"""Shared safe IO for private authoring and explicit public exports (stdlib)."""
from __future__ import annotations
import datetime as dt
import hashlib
import json
from pathlib import Path, PurePosixPath

SCHEMA_VERSION = 2
SUPPORT_FILES = ('AI_USAGE.md', 'llms.txt', 'component-contract-template.md')
REQUIRED_ARTIFACTS = ('inventory', 'publicApi', 'componentCandidates', 'componentLifecycle',
                      'contextIndex', 'tokens', 'content', 'rules', 'migrations',
                      'recipes', 'decisions', 'release')
REQUIREMENTS = ('failClosedSelection', 'selfContainedInterface', 'stableEntryPoint',
                'exactRevision', 'checksummedArtifacts', 'structuredContent',
                'expiringExceptions', 'privateComponentCandidates',
                'reviewedComponentLifecycle', 'measuredResponsiveFixtures',
                'referenceComparedVisualQa')

class ContractError(Exception):
    pass

def relative_path(value):
    if not isinstance(value, str) or not value or '\\' in value:
        raise ContractError(f'Invalid relative path: {value!r}')
    p = PurePosixPath(value)
    if p.is_absolute() or any(part in ('', '.', '..') for part in value.split('/')) or ':' in value:
        raise ContractError(f'Path must be a normalized in-root path: {value!r}')
    return value

def safe_path(root, value):
    relative_path(value)
    root = Path(root).resolve()
    path = root / value
    for parent in (path, *path.parents):
        if parent == root:
            break
        if parent.is_symlink():
            raise ContractError(f'Symlinks are not permitted in contract paths: {value}')
    if not path.resolve().is_relative_to(root):
        raise ContractError(f'Path escapes root: {value}')
    return path

def load_json(path):
    if not path.is_file():
        raise ContractError(f'Missing file: {path}')
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
    except (ValueError, UnicodeError) as exc:
        raise ContractError(f'Invalid JSON: {path}') from exc
    if not isinstance(value, dict):
        raise ContractError(f'Expected object: {path}')
    return value

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def object_sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()).hexdigest()

def timestamp(value, label, future=False):
    try:
        parsed = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
        if parsed.tzinfo is None:
            raise ValueError()
    except (AttributeError, TypeError, ValueError) as exc:
        raise ContractError(f'{label} requires an ISO timestamp with timezone') from exc
    if not future and parsed > dt.datetime.now(dt.timezone.utc):
        raise ContractError(f'{label} cannot be in the future')
    return parsed

def evidence(root, values, label):
    if not isinstance(values, list) or not values:
        raise ContractError(f'{label} requires non-empty local evidence paths')
    for value in values:
        if not safe_path(root, value).is_file():
            raise ContractError(f'{label} references missing evidence: {value}')

def authoring_files(directory, manifest):
    artifacts = manifest.get('artifacts', {})
    if not isinstance(artifacts, dict) or any(k not in artifacts for k in REQUIRED_ARTIFACTS):
        raise ContractError('Missing required manifest artifact; see portable-contract.md')
    paths = list(artifacts.values())
    if len(paths) != len(set(paths)):
        raise ContractError('Artifact paths must be unique')
    expected = {'manifest.json', *SUPPORT_FILES, *paths} - {artifacts['release']}
    for relative in expected:
        if not safe_path(directory, relative).is_file():
            raise ContractError(f'Missing authoring artifact: {relative}')
    return sorted(expected)

def authoring_hashes(directory, manifest):
    return {name: sha(safe_path(directory, name)) for name in authoring_files(directory, manifest)}

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
