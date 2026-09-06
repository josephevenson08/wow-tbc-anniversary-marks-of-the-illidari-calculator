# -*- coding: utf-8 -*-
import json
g=json.load(open('gold_data.json')); P=g['players']
old={p['name']:p for p in json.load(open('page_data.json'))}
CLABEL=[("haste","Haste"),("destr","Destr"),("iron","Iron"),("smana","S.Mana"),
 ("omana","Mana−"),("felmana","FelMana"),("rune","Rune"),("emerald","Emerald"),
 ("thistle","Thistle"),("sheal","S.Heal"),("hs","HStone"),("seed","Seed"),
 ("flame","FlameCap"),("felbl","FelBloss"),("freeact","FAP"),("band","Bandg"),
 ("lei","Lei"),("drum","Drums")]
ENGK=["felbomb","ssap","gsap","arcbomb","adagren","mine","thorn","holywater"]
out=[]
for p in sorted(P,key=lambda x:x['rank']):
    o=old[p['name']]
    c=p['counts']
    out.append(dict(
        rank=p['rank'], key=p['key'], name=p['name'], role=p['role'], score=round(p['total'],1),
        tier=o['tier'], tank=p['isTank'],
        flask=p['flask'], battleE=p['battleOnly'], guardE=p['guardOnly'],
        battle=p['battle_slot'], guard=p['guard_slot'], food=p['food'],
        weapon=p['weap'], scroll=p['scroll'], scrollTypes=p['scroll_types'],
        actRate=p['act_r'], utilRate=p['util_r'],
        drumScore=p['drum_score'], drumWaste=p['drum_waste'], engiDmg=p['engi'],
        flags=p['sub'], verdict=o['verdict'], engiDetail=o['engiDetail'],
        cov=p['cov'], counts=c,
        parts=dict(battle=round(p['A'],1),guard=round(p['B'],1),food=round(p['C'],1),
                   weapon=round(p['D'],1),scroll=round(p['E'],1),active=round(p['P'],1),
                   util=round(p['U'],1),drum=round(p['bd'],1),engi=round(p['be'],1),
                   goa=round(p['bg'],1),pen=round(-p['pen'],1)),
        eng=sum(c.get(k,0) for k in ENGK),
        gold=p['gold']))
json.dump(dict(players=out, units=g['units'], price=g['price'],
               clabels=CLABEL, engk=ENGK),
          open('page_data2.json','w'), ensure_ascii=False, separators=(',',':'))
print("bytes", len(open('page_data2.json').read()), "| players", len(out))
print(json.dumps(out[0],ensure_ascii=False)[:400])
