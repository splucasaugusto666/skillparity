"""Reproducible synthetic parity benchmark; no real skills are read."""
import argparse
import json
from pathlib import Path
import platform
import statistics
import sys
import tempfile
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from skillparity import compare, exit_code


def run(skills=100, repeats=5):
    if not 1 <= skills <= 1000 or not 1 <= repeats <= 20:
        raise ValueError('skills must be 1..1000 and repeats 1..20')
    with tempfile.TemporaryDirectory() as directory:
        roots = {label: Path(directory) / label for label in ('source', 'target')}
        for root in roots.values():
            for index in range(skills):
                skill = root / f'skill-{index:04d}'
                skill.mkdir(parents=True)
                (skill / 'SKILL.md').write_bytes(b'# Synthetic skill\n')
                (skill / 'reference.bin').write_bytes(b'x' * 4096)
        (roots['target'] / 'skill-0000/reference.bin').write_bytes(b'y' * 4096)
        timings = []
        for _ in range(repeats):
            start = time.perf_counter()
            report = compare(roots, 'source')
            timings.append(time.perf_counter() - start)
            statuses = [row['roots']['target']['status'] for row in report['skills']]
            if exit_code(report) != 1 or statuses.count('DRIFT') != 1 or statuses.count('MATCH') != skills - 1:
                raise RuntimeError('unexpected benchmark comparison result')
        return {'python': platform.python_version(), 'platform': platform.system(),
                'skills_per_root': skills, 'roots': 2, 'files_compared': skills * 4,
                'repeats': repeats, 'median_seconds': statistics.median(timings),
                'min_seconds': min(timings), 'max_seconds': max(timings),
                'expected_drift_detected': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skills', type=int, default=100)
    parser.add_argument('--repeats', type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(run(args.skills, args.repeats), indent=2))
