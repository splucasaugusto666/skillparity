import json
from pathlib import Path
import tempfile
import unittest

from skillparity_mcp import configured_check


class AdapterTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.workspace = self.base / 'workspace'
        for root in ('source', 'target'):
            skill = self.workspace / root / 'private-skill'
            skill.mkdir(parents=True)
            (skill / 'SKILL.md').write_text('same', encoding='utf-8')
        self.config = self.workspace / 'config.json'
        self.configure('target')

    def configure(self, target):
        self.config.write_text(json.dumps({'baseline': 'source', 'roots': {
            'source': 'source', 'target': target}}), encoding='utf-8')

    def test_match(self):
        self.assertEqual(configured_check(self.workspace, self.config)()['exit_code'], 0)

    def test_private_drift(self):
        (self.workspace / 'target/private-skill/SKILL.md').write_text('different', encoding='utf-8')
        result = configured_check(self.workspace, self.config)()
        self.assertEqual(result['counts'], {'DRIFT': 1})
        self.assertNotIn('private', json.dumps(result))

    def test_external_catalog(self):
        self.configure(str(self.base))
        with self.assertRaises(ValueError):
            configured_check(self.workspace, self.config)

    def test_external_config(self):
        outside = self.base / 'config.json'
        outside.write_bytes(self.config.read_bytes())
        with self.assertRaises(ValueError):
            configured_check(self.workspace, outside)

    def test_config_fixed_at_startup(self):
        check = configured_check(self.workspace, self.config)
        self.configure(str(self.base))
        self.assertEqual(check()['exit_code'], 0)

    def test_missing_root_after_startup(self):
        check = configured_check(self.workspace, self.config)
        (self.workspace / 'target').rename(self.workspace / 'moved')
        self.assertEqual(check(), {'schema_version': 1, 'exit_code': 2, 'error': 'incomplete verification'})
