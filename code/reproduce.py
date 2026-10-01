"""Reproduce all numerical results offline with Python's standard library.
Usage: python code/reproduce.py [--output OUTPUT_DIRECTORY]
Input: data/assets/*/{source_snapshot.json,consensus/*/*.json}.
Percent is the source unit; pp denotes percentage points. No API calls.
"""
from pathlib import Path
import argparse,csv,json,math,statistics,hashlib
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'analysis/recomputed');args=parser.parse_args();OUT=args.output;OUT.mkdir(parents=True,exist_ok=True)
def load(p):return json.loads(p.read_text())
def save(name,rows):
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def growth(q):
 g=1.;out=[]
 for r in q:g*=1+r/100;out.append(g)
 return out
def quantile(x,q):
 x=sorted(x);p=(len(x)-1)*q;i=int(p);return x[i]+(p-i)*(x[min(i+1,len(x)-1)]-x[i])
checks=[]
def check(name,ok):
 checks.append({'check':name,'passed':bool(ok)})
 if not ok:raise AssertionError(name)
ids=load(ROOT/'data/source_model_identity.json');manifest=load(ROOT/'data/experiment_manifest.json')
models=['gemini_3_8_flash','gpt_6_astra'];conditions=manifest['conditions_per_model']
runs=[];weights=[];paths=[];spreads=[];baselines=[];matrices={};results={}
for asset in manifest['assets']:
 ad=ROOT/'data/assets'/asset;s=load(ad/'source_snapshot.json');reps=sorted(s['canonical_prompt_object']['latest_asset_forecast_report']['task_config_reports'],key=lambda x:x['opinion_id']);keys=[r['opinion_id'] for r in reps];cohort=s['selection']['cohort'];R=[[float(t['predicted_most_reasonable_pct_change']) for t in r['timeseries']] for r in reps];G=[growth(r) for r in R];terminal=[(g[-1]-1)*100 for g in G];matrices[asset]=(keys,R,G)
 check(asset+':14_by_20',len(R)==14 and all(len(r)==20 for r in R));check(asset+':finite_positive_growth',all(math.isfinite(x) and x>-100 for r in R for x in r))
 spreads.append(dict(asset=asset,cohort=cohort,positive_terminal=sum(t>0 for t in terminal),negative_terminal=sum(t<0 for t in terminal),terminal_min_percent=min(terminal),terminal_max_percent=max(terminal),terminal_iqr_pp=quantile(terminal,.75)-quantile(terminal,.25)))
 for model in models:
  for cond in conditions:
   o=load(ad/'consensus'/model/(cond+'.json'));ow={x['opinion_id']:x for x in o['opinion_weights']};raw={x['opinion_id']:x['weight'] for x in o['submitted_opinion_weights']};w=[float(ow[k]['weight']) for k in keys];rs=sum(raw.values());q=[sum(w[i]*R[i][t] for i in range(14)) for t in range(20)];g=growth(q)
   tag=f'{asset}:{model}:{cond}'
   check(tag+':weight_ids',len(o['opinion_weights'])==len(o['submitted_opinion_weights'])==14 and set(ow)==set(raw)==set(keys));check(tag+':weight_simplex',all(x>=0 for x in w) and abs(sum(w)-1)<1e-10);check(tag+':normalization',max(abs(w[i]-raw[k]/rs) for i,k in enumerate(keys))<2e-11)
   check(tag+':all_20_quarters',max(abs(q[t]-o['consensus_timeseries'][t]['predicted_most_reasonable_pct_change']) for t in range(20))<1e-9)
   check(tag+':all_20_cumulative',max(abs((g[t]-1)*100-o['consensus_timeseries'][t]['compounded_return_percent']) for t in range(20))<1e-8)
   check(tag+':all_20_prices',max(abs(g[t]*o['consensus_calculation']['anchor_price']-o['consensus_timeseries'][t]['predicted_price']) for t in range(20))<1e-6)
   results[(asset,model,cond)]=(w,q,g)
   runs.append(dict(asset=asset,cohort=cohort,synthesizer=model,condition=cond,submitted_weight_sum=rs,effective_n=1/sum(x*x for x in w),one_year_return_percent=(g[3]-1)*100,five_year_return_percent=(g[-1]-1)*100,path_pool_five_year_percent=sum(w[i]*terminal[i] for i in range(14))))
   for i,k in enumerate(keys):weights.append(dict(asset=asset,synthesizer=model,condition=cond,opinion_id=k,source_model=ids[k],framework=reps[i]['investment_framework'],weight=w[i],submitted_weight=raw[k],rationale=ow[k]['rationale']))
   for t in range(20):paths.append(dict(asset=asset,synthesizer=model,condition=cond,step=t+1,quarter_return_percent=q[t],cumulative_return_percent=(g[t]-1)*100,normalized_price=g[t]*100))
 for method,w in [('equal_report',[1/14]*14),('equal_model',[1/3/sum(ids[j]==ids[k] for j in keys) for k in keys])]:
  g=growth([sum(w[i]*R[i][t] for i in range(14)) for t in range(20)])
  baselines.append(dict(asset=asset,method=method,one_year_return_percent=(g[3]-1)*100,five_year_return_percent=(g[-1]-1)*100))
paired=[];disclosure=[];cross=[]
for a in manifest['assets']:
 keys,R,G=matrices[a]
 for m in models:
  bw,bq,bg=results[(a,m,'baseline_blinded')]
  for c in conditions[1:]:
   w,q,g=results[(a,m,c)];tv=sum(abs(x-y) for x,y in zip(w,bw))/2
   check(f'{a}:{m}:{c}:quarter_bound',all(abs(q[t]-bq[t])<=tv*(max(r[t] for r in R)-min(r[t] for r in R))+1e-9 for t in range(20)))
   paired.append(dict(asset=a,synthesizer=m,condition=c,weight_TV=tv,abs_one_year_pp=abs(g[3]-bg[3])*100,abs_five_year_pp=abs(g[-1]-bg[-1])*100))
  for fam in ['GPT-6 Astra','Claude Opus 5','Gemini 3.8 Flash']:
   vals={c:sum(results[(a,m,c)][0][i] for i,k in enumerate(keys) if ids[k]==fam) for c in conditions}
   disclosure.append(dict(asset=a,synthesizer=m,source_family=fam,family_n=sum(ids[k]==fam for k in keys),baseline_weight=vals['baseline_blinded'],disclosed_weight=vals['model_disclosed'],baseline_delta_pp=100*(vals['model_disclosed']-vals['baseline_blinded']),two_blind_delta_pp=100*(vals['model_disclosed']-(vals['baseline_blinded']+vals['same_order_repeat_blinded'])/2)))
 for c in conditions:
  w,q,g=results[(a,models[0],c)];v,u,h=results[(a,models[1],c)]
  cross.append(dict(asset=a,condition=c,weight_TV=sum(abs(x-y) for x,y in zip(w,v))/2,five_year_astra_minus_gemini_pp=(h[-1]-g[-1])*100,one_year_astra_minus_gemini_pp=(h[3]-g[3])*100))
summary=[]
for m in models:
 for c in conditions[1:]:
  ss=[r for r in paired if r['synthesizer']==m and r['condition']==c and r['asset']!='bitcoin']
  summary.append(dict(synthesizer=m,condition=c,n_assets=len(ss),**{k:statistics.mean(r[k] for r in ss) for k in ['weight_TV','abs_one_year_pp','abs_five_year_pp']}))
for n,rows in [('runs.csv',runs),('weights.csv',weights),('paths.csv',paths),('source_spread.csv',spreads),('numerical_baselines.csv',baselines),('paired.csv',paired),('disclosure.csv',disclosure),('cross_synthesizer.csv',cross),('six_equity_summary.csv',summary),('checks.csv',checks)]:save(n,rows)
audit={'check_count':len(checks),'failed':0,'source_reports':98,'consensus_outputs':len(runs),'weights':len(weights),'source_steps':1960,'consensus_steps':len(paths),'new_inference_calls':0};(OUT/'validation.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps(audit))
