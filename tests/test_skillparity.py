import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from skillparity import compare, exit_code, main, demo

class ParityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.roots = {k: self.base/k for k in ('source','target')}
        for p in self.roots.values(): p.mkdir()
    def skill(self, label, name='review', content='hello'):
        p = self.roots[label]/name
        p.mkdir()
        (p/'SKILL.md').write_text(content)
        return p
    def report(self): return compare(self.roots,'source')
    def cell(self, name='review', label='target'):
        return next(r['roots'][label] for r in self.report()['skills'] if r['skill']==name)
    def test_match(self):
        self.skill('source'); self.skill('target')
        self.assertEqual(exit_code(self.report()),0)
    def test_drift(self):
        a=self.skill('source'); b=self.skill('target',content='different')
        (a/'old.md').touch(); (b/'new.md').touch()
        c=self.cell(); self.assertEqual(c['status'],'DRIFT')
        self.assertEqual(c['changed'],['SKILL.md']); self.assertEqual(c['added'],['new.md']); self.assertEqual(c['removed'],['old.md'])
        self.assertEqual(exit_code(self.report()),1)
    def test_missing(self):
        self.skill('source'); self.assertEqual(self.cell()['status'],'MISSING')
    def test_extra(self):
        self.skill('target'); self.assertEqual(self.cell()['status'],'EXTRA')
    def test_empty(self): self.assertEqual(exit_code(self.report()),2)
    def link(self,p,target):
        try: p.symlink_to(target,target_is_directory=target.is_dir())
        except (OSError,NotImplementedError): self.skipTest('symlinks unavailable')
    def test_shared_symlink(self):
        p=self.skill('source'); self.link(self.roots['target']/'review',p)
        self.assertEqual(self.cell()['status'],'MATCH'); self.assertEqual(self.cell()['kind'],'symlink')
    def test_external_symlink(self):
        p=self.base/'external'; p.mkdir(); (p/'SKILL.md').touch()
        self.link(self.roots['target']/'review',p)
        self.assertEqual(self.cell()['status'],'ERROR'); self.assertEqual(exit_code(self.report()),2)
        r=compare(self.roots,'source',[p]); self.assertEqual(r['skills'][0]['roots']['target']['status'],'EXTRA')
    def test_broken_symlink(self):
        self.link(self.roots['target']/'review',self.base/'missing')
        self.assertEqual(exit_code(self.report()),2)
    def test_internal_symlink(self):
        a=self.skill('source'); b=self.skill('target'); self.link(b/'outside',a/'SKILL.md')
        self.assertEqual(self.cell()['status'],'ERROR')
    def test_nested_file(self):
        a=self.skill('source'); b=self.skill('target')
        for p in (a,b): (p/'refs').mkdir(); (p/'refs'/'a.md').write_text(str(p))
        self.assertEqual(self.cell()['changed'],['refs/a.md'])
    def test_unverified_baseline(self):
        a=self.skill('source'); self.skill('target'); self.link(a/'broken',self.base/'missing')
        self.assertEqual(self.cell()['status'],'UNVERIFIED')
    def test_demo(self): self.assertEqual(exit_code(demo()),1)
    def test_json_cli(self):
        self.skill('source'); self.skill('target')
        out=io.StringIO()
        with contextlib.redirect_stdout(out):
            rc=main(['check','--root',f"source={self.roots['source']}",'--root',f"target={self.roots['target']}",'--baseline','source','--json'])
        self.assertEqual(rc,0); self.assertEqual(json.loads(out.getvalue())['schema_version'],1)
    def test_duplicate_cli(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(['check','--root','x=a','--root','x=b','--baseline','x']),2)
    def test_no_mutation(self):
        a=self.skill('source'); self.skill('target'); before=(a/'SKILL.md').stat().st_mtime_ns
        self.report(); self.assertEqual((a/'SKILL.md').stat().st_mtime_ns,before)

if __name__=='__main__': unittest.main()
