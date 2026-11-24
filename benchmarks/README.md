# Synthetic benchmark

Run from a trusted clone:
```sh
python benchmarks/benchmark.py --skills 100 --repeats 5
python benchmarks/benchmark.py --skills 1000 --repeats 5
```

Each catalog contains N skills and two small files per skill. Exactly one supporting file differs. Each timed comparison must identify one DRIFT and N-1 MATCH results. Fixture creation is excluded. All fixture data is temporary.

Observed on local Linux, Python 3.13.5 (2026-11-23, America/Sao_Paulo):

| Skills per root | Total files across two roots | Median seconds | Min | Max | Repeats |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 100 | 400 | 0.0164 | 0.0158 | 0.0198 | 5 |
| 1000 | 4000 | 0.1676 | 0.1634 | 0.2216 | 5 |

All ten timed comparisons detected the expected drift. Results are machine-specific, include potential filesystem caching, and do not establish comparative performance against other software or guarantee production throughput.
