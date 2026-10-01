"""Reconcile completed-release provider usage without credentials or network calls."""
from pathlib import Path
import csv, json, collections
R = Path(__file__).resolve().parents[1]
rows = [json.loads(s) for s in (R/'data/parent_batch_usage.jsonl').read_text().splitlines()]
ledger = list(csv.DictReader((R/'provenance/parent_asset_ledger.csv').open()))
expected = {h for r in ledger for h in r['source_task_sha256'].split(';')}
assert {r['task_sha256'] for r in rows if r['layer']=='source'} == expected
assert len({(r['layer'],r['task_sha256'],r['stage']) for r in rows}) == len(rows)
groups = collections.defaultdict(collections.Counter)
tasks = collections.defaultdict(set)
for r in rows:
    u = r['usage']; model = r['model']; key = (r['layer'],model)
    if model == 'gemini-3.8-flash':
        inp=u['promptTokenCount']; nonreason=u['candidatesTokenCount']
        reason=u.get('thoughtsTokenCount',0)
        assert inp+nonreason+reason == u['totalTokenCount']
    elif model == 'claude-opus-5':
        inp=u['input_tokens']+u.get('cache_creation_input_tokens',0)+u.get('cache_read_input_tokens',0)
        reason=u['output_tokens_details']['thinking_tokens']; nonreason=u['output_tokens']-reason
    elif model == 'gpt-6-astra':
        inp=u['input_tokens']; reason=u['output_tokens_details']['reasoning_tokens']
        nonreason=u['output_tokens']-reason
        assert inp+u['output_tokens'] == u['total_tokens']
    else:
        raise AssertionError(model)
    assert min(inp,nonreason,reason)>=0
    groups[key].update(stages=1,input_tokens=inp,nonreasoning_output_tokens=nonreason,
                       reasoning_tokens=reason,generated_tokens=nonreason+reason,total_tokens=inp+nonreason+reason)
    tasks[key].add(r['task_sha256'])
out=[]
for key,g in sorted(groups.items()):
    out.append(dict(layer=key[0],model=key[1],logical_tasks=len(tasks[key]),**dict(g)))
total=collections.Counter()
for r in out:
    total.update({k:v for k,v in r.items() if isinstance(v,int)})
out.append(dict(layer='ALL',model='ALL',**dict(total)))
assert total['logical_tasks']==6390 and total['stages']==6816
assert len([r for r in rows if r['layer']=='consensus'])==426
assert total['input_tokens']==643294386 and total['generated_tokens']==141182977
target=R/'analysis/recomputed/parent_batch_usage.csv'
with target.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=out[0].keys());w.writeheader();w.writerows(out)
print(json.dumps(dict(total),indent=2))
