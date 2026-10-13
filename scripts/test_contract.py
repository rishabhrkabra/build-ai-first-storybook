"""Offline regression tests for the portable contract, not app visual acceptance."""
from __future__ import annotations
import http.server
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from contract_io import load_json, dump, sha, object_sha
from policy import source_files, contract_payload

SCRIPTS = Path(__file__).parent
DATE = '2026-01-01T00:00:00+00:00'

class ContractTests(unittest.TestCase):
    def run_script(self, name, *args):
        return subprocess.run([sys.executable, str(SCRIPTS/name), *map(str,args)], capture_output=True, text=True)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.author = self.root/'ai-design-system'
        self.assertEqual(self.run_script('scaffold.py', '--target', self.root, '--name', 'Example').returncode, 0)
        for path in ['src/shared', 'build', 'proof']:
            (self.root/path).mkdir(parents=True)
        for path, text in [('src/example.tsx','export const Example = () => null;'), ('src/example.test.ts','test fixture'),
                           ('proof/owner.md','Synthetic owner receipt, not a real approval'), ('proof/result.md','Synthetic test output'),
                           ('proof/docs.md','Example docs'), ('proof/context.json','{}')]:
            (self.root/path).write_text(text)
        self.edit('manifest.json', lambda d: d.update(frameworks=['react'], repositoryPolicy={
            'configured':True, 'sourceRoots':['src'], 'sharedRoots':['src/shared'], 'storyRoots':['src'],
            'storyIndex':'build/index.json', 'exportsManifest':'build/exports.json'}))
        dump(self.root/'build/index.json', {'entries': {'example--default': {'id':'example--default','importPath':'./src/example.stories.tsx'}}})
        self.edit('component-lifecycle.json',lambda d:d['freezeLine'].update(publishedStoryIds=['example--default']))
        self.refresh()
        self.git('init', '-q')
        self.git('add', '.')
        self.git('-c', 'user.name=Synthetic Test', '-c', 'user.email=test@example.invalid', 'commit', '-qm', 'fixture baseline')
        self.base = self.git('rev-parse','HEAD').strip()
        self.edit('release.json', lambda d: d.update(revision=self.base))
        self.observe()

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, check=True, capture_output=True, text=True).stdout

    def edit(self, name, fn):
        data = load_json(self.author/name)
        fn(data)
        dump(self.author/name, data)

    def refresh(self):
        result = self.run_script('update_checksums.py', '--root', self.root)
        self.assertEqual(result.returncode, 0, result.stderr)

    def observe(self):
        api = load_json(self.author/'public-api.json')
        dump(self.root/'build/exports.json', {'revision':load_json(self.author/'release.json')['revision'],
             'sourceDigest':object_sha(source_files(self.root,['src'])),
             'exports':[{'componentId':c['id'],'importPath':c.get('importPath')} for c in api['components']]})

    def validate(self, policy=False, refresh=True):
        if refresh:
            self.refresh()
        return self.run_script('validate.py', '--root', self.root, *(['--base-ref',self.base] if policy else []))

    def reject(self, policy=False, message=None):
        result = self.validate(policy)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        if message:
            self.assertIn(message, result.stderr)

    def candidate(self):
        row = dict(id='example-candidate',status='review',occurrences=[{'module':'feature','path':'src/example.tsx'}],
                   semanticPurpose='An example', nonGoals=['Not a screen'], behaviorDifferences=[],responsive=['Container width'],
                   accessibility=['Semantic control'], appLogicBoundary='Data stays in app',owner='Synthetic owner',decisionNeeded='Review')
        self.edit('component-candidates.json',lambda d:d['candidates'].append(row))
        return row

    def public(self, approved=True):
        self.edit('inventory.json',lambda d:d['families'].append(dict(id='example',name='Example',sourceName='Example',
                  lifecycle='current',publication='public',readiness='review',source=['src/example.tsx'])))
        self.edit('public-api.json',lambda d:d['components'].append(dict(id='example',name='Example',status='review',importPath='@example/ui')))
        self.edit('context-index.json',lambda d:d['components'].append(dict(id='example')))
        if approved:
            candidate = self.candidate()
            self.edit('component-lifecycle.json',lambda d:d['promotionApprovals'].append(dict(id='promotion',componentId='example',
                      candidateId=candidate['id'],owner='Synthetic owner',approvedAt=DATE,evidence=['proof/owner.md'],candidateSnapshot=candidate)))
        self.observe()

    def ready(self):
        self.public()
        self.edit('inventory.json',lambda d:d['families'][0].update(readiness='ready'))
        self.edit('context-index.json',lambda d:d['components'][0].update(contextFile='proof/context.json'))
        verification = {'revision':self.base,'artifactSha256':'a'*64,'checks':{name:{'status':'passed','evidence':['proof/result.md']}
                        for name in ['build','interaction','accessibility','responsive','visual','consumer']}}
        self.edit('public-api.json',lambda d:d['components'][0].update(status='ready',framework='react',contextFile='proof/context.json',
                  source=['src/example.tsx'],styles=[],types=[],storyIds=['example--default'],docs='proof/docs.md',
                  tests=['src/example.test.ts'],authority=['proof/owner.md'],verification=verification,
                  contract={k:['Synthetic declared contract'] for k in ['states','behavior','responsive','accessibility','composition']}))
        self.observe()

    def mapping(self, source, target):
        row = dict(source=source,target=target,owner='Synthetic owner',approvedAt=DATE,sha256=sha(self.root/source))
        self.edit('manifest.json',lambda d:d['distribution']['files'].append(row))

    def checkpoint(self):
        self.refresh()
        self.git('add', '.')
        self.git('-c','user.name=Synthetic Test','-c','user.email=test@example.invalid','commit','-qm','approved fixture')
        self.base=self.git('rev-parse','HEAD').strip()
        self.edit('release.json',lambda d:d.update(revision=self.base))
        self.observe()

    def approve_catalog(self):
        digest=object_sha(load_json(self.author/'public-api.json'))
        self.edit('manifest.json',lambda d:d['distribution'].update(catalogApproval={'owner':'Synthetic','approvedAt':DATE,'sha256':digest}))

    def export(self, policy=False):
        self.refresh()
        return self.run_script('export_public.py','--root',self.root,'--output',self.root/'export',
                               *(['--base-ref',self.base] if policy else []))

    def test_empty_scaffold_is_not_readiness(self):
        result=self.validate()
        self.assertEqual(result.returncode,0,result.stderr)
        data=json.loads(result.stdout)
        self.assertEqual(data['declaredReady'],0)
        self.assertEqual(data['repositoryPolicy'],'not-run')

    def test_valid_configured_policy(self):
        self.assertEqual(self.validate(True).returncode,0)

    def test_new_public_without_approval(self):
        self.public(False)
        self.reject()

    def test_rewritten_baseline_cannot_bypass_policy(self):
        self.public(False)
        self.edit('component-lifecycle.json',lambda d:d['freezeLine']['publicComponentIds'].append('example'))
        self.reject(True,'BASELINE_REWRITE')

    def test_policy_scope_cannot_shrink(self):
        self.edit('manifest.json',lambda d:d['repositoryPolicy'].update(sharedRoots=[]))
        self.reject(True,'POLICY_SCOPE_CHANGED')

    def test_valid_promotion(self):
        self.public()
        result=self.validate(True)
        self.assertEqual(result.returncode,0,result.stderr)

    def test_unapproved_deprecation(self):
        self.public()
        self.checkpoint()
        self.edit('inventory.json',lambda d:d['families'][0].update(lifecycle='deprecated'))
        self.reject(True,'DEPRECATION')

    def test_unapproved_removal_from_trusted_api(self):
        self.public()
        self.checkpoint()
        self.edit('public-api.json',lambda d:d.update(components=[]))
        self.edit('context-index.json',lambda d:d.update(components=[]))
        self.observe()
        self.reject(True,'PUBLIC_REMOVAL')

    def test_prior_approval_cannot_be_rewritten(self):
        self.public()
        self.checkpoint()
        self.edit('component-lifecycle.json',lambda d:d['promotionApprovals'][0].update(owner='Different owner'))
        self.reject(True,'APPROVAL_REWRITE')

    def test_existing_contract_change_needs_exact_approval(self):
        self.public()
        self.checkpoint()
        self.edit('public-api.json',lambda d:d['components'][0].update(name='Updated example'))
        self.reject(True,'CONTRACT_CHANGE')

    def test_multiple_exact_contract_approvals_are_appendable(self):
        self.public()
        self.checkpoint()
        for n in [1,2]:
            self.edit('public-api.json',lambda d:d['components'][0].update(name=f'Example revision {n}'))
            digest=object_sha(contract_payload(load_json(self.author/'public-api.json')['components'][0]))
            self.edit('component-lifecycle.json',lambda d:d['contractApprovals'].append(dict(id=f'contract-{n}',componentId='example',
                      owner='Synthetic',approvedAt=DATE,evidence=['proof/owner.md'],contractSha256=digest,decision='change-contract')))
            result=self.validate(True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.checkpoint()

    def test_empty_approval_evidence(self):
        self.public()
        self.edit('component-lifecycle.json',lambda d:d['promotionApprovals'][0].update(evidence=[]))
        self.reject()

    def test_invalid_approval_date(self):
        self.public()
        self.edit('component-lifecycle.json',lambda d:d['promotionApprovals'][0].update(approvedAt='not-a-date'))
        self.reject()

    def test_rejected_candidate(self):
        self.public()
        self.edit('component-candidates.json',lambda d:d['candidates'][0].update(status='rejected'))
        self.reject()

    def test_empty_snapshot(self):
        self.public()
        self.edit('component-lifecycle.json',lambda d:d['promotionApprovals'][0].update(candidateSnapshot={}))
        self.reject()

    def test_keep_is_not_retire(self):
        self.edit('component-lifecycle.json',lambda d:d['retirementApprovals'].append(dict(id='keep',componentId='example',owner='Synthetic',
                  approvedAt=DATE,consumerEvidence=['proof/owner.md'],decision='keep')))
        self.reject()

    def test_candidate_cannot_leak_context(self):
        self.candidate()
        self.edit('context-index.json',lambda d:d['components'].append({'id':'example-candidate'}))
        self.reject()

    def test_unapproved_shared_file(self):
        (self.root/'src/shared/InvoiceHero.tsx').write_text('one-off')
        self.observe()
        self.reject(True,'SHARED_PLACEMENT')

    def test_unapproved_story(self):
        (self.root/'src/InvoiceHero.stories.tsx').write_text('one-off')
        self.observe()
        self.reject(True,'CANONICAL_STORY')

    def test_story_added_in_existing_file_is_gated(self):
        index=load_json(self.root/'build/index.json')
        index['entries']['example--new']={'id':'example--new','importPath':'./src/example.stories.tsx'}
        dump(self.root/'build/index.json',index)
        self.reject(True,'CANONICAL_STORY')

    def test_explicit_story_id_approval_passes(self):
        index=load_json(self.root/'build/index.json')
        index['entries']['example--new']={'id':'example--new','importPath':'./src/example.stories.tsx'}
        dump(self.root/'build/index.json',index)
        self.edit('component-lifecycle.json',lambda d:d['storyApprovals'].append(dict(id='story',path='src/example.stories.tsx',
                  storyIds=['example--new'],owner='Synthetic',approvedAt=DATE,evidence=['proof/owner.md'],decision='publish-story')))
        result=self.validate(True)
        self.assertEqual(result.returncode,0,result.stderr)

    def test_stale_export_observation(self):
        (self.root/'src/example.tsx').write_text('changed')
        self.reject(True,'STALE_EXPORT_OBSERVATION')

    def test_unregistered_export(self):
        d=load_json(self.root/'build/exports.json')
        d['exports'].append({'componentId':'rogue','importPath':'@rogue'})
        dump(self.root/'build/exports.json',d)
        self.reject(True,'UNREGISTERED_EXPORT')

    def test_contradictory_automation(self):
        self.edit('component-lifecycle.json',lambda d:d['policy']['automationMay'].append('merge'))
        self.reject()

    def test_empty_requirements(self):
        self.edit('manifest.json',lambda d:d.update(requirements={}))
        self.reject()

    def test_expired_exception(self):
        self.edit('rules.json',lambda d:d['rules'].append(dict(id='rule',principle='Rule',appliesWhen=[],requires=[],forbids=[],rationale='Test',severity='error',evidence=[])))
        self.edit('rules.json',lambda d:d['exceptions'].append(dict(id='old',ruleId='rule',reason='Test',owner='Synthetic',expiresAt='2000-01-01T00:00:00Z',status='active')))
        self.reject()

    def test_partial_checksums(self):
        self.refresh()
        self.edit('release.json',lambda d:d.update(checksums={'AI_USAGE.md':sha(self.author/'AI_USAGE.md')}))
        self.assertNotEqual(self.validate(refresh=False).returncode,0)

    def test_path_traversal(self):
        self.edit('manifest.json',lambda d:d['artifacts'].update(tokens='../tokens.json'))
        self.assertNotEqual(self.run_script('validate.py','--root',self.root).returncode,0)

    def test_symlink_artifact(self):
        path=self.author/'tokens.json'
        data=path.read_bytes()
        path.unlink()
        (self.root/'other.json').write_bytes(data)
        path.symlink_to(self.root/'other.json')
        self.assertNotEqual(self.run_script('validate.py','--root',self.root).returncode,0)

    def test_v1_fails_with_migration_message(self):
        self.edit('manifest.json',lambda d:d.update(schemaVersion=1))
        result=self.run_script('validate.py','--root',self.root)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('migrate v1',result.stderr)

    def test_unsupported_framework(self):
        self.ready()
        self.edit('public-api.json',lambda d:d['components'][0].update(framework='vue'))
        self.reject()

    def test_missing_test(self):
        self.ready()
        self.edit('public-api.json',lambda d:d['components'][0].update(tests=['missing.test.ts']))
        self.reject()

    def test_missing_story(self):
        self.ready()
        self.edit('public-api.json',lambda d:d['components'][0].update(storyIds=['missing-story']))
        self.reject()

    def test_unrun_gate(self):
        self.ready()
        self.edit('public-api.json',lambda d:d['components'][0]['verification']['checks']['visual'].update(status='skipped'))
        self.reject()

    def test_ready_export_requires_policy(self):
        self.ready()
        self.assertNotEqual(self.export().returncode,0)

    def test_ready_export_requires_catalog_approval(self):
        self.ready()
        result=self.export(True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('catalogApproval',result.stderr)

    def test_positive_ready_export_is_allowlisted(self):
        self.ready()
        self.mapping('src/example.tsx','source/example.tsx')
        self.mapping('proof/docs.md','docs/example.md')
        self.approve_catalog()
        result=self.export(True)
        self.assertEqual(result.returncode,0,result.stderr)
        output=self.root/'export'
        row=load_json(output/'catalog.json')['components'][0]
        self.assertEqual(row['source'],['/ai/source/example.tsx'])
        self.assertEqual(row['storyIds'],['example--default'])
        self.assertNotIn('authority',row)
        self.assertNotIn('verification',row)
        self.assertEqual(load_json(output/'context/example.json'),row)
        for path,digest in load_json(output/'current.json')['checksums'].items():
            self.assertEqual(sha(output/path),digest)

    def test_copied_private_file_is_denied(self):
        (self.root/'proof/disguised.json').write_bytes((self.author/'component-lifecycle.json').read_bytes())
        self.mapping('proof/disguised.json','disguised.json')
        result=self.export()
        self.assertNotEqual(result.returncode,0)
        self.assertIn('Copied private artifact',result.stderr)

    def test_second_framework_profile_and_changed_catalog(self):
        self.ready()
        self.edit('manifest.json',lambda d:d.update(frameworks=['web-components']))
        self.edit('public-api.json',lambda d:d['components'][0].update(framework='web-components',name='BrandMark'))
        self.edit('manifest.json',lambda d:d['distribution'].update(access='authenticated',basePath='/design/ai'))
        self.mapping('src/example.tsx','source/brand-mark.js')
        self.mapping('proof/docs.md','docs/brand-mark.md')
        self.approve_catalog()
        self.edit('public-api.json',lambda d:d['components'][0].update(name='Changed after approval'))
        self.assertNotEqual(self.export(True).returncode,0)
        self.approve_catalog()
        result=self.export(True)
        self.assertEqual(result.returncode,0,result.stderr)
        # This is framework metadata portability, not a web-component build test.
        self.assertEqual(load_json(self.root/'export/catalog.json')['components'][0]['framework'],'web-components')

    def test_empty_export_has_one_truth_and_no_private_files(self):
        self.candidate()
        result=self.export()
        self.assertEqual(result.returncode,0,result.stderr)
        output=self.root/'export'
        paths={p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}
        self.assertEqual(paths,{'current.json','catalog.json','context/index.json','llms.txt'})
        self.assertEqual(load_json(output/'catalog.json')['components'],[])
        self.assertEqual(load_json(output/'current.json')['status'],'empty-preview')
        self.assertEqual(set(load_json(output/'current.json')['checksums']),paths-{'current.json'})

    def test_explicit_private_file_is_denied(self):
        self.mapping('ai-design-system/component-candidates.json','innocent.json')
        self.assertNotEqual(self.export().returncode,0)

    def test_stale_distributable_approval(self):
        self.mapping('src/example.tsx','source/example.tsx')
        (self.root/'src/example.tsx').write_text('changed')
        self.assertNotEqual(self.export().returncode,0)

    def test_export_refuses_overwrite(self):
        (self.root/'export').mkdir()
        self.assertNotEqual(self.export().returncode,0)

    def test_nested_base_url_and_http_private_canary(self):
        self.edit('manifest.json',lambda d:d['distribution'].update(basePath='/storybook/ai'))
        self.assertEqual(self.export().returncode,0)
        output=self.root/'export'
        self.assertEqual(load_json(output/'current.json')['endpoints']['catalog'],'/storybook/ai/catalog.json')
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self,*a,**kw):super().__init__(*a,directory=str(output),**kw)
            def log_message(self,*a):pass
            def do_GET(self):
                if not self.path.startswith('/storybook/ai/'):
                    self.send_error(404)
                    return
                self.path=self.path[len('/storybook/ai'):]
                super().do_GET()
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
        thread=threading.Thread(target=server.serve_forever,daemon=True)
        thread.start()
        try:
            base=f'http://127.0.0.1:{server.server_port}'
            for url in load_json(output/'current.json')['endpoints'].values():
                with urllib.request.urlopen(base+url) as response:
                    self.assertEqual(response.status,200)
            for path in ['component-candidates.json','component-lifecycle.json','manifest.json']:
                with self.assertRaises(urllib.error.HTTPError) as error:
                    urllib.request.urlopen(base+'/storybook/ai/'+path)
                self.assertEqual(error.exception.code,404)
        finally:
            server.shutdown(); server.server_close(); thread.join()

if __name__=='__main__':unittest.main()
