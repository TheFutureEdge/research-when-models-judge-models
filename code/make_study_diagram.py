"""Draw the study overview from verified archive counts; no model calls.

Sources: provenance/parent_reconciliation.json, provenance/chronology.json,
analysis/recomputed/validation.json, and the archived experimental protocol.
Node size and connecting lines are schematic, not weights or a neural network.
"""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
parent = json.loads((ROOT/'provenance/parent_reconciliation.json').read_text())
assert parent['assets'] == 426 and parent['unique_source_tasks'] == 5964
assert parent['all_fourteen'] and parent['audited_at_utc'].startswith('2026-09-21')
assert 426 * 14 == 5964 and 7 * 14 == 98 and 7 * 2 * 4 == 56
plt.rcParams.update({'font.family': 'DejaVu Sans', 'pdf.fonttype': 42})
fig, ax = plt.subplots(figsize=(9, 7.9))
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax.set(xlim=(0, 9), ylim=(0, 7.9)); ax.axis('off')
ink='#163047'; muted='#496174'; teal='#087e8b'; orange='#b64b25'; purple='#7955a1'

def text(x,y,s,size=12,color=ink,bold=False,ha='left',**kw):
    return ax.text(x,y,s,fontsize=size,color=color,weight='bold' if bold else 'normal',
                   ha=ha,va='center',linespacing=kw.pop('linespacing',1.45),**kw)
def box(x,y,w,h,fill='#f1f6f9',edge='#cedce4'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.015,rounding_size=0.09',
                             facecolor=fill,edgecolor=edge,lw=1))
def arrow(x1,y1,x2,y2,color=muted,style='-'):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=12,
                                lw=1.3,color=color,linestyle=style))

text(.15,7.63,'A   THE REGULAR iPulse AI PIPELINE',14,bold=True)
text(.15,7.27,'Batch 7  |  September 2026 run; completed-batch audit: 21 September',11.8,muted)
box(.15,5.70,2.0,1.28)
text(1.15,6.63,'426 assets',20,bold=True,ha='center')
text(1.15,6.10,'Curated cross-asset\nresearch universe',12,ha='center')
arrow(2.18,6.32,2.57,6.32)
box(2.60,5.70,3.27,1.28)
text(4.235,6.72,'14 reports per asset',16,bold=True,ha='center')
for i in range(14):
    c=teal if i<12 else (orange if i==12 else purple)
    ax.add_patch(Circle((2.86+i*.212,6.35),.069,facecolor=c,edgecolor='white',lw=.6))
text(4.235,5.96,'12 Gemini  +  1 Astra  +  1 Opus',11.6,ha='center')
arrow(5.90,6.32,6.28,6.32)
box(6.31,5.70,2.52,1.28)
text(7.57,6.62,'1 consensus / asset',14,bold=True,ha='center')
text(7.57,6.12,'Gemini synthesizer\n+ deterministic calculation',11.7,ha='center')
text(4.5,5.37,'5,964 source reports   →   426 completed consensuses',13,bold=True,ha='center')
ax.plot([.15,8.83],[5.08,5.08],color='#cedce4',lw=1)

text(.15,4.80,'B   THIS PAPER: TEST THE FINAL DECISION LAYER',14,bold=True)
text(.15,4.44,'Reuse seven assets’ reports. Change how those reports are combined.',12,muted)
box(.15,2.48,2.72,1.66)
text(.33,3.87,'7 selected assets',16,bold=True)
text(.33,3.43,'3 equities with\naligned forecasts',12,bold=True,linespacing=1.1)
text(.33,2.98,'3 equities with\ndivergent forecasts',12,bold=True,linespacing=1.1)
text(.33,2.60,'1 crypto forecast',12,bold=True)
arrow(2.9,3.30,3.22,3.30)
box(3.25,2.48,5.58,1.66,fill='#eef8f7',edge='#acd0ce')
text(3.45,3.86,'98 fixed reports',15,bold=True)
text(3.45,3.52,'14 for each asset',11.8)
text(3.45,2.82,'Evidence + forecast paths\nheld fixed across conditions',11.5,muted)
for yy,col in [(3.67,teal),(2.97,orange)]:
    arrow(5.30,3.31,5.90,yy,color=col)
    box(5.94,yy-.24,2.64,.48,fill='white',edge=col)
text(7.26,3.67,'Gemini 3.8 Flash',12,bold=True,ha='center',color=teal)
text(7.26,2.97,'GPT-6 Astra',12,bold=True,ha='center',color=orange)
arrow(6.95,2.45,6.95,2.23)
text(.15,2.08,'4 conditions for each synthesizer and asset',12.5,bold=True)
for i,(a,b) in enumerate([('BLIND','Hide source model'),('REPEAT','Rerun blind'),('REVERSE','Reverse blind order'),('DISCLOSE','Reveal source model')]):
    x=.15+i*2.22
    box(x,1.27,2.02,.56,fill='#f6f7fa')
    text(x+1.01,1.65,a,11.5,bold=True,ha='center')
    text(x+1.01,1.40,b,10.7,ha='center')
arrow(4.50,1.23,4.50,.99)
for x,w,title,sub in [(.15,2.36,'56 consensus outputs','7 assets × 2 synthesizers\n× 4 conditions'),
                      (3.01,2.66,'14 weights per output','AI assigns report influence'),
                      (6.17,2.66,'1 five-year path per output','Code pools 20 quarterly returns')]:
    box(x,.08,w,.84)
    text(x+w/2,.65,title,12,bold=True,ha='center')
    text(x+w/2,.28,sub,10.5,ha='center')
arrow(2.55,.50,2.97,.50); arrow(5.71,.50,6.13,.50)

out=ROOT/'paper/figures'
fig.savefig(out/'design.pdf',facecolor='white')
fig.savefig(out/'design.png',dpi=200,facecolor='white')
plt.close(fig)
print('Study overview: 426 × 14 reports; 7 × 2 × 4 consensus outputs.')
