# -*- coding: utf-8 -*-
import json
buffs=json.load(open('wcl_buffs.json'))
data=json.load(open('page_data2.json')); P=data['players']
UNITS=data['units']; PRICE=dict(data['price'])
PRICE['flaskMark']=160          # a Shattrath flask costs 1 Mark, valued at the mark rate
UNITS['flaskMark']=UNITS['flask']

SHAT={'Relentless Assault of Shattrath','Blinding Light of Shattrath','Pure Death of Shattrath',
      'Fortification of Shattrath','Mighty Restoration of Shattrath','Supreme Power of Shattrath'}
REG={'Flask of Relentless Assault','Flask of Pure Death','Flask of Blinding Light',
     'Flask of Fortification','Flask of Mighty Restoration','Flask of Chromatic Wonder'}
NAME={'Agility':'Scroll of Agility','Strength':'Scroll of Strength','Spirit':'Scroll of Spirit',
 'Armor':'Scroll of Protection','Haste':'Haste Potion','Destruction':'Destruction Potion',
 'Ironshield':'Ironshield Potion','Fel Mana':'Fel Mana Potion','Chromatic Wonder':'Flask of Chromatic Wonder',
 'Healing Power':'Elixir of Healing Power','Lightning Speed':'Windfury Totem (party)',
 'Blessing of Might':'Blessing of Might','Well Fed':'Well Fed (food)','Greater Versatility':'Greater Versatility'}
SKIP={'Blessing of Might','Lightning Speed','First Aid','Rocket Boots Engaged','Prayer of Fortitude'}

for p in P:
    b=buffs.get(p['name'],[])
    shat=sum(x[1] for x in b if x[0] in SHAT)
    reg =sum(x[1] for x in b if x[0] in REG and x[0]!='Flask of Chromatic Wonder')
    tot = shat+reg
    share = (shat/tot) if tot else 0.0
    fl=p['cov']['flask']
    p['cov']['flaskMark']=round(fl*share,2)
    p['cov']['flask']=round(fl*(1-share),2)
    p['markFlasks']=shat
    p['demon']=sum(x[1] for x in b if x[0]=='Elixir of Demonslaying')
    p['chrom']=sum(x[1] for x in b if x[0]=='Flask of Chromatic Wonder' or x[0]=='Chromatic Wonder')
    p['items']=[[NAME.get(x[0],x[0]), x[1], x[2]] for x in b if x[0] not in SKIP]

def spend(o,price):
    s=sum(o['cov'][k]*price.get(k,0) for k in o['cov'])
    s+=sum(v*price.get(k,0) for k,v in o['counts'].items())
    return s
for p in P: p['gold']=round(spend(p,PRICE))
P.sort(key=lambda x:-x['gold'])
print(f"{'Player':<13}{'gold':>7}{'AHflask%':>9}{'Mkflask%':>9}{'marks used':>11}{'demon':>6}")
for p in P:
    print(f"{p['name']:<13}{p['gold']:>7}{p['cov']['flask']/UNITS['flask']*100:>8.0f}%"
          f"{p['cov']['flaskMark']/UNITS['flask']*100:>8.0f}%{p['markFlasks']:>11}{p['demon']:>6}")
print("\nraid total:", sum(p['gold'] for p in P), "| marks already spent on flasks:", sum(p['markFlasks'] for p in P))
data['price']=PRICE; data['units']=UNITS
json.dump(data, open('page_data3.json','w'), ensure_ascii=False, separators=(',',':'))
print("bytes", len(open('page_data3.json').read()))
