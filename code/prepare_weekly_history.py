"""Weekly last-observed-close sampling of the frozen BigQuery extract; no network."""
from pathlib import Path
import csv,json,datetime as dt,math,collections
R=Path(__file__).resolve().parents[1];H=R/'data/history'
if not (H/'bigquery_daily_closes.csv').exists():
    raise SystemExit('Historical prices are not redistributed. Supply an independently authorized daily CSV in the documented schema to run optional history sampling.')
with (H/'bigquery_daily_closes.csv').open() as f:daily=list(csv.DictReader(f))
assert len({(x['asset'],x['date']) for x in daily})==len(daily)
weekly=[];coverage=[]
for p in sorted((R/'data/assets').glob('*/source_snapshot.json')):
    asset=p.parent.name;s=json.loads(p.read_text());o=s['canonical_prompt_object']['asset_overview'];anchor=dt.date.fromisoformat(o['anchor_price_timestamp_utc'][:10]);start=anchor.replace(year=anchor.year-5);end=anchor.replace(year=anchor.year+5)
    assert (anchor-start)==(end-anchor)
    rows=sorted([x for x in daily if x['asset']==asset],key=lambda x:x['date']);bins={}
    for x in rows:
        date=dt.date.fromisoformat(x['date']);price=float(x['close'])
        assert start<=date<=anchor and math.isfinite(price) and price>0 and x['currency']==o['anchor_price_currency']
        if asset=='bitcoin':assert date<anchor
        week=date-dt.timedelta(days=date.weekday());bins[week]=x
    sampled=[];segment=0;previous=None;gaps=[]
    for week,x in sorted(bins.items()):
        date=dt.date.fromisoformat(x['date'])
        if previous and (date-previous).days>14:
            segment+=1;gaps.append(dict(last_observed_date=str(previous),next_observed_date=str(date),days_between=(date-previous).days))
        row=dict(asset=asset,week_start=str(week),plot_date=str(date),price=x['close'],currency=x['currency'],segment=segment,observation_type='weekly_last_observed_close',source='BigQuery stored close')
        sampled.append(row);weekly.append(row);previous=date
    assert sampled and len(sampled)<=263
    last=rows[-1];delta=float(last['close'])-float(o['anchor_price'])
    if asset!='bitcoin':assert last['date']==str(anchor) and abs(delta)<1e-9
    coverage.append(dict(asset=asset,window_start=str(start),forecast_anchor=str(anchor),forecast_end=str(end),daily_observations=len(rows),weekly_observations=len(sampled),first_observed=rows[0]['date'],last_observed=last['date'],last_close_minus_anchor=delta,anchor_is_separate=True,gaps=gaps,history_width_fraction=.5))
with (H/'historical_weekly_prices.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=weekly[0]);w.writeheader();w.writerows(weekly)
(R/'provenance/weekly_history_validation.json').write_text(json.dumps(dict(daily_observations=len(daily),weekly_observations=len(weekly),assets=coverage,method='Last available close per Monday-Sunday week, using actual date; no interpolation; final partial week included.'),indent=2)+'\n')
print('Validated',len(daily),'daily observations;',len(weekly),'weekly closes; all seven anchors centered at 50%.')
