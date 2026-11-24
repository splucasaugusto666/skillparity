import contextlib
import io
import unittest
from skillparity import main, render_summary


class SummaryTests(unittest.TestCase):
    def test_demo_counts(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = main(['demo', '--summary'])
        self.assertEqual(rc, 1)
        self.assertEqual(out.getvalue().strip(), 'SkillParity | skills=1 | targets=2 | DRIFT=2 | exit=1')

    def test_summary_excludes_baseline_but_keeps_failure(self):
        report = {'baseline': 'source', 'labels': ['source', 'target'],
                  'skills': [{'skill': 'x', 'roots': {'source': {'status': 'ERROR'},
                  'target': {'status': 'UNVERIFIED'}}}]}
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            render_summary(report)
        self.assertIn('UNVERIFIED=1 | exit=2', out.getvalue())

    def test_empty_summary(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            render_summary({'baseline': 'source', 'labels': ['source', 'target'], 'skills': []})
        self.assertEqual(out.getvalue().strip(), 'SkillParity | skills=0 | targets=1 | exit=2')

    def test_json_summary_mutually_exclusive(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as cm:
            main(['demo', '--json', '--summary'])
        self.assertEqual(cm.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
