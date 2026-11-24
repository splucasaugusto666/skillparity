# Growth experiments

Hypothesis: a working one-command demo helps a developer understand the tool quickly.
Change: lead README with real terminal output and a local demo.
Baseline: not measured.
Metric: unique visitors and cloners when available, plus independent reproducible feedback; stars are a secondary signal.
Window: 7 days after publication; no causal attribution without comparable traffic.
Result: not measured.
Next action: recruit voluntary testers through relevant channels without spam or requests for artificial engagement.

## G-001 — official wheel first

Hypothesis: a prominent direct release install and a feedback link reduce friction and increase genuine trial and useful reports.
Change: README prioritizes the versioned wheel, demo and one early-adopter feedback thread; also corrects outdated CI statements.
Baseline: 1 star, 0 forks, 0 wheel downloads; visitor/cloner counts not measured. See PRODUCT_METRICS.md.
Primary metrics: wheel downloads, distinct external reproducible feedback. Secondary metrics: stars/forks.
Window: 7 days after publication of this change.
Result: pending observation. No causal claim without comparison data; concurrent external promotion and traffic changes can confound attribution.
Next action: review feedback and prioritize demonstrated issues. Do not manipulate engagement.

## G-002 — problem-specific adoption guide

Hypothesis: a concrete diagnostic for documented skill-link issues and a pinned CI example help qualified developers decide whether to try the tool.
Change: publish USE_CASES.md with source links, caveats and reproducible examples; pin integration examples to v1.0.0. No unsolicited comments on third-party issues.
Observation before this change: 1 star, 0 forks, 1 wheel download, 1 checksum download, 0 comments on feedback issue #1. Downloads do not establish distinct users. G-001 remains open; overlapping changes prevent independent causal attribution.
Primary outcome: independent technical feedback; secondary outcomes: wheel downloads and stars. Aspirational milestone: 50 genuine stars, not guaranteed. Review at 7 and 30 days.
