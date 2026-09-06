import json, random, statistics
rows=json.load(open('ranked.json'))
random.seed(7)
base=dict(battle=18,guard=18,food=12,weap=12,scroll=10,active=22,util=8,drum=8,engi=3,goa=2,pen=1.5)
def score(r,W,capA=2.0,capU=0.8):
    c=(r['battle_slot']/100*W['battle']+r['guard_slot']/100*W['guard']+r['food']/100*W['food']
       +r['weap']/100*W['weap']+r['scroll']/100*W['scroll']
       +min(r['act_r']/capA,1)*W['active']+min(r['util_r']/capU,1)*W['util'])
    b=min(r['drum_score']/237,1)*W['drum']+min(r['engi']/107315,1)*W['engi']
    g=(0.40 if r['name']=='Captrawr' else 0.33 if r['name']=='Oddbird' else 0)/0.40*W['goa']
    return c+b+g-W['pen']*len(r['sub'])
ranks={r['name']:[] for r in rows}
for _ in range(4000):
    W={k:v*random.uniform(0.6,1.4) for k,v in base.items()}
    capA=random.uniform(1.5,2.5); capU=random.uniform(0.6,1.1)
    s=sorted(rows,key=lambda r:-score(r,W,capA,capU))
    for i,r in enumerate(s,1): ranks[r['name']].append(i)
print(f"{'#':>3} {'Player':<13}{'score':>7}  {'median':>6} {'p5-p95 band':>12}  stability")
for r in rows:
    v=sorted(ranks[r['name']]); n=len(v)
    med=v[n//2]; lo=v[int(n*.05)]; hi=v[int(n*.95)]
    same=sum(1 for x in v if abs(x-r['rank'])<=2)/n
    print(f"{r['rank']:>3} {r['name']:<13}{r['total']:>7.1f}  {med:>6} {str(lo)+'-'+str(hi):>12}   {same*100:>5.1f}% within +/-2")
