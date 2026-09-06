import json, itertools, random
rows=json.load(open('ranked.json'))
# 1) verify 17-fight denominator: every CLA pct should be ~ k/17
import re
pcts=[]
for r in rows:
    pcts += [r['battle_slot'],r['guard_slot'],r['food'],r['weap'],r['scroll']]
bad=[p for p in set(pcts) if min(abs(p-round(p*17/100)*100/17) for _ in [0])>0.6]
print("distinct pct values:",sorted(set(pcts)))
print("values NOT matching k/17 (tol 0.6):",sorted(bad))
# also test k/16 and k/18 to show 17 is the unique fit
for F in (15,16,17,18,19):
    err=sum(min(abs(p-k*100/F) for k in range(F+1)) for p in set(pcts))
    print(f"  denominator {F}: total abs error {err:.2f}")
