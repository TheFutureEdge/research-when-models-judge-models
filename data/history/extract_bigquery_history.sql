WITH assets AS (
SELECT 'bitcoin' AS asset, 'crypto_8f824f2d-c67f-55e7-8124-aa113059635d' AS asset_id, DATE '2026-09-20' AS anchor_date
UNION ALL
SELECT 'ibm' AS asset, 'equity_49812ec8-b303-53bb-91a7-8f6d041625cd' AS asset_id, DATE '2026-09-18' AS anchor_date
UNION ALL
SELECT 'kratos' AS asset, 'equity_98f68dc4-34bc-5a56-be20-3e3221770b59' AS asset_id, DATE '2026-09-18' AS anchor_date
UNION ALL
SELECT 'moderna' AS asset, 'equity_cdc413d2-1e92-5151-9d6b-1cbb7c013976' AS asset_id, DATE '2026-09-18' AS anchor_date
UNION ALL
SELECT 'nebius' AS asset, 'equity_6f455cc1-fa98-5ef5-8e6e-dbabed0ea6a1' AS asset_id, DATE '2026-09-18' AS anchor_date
UNION ALL
SELECT 'sap' AS asset, 'equity_e2379ea8-6a57-5013-be82-8037aafa519d' AS asset_id, DATE '2026-09-18' AS anchor_date
UNION ALL
SELECT 'visa' AS asset, 'equity_013d2cbc-1a8a-5434-a2ad-8d6d943eb036' AS asset_id, DATE '2026-09-18' AS anchor_date
) SELECT a.asset, p.asset_id, p.asset_symbol_pulse, p.currency_code, p.date_id, p.close_ts_utc, p.close, p.updated_at FROM `data-platform-436809.prod__dp_oracle_fincore_historic_market__datasets.fact_ohlcva_eod` p JOIN assets a USING(asset_id) WHERE p.date_id BETWEEN DATE '2021-09-18' AND DATE '2026-09-20' AND p.date_id>=DATE_SUB(a.anchor_date, INTERVAL 5 YEAR) AND (p.date_id<=a.anchor_date AND (a.asset!='bitcoin' OR p.date_id<a.anchor_date)) QUALIFY ROW_NUMBER() OVER(PARTITION BY p.asset_id,p.date_id ORDER BY p.updated_at DESC)=1 ORDER BY a.asset,p.date_id
