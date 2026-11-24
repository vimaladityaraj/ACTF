import copy,csv,itertools,json,math,subprocess
from pathlib import Path
from actf import *
from analysis import WEIGHTS
ROOT=Path(__file__).parent
R=read_synthetic_csv(ROOT/'profiles.csv')
R2=[loads(dumps(r)) for r in R]
assert R==R2
(ROOT/'records.json').write_text(json.dumps(R2,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
J=json.loads(subprocess.check_output(['node',str(ROOT/'compare.mjs'),str(ROOT/'records.json')],text=True))
E=[]
for (a,b),j in zip(itertools.combinations(R2,2),J,strict=True):
    d=distance(a,b);assert (a['sample']['id'],b['sample']['id'])==(j['a'],j['b']); E.append(abs(d-j['Dn']))
assert max(E)<1e-12
# Mask every subset of dimensions on both members of each of 28 pairs.
# Compare zero-fill and exact interval, using hidden original vector only as synthetic reference.
rows=[]
for mask in range(1,64):
    keys=[k for i,k in enumerate(AXES) if mask>>i&1]
    for a,b in itertools.combinations(R2,2):
        aa,bb=copy.deepcopy(a),copy.deepcopy(b)
        for k in keys: aa['coordinates'][k]=bb['coordinates'][k]=None
        lo,hi,known=bounds(aa,bb); truth=distance(a,b)
        za,zb=copy.deepcopy(aa),copy.deepcopy(bb)
        for k in keys: za['coordinates'][k]=zb['coordinates'][k]=0
        z=distance(za,zb)
        assert lo-1e-12<=truth<=hi+1e-12 and abs(z-lo)<1e-12
        rows.append(dict(mask='|'.join(keys),a=a['sample']['id'],b=b['sample']['id'],known=known,lower=lo,upper=hi,complete=truth,zero_fill=z,zero_error=truth-z))
with (ROOT/'masked_pairs.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
subset=[r for r in rows if r['mask']=='P|A']
# For every anchor, certify pairwise candidate order only when intervals are disjoint.
rank_total=cert=zero_reversed=both_orders=0
for a in R2:
    aid=a['sample']['id']; candidates=[r for r in subset if aid in (r['a'],r['b'])]
    for x,y in itertools.combinations(candidates,2):
        rank_total+=1
        if x['upper']<y['lower'] or y['upper']<x['lower']: cert+=1
        if (x['zero_fill']-y['zero_fill'])*(x['complete']-y['complete'])<0: zero_reversed+=1
        # Construct two simultaneous completions sharing the anchor: unknowns 0 for anchor and one candidate, 1 for the other.
        base=x['lower']**2-y['lower']**2
        if base-2/6<0<base+2/6: both_orders+=1
summary={'round_trips':len(R2),'cross_language_pairs':len(J),'max_abs_difference':max(E),'masked_cases':len(rows),'interval_containment':len(rows),'PA_cases':len(subset),'PA_mean_zero_underestimate':sum(r['zero_error'] for r in subset)/len(subset),'PA_mean_interval_width':sum(r['upper']-r['lower'] for r in subset)/len(subset),'rank_comparisons':rank_total,'certified_orders':cert,'zero_fill_reversals':zero_reversed,'both_orders_feasible':both_orders}
(ROOT/'exchange_results.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8',newline='\n'); print(json.dumps(summary,indent=2))
