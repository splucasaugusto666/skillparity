import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from skillparity import compare, load_config, main, MAX_CONFIG


class ConfigTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.config = self.base / 'parity.json'
        for label in ('source', 'target'):
            p = self.base / label / 'review'
            p.mkdir(parents=True)
            (p / 'SKILL.md').write_text('review', encoding='utf-8')
        self.config.write_text(json.dumps({'baseline': 'source', 'roots': {'source': 'source', 'target': 'target'}}), encoding='utf-8')

    def test_relative_roots(self):
        roots, baseline = load_config(self.config)
        self.assertEqual(roots['target'], self.base / 'target')
        self.assertEqual(baseline, 'source')

    def test_cli_config(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            rc = main(['check', '--config', str(self.config), '--summary'])
        self.assertEqual(rc, 0)
        self.assertIn('MATCH=1 | exit=0', out.getvalue())

    def test_duplicate_keys(self):
        self.config.write_text('{"baseline":"a","baseline":"b","roots":{}}', encoding='utf-8')
        with self.assertRaises(ValueError):
            load_config(self.config)

    def test_unknown_keys(self):
        self.config.write_text('{"baseline":"a","roots":{},"allow_target":["/"]}', encoding='utf-8')
        with self.assertRaises(ValueError):
            load_config(self.config)

    def test_size_limit(self):
        self.config.write_bytes(b' ' * (MAX_CONFIG + 1))
        with self.assertRaises(ValueError):
            load_config(self.config)

    def test_invalid_label(self):
        with self.assertRaises(ValueError):
            compare({'bad\nlabel': self.base, 'target': self.base}, 'bad\nlabel')

    def test_no_baseline_override(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(['check', '--config', str(self.config), '--baseline', 'target']), 2)

    def test_config_and_root_exclusive(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as cm:
            main(['check', '--config', str(self.config), '--root', 'a=b'])
        self.assertEqual(cm.exception.code, 2)
