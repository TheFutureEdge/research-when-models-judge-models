# When Models Judge Models

**How Source Identity and Disagreement Shape Multi-Agent Financial Forecasts**

Russlan Ramdowar, Future Edge Group FZE / iPulse AI. Contact:
russlan@ipulseai.com. ORCID: https://orcid.org/0009-0004-9311-6957.

This is version 1.0.0 of the companion research release, prepared on 2026-10-01.

- Repository: https://github.com/TheFutureEdge/research-when-models-judge-models
- Archival dataset: https://doi.org/10.5281/zenodo.23083356
- Licenses: CC BY 4.0 for original paper/research data; MIT for code.

The dataset and standalone PDF were published on Zenodo on 1 October 2026.
The paper has been submitted to arXiv in cs.MA and is awaiting processing and
moderation; a public arXiv identifier has not yet been assigned.
See `PUBLICATION_STATUS.md` for links and verification details.

## Start here

- `paper/When_Models_Judge_Models.pdf`: the typeset manuscript.
- `data/assets/`: all seven assets, each with fourteen source reports, the
  frozen source snapshot, and eight complete consensus outputs.
- `data/requests/`: all 56 original request bodies, including the seven
  primary Gemini baselines. These are for inspection, not submission.
- `data/parent_batch_usage.jsonl`: 6,816 recorded completed-release generation stages; provider usage with hashed task IDs.
- `data/source_configurations.csv`: framework, mode and model for each of the 98 reports.
- `data/history/`: historical sampling methodology, SQL, schemas and provenance; price CSVs are excluded.
- `data/initial_forecast_price_paths.csv`: all fourteen initial report paths,
  both original consensus paths and equal-report pooling in original price units.
- `analysis/recomputed/`: independently recomputed weights, paths,
  disclosure effects, comparisons, and validation results.
- `DATA_CARD.md` and `DATA_DICTIONARY.md`: interpretation and field definitions.
- `provenance/`: source integrity, parent counts, chronology, limitations.
- `protocol/`: original internal protocol and proposed future evaluation plan.
- `metadata/`: author information and deposit-ready descriptive metadata.
- `PUBLICATION_CHECKLIST.md`: actual remaining publication decisions.

## Reproduce the results

Python 3.10 or later is sufficient for the numerical analysis. No credentials,
network access, database, inference calls, or production code are required.

```sh
python3 code/reproduce.py
python3 code/prepare_history_comparison.py
python3 code/reproduce_parent_usage.py
python3 code/reproduce_matched_framework.py
```

Expected: 392 successful checks, 98 source reports, 56 consensus outputs,
784 allocation rows and 1,120 consensus-quarter rows. The script fails immediately
on an inconsistent input. It writes deterministic CSVs to `analysis/recomputed/`.
Use `--output /some/other/directory` to preserve the bundled reference files.

To regenerate the figures in an environment with NumPy and Matplotlib:

```sh
python3 code/make_figures.py
```

`requirements-figures.txt` records the tested versions. The manuscript is a
standard LaTeX article with an inline bibliography and external vector
figures. Compile `paper/main.tex` with Tectonic or a compatible TeX engine.
No shell escape, custom class, BibTeX run, or network data access is required.
The first TeX build may retrieve ordinary LaTeX packages.

## Scope in one paragraph

This deliberately selected panel contains Visa, SAP, IBM, Nebius, Moderna,
Kratos, and Bitcoin. Each has 12 Gemini 3.8 Flash reports, one Claude Opus 5
report, and one GPT-6 Astra report. Gemini and Astra each have a blinded baseline,
a blinded repeat, a reversed-order run and a model-disclosed run. Seven Gemini
baselines were reused and 49 requests were new. The six equities form the matched
treatment analysis; Bitcoin's reverse/disclosed prompts add a checklist and are
not clean label/order-only contrasts. All seven remain in baseline comparisons.

## Interpretation

These are archived forecasts, not verified facts or realized returns. Source
bands depict disagreement, not prediction intervals. Results do not establish
self-preference causally, model superiority, calibration, or trading performance.
No forecast has matured at the manuscript cutoff. Report weights are not
probabilities or a count of independent models. Twelve Gemini reports must not
be treated as equivalent to twelve independent model families.

## Integrity and release status

`SHA256SUMS.txt` covers the release files. `FILE_MANIFEST.json` gives paths,
sizes, hashes, and evidence roles. Source task identifiers in the parent ledger
are hashed; internal provider transport envelopes are excluded from the public
candidate. Third-party historical price CSVs are excluded. Their provenance and optional sampling code document the chart method without redistributing the underlying series. Full source narratives and
weight rationales are retained. The original private evidence remains separate.

Read `RIGHTS_AND_LICENSES.md` before redistribution. This release
does not itself grant a blanket license to all underlying content.

## Parent pipeline context

This study is a side experiment within the regular iPulse AI deep-analysis pipeline.
The completed Batch 7 release contains 426 assets, 5,964 source reports and 426
consensus syntheses. Nine frameworks, three extra Thinker variants and two
Universal Investor Researcher reports from other model families explain the
12 Gemini / 1 Astra / 1 Opus recipe. The completed-release footprint is
643,294,386 input and 141,182,977 generated tokens (including 102,562,383 reasoning).
It excludes retries, preview syntheses and the extra research requests. No ranking
of millions of assets or quality advantage follows from these workload counts.

## Optional historical chart reproduction

The manuscript's historical context used 8,711 daily observations sampled to
1,689 weekly closes. These daily, weekly and legacy monthly CSVs are not included
in the public edition. They are not needed to reproduce the reports, weights,
forecast paths, treatment contrasts, or parent-pipeline accounting.

With independently authorized historical prices in the documented schema, run
`python3 code/prepare_weekly_history.py` and then
`python3 code/make_history_figures.py`. Different historical snapshots or
adjustment conventions can produce different backgrounds. Archived coverage
counts are metadata, not a new validation of missing historical files.

The private source archive is separate and is not part of this repository.
