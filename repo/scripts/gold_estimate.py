# -*- coding: utf-8 -*-
import json, runpy
ns=runpy.run_path('rank.py'); rows=json.load(open('ranked.json'))
rpb, cla = ns['rpb'], ns['cla']
drum_counts=ns['drum_counts']
# engineering item counts per player
ENG={
"Pierogi":dict(felbomb=13,gsap=4,thorn=1),
"Thundaqt":dict(ssap=10,gsap=9,mine=1),
"Thotiana":dict(arcbomb=1,felbomb=10,ssap=6,gsap=4),
"Junnox":dict(arcbomb=1,adagren=1,ssap=5,gsap=1),
"Threatbull":dict(felbomb=10,ssap=16,gsap=6,thorn=1),
"Woksauce":dict(arcbomb=1,felbomb=8,ssap=8,gsap=5,thorn=1),
"Captrawr":dict(thorn=1),"Grazzyknoll":dict(thorn=1),"Azzblast":dict(thorn=1,holywater=1),
"Caicey":dict(thorn=1),"Donkin":dict(thorn=1),"Zev":dict(thorn=1),"Shoutofearth":dict(thorn=1),
}
# units needed for 100% coverage across a 3:24 raid / 17 boss fights
UNITS=dict(flask=2, battle=6, guard=6, food=8, weapon=6, scroll=6)
# default per-unit gold (server-dependent; editable on the page)
PRICE=dict(flask=110, battle=18, guard=14, food=6, weapon=8, scroll=4,
  haste=16, destr=16, iron=12, smana=12, omana=5, felmana=14, sheal=12, rune=10,
  emerald=0, thistle=2, hs=0, seed=8, flame=9, felbl=6, freeact=10, band=1, lei=3,
  drum=2, felbomb=3, ssap=12, gsap=6, arcbomb=8, adagren=4, mine=2, thorn=5, holywater=3)
COUNTED=["haste","destr","iron","smana","omana","felmana","sheal","rune","emerald",
         "thistle","hs","seed","flame","felbl","freeact","band","lei"]
DISPLAY={"Pierogi":"Pierogï","Planet":"Plánet","Spliff":"Splïff","Ohm":"Õhm","Zev":"Zèv"}
TANKS={"Captrawr","Oddbird","Thotiana"}

out=[]
for r in rows:
    n=r['name']; raw=rpb[n]; b,g,fl,fd,sc,wp,st,sub = cla[n]
    # coverage spend: battle/guardian columns are elixir-only; flask column is separate
    cov=dict(flask=fl/100*UNITS['flask'], battle=b/100*UNITS['battle'],
             guard=g/100*UNITS['guard'], food=fd/100*UNITS['food'],
             weapon=wp/100*UNITS['weapon'], scroll=sc/100*UNITS['scroll'])
    counts=dict((k,raw.get(k,0)) for k in COUNTED)
    counts['drum']=drum_counts.get(n,0)
    for k,v in ENG.get(n,{}).items(): counts[k]=v
    o=dict(r)
    o['name']=DISPLAY.get(n,n); o['key']=n
    o['flask']=fl; o['battleOnly']=b; o['guardOnly']=g
    o['isTank']= n in TANKS
    o['cov']={k:round(v,2) for k,v in cov.items()}
    o['counts']={k:v for k,v in counts.items() if v}
    out.append(o)

def spend(o,price=PRICE):
    s=sum(o['cov'][k]*price[k] for k in o['cov'])
    s+=sum(v*price.get(k,0) for k,v in o['counts'].items())
    return s
for o in out: o['gold']=round(spend(o))
out.sort(key=lambda o:-o['gold'])
print(f"{'Player':<14}{'gold':>7} {'flask%':>7}{'btlE%':>6}{'grdE%':>6} | top spend drivers")
for o in out:
    drivers=sorted(((v*PRICE.get(k,0),k) for k,v in o['counts'].items()),reverse=True)[:3]
    cd=sorted(((o['cov'][k]*PRICE[k],k) for k in o['cov']),reverse=True)[:2]
    d=", ".join(f"{k} {int(c)}g" for c,k in cd+drivers if c>0)
    print(f"{o['name']:<14}{o['gold']:>7} {o['flask']:>6}%{o['battleOnly']:>5}%{o['guardOnly']:>5}% | {d}")
print()
print("raid total gold:", sum(o['gold'] for o in out), "| mean", round(sum(o['gold'] for o in out)/25))
json.dump({"players":out,"units":UNITS,"price":PRICE}, open('gold_data.json','w'), ensure_ascii=False, indent=0)
