# Batch 7 consensus robustness experiment v1

## Research questions

1. How stable is a weighted consensus synthesis when the model, prompt, opinion
   order and inputs are unchanged?
2. Does reversing the order of the 14 opinions materially change the assigned
   weights, calculated 20-quarter path or narrative?
3. Does disclosing each opinion's source model change its assigned weight, and
   does the synthesizer give more weight to opinions from its own model family?
4. Do those effects differ between assets whose source forecasts agree and
   assets whose source forecasts are dispersed?

This is a research-only experiment. Its requests and results stay in local files.
It does not write `predictions_review_and_analysis`, consumer consensus tables or
Firestore publication inputs.

## Asset selection

The eligible universe contains 189 Batch 7 equities with exactly 12 valid Gemini
3.8 Flash opinions, one valid Claude Opus 5 opinion, one valid GPT-6 Astra opinion,
and 20 parsed forecast steps per opinion.

For each asset:

- `terminal_sign_agreement` is the largest positive/negative/zero share across
  the 14 five-year compounded opinion returns.
- `mean_step_sign_agreement` is the mean, over 20 quarters, of the largest
  positive/negative/zero share among the 14 quarterly returns.
- `terminal_iqr_percentile` is the cross-sectional percentile rank of the IQR of
  the 14 five-year compounded returns.
- `consistency_score = 0.50 * terminal_sign_agreement + 0.30 *
  mean_step_sign_agreement + 0.20 * (1 - terminal_iqr_percentile)`.
- `dispersion_score = 0.40 * (1 - terminal_sign_agreement) + 0.30 *
  (1 - mean_step_sign_agreement) + 0.30 * terminal_iqr_percentile`.

The ten highest consistency scores were Deutsche Telekom, Visa, Midea, Linde,
Marsh McLennan, Ping An, Haier Smart Home, Thales, IBM and SAP. The ten highest
dispersion scores were POET Technologies, NuScale Power, Nebius, Eos Energy,
Kratos Defense, Moderna, EVgo, Recursion Pharmaceuticals, Oklo and Archer Aviation.

Market capitalization at the 18 September 2026 close is the reproducible
recognition/scale proxy within each top-ten list. The experiment selects:

| Cohort | Asset | Batch 7 rank | Selection market cap |
| --- | --- | ---: | ---: |
| Directionally consistent | Visa (`V.NYSE`) | 2 | $676.04B |
| Directionally consistent | SAP (`SAP.XETRA`) | 10 | $241.74B |
| Directionally consistent | IBM (`IBM.NYSE`) | 9 | approximately $224B |
| Forecast dispersed | Nebius (`NBIS.NASDAQ`) | 3 | $61.989B |
| Forecast dispersed | Moderna (`MRNA.NASDAQ`) | 6 | $61.574B |
| Forecast dispersed | Kratos Defense (`KTOS.NASDAQ`) | 5 | $8.91B |
| Fixed reference | Bitcoin (`BTC-USD.CC`) | n/a | n/a |

Market-cap snapshot sources: [Visa](https://stockanalysis.com/stocks/v/market-cap/),
[SAP](https://companiesmarketcap.com/sap/marketcap/),
[IBM](https://capital.com/en-int/markets/shares/ibm-corp-share-price/market-cap),
[Nebius](https://www.financecharts.com/stocks/NBIS/summary/market-cap),
[Moderna](https://www.financecharts.com/stocks/MRNA/summary/market-cap), and
[Kratos](https://stockanalysis.com/stocks/ktos/market-cap/).

## Experimental cells

The Gemini operational baseline is the already successful v7 production result.
Three new Gemini cells and four new Astra cells are prepared for every asset.

| Synthesizer | Cell | Opinion order | Source model identity |
| --- | --- | --- | --- |
| Gemini 3.8 Flash | existing baseline | canonical | blinded |
| Gemini 3.8 Flash | same-order repeat | canonical | blinded |
| Gemini 3.8 Flash | reverse order | exact reverse of canonical | blinded |
| Gemini 3.8 Flash | model disclosed | canonical | disclosed |
| GPT-6 Astra | baseline primary | canonical | blinded |
| GPT-6 Astra | same-order repeat | canonical | blinded |
| GPT-6 Astra | reverse order | exact reverse of canonical | blinded |
| GPT-6 Astra | model disclosed | canonical | disclosed |

This produces 56 analyzed outputs: seven existing Gemini baselines, 21 new Gemini
requests and 28 new Astra requests.

The canonical input and Gemini generation settings are copied from the exact dry
run previews used for the successful production submissions. These include the
v7 response contract, web-search availability, temperature 0.2 for Gemini and a
65,536-token combined thinking/output ceiling. Astra uses high reasoning, the
same 65,536 output-token ceiling, the same system/user content and output
contract, and an available web-search tool.

The disclosure cell adds only `source_model_identity` to every opinion and
replaces the statement that identities are withheld with a statement that they
are supplied for the controlled experiment. It still directs the synthesizer to
judge evidence and causal reasoning rather than model prestige. The labels are
`Gemini 3.8 Flash`, `Claude Opus 5` and `GPT-6 Astra`.

## Preregistered comparisons

Primary numerical comparisons are paired within asset and synthesizer:

- L1 distance and Jensen-Shannon divergence between normalized weight vectors.
- Spearman rank correlation and agreement on the highest-weighted opinion.
- Quarterly-return path RMSE, maximum absolute quarterly difference and final
  compounded-return difference.
- Change in each source opinion's weight after model disclosure.
- Mean per-opinion change by source model family. Total family weight is not the
  primary statistic because the source set is intentionally unbalanced at
  12 Gemini, one Opus and one Astra opinion.

Secondary comparisons include structured-field agreement and semantic similarity
of the weighting assessment, disagreement summary and thesis. Results should be
reported separately for consistent stocks, dispersed stocks and Bitcoin, with
paired asset bootstrap intervals where the sample supports them.

## Interpretation limits

- Seven assets make this a focused controlled pilot, not a universal estimate of
  synthesizer behavior.
- One reverse-order treatment detects a large order sensitivity but does not map
  every possible permutation.
- The existing Gemini baseline preceded the repeat. Although the evidence cutoff
  is frozen, search retrieval and provider execution may vary with time.
- Gemini and Astra use different provider search systems and reasoning controls;
  cross-synthesizer differences are operational comparisons, not a pure model-
  architecture causal effect.
- Model disclosure can reveal bias or calibration changes, but forecast accuracy
  requires later realized outcomes and a separately preregistered scoring study.

## Execution and storage

Use `research_consensus_experiment.py`. `prepare` creates immutable request files,
input snapshots, hashes, the seven existing baselines and a manifest under
`research_runs/<experiment_id>/`. `submit`, `download` and `parse` operate only on
that directory. Existing receipts block accidental duplicate submission.
