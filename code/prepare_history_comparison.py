"""Validate sampled weekly context; export original baseline paths in price units.
No inference, market-data requests, interpolation or retrospective forecast changes.
"""
from pathlib import Path
import csv,json,math
R=Path(__file__).resolve().parents[1];H=R/'data/history'
def read(p):
 with p.open() as f:return list(csv.DictReader(f))
def write(p,rows):
 with p.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
hist=read(H/'historical_weekly_prices.csv') if (H/'historical_weekly_prices.csv').exists() else []
coverage={x['asset']:x['weekly_observations'] for x in json.loads((R/'provenance/weekly_history_validation.json').read_text())['assets']}
manifest=json.loads((R/'data/experiment_manifest.json').read_text());rows=[];features=[];checks=[]
for a in manifest['assets']:
 s=json.loads((R/'data/assets'/a/'source_snapshot.json').read_text());ov=s['canonical_prompt_object']['asset_overview'];anchor=float(ov['anchor_price']);date=ov['anchor_price_timestamp_utc'][:10];currency=ov['anchor_price_currency'];rr=sorted(s['canonical_prompt_object']['latest_asset_forecast_report']['task_config_reports'],key=lambda x:x['opinion_id']);dates=[x['date'] for x in rr[0]['timeseries']]
 hh=[x for x in hist if x['asset']==a];weeks=hh
 if hist:
  assert weeks and all(x['plot_date']<=date and float(x['price'])>0 and x['currency']==currency for x in weeks)
  assert len({x['week_start'] for x in weeks})==len(weeks)
 matrix=[[float(x['predicted_most_reasonable_pct_change']) for x in r['timeseries']] for r in rr]
 def append(series_type,series_id,label,q):
  g=1.;rows.append(dict(asset=a,series_type=series_type,series_id=series_id,series_label=label,step=0,date=date,price=anchor,currency=currency))
  for step,(d,v) in enumerate(zip(dates,q),1):
   g*=1+v/100;rows.append(dict(asset=a,series_type=series_type,series_id=series_id,series_label=label,step=step,date=d,price=anchor*g,currency=currency))
 for i,r in enumerate(rr):
  assert [x['date'] for x in r['timeseries']]==dates
  append('source',r['opinion_id'],r['investment_framework'],matrix[i])
 for m,label in [('gemini_3_8_flash','Gemini 3.8 Flash'),('gpt_6_astra','GPT-6 Astra')]:
  obj=json.loads((R/'data/assets'/a/'consensus'/m/'baseline_blinded.json').read_text());append('consensus',m,label,[x['predicted_most_reasonable_pct_change'] for x in obj['consensus_timeseries']])
  result=[x for x in rows if x['asset']==a and x['series_id']==m and x['step']>0]
  assert all(abs(x['price']-y['predicted_price'])<1e-6 for x,y in zip(result,obj['consensus_timeseries']))
 append('baseline','equal_report','Equal-report quarter pool',[sum(r[t] for r in matrix)/14 for t in range(20)])
 terminal=[100*(math.prod(1+x/100 for x in r)-1) for r in matrix];spread=next(x for x in read(R/'analysis/recomputed/source_spread.csv') if x['asset']==a)
 features.append(dict(asset=a,cohort=s['selection']['cohort'],positive_terminal=sum(x>0 for x in terminal),negative_terminal=sum(x<0 for x in terminal),terminal_sign_agreement=max(sum(x>0 for x in terminal),sum(x<0 for x in terminal),sum(x==0 for x in terminal))/14,mean_quarter_sign_agreement=sum(max(sum(r[t]>0 for r in matrix),sum(r[t]<0 for r in matrix),sum(r[t]==0 for r in matrix))/14 for t in range(20))/20,terminal_iqr_pp=spread['terminal_iqr_pp'],historical_weeks=len(weeks) if hist else coverage[a],anchor_price=anchor,currency=currency,anchor_date=date))
 checks.append(dict(asset=a,history_count=len(weeks),anchor_matches=True,all_baseline_consensus_prices_match=True,all_dates_aligned=True))
write(R/'data/initial_forecast_price_paths.csv',rows);write(R/'analysis/recomputed/cohort_source_diagnostics.csv',features)
(R/'provenance/history_comparison_validation.json').write_text(json.dumps({'history_validation': 'performed from supplied historical CSV' if hist else 'not rerun: historical CSV is not redistributed; coverage counts are archived metadata', 'history_rows':len(hist),'weekly_observations':len(hist),'anchors':7,'forecast_price_rows_including_anchors':len(rows),'assets':checks,'limits':'Validates frozen forecast consistency. Historical observations are validated only when the optional CSV is supplied. No independent price or adjustment audit is claimed.'},indent=2)+'\n')
print('Validated',len(hist),'weekly observations, 7 anchors and',len(rows),'baseline forecast points.')
