"""History + all 14 initial predictions + two blinded consensus baselines."""
from pathlib import Path
import csv,datetime as dt
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
R=Path(__file__).resolve().parents[1];F=R/'paper/figures';F.mkdir(exist_ok=True)
def read(p):
 with p.open() as f:return list(csv.DictReader(f))
def dates(rows):return [dt.date.fromisoformat(x['date']) for x in rows]
hist=read(R/'data/history/historical_weekly_prices.csv');paths=read(R/'data/initial_forecast_price_paths.csv');diag=read(R/'analysis/recomputed/cohort_source_diagnostics.csv');cross=read(R/'analysis/recomputed/cross_synthesizer.csv')
assets=['visa','sap','ibm','nebius','moderna','kratos','bitcoin'];names=['Visa','SAP','IBM','Nebius','Moderna','Kratos Defense','Bitcoin']
colors=['#087e8b','#b64b25'];plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':11,'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':.17,'pdf.fonttype':42,'savefig.facecolor':'white'})
legend=[Line2D([0],[0],color='#202938',lw=2,label='Weekly history'),Line2D([0],[0],color='#90a2b5',lw=.8,label='14 initial source paths'),Patch(facecolor='#d8e1e9',label='Source middle 50%'),Line2D([0],[0],color=colors[0],lw=2,label='Gemini consensus'),Line2D([0],[0],color=colors[1],ls='--',lw=2,label='Astra consensus'),Line2D([0],[0],color='#454c56',ls='-.',lw=1.2,label='Equal-report pool')]
for a,name in zip(assets,names):
 d=next(x for x in diag if x['asset']==a);hh=sorted([x for x in hist if x['asset']==a],key=lambda x:x['plot_date']);pp=[x for x in paths if x['asset']==a];anchor=dt.date.fromisoformat(d['anchor_date']);first=anchor.replace(year=anchor.year-5);last=dt.date.fromisoformat(max(x['date'] for x in pp));sourceids=sorted({x['series_id'] for x in pp if x['series_type']=='source'});source=[[x for x in pp if x['series_id']==k] for k in sourceids];matrix=np.array([[float(x['price']) for x in r] for r in source]);xx=dates(source[0]);fig,ax=plt.subplots(figsize=(9,3.45));fig.subplots_adjust(left=.09,right=.98,bottom=.25,top=.81)
 lo,hi=np.quantile(matrix,[.25,.75],axis=0);ax.fill_between(xx,lo,hi,color='#d8e1e9',alpha=.9,zorder=1)
 for yy in matrix:ax.plot(xx,yy,c='#90a2b5',lw=.7,alpha=.63,zorder=2)
 for segment in sorted({x['segment'] for x in hh}):
  part=[x for x in hh if x['segment']==segment];ax.plot([dt.date.fromisoformat(x['plot_date']) for x in part],[float(x['price']) for x in part],c='#202938',lw=1.65,zorder=4)
 for left,right in zip(hh,hh[1:]):
  if left['segment']!=right['segment']:
   ld=dt.date(2022,2,28) if a=='nebius' else dt.date.fromisoformat(left['plot_date']);rd=dt.date(2024,10,21) if a=='nebius' else dt.date.fromisoformat(right['plot_date']);label='Nasdaq trading halted\nFeb 2022 - Oct 2024' if a=='nebius' else 'No observations';ax.axvspan(ld,rd,color='#8993a0',alpha=.12,zorder=0);ax.text(ld+(rd-ld)/2,.47,label,transform=ax.get_xaxis_transform(),ha='center',va='center',fontsize=7.5,color='#596573')
 for m,c,ls in [('gemini_3_8_flash',colors[0],'-'),('gpt_6_astra',colors[1],'--'),('equal_report','#454c56','-.')]:
  rr=[x for x in pp if x['series_id']==m];ax.plot(dates(rr),[float(x['price']) for x in rr],c=c,ls=ls,lw=2 if m!='equal_report' else 1.15,zorder=5)
 ax.axvline(anchor,color='#4b5563',ls=':',lw=1.05);ax.scatter([anchor],[float(d['anchor_price'])],s=28,edgecolors='#202938',facecolors='white',zorder=6)
 ticks=[first,anchor.replace(year=2023),anchor,anchor.replace(year=2028),last];ax.set_xticks(ticks,[x.strftime('%b %Y') for x in ticks]);ax.get_xticklabels()[-1].set_ha('right');ax.set_xlim(first,last);ax.set_ylim(bottom=0);ax.set_ylabel('Price ('+d['currency']+')');ax.ticklabel_format(axis='y',style='plain',useOffset=False)
 if a=='bitcoin':ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v,p:f'{v/1000:g}k'))
 cohort='Aligned equity' if a in assets[:3] else 'Divergent equity' if a in assets[3:6] else 'Crypto reference'
 fig.text(.09,.96,f'{name} | {cohort}',ha='left',va='top',fontsize=12,weight='bold');fig.text(.09,.875,f'Initial five-year forecasts: {d["positive_terminal"]} positive / {d["negative_terminal"]} negative; IQR {float(d["terminal_iqr_pp"]):.2f} pp',fontsize=9,color='#405266')
 ax.text(.02,.94,'FIVE-YEAR HISTORY',transform=ax.transAxes,fontsize=8,color='#596573');ax.text(.54,.94,'FIVE-YEAR FORECASTS',transform=ax.transAxes,fontsize=8,color='#596573')
 fig.legend(handles=legend,loc='lower center',bbox_to_anchor=(.54,.012),ncol=3,frameon=False,fontsize=8,columnspacing=1.5)
 for ext in ['pdf','png']:fig.savefig(F/f'history_forecast_{a}.{ext}',dpi=180)
 plt.close(fig)
# A comparison of dispersion and consequence, with seven labeled observations only.
fig,ax=plt.subplots(figsize=(8,4.7),layout='constrained')
palette={'directionally_consistent':'#087e8b','forecast_dispersed':'#b64b25','fixed_reference_asset':'#7554a3'};markers={'directionally_consistent':'o','forecast_dispersed':'s','fixed_reference_asset':'D'}
for a,name in zip(assets,names):
 d=next(x for x in diag if x['asset']==a);gap=abs(float(next(x for x in cross if x['asset']==a and x['condition']=='baseline_blinded')['five_year_astra_minus_gemini_pp']));x=float(d['terminal_iqr_pp']);ax.scatter(x,gap,s=62,c=palette[d['cohort']],marker=markers[d['cohort']],zorder=4);ax.annotate(name,(x,gap),xytext=(7,7 if a!='nebius' else -15),textcoords='offset points',fontsize=9)
ax.set_xlim(0,111);ax.set_ylim(-1,34);ax.set_xlabel('Disagreement among initial forecasts: five-year source IQR (pp)');ax.set_ylabel('Absolute five-year gap between synthesizers (pp)');ax.set_title('Source disagreement and the consequences of synthesis',loc='left',pad=14)
handles=[Line2D([0],[0],ls='',marker=markers[k],color=v,label=l) for (k,v),l in zip(palette.items(),['Aligned equities (3)','Divergent equities (3)','Bitcoin reference (1)'])];ax.legend(handles=handles,frameon=False,loc='upper left',fontsize=9)
for ext in ['pdf','png']:fig.savefig(F/f'dispersion_vs_synthesis.{ext}',dpi=180)
plt.close(fig)
print('Generated seven full history/forecast figures and one cohort comparison.')
