"""Configured-scope policy checks. Protected CI selects the base and generates exports."""
from __future__ import annotations
import json
import re
import subprocess
from contract_io import ContractError, safe_path, load_json, sha, object_sha

def git(root, *args):
    result = subprocess.run(['git', *args], cwd=root, capture_output=True, text=True)
    if result.returncode:
        raise ContractError('Cannot read trusted git base: ' + result.stderr.strip())
    return result.stdout

def at_base(root, revision, path):
    safe_path(root, path)
    try:
        return json.loads(git(root, 'show', f'{revision}:{path}'))
    except ValueError as exc:
        raise ContractError('Trusted base artifact must be valid JSON') from exc

def source_files(root, roots):
    root = root.resolve()
    found = {}
    if not isinstance(roots, list):
        raise ContractError('Configured roots must be arrays')
    for directory in roots:
        path = safe_path(root, directory)
        if not path.is_dir():
            raise ContractError(f'Configured source root missing: {directory}')
        for child in sorted(path.rglob('*')):
            relative = child.relative_to(root).as_posix()
            safe_path(root, relative)
            if child.is_file():
                found[relative] = sha(child)
    return found

def contract_payload(component):
    return {k: v for k, v in component.items() if k != 'verification'}

def check_policy(root, directory, base_ref, manifest, lifecycle, public_api, inventory):
    if not re.fullmatch(r'[0-9a-f]{40}|[0-9a-f]{64}', base_ref):
        raise ContractError('Use a full immutable --base-ref supplied by protected CI')
    git(root, 'merge-base', '--is-ancestor', base_ref, 'HEAD')
    base_manifest = at_base(root, base_ref, directory + '/manifest.json')
    if base_manifest.get('schemaVersion') != 2:
        raise ContractError('Trusted base must complete the separately reviewed v2 migration')
    policy = manifest['repositoryPolicy']
    if not isinstance(policy, dict) or policy.get('configured') is not True:
        raise ContractError('POLICY_NOT_CONFIGURED: declare source/shared/story roots and generated export manifest; see portable-contract.md')
    if policy != base_manifest['repositoryPolicy']:
        raise ContractError('POLICY_SCOPE_CHANGED: review and land policy configuration separately; a change cannot shrink its own scan')
    def base_artifact(key):
        return at_base(root, base_ref, directory + '/' + base_manifest['artifacts'][key])
    base_lifecycle = base_artifact('componentLifecycle')
    if lifecycle['freezeLine'] != base_lifecycle['freezeLine']:
        raise ContractError('BASELINE_REWRITE: changing the freeze line is not approval')
    for key, current in lifecycle.items():
        if key.endswith('Approvals'):
            by_id = {r['id']: r for r in current}
            for old in base_lifecycle.get(key, []):
                if by_id.get(old['id']) != old:
                    raise ContractError('APPROVAL_REWRITE: append a new decision; preserve old receipts')
    previous = {r['id']: r for r in base_artifact('publicApi')['components']}
    current = {r['id']: r for r in public_api['components']}
    def approved(collection, field, value, predicate=lambda r: True):
        return any(r.get(field) == value and predicate(r) for r in lifecycle[collection])
    for name in set(current) - set(previous):
        if not approved('promotionApprovals', 'componentId', name):
            raise ContractError(f'PUBLIC_ADDITION: {name} needs promotion approval; keep the composition feature-local and register a private candidate')
    for name in set(previous) - set(current):
        if not approved('retirementApprovals', 'componentId', name):
            raise ContractError(f'PUBLIC_REMOVAL: {name} needs reachability evidence and retirement approval')
    old_families = {r['id']: r for r in base_artifact('inventory')['families']}
    for family in inventory['families']:
        old = old_families.get(family['id'])
        if old and old['lifecycle'] != family['lifecycle'] and family['lifecycle'] in {'deprecated', 'legacy'}:
            if not approved('deprecationApprovals', 'componentId', family['id']):
                raise ContractError(f"DEPRECATION: {family['id']} needs explicit owner decision")
    for name in set(previous) & set(current):
        if contract_payload(previous[name]) != contract_payload(current[name]):
            digest = object_sha(contract_payload(current[name]))
            if not approved('contractApprovals', 'componentId', name, lambda r: r['contractSha256'] == digest):
                raise ContractError(f'CONTRACT_CHANGE: {name} needs approval for the exact contract digest')

    if not policy.get('sourceRoots') or not policy.get('exportsManifest'):
        raise ContractError('POLICY_NOT_CONFIGURED: sourceRoots and exportsManifest are required')
    sources = source_files(root, policy['sourceRoots'])
    exports = load_json(safe_path(root, policy['exportsManifest']))
    release = load_json(safe_path(root, directory + '/' + manifest['artifacts']['release']))
    if exports.get('sourceDigest') != object_sha(sources) or exports.get('revision') != release['revision']:
        raise ContractError('STALE_EXPORT_OBSERVATION: rebuild the framework export adapter against current sources/revision')
    records = exports.get('exports')
    if not isinstance(records, list) or any(not isinstance(r, dict) for r in records):
        raise ContractError('Export observation needs an exports array')
    for record in records:
        component = current.get(record.get('componentId'))
        if not component or record.get('importPath') != component.get('importPath'):
            raise ContractError('UNREGISTERED_EXPORT: public export lacks matching approved component/import path')
    if {r.get('componentId') for r in records} != set(current):
        raise ContractError('EXPORT_COVERAGE: public records and observed exports differ')
    if len(records) != len(current):
        raise ContractError('EXPORT_COVERAGE: duplicate observed component IDs')
    index = load_json(safe_path(root, policy.get('storyIndex'))).get('entries')
    if not isinstance(index, dict):
        raise ContractError('STORY_INDEX: built index needs entries object')
    frozen_stories = set(base_lifecycle['freezeLine']['publishedStoryIds'])
    for story_id, entry in index.items():
        if not isinstance(entry, dict) or entry.get('id') != story_id:
            raise ContractError('STORY_INDEX: inconsistent entry ID')
        if story_id in frozen_stories:
            continue
        path = entry.get('importPath', '')
        path = path[2:] if path.startswith('./') else path
        safe_path(root, path)
        if not approved('storyApprovals', 'path', path, lambda r: story_id in r['storyIds']):
            raise ContractError(f'CANONICAL_STORY: published ID {story_id} needs explicit approval, even in an existing file')
    base_files = set(git(root, 'ls-tree', '-r', '--name-only', base_ref).splitlines())
    for roots_key, collection, label in [('sharedRoots', 'sharedPlacementApprovals', 'SHARED_PLACEMENT'), ('storyRoots', 'storyApprovals', 'CANONICAL_STORY')]:
        files = source_files(root, policy.get(roots_key, []))
        if roots_key == 'storyRoots':
            files = {p: h for p, h in files.items() if '.stories.' in p or p.endswith('.mdx')}
        for path in set(files) - base_files:
            if not approved(collection, 'path', path):
                raise ContractError(f'{label}: {path} lacks approval. Keep workflow UI feature-local or register a candidate; see portable-contract.md')
