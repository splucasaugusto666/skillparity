import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ci_check import check, main


@unittest.skipUnless(os.name == 'posix', 'composite action requires POSIX')
class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.workspace = self.base / 'workspace'
        self.workspace.mkdir()
        for name in ('source', 'target'):
            skill = self.workspace / name / 'review'
            skill.mkdir(parents=True)
            (skill / 'SKILL.md').write_text('review', encoding='utf-8')
        self.config = self.workspace / 'skillparity.json'
        self.write_config('source', 'target')

    def write_config(self, source, target):
        self.config.write_text(json.dumps({'baseline': 'source', 'roots': {
            'source': str(source), 'target': str(target)}}), encoding='utf-8')

    def invoke(self, config='skillparity.json'):
        with patch.dict(os.environ, {'GITHUB_WORKSPACE': str(self.workspace),
                                    'SKILLPARITY_CONFIG': config}), \
                contextlib.redirect_stdout(io.StringIO()) as out, \
                contextlib.redirect_stderr(io.StringIO()) as err:
            rc = main()
        return rc, out.getvalue(), err.getvalue()

    def test_match(self):
        rc, out, _ = self.invoke()
        self.assertEqual(rc, 0)
        self.assertIn('MATCH=1 | exit=0', out)

    def test_drift(self):
        (self.workspace / 'target/review/SKILL.md').write_text('changed', encoding='utf-8')
        rc, out, _ = self.invoke()
        self.assertEqual(rc, 1)
        self.assertIn('DRIFT=1 | exit=1', out)
        self.assertNotIn('review', out)

    def test_outside_config(self):
        outside = self.base / 'outside.json'
        outside.write_text(self.config.read_text(), encoding='utf-8')
        self.assertEqual(self.invoke(str(outside))[0], 2)

    def test_outside_root(self):
        self.write_config('source', self.base)
        rc, _, err = self.invoke()
        self.assertEqual(rc, 2)
        self.assertNotIn(str(self.base), err)

    def test_symlink_root_escape(self):
        try:
            (self.workspace / 'escape').symlink_to(self.base, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest('symlinks unavailable')
        self.write_config('source', 'escape')
        self.assertEqual(self.invoke()[0], 2)

    def test_config_symlink_escape(self):
        outside = self.base / 'outside.json'
        outside.write_text(self.config.read_text(), encoding='utf-8')
        try:
            (self.workspace / 'escape.json').symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest('symlinks unavailable')
        self.assertEqual(self.invoke('escape.json')[0], 2)

    def test_external_skill_link(self):
        outside = self.base / 'outside-skill'
        outside.mkdir()
        (outside / 'SKILL.md').write_text('private', encoding='utf-8')
        try:
            (self.workspace / 'target/escape').symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest('symlinks unavailable')
        rc, out, err = self.invoke()
        self.assertEqual(rc, 2)
        self.assertNotIn(str(outside), out + err)
        self.assertNotIn('private', out + err)

    def test_missing_config(self):
        self.assertEqual(self.invoke('missing.json')[0], 2)

    def test_special_filename(self):
        self.assertEqual(self.invoke('$(echo unsafe).json')[0], 2)
