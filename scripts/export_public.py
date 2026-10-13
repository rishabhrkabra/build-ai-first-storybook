#!/usr/bin/env python3
"""Generate a fresh allow-listed /ai tree, never deploy or publish authoring data."""
from __future__ import annotations
import argparse
from pathlib import Path
import re
import subprocess
import sys
from contract_io import (ContractError, safe_path, relative_path, load_json, sha,
                         object_sha, timestamp, dump)

GENERATED = {'current.json', 'catalog.json', 'context/index.json', 'llms.txt'}

def build_export(root, directory, output, base_ref=None):
    authoring = safe_path(root, directory)
    output = output.absolute()
    if output.exists() or output.is_symlink():
        raise ContractError('Output must be a new directory; refusing to overwrite or retain stale artifacts')
    if output.resolve().is_relative_to(authoring.resolve()) or authoring.resolve().is_relative_to(output.resolve()):
        raise ContractError('Output must be separate from private authoring data')
    # Resolve existing parent aliases (e.g. macOS /var) before creating a fresh tree.
    # The output itself may not exist or be a symlink, and containment is checked above.
    output = output.resolve()
    command = [sys.executable, str(Path(__file__).with_name('validate.py')), '--root', str(root), '--directory', directory]
    if base_ref:
        command.extend(['--base-ref', base_ref])
    checked = subprocess.run(command, capture_output=True, text=True)
    if checked.returncode:
        raise ContractError(checked.stderr.strip())
    manifest = load_json(authoring / 'manifest.json')
    api = load_json(safe_path(authoring, manifest['artifacts']['publicApi']))
    release = load_json(safe_path(authoring, manifest['artifacts']['release']))
    ready = [c for c in api['components'] if c['status'] == 'ready']
    dist = manifest['distribution']
    if ready and not base_ref:
        raise ContractError('Ready export requires trusted-base policy validation; no unverified selectable preview')
    if ready:
        approval = dist.get('catalogApproval')
        if not isinstance(approval, dict) or not isinstance(approval.get('owner'), str) or not approval['owner'].strip():
            raise ContractError('Ready export requires catalogApproval with a named owner')
        timestamp(approval.get('approvedAt'), 'catalog approval')
        if approval.get('sha256') != object_sha(api):
            raise ContractError('Catalog approval must match exact public API object digest')
    blocked = [safe_path(authoring, manifest['artifacts'][k]) for k in
               ('componentCandidates', 'componentLifecycle', 'inventory', 'decisions', 'release', 'publicApi', 'contextIndex')]
    blocked.append(authoring / 'manifest.json')
    blocked_hashes = {sha(p) for p in blocked}
    files, source_targets = {}, {}
    for item in dist['files']:
        if not isinstance(item, dict):
            raise ContractError('Distribution files must be reviewed mapping objects')
        source = safe_path(root, item.get('source'))
        target = relative_path(item.get('target'))
        if source in blocked or source.name.startswith('.env') or source.suffix in {'.pem', '.key'}:
            raise ContractError('Private or credential artifact cannot be distributed')
        if target in GENERATED or target.startswith('context/') or target in files:
            raise ContractError('Duplicate/reserved distribution target: ' + target)
        if not isinstance(item.get('owner'), str) or not item['owner'].strip():
            raise ContractError('Distribution mapping requires owner approval')
        timestamp(item.get('approvedAt'), 'file approval')
        if not source.is_file() or sha(source) != item.get('sha256'):
            raise ContractError('Missing or changed approved distributable: ' + item['source'])
        if sha(source) in blocked_hashes:
            raise ContractError('Copied private artifact cannot be distributed under another name')
        if item['source'] in source_targets:
            raise ContractError('One source must have one distribution target')
        files[target] = source.read_bytes()
        source_targets[item['source']] = target
    prefix = dist['basePath']
    def artifact_url(source):
        if source not in source_targets:
            raise ContractError('Ready component artifact is not explicitly distributable: ' + source)
        return prefix + '/' + source_targets[source]
    catalog, contexts = [], []
    for component in ready:
        component_id = component['id']
        if not re.fullmatch(r'[a-z0-9][a-z0-9_-]*', component_id):
            raise ContractError('Component IDs must be safe semantic URL segments')
        row = {k: component[k] for k in ('id', 'name', 'status', 'framework', 'importPath', 'storyIds', 'contract')}
        for key in ('source', 'styles', 'types'):
            row[key] = [artifact_url(p) for p in component[key]]
        row['docs'] = artifact_url(component['docs'])
        row['assets'] = [artifact_url(p) for p in component.get('assets', [])]
        row['contextFile'] = prefix + '/context/' + component_id + '.json'
        catalog.append(row)
        contexts.append({'id': component_id, 'contextFile': row['contextFile']})
        files['context/' + component_id + '.json'] = row
    files['catalog.json'] = {'schemaVersion': 2, 'version': release['version'], 'components': catalog,
                             'selectionPolicy': 'Ready records only; match target framework. Unknown capabilities are gaps.'}
    files['context/index.json'] = {'schemaVersion': 2, 'version': release['version'], 'components': contexts}
    files['llms.txt'] = (f'Fetch {prefix}/current.json for every new task. Follow its endpoint map and checksums. '
                         'Select only ready records for the target framework. Private inventory/candidates are not public APIs.\n').encode()
    output.mkdir(parents=True)
    for target, data in files.items():
        path = safe_path(output, target)
        if isinstance(data, dict):
            dump(path, data)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    checksums = {p: sha(safe_path(output, p)) for p in sorted(files)}
    endpoints = {'current': prefix + '/current.json', 'catalog': prefix + '/catalog.json',
                 'contextIndex': prefix + '/context/index.json', 'entryPoint': prefix + '/llms.txt'}
    for name in ('tokens', 'content', 'rules', 'migrations', 'recipes'):
        if name + '.json' in files:
            endpoints[name] = prefix + '/' + name + '.json'
    current = {k: release[k] for k in ('name', 'version', 'revision', 'releasedAt')}
    current.update(schemaVersion=2, access=dist['access'], status='candidate-release' if base_ref else 'empty-preview',
                   endpoints=endpoints, checksums=checksums)
    dump(output / 'current.json', current)
    return {'output': str(output), 'selectable': len(ready), 'deployed': False, 'status': current['status']}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--directory', default='ai-design-system')
    parser.add_argument('--output', required=True)
    parser.add_argument('--base-ref')
    args = parser.parse_args()
    try:
        result = build_export(Path(args.root).expanduser().resolve(), args.directory, Path(args.output).expanduser(), args.base_ref)
        import json
        print(json.dumps(result, indent=2))
        return 0
    except (ContractError, OSError, KeyError, TypeError, ValueError) as exc:
        print('EXPORT_BLOCKED: ' + str(exc), file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
