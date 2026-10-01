# Data dictionary and numerical contract

## Canonical JSON

`data/assets/{asset}/source_snapshot.json` is the frozen input. The fourteen
records under `canonical_prompt_object.latest_asset_forecast_report.task_config_reports`
are the exact consensus-ready source reports. Each report has an `opinion_id`,
`investment_framework`, anchor, generation time, research references, investment
assessment, event analysis and `timeseries` (twenty dated quarterly returns).
`context.opinion_snapshot` is a parallel numeric snapshot, not a new forecast.

`data/assets/{asset}/source_reports/{opinion_id}.json` gives the same report
separately for convenience. Preserve opaque IDs when joining across conditions.

`data/assets/{asset}/consensus/{synthesizer}/{condition}.json` contains the complete
parsed consensus: submitted and normalized weights, rationale per opinion,
weighting assessment, disagreement summary, narrative fields, twenty-step path
and the deterministic calculation metadata. Its emitted narrative is model output,
not adjudicated ground truth. Null and empty fields remain as archived.

`data/requests/{provider}/{asset}/{condition}.json` is the original provider request
body. The seven Gemini `baseline_original.json` files were recovered independently
and hash-checked. The request names `base`, `repeat`, `reverse`, `disclosed`
correspond to the longer names below (`base` is the parsed `baseline_primary`); the primary
Gemini baseline is `baseline_original`, rather than a new experimental request.

## Tabular files

| File | Grain and key | Important fields |
|---|---|---|
| data/assets.csv | One asset; asset | Name, ticker, recorded cohort, anchor, selection proxy |
| Optional local input: data/history/bigquery_daily_closes.csv | Asset-date | Not bundled; stored close, instrument symbol, verified currency and source update timestamp |
| Optional local derivative: data/history/historical_weekly_prices.csv | Asset-week | Not bundled; last available actual close and date; segment changes at gaps over 14 days |
| data/initial_forecast_price_paths.csv | Asset-series-step | Source or consensus identity, original price, currency, date; step zero is the anchor |
| analysis/recomputed/cohort_source_diagnostics.csv | Asset | Terminal positive/negative counts, terminal and mean-quarter sign agreement, IQR, history coverage and anchor |
| data/source_paths.csv | Asset-opinion-step | source_model, framework, date, quarter_return_percent, cumulative_return_percent, normalized_price, scenario_rationale |
| data/consensus_paths.csv | Asset-synthesizer-condition-step | date, quarter_return_percent, cumulative_return_percent, predicted_price, scenario_rationale |
| analysis/recomputed/weights.csv | Asset-synthesizer-condition-opinion | weight, submitted_weight, source_model, framework, rationale |
| analysis/recomputed/runs.csv | Asset-synthesizer-condition | effective_n, one_year_return_percent, five_year_return_percent, path_pool_five_year_percent |
| analysis/recomputed/paired.csv | Asset-synthesizer-treatment | weight_TV, abs_one_year_pp, abs_five_year_pp, relative to original blinded baseline |
| analysis/recomputed/disclosure.csv | Asset-synthesizer-source family | family_n, baseline_weight, disclosed_weight, baseline_delta_pp, two_blind_delta_pp |
| analysis/recomputed/cross_synthesizer.csv | Asset-condition | weight_TV, signed Astra-minus-Gemini horizon differences |
| analysis/recomputed/source_spread.csv | Asset | Terminal positive/negative counts, range, IQR |
| analysis/recomputed/numerical_baselines.csv | Asset-method | Equal-report and equal-model quarter-pooling comparisons |
| analysis/recomputed/six_equity_summary.csv | Synthesizer-treatment | Descriptive unweighted means across six equities; excludes Bitcoin |
| analysis/audit/usage_and_retrieval.csv | New provider request | Recorded token fields and observable retrieval metadata counts |
| provenance/parent_asset_ledger.csv | Parent asset | Category, counts, hashed task IDs, source snapshot hash |

## Units and semantics

- A quarter return stored as `2.0` means 2 percent, not a decimal return of 2.
- Cumulative return compounds quarter returns; it is not their sum.
- A difference between 10% and 15% is 5 percentage points (pp).
- A weight of 0.13 means 13% of influence; it is not a 13% probability of correctness.
- `normalized_price` starts at 100 and multiplies it by cumulative growth.
- `predicted_price` uses the archived asset anchor and original currency.
- Prices exclude dividends and transaction costs. They are not portfolio returns.
- `effective_n = 1 / sum(weight**2)` counts equally weighted equivalents,
  not independent information sources.
- `weight_TV = sum(abs(treatment_weight - baseline_weight)) / 2`.
- IQR uses linear interpolation at the 25th and 75th percentiles (n-1 convention).
- Source `predicted_most_reasonable_pct_change` is a base-case point forecast;
  its identity as mean, median, or mode is not established.

## Historical context

The daily extraction contains 8,711 records; its weekly derivative contains 1,689.
Calendar weeks run Monday-Sunday. Select the last available observation and retain
its date; a weekly value is not a mean or interpolated price. Include the last
partial week. `segment` increments after gaps longer than fourteen days so plots
do not connect unobserved spans. Windows end at equity anchor dates and before
Bitcoin's anchor date. Source close timestamps are null. Currency is resolved
from asset controls and cross-checked with the frozen anchor. The seven anchors
and all 2,499 prediction-path points are unchanged. Each time axis places the
anchor exactly halfway between its five-year history and forecast endpoints.
Daily, weekly and legacy monthly price CSVs are not redistributed. The counts above describe the privately retained chart inputs, not files bundled in this edition.

## Conditions

`baseline_blinded`: original primary synthesis with explicit model labels withheld.
`same_order_repeat_blinded`: second blinded execution, same report presentation.
`reverse_order_blinded`: reversed report/checklist order, model labels withheld.
`model_disclosed`: canonical order with true source-model identities shown.

The long names identify the parsed outputs. See the request crosswalk above for
short execution names. The Bitcoin wrapper caveat applies to reverse/disclosed.

## Formula

Submitted nonnegative scores with positive sum are normalized to one. One
asset-specific vector applies to all twenty periods. Each period is the weighted
sum of source returns. The consensus compounds those period sums. Rounding of
the saved weights occurs to twelve decimals with a residual adjustment; exact
reproduction validates within 1e-9 for quarterly percentage returns and 1e-8
for cumulative percentage returns. Pooling completed paths is a separate
comparator and must not silently replace the deployed formula.

Token conventions differ: Astra reasoning tokens are included in output;
Gemini thinking tokens are separate from candidate output. Cached input is a
subset of input, not an additional quantity. The audit column `query_count`
is provider-specific: Astra counts web-search tool events (including open actions),
while Gemini counts exposed grounding queries. It must not be summed into a
cross-provider count of distinct queries.

## Parent usage and source configurations

- `data/parent_batch_usage.jsonl`: one recorded generation stage; key is layer, task_sha256, stage. Provider usage fields are retained, with transport identifiers omitted.
- `analysis/recomputed/parent_batch_usage.csv`: layer/model totals, logical tasks, stages, input_tokens, nonreasoning_output_tokens, reasoning_tokens, generated_tokens and total_tokens. The ALL row is a sum; do not sum it with its components.
- Gemini input includes cache; generated is candidates plus thoughts. Opus input is ordinary plus cache creation plus cache read; output already includes thinking. Astra output already includes reasoning. Generated is nonreasoning plus reasoning for all providers.
- `data/source_configurations.csv`: one of the 98 archived reports, with framework, model, mode and source task hash. The metadata is matched using the original source task ID.
- `analysis/recomputed/matched_framework_disclosure.csv`: six equities x two synthesizers x three Universal Investor Researcher source models. Deltas are absolute weight percentage points in the full fourteen-report ensemble.
- `analysis/recomputed/matched_framework_summary.csv`: unweighted means across the six equities for the preceding contrasts; not a quality-matched experiment.
