"""Descriptive disclosure contrasts within Universal Investor researcher reports."""
from pathlib import Path
import csv,statistics
R=Path(__file__).resolve().parents[1]
def read(p):
    with p.open() as f:return list(csv.DictReader(f))
configs=read(R/'data/source_configurations.csv')
weights=read(R/'analysis/recomputed/weights.csv')
w={(x['asset'],x['synthesizer'],x['condition'],x['opinion_id']):float(x['weight']) for x in weights}
out=[];summary=[]
for synth in ['gemini_3_8_flash','gpt_6_astra']:
    for model in ['gemini-3.8-flash','gpt-6-astra','claude-opus-5']:
        block=[]
        for x in configs:
            if x['asset']=='bitcoin' or x['model']!=model or x['mode']!='researcher' or not x['framework'].startswith('universal_investor'):continue
            v=lambda c:w[(x['asset'],synth,c,x['opinion_id'])]
            block.append(dict(asset=x['asset'],synthesizer=synth,source_model=model,opinion_id=x['opinion_id'],baseline_delta_pp=100*(v('model_disclosed')-v('baseline_blinded')),two_blind_delta_pp=100*(v('model_disclosed')-(v('baseline_blinded')+v('same_order_repeat_blinded'))/2)))
        assert len(block)==6
        out.extend(block)
        summary.append(dict(synthesizer=synth,source_model=model,assets=6,baseline_delta_pp=statistics.mean(x['baseline_delta_pp'] for x in block),two_blind_delta_pp=statistics.mean(x['two_blind_delta_pp'] for x in block)))
for name,rows in [('matched_framework_disclosure.csv',out),('matched_framework_summary.csv',summary)]:
    with (R/'analysis/recomputed'/name).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)
print('Reproduced 36 matched-framework contrasts and six summaries; no claim of quality matching.')
