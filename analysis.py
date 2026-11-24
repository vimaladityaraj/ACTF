"""ACTF: synthetic computational demonstration, not sensory measurement."""
import csv, itertools, json, math, platform
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
AXES=('S','So','Sa','B','P','A')
WEIGHTS={'uniform':[1/6]*6,'pungency_high':[.08,.08,.08,.08,.60,.08], 'pungency_low':[.19,.19,.19,.19,.05,.19], 'astringency_high':[.08,.08,.08,.08,.08,.60], 'gustatory_high':[.225,.225,.225,.225,.05,.05]}
LEVELS=(0,.025,.05,.1,.2)
def vector(x):
    raw=np.asarray(x,dtype=object)
    if raw.shape!=(6,) or not all(isinstance(v,(int,float,np.integer,np.floating)) and not isinstance(v,(bool,np.bool_)) for v in raw): raise ValueError("Expected numeric coordinates")
    a=np.asarray(x,dtype=float)
    if a.shape!=(6,) or not np.isfinite(a).all() or (a<0).any() or (a>1).any(): raise ValueError('Expected six finite values in [0,1]')
    return a
def distance(x,y,w=None):
    x,y=vector(x),vector(y)
    w=vector(WEIGHTS['uniform'] if w is None else w)
    if w.shape!=(6,) or not np.isfinite(w).all() or (w<0).any() or not math.isclose(float(w.sum()),1,rel_tol=0,abs_tol=1e-12): raise ValueError('Expected six nonnegative weights summing to one')
    return float(np.sqrt(np.dot(w,(x-y)**2)))
def normalize(r,M):
    if isinstance(M,(bool,np.bool_)) or not isinstance(M,(int,float,np.integer,np.floating)) or not np.isfinite(M) or M<=0: raise ValueError('Invalid maximum')
    raw=np.asarray(r,dtype=object)
    if raw.shape!=(6,) or not all(isinstance(v,(int,float,np.integer,np.floating)) and not isinstance(v,(bool,np.bool_)) for v in raw): raise ValueError("Expected numeric ratings")
    return vector(np.asarray(r,dtype=float)/M)
def reflect(z): return 1-np.abs(1-np.mod(z,2))
def profiles():
    with (ROOT/'profiles.csv').open() as f:
        return {r['label']:vector([float(r[k]) for k in AXES]) for r in csv.DictReader(f)}
def noise(x,y):
    rows=[]
    for i,s in enumerate(LEVELS):
        rng=np.random.Generator(np.random.PCG64(np.random.SeedSequence([20261103,i])))
        z=np.array([x,y])+rng.normal(0,s,size=(5000,2,6))
        outside=float(np.mean((z<0)|(z>1))*100)
        for rule,p in [('clipping',np.clip(z,0,1)),('reflection',reflect(z))]:
            d=np.sqrt(np.mean((p[:,0,:]-p[:,1,:])**2,axis=1)); sd=float(np.std(d,ddof=1))
            rows.append(dict(rule=rule,sigma=s,mean=float(d.mean()),sd=sd,mc_se=sd/math.sqrt(len(d)),outside_pct=outside,p05=float(np.quantile(d,.05)),p95=float(np.quantile(d,.95))))
    return rows
def save_csv(name,rows):
    with (ROOT/name).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
def main():
    p=profiles(); pairs=[]; weighted=[]
    for (a,x),(b,y) in itertools.combinations(p.items(),2):
        d=distance(x,y); pairs.append(dict(a=a,b=b,D2=d*math.sqrt(6),Dn=d,Q=1-d))
        for name,w in WEIGHTS.items(): weighted.append(dict(a=a,b=b,scheme=name,Dw=distance(x,y,w)))
    n=noise(p['Jalapeno pepper'],p['Vanilla ice cream']); save_csv('pairwise.csv',pairs);save_csv('weighted.csv',weighted);save_csv('noise.csv',n)
    summary={'pair_count':len(pairs),'weighted_count':len(weighted),'min':min(pairs,key=lambda r:r['Dn']),'max':max(pairs,key=lambda r:r['Dn']),'environment':{'python':platform.python_version(),'numpy':np.__version__,'matplotlib':matplotlib.__version__}}
    (ROOT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8',newline='\n')
    fig,axs=plt.subplots(1,2,figsize=(10,4.0),layout='constrained',gridspec_kw={'width_ratios':[1,1.15]})
    a,b=p['Jalapeno pepper'],p['Vanilla ice cream']; t=np.arange(6)
    axs[0].bar(t-.19,a,.38,label='Jalapeno');axs[0].bar(t+.19,b,.38,label='Vanilla');axs[0].set(xticks=t,xticklabels=AXES,ylim=(0,1),ylabel='Assigned intensity',title='A. Constructed profiles');axs[0].legend(frameon=False,fontsize=9)
    ds=sorted([(k,distance(a,v)) for k,v in p.items() if k!='Jalapeno pepper'],key=lambda z:z[1]);axs[1].barh([k for k,d in ds],[d for k,d in ds]);axs[1].invert_yaxis();axs[1].set(xlim=(0,1),xlabel='Normalized Euclidean distance',title='B. Distances from jalapeno')
    fig.suptitle('Synthetic examples only — not measured food intensities',fontsize=12);fig.savefig(ROOT/'figure3.png',dpi=220);plt.close(fig)
if __name__=='__main__': main()
