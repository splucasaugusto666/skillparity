import contextlib
import io
import json
import unittest

from skillparity import main, summarize


class AggregateTests(unittest.TestCase):
    def test_demo_json(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            rc = main(['demo', '--summary-json'])
        self.assertEqual(rc, 1)
        self.assertEqual(json.loads(out.getvalue()), {
            'schema_version': 1, 'skills': 1, 'targets': 2,
            'counts': {'DRIFT': 2}, 'exit_code': 1})

    def test_no_identifiers_or_paths(self):
        report = {'baseline': 'private-source', 'labels': ['private-source', 'private-target'],
                  'skills': [{'skill': 'private-skill', 'roots': {
                      'private-source': {'status': 'MATCH'},
                      'private-target': {'status': 'DRIFT', 'changed': ['private-file']}}}]}
        result = summarize(report)
        self.assertNotIn('private', json.dumps(result))
        self.assertEqual(result['counts'], {'DRIFT': 1})

    def test_baseline_error_preserved(self):
        report = {'baseline': 'source', 'labels': ['source', 'target'],
                  'skills': [{'skill': 'x', 'roots': {'source': {'status': 'ERROR'},
                  'target': {'status': 'MISSING'}}}]}
        self.assertEqual(summarize(report)['exit_code'], 2)

    def test_empty(self):
        self.assertEqual(summarize({'baseline': 'source', 'labels': ['source', 'target'], 'skills': []}),
                         {'schema_version': 1, 'skills': 0, 'targets': 1, 'counts': {}, 'exit_code': 2})

    def test_all_statuses_counted(self):
        statuses = ['MATCH', 'DRIFT', 'MISSING', 'EXTRA', 'ABSENT', 'ERROR', 'UNVERIFIED']
        report = {'baseline': 'source', 'labels': ['source', 'target'],
                  'skills': [{'skill': s, 'roots': {'source': {'status': 'MATCH'},
                  'target': {'status': s}}} for s in statuses]}
        result = summarize(report)
        self.assertEqual(result['counts'], dict.fromkeys(statuses, 1))
        self.assertEqual(result['exit_code'], 2)

    def test_mutual_exclusion(self):
        for flag in ('--summary', '--json', '--html'):
            with self.subTest(flag=flag), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as cm:
                main(['demo', '--summary-json', flag])
            self.assertEqual(cm.exception.code, 2)
