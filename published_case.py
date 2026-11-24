"""Secondary calculation on four published cluster means, not raw participant records.
Source: Viskaal van Dongen et al. (2012), BJN 108:140–147, Table 2 p.145.
DOI 10.1017/S0007114511005277. Only factual mean values transcribed; no table reproduction.
"""
import itertools,json,csv
from pathlib import Path
from actf import *
# Source order here is ACTF S,So,Sa,B; fifth reported attribute is savouriness.
means=[('neutral',25,[2.5,1.3,2.8,1.7],2.3),('salty-savoury',6,[2.9,2.4,9.6,1.7],6.8),('sweet-sour',9,[7.6,6.6,1.4,2.3],.9),('sweet',10,[8.9,1.2,1.9,1.3],1.2)]
records=[]
for name,n,raw,umami in means:
    r=synthetic(name,[normalize(v,0,15) for v in raw]+[None,None]);r['data_kind']='observed';r['sample'].update(preparation='cluster of multiple products; see source',batch='not reported for cluster',concentration_description='not reported for cluster',portion_g=None);r['protocol'].update(id='BJN-2012-table2',definitions='source study four basic taste labels; provisional mapping',language='not reported',assessor_population='19 adults in source study',method='anchored Spectrum intensity ratings',scale={'lower':0,'upper':15,'anchors':'source Table 1'},window_s=None,aggregation='published cluster mean across foods');r['source']='https://doi.org/10.1017/S0007114511005277 Table 2 p.145';records.append({'record':validate(r),'foods_in_cluster':n,'source_savouriness_0_15':umami,'source_raw_four':raw})
Path('published_records.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
rows=[]
for a,b in itertools.combinations(records,2):
    l,u,k=completion_bounds(a['record'],b['record']);issues=compatibility(a['record'],b['record']);assert issues==['unknown window'];rows.append(dict(a=a['record']['sample']['id'],b=b['record']['sample']['id'],lower=l,upper=u,known=k,strict_gate='rejected: unknown window'))
with open('published_bounds.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
assert all(x["lower"]**2-y["lower"]**2<2/6 and y["lower"]**2-x["lower"]**2<2/6 for x,y in itertools.combinations(rows,2))
print(rows)
