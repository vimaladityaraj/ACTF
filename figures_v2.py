from pathlib import Path
import csv,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R=Path(__file__).parent
# Exchange and comparison workflow, not sensory acquisition itself.
fig,ax=plt.subplots(figsize=(10,3));ax.set(xlim=(0,10),ylim=(0,3));ax.axis('off')
items=[(.15,1.6,1.75,.85,'External ratings\n+ source protocol'),(2.15,1.6,1.75,.85,'Normalize and\nname six fields'),(4.15,1.6,1.75,.85,'Validate JSON\n+ preserve nulls'),(6.15,1.6,1.75,.85,'Protocol gate\n(exact match)'),(8.15,1.6,1.7,.85,'Complete: point\nIncomplete: bounds')]
for x,y,w,h,t in items:
 ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.03',facecolor='#e8f0f7',edgecolor='#31536e'));ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=10)
for a,b in zip(items,items[1:]):ax.annotate('',xy=(b[0]-.03,2.03),xytext=(a[0]+a[2]+.03,2.03),arrowprops=dict(arrowstyle='->',lw=1.3,color='#31536e'))
ax.annotate('Reject incompatible or\ninsufficient protocol metadata',xy=(7.02,1.55),xytext=(7.02,.57),ha='center',va='center',fontsize=10,arrowprops=dict(arrowstyle='<-',color='#985b40'))
ax.text(.2,.1,'The source acquisition method is external to ACTF; the software does not infer taste.',fontsize=10,color='#333333');fig.savefig(R/'figure2.png',dpi=240,bbox_inches='tight');plt.close(fig)
rows=list(csv.DictReader(open(R/'published_bounds.csv')));fig,ax=plt.subplots(figsize=(9,3.6),layout='constrained')
for i,r in enumerate(rows):
 l,u=float(r['lower']),float(r['upper']);ax.plot([l,u],[i,i],lw=3,color='#527b94');ax.scatter([l,u],[i,i],s=26,color='#31536e',zorder=3)
ax.set(yticks=range(len(rows)),yticklabels=[r['a']+' / '+r['b'] for r in rows],xlim=(0,1),xlabel='Conditional normalized distance',title='Published cluster means: feasible distance under missing P and A');ax.invert_yaxis();ax.grid(axis='x',alpha=.25);fig.savefig(R/'figure4.png',dpi=240);plt.close(fig)
