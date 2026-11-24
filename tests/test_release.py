import contextlib
import io
import os
from pathlib import Path
import tempfile
import unittest
from skillparity import main, render_html, load_config


class ReleaseTests(unittest.TestCase):
    def test_demo_html(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(main(['demo', '--html']), 1)
        self.assertIn('<table>', out.getvalue())
        self.assertIn('DRIFT', out.getvalue())
        self.assertIn('Exit code: 1', out.getvalue())

    def test_html_escapes_untrusted_names(self):
        report = {'baseline': 'source', 'labels': ['source', 'target'],
                  'skills': [{'skill': '<script>alert(1)</script>', 'roots': {
                      'target': {'status': 'DRIFT', 'changed': ['<img src=x onerror=alert(1)>']}}}]}
        with contextlib.redirect_stdout(io.StringIO()) as out:
            render_html(report)
        self.assertNotIn('<script>', out.getvalue())
        self.assertNotIn('<img ', out.getvalue())
        self.assertIn('&lt;script&gt;', out.getvalue())

    def test_empty_html(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            render_html({'baseline': 'source', 'labels': ['source', 'target'], 'skills': []})
        self.assertIn('Exit code: 2', out.getvalue())

    def test_output_exclusive(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as cm:
            main(['demo', '--html', '--json'])
        self.assertEqual(cm.exception.code, 2)

    def test_directory_config(self):
        with tempfile.TemporaryDirectory() as d, self.assertRaises(ValueError):
            load_config(d)

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'FIFO unavailable')
    def test_fifo_config_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'fifo'
            os.mkfifo(p)
            with self.assertRaises(ValueError):
                load_config(p)
