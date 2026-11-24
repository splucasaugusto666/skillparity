#!/usr/bin/env python3
"""Read-only comparison of explicitly selected Agent Skills directories."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile

VERSION = '0.3.0'
MAX_FILE = 32 * 1024 * 1024
MAX_FILES = 10000
MAX_CONFIG = 65536
LABEL = re.compile(r'[A-Za-z0-9_-]+')


def within(path, roots):
    return any(path == r or r in path.parents for r in roots)


def inventory(folder):
    """Hash regular files; reject internal symlinks and special files."""
    entries = {}
    def fail(exc):
        raise exc
    for base, dirs, files in os.walk(folder, followlinks=False, onerror=fail):
        for name in sorted(dirs + files):
            p = Path(base) / name
            rel = p.relative_to(folder).as_posix()
            mode = p.lstat().st_mode
            if stat.S_ISDIR(mode):
                continue
            if not stat.S_ISREG(mode):
                raise ValueError(f'unsupported file type: {rel}')
            if len(entries) >= MAX_FILES:
                raise ValueError('file count limit exceeded')
            # O_NOFOLLOW protects the final path component where supported.
            fd = os.open(p, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0) | getattr(os, 'O_BINARY', 0))
            with os.fdopen(fd, 'rb') as f:
                st = os.fstat(f.fileno())
                if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_FILE:
                    raise ValueError(f'unsupported or oversized file: {rel}')
                h = hashlib.sha256()
                total = 0
                while chunk := f.read(65536):
                    total += len(chunk)
                    if total > MAX_FILE:
                        raise ValueError(f'file exceeds limit: {rel}')
                    h.update(chunk)
                entries[rel] = h.hexdigest()
    if 'SKILL.md' not in entries:
        raise ValueError('SKILL.md is missing or not a regular file')
    return entries


def scan(roots, allowed):
    catalogs = {}
    for label, path in roots.items():
        if not path.is_dir():
            raise ValueError(f'root is not a directory: {label}')
        catalog = {}
        for child in sorted(path.iterdir(), key=lambda p: p.name):
            if child.name.startswith('.'):
                continue
            link = child.is_symlink()
            if not link and (not child.is_dir() or not os.path.lexists(child / 'SKILL.md')):
                continue
            try:
                target = child.resolve(strict=True)
                if not within(target, allowed):
                    raise ValueError('symlink target is outside explicitly allowed roots')
                if not target.is_dir():
                    raise ValueError('skill target is not a directory')
                catalog[child.name] = {'kind': 'symlink' if link else 'directory', 'files': inventory(target)}
            except (OSError, RuntimeError, ValueError) as exc:
                # Do not emit raw OS exception paths.
                catalog[child.name] = {'kind': 'symlink' if link else 'directory', 'error': str(exc) if isinstance(exc, ValueError) else type(exc).__name__}
        catalogs[label] = catalog
    return catalogs


def compare(roots, baseline, allowed=()):
    if any(not isinstance(k, str) or not LABEL.fullmatch(k) for k in roots):
        raise ValueError('root labels must contain only letters, digits, underscores or hyphens')
    roots = {k: Path(v).expanduser().resolve(strict=True) for k, v in roots.items()}
    if baseline not in roots or len(roots) < 2:
        raise ValueError('provide at least two roots and an existing baseline label')
    allowed = list(roots.values()) + [Path(p).expanduser().resolve(strict=True) for p in allowed]
    catalogs = scan(roots, allowed)
    names = sorted(set().union(*(c.keys() for c in catalogs.values())))
    rows = []
    for name in names:
        reference = catalogs[baseline].get(name)
        cells = {}
        for label, catalog in catalogs.items():
            item = catalog.get(name)
            cell = {}
            if item is None:
                cell['status'] = 'MISSING' if reference is not None else 'ABSENT'
            elif 'error' in item:
                cell = {'status': 'ERROR', 'kind': item['kind'], 'error': item['error']}
            elif reference is None:
                cell = {'status': 'EXTRA', 'kind': item['kind']}
            elif 'error' in reference:
                cell = {'status': 'UNVERIFIED', 'kind': item['kind']}
            else:
                a, b = reference['files'], item['files']
                added, removed = sorted(b.keys()-a.keys()), sorted(a.keys()-b.keys())
                changed = sorted(k for k in a.keys() & b.keys() if a[k] != b[k])
                cell = {'status': 'DRIFT' if added or removed or changed else 'MATCH', 'kind': item['kind'], 'added': added, 'removed': removed, 'changed': changed}
            cells[label] = cell
        rows.append({'skill': name, 'roots': cells})
    return {'schema_version': 1, 'baseline': baseline, 'labels': list(roots), 'skills': rows}


def exit_code(report):
    statuses = {c['status'] for row in report['skills'] for c in row['roots'].values()}
    if statuses & {'ERROR', 'UNVERIFIED'} or not report['skills']:
        return 2
    return int(bool(statuses & {'DRIFT', 'MISSING', 'EXTRA'}))


def render(report):
    # JSON quoting prevents terminal control characters in untrusted file names.
    safe = lambda s: json.dumps(s, ensure_ascii=True)
    print('SkillParity | baseline:', safe(report['baseline']))
    for row in report['skills']:
        print(safe(row['skill']))
        for label, cell in row['roots'].items():
            print(f"  {label}: {cell['status']}" + (f" ({cell['kind']})" if 'kind' in cell else ''))
            for key in ('added', 'removed', 'changed'):
                for path in cell.get(key, []):
                    print(f'    {key}: {safe(path)}')
            if 'error' in cell:
                print('    error:', safe(cell['error']))
    if not report['skills']:
        print('No skills found; parity cannot be verified.')


def render_summary(report):
    counts = {}
    for row in report['skills']:
        for label, cell in row['roots'].items():
            if label == report['baseline']:
                continue
            status = cell['status']
            counts[status] = counts.get(status, 0) + 1
    details = ' | '.join(f'{key}={counts[key]}' for key in sorted(counts))
    print(f"SkillParity | skills={len(report['skills'])} | targets={len(report['labels']) - 1}"
          + (f' | {details}' if details else '') + f' | exit={exit_code(report)}')


def demo():
    with tempfile.TemporaryDirectory() as d:
        base = Path(d)
        for label in ('source', 'claude', 'codex'):
            p = base / label / 'review'
            p.mkdir(parents=True)
            (p / 'SKILL.md').write_text('# Review\nCheck tests.\n', encoding='utf-8')
            (p / 'checklist.md').write_text('Run tests.\n', encoding='utf-8')
        (base / 'codex/review/checklist.md').write_text('Run tests and lint.\n', encoding='utf-8')
        (base / 'claude/review/checklist.md').unlink()
        return compare({k: base/k for k in ('source','claude','codex')}, 'source')


def load_config(path):
    """Read a small, explicitly selected JSON config; reject ambiguous keys."""
    path = Path(path).expanduser().absolute()
    with path.open('rb') as stream:
        data = stream.read(MAX_CONFIG + 1)
    if len(data) > MAX_CONFIG:
        raise ValueError('config exceeds size limit')

    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate config key')
            result[key] = value
        return result

    try:
        config = json.loads(data.decode('utf-8'), object_pairs_hook=unique)
    except (UnicodeError, RecursionError):
        raise ValueError('invalid config encoding or nesting') from None
    if not isinstance(config, dict) or set(config) != {'baseline', 'roots'}:
        raise ValueError('config must contain exactly baseline and roots')
    roots, baseline = config['roots'], config['baseline']
    if not isinstance(roots, dict) or len(roots) < 2 or not isinstance(baseline, str) or baseline not in roots:
        raise ValueError('config needs two or more roots and an existing baseline')
    if any(not LABEL.fullmatch(k) or not isinstance(v, str) or not v for k, v in roots.items()):
        raise ValueError('config roots must use valid labels and nonempty paths')
    return {k: path.parent / Path(v).expanduser() for k, v in roots.items()}, baseline


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version=VERSION)
    sub = parser.add_subparsers(dest='command', required=True)
    for cmd in ('check','demo'):
        p = sub.add_parser(cmd)
        output = p.add_mutually_exclusive_group()
        output.add_argument('--json', action='store_true')
        output.add_argument('--summary', action='store_true', help='Print compact counts and exit status')
        if cmd == 'check':
            source = p.add_mutually_exclusive_group(required=True)
            source.add_argument('--root', action='append', metavar='LABEL=PATH')
            source.add_argument('--config', metavar='FILE', help='Read baseline and roots from a JSON file')
            p.add_argument('--baseline')
            p.add_argument('--allow-target', action='append', default=[], metavar='PATH')
    args = parser.parse_args(argv)
    try:
        if args.command == 'demo':
            report = demo()
        elif args.config is not None:
            if args.baseline is not None:
                raise ValueError('--baseline cannot be combined with --config')
            roots, baseline = load_config(args.config)
            report = compare(roots, baseline, args.allow_target)
        else:
            roots = {}
            for spec in args.root:
                label, sep, path = spec.partition('=')
                if not sep or not path or not LABEL.fullmatch(label) or label in roots:
                    raise ValueError('roots must use unique LABEL=PATH values')
                roots[label] = path
            report = compare(roots, args.baseline, args.allow_target)
        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=True))
        elif args.summary:
            render_summary(report)
        else:
            render(report)
        return exit_code(report)
    except (ValueError, OSError, RuntimeError) as exc:
        print('skillparity: ' + json.dumps(str(exc) if isinstance(exc, ValueError) else type(exc).__name__), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
