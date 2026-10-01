"""Generate vector PDF and 180-dpi PNG figures from independently recomputed tables."""
from pathlib import Path
import csv,json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'analysis/recomputed';F=ROOT/'paper/figures';F.mkdir(parents=True,exist_ok=True)
def rows(name):
 with (D/name).open() as f:return list(csv.DictReader(f))
def val(row,k):return float(row[k])
assets=['visa','sap','ibm','nebius','moderna','kratos','bitcoin'];names=['Visa','SAP','IBM','Nebius','Moderna','Kratos','Bitcoin'];models=['gemini_3_8_flash','gpt_6_astra'];colors=['#087e8b','#b64b25'];labels=['Gemini 3.8 Flash','GPT-6 Astra']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':11,'axes.labelsize':9,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':.18,'pdf.fonttype':42,'savefig.facecolor':'white','axes.titleweight':'bold'})
def save(fig,name):
 fig.savefig(F/(name+'.pdf'),bbox_inches='tight');fig.savefig(F/(name+'.png'),dpi=180,bbox_inches='tight');plt.close(fig)
r=rows('runs.csv');b={(x['asset'],x['synthesizer']):x for x in r if x['condition']=='baseline_blinded'}
fig,axs=plt.subplots(1,2,figsize=(10.1,4),gridspec_kw={'width_ratios':[1.6,1]},layout='constrained')
for j,ax in enumerate(axs):
 for i,a in enumerate(assets):
  key=['five_year_return_percent','effective_n'][j];x=[val(b[(a,m)],key) for m in models]
  ax.plot(x,[i,i],color='#a7b1bd',lw=2,zorder=1)
  for k in range(2):ax.scatter(x[k],i,color=colors[k],s=43,marker=['o','D'][k],zorder=3,label=labels[k] if i==0 else None)
  if j==0:ax.text(max(x)+3,i,f'{abs(x[1]-x[0]):.2f} pp',va='center',fontsize=8,color='#465467')
 ax.set_yticks(range(7),names if j==0 else ['']*7);ax.invert_yaxis();ax.axhline(2.5,c='#9ca3af',ls=':',lw=.8);ax.axhline(5.5,c='#9ca3af',ls=':',lw=.8)
 ax.set_xlabel(['Predicted five-year price return (%)','Effective number of reports (1 / sum of squared weights)'][j]);ax.set_title(['A  Same reports, different forecasts','B  Concentration of influence'][j],loc='left')
axs[0].axvline(0,color='#333',lw=.8);axs[0].set_xlim(-25,194);axs[0].legend(loc='upper right',fontsize=8,frameon=False);axs[1].set_xlim(0,14.8)
save(fig,'synthesizer_choice')

disc=rows('disclosure.csv');fig,axs=plt.subplots(1,2,figsize=(10,4.1),sharex=True,sharey=True,layout='constrained')
for ax,m,title in zip(axs,models,labels):
 for f,col,marker,offset in [('GPT-6 Astra',colors[1],'D',-.12),('Claude Opus 5','#7554a3','s',.12)]:
  rr=[next(x for x in disc if x['asset']==a and x['synthesizer']==m and x['source_family']==f) for a in assets[:6]]
  ax.scatter([val(x,'baseline_delta_pp') for x in rr],np.arange(6)+offset,c=col,marker=marker,s=42,label=f)
  ax.scatter([val(x,'two_blind_delta_pp') for x in rr],np.arange(6)+offset,facecolors='none',edgecolors=col,marker=marker,s=65,linewidth=1)
 ax.axvline(0,c='#333',lw=.8);ax.set_title(title+' synthesizer',loc='left');ax.set_yticks(range(6),names[:6]);ax.set_xlabel('Disclosed minus blinded weight (percentage points)');ax.set_xlim(-4.5,8.5)
axs[0].invert_yaxis();axs[0].legend(frameon=False,fontsize=8,loc='lower right');save(fig,'source_disclosure')

s=rows('six_equity_summary.csv');conds=['same_order_repeat_blinded','reverse_order_blinded','model_disclosed'];fig,axs=plt.subplots(1,2,figsize=(10,3.1),layout='constrained')
for ax,key,title in zip(axs,['weight_TV','abs_five_year_pp'],['A  Weight movement','B  Five-year forecast movement']):
 for j,m in enumerate(models):
  vals=[val(next(x for x in s if x['synthesizer']==m and x['condition']==c),key) for c in conds]
  ax.bar(np.arange(3)+(j-.5)*.33,vals,width=.31,color=colors[j],label=labels[j])
 ax.set_xticks(range(3),['Repeat','Reverse order','Disclose models']);ax.set_title(title,loc='left');ax.set_ylabel('Mean total variation' if key=='weight_TV' else 'Mean absolute change (pp)');ax.set_axisbelow(True)
axs[1].legend(frameon=False,fontsize=8);save(fig,'stability')

source=ROOT/'data/source_paths.csv'
with source.open() as f:sr=list(csv.DictReader(f))
p=rows('paths.csv');fig,axes=plt.subplots(4,2,figsize=(10,12),layout='constrained')
for ax,a,name in zip(axes.flat,assets,names):
 keys=sorted(set(x['opinion_id'] for x in sr if x['asset']==a));matrix=np.array([[100]+[val(x,'normalized_price') for x in sr if x['asset']==a and x['opinion_id']==k] for k in keys]);xx=np.arange(21)/4
 ax.fill_between(xx,matrix.min(axis=0),matrix.max(axis=0),color='#e9edf1',label='Full source range')
 ax.fill_between(xx,*np.quantile(matrix,[.25,.75],axis=0),color='#bfcbd8',alpha=.8,label='Middle 50% of sources')
 for j,m in enumerate(models):
  yy=[100]+[val(x,'normalized_price') for x in p if x['asset']==a and x['synthesizer']==m and x['condition']=='baseline_blinded'];ax.plot(xx,yy,color=colors[j],lw=2,label=labels[j])
 RR=np.array([[val(x,'quarter_return_percent') for x in sr if x['asset']==a and x['opinion_id']==k] for k in keys]);equal=np.r_[100,100*np.cumprod(1+RR.mean(axis=0)/100)];ax.plot(xx,equal,c='#28374a',ls='--',lw=1.15,label='Equal-report step pool')
 ax.axhline(100,c='#8993a0',lw=.7);ax.set_title(name,loc='left');ax.set_xlabel('Years from archived anchor');ax.set_ylabel('Forecast index (anchor = 100)');ax.set_xticks(range(6));ax.set_xlim(0,5)
axes.flat[-1].axis('off');handles,legend=axes.flat[0].get_legend_handles_labels();axes.flat[-1].legend(handles,legend,loc='upper left',frameon=False,fontsize=10);axes.flat[-1].text(.04,.39,'Shading is disagreement among forecasts,\nnot a confidence or prediction interval.\n\nAll paths are archived forecasts.\nNo realized-performance claim is made.\nVertical scales vary across panels.',transform=axes.flat[-1].transAxes,va='top',fontsize=10,linespacing=1.8)
save(fig,'all_seven_paths')

# Keep the overview reproducible through this original entry point.
import runpy
runpy.run_path(str(Path(__file__).with_name('make_study_diagram.py')), run_name='__main__')
print('Generated analytical figures and the study overview as vector PDF and PNG.')
