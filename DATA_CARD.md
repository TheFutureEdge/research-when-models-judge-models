# Dataset card

## Purpose and unit of observation

Study how an LLM synthesizer allocates influence to a fixed collection of reports,
and how that allocation affects a deterministic forecast. The experimental unit
for comparisons is an asset. The 14 reports and 20 steps within an asset are
dependent observations, not extra independent experiments.

## Contents

| Layer | Count | Meaning |
|---|---:|---|
| Assets | 7 | Six selected equities and Bitcoin |
| Frozen source reports | 98 | 14 per asset |
| Source-quarter forecasts | 1,960 | 98 reports x 20 quarters |
| Synthesizers | 2 | Recorded Gemini and Astra deployments |
| Conditions | 4 | Baseline, repeat, reverse, disclosed |
| Parsed synthesis outputs | 56 | 7 assets x 2 synthesizers x 4 conditions |
| Weight allocations | 784 | 56 outputs x 14 source reports |
| Consensus-quarter forecasts | 1,120 | 56 outputs x 20 quarters |
| Historical daily closes used privately | 8,711 | Not redistributed; contextual chart input only |
| Weekly observations used for charts | 1,689 | Price CSV excluded; sampling method and coverage documented |
| Archived price anchors | 7 | Frozen independently of the history query |
| Initial comparison price points | 2,499 | 7 assets x 17 paths x 21 points including anchors |
| Parent recorded generation stages | 6,816 | Successful release only; 6,390 logical tasks |
| Source configuration mappings | 98 | Framework, mode, model and hashed source task |
| New inference calls in paper preparation | 0 | Read-only telemetry recovery; no inference |

All source research narratives supplied to synthesis are retained in JSON, as are
the final rationales, submitted scores, normalized allocations and paths. These
are consensus-ready source reports, not a claim to possess every upstream
proposer's original provider response or tool trace.

## Collection and selection

The source forecasts were generated on 2026-09-20. Equity anchors are dated
2026-09-18; Bitcoin is anchored at 2026-09-20 00:00 UTC. The anchor date is not the
generation, issuance, completion, or publication date. Per-asset intended
evidence cutoffs are in `source_snapshot.json` and the prompt metadata table.

The archived selection protocol reports 189 eligible equities, with consistency
and dispersion rankings followed by a market-capitalization proxy. Full ranking
inputs and all historical proxy evidence were not recovered. The selected-source
matrices are reproducible, but the original candidate ranking is not fully
reproducible from this dataset. No random sampling is claimed.

The current history is a read-only BigQuery extract retrieved on 2026-10-01.
It spans five years before each anchor and is sampled to one last-observed close
per Monday-Sunday week. The actual daily date is retained. Lines break across
gaps longer than fourteen days; Nebius predecessor history and its 2022-2024
gap are explicitly identified. Daily close timestamps and currencies are null
in source rows; currencies are resolved from asset controls and checked against
the archived anchors. Stored close is not locally adjusted or rebased. The SQL and sampling code are included; daily, weekly and legacy monthly price
CSVs are excluded from the public release. Exact historical chart reproduction
requires independently authorized data. Point-in-time historical vintages are
not asserted. All original forecast paths remain available.


The separate parent ledger verifies 426 successful asset syntheses and 5,964
distinct source task IDs. Its hashed IDs support deduplication without publishing
the operational identifiers. It is not a complete ledger of submissions, retries,
failures, charges or upstream artifacts.

## Experimental differences

The archive records the synthesizer deployments as `gemini-3.8-flash` and
`gpt-6-astra`. Reports are attributed to Gemini 3.8 Flash (12), Claude Opus 5 (1)
and GPT-6 Astra (1). These names are archived metadata, not independently
established relative capability tiers. Model labels are explicitly withheld in
blinded conditions, but style or content may still reveal source identity.

All six equities pass substantive prompt invariance after accounting for the
intended disclosure and order changes. Bitcoin has an additional checklist in
reverse/disclosed wrappers; retain those records but do not interpret them as
isolated effects of the source label or report order. Cross-provider matched
experimental system/user content is identical, but provider controls and
retrieval behavior are not fixed. Baseline Gemini request bodies exactly equal
their respective repeat request bodies and match original hashes.

## Intended and unsuitable uses

Intended: offline replication, methodological audit, sensitivity analysis,
inspection of influence and rationales, and design of prospective replications.

Unsuitable: treating predictions as actual returns; using this selected sample
as a representative market benchmark; calling allocation changes proof of
discrimination or self-preference; ranking vendor quality or cost-effectiveness;
interpreting source intervals as calibrated uncertainty; deriving a trading
recommendation without independent validation.

## Known gaps

- Six reused equity baseline raw provider receipts and complete per-response
  billing/completion metadata are not recovered; numerical outputs and exact
  request bodies are present for all seven baselines. Bitcoin's raw baseline
  receipt was recovered and is retained in private evidence.
- Full 189-candidate ranking and exclusion ledger are missing.
- Complete original proposer prompts, all upstream tool traces, and complete
  426-asset forecast matrices are not part of this comparative release.
- Retrieval is not replayable from the source reports alone.
- Costs, provider credits, and complete funding declarations are unconfirmed.
- No external preregistration is verified; follow-up registry is a proposal.
- No forecast targets have matured as of 2026-10-01.

## Stewardship

Author/contact: Russlan Ramdowar, russlan@ipulseai.com,
https://orcid.org/0009-0004-9311-6957. Commercial interest: founder of the
organization developing the studied platform. AI-assisted preparation is disclosed
in the manuscript. See rights inventory before public redistribution.

## Recovered parent telemetry

Usage metadata was retrieved read-only on 2026-10-01 and matched to all 5,964
archived source task hashes and all 426 consensus assets. Opus has separate
research and forecast stages. Input counts include cache and repeated context;
generated counts include reasoning. Missing raw provider receipts do not prevent
reconciliation of retained usage fields, but billing and all-attempts coverage
remain incomplete. See `provenance/parent_usage_reconciliation.json`.

All fourteen framework/model/mode recipes occur for every parent asset. The
Universal Investor Researcher comparisons match framework and mode, not report
quality, tool behavior, or all execution settings. They are descriptive additions
from the archived results, not new model experiments.
