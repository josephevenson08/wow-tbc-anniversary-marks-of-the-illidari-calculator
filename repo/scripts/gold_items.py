# -*- coding: utf-8 -*-
import json
buffs=json.load(open('wcl_buffs.json'))
L=json.load(open('live_prices.json'))['items']
d=json.load(open('page_data4.json')); P=d['players']
F=17
MARK=max(L['Flask of Blinding Light'],10*L['Haste Potion'],10*L['Destruction Potion'])
L.update({'Gift of Arthas':4.13,'Deadly Poison VII':0.40,"Kreeg's Stout Beatdown":1.0,
 'Noggenfogger Elixir':1.0,'Scourgebane Draught':2.0,'Demonic Rune':L['Dark Rune'],
 'Thornling Seed':4.0,'Stratholme Holy Water':1.0,'Greater Versatility':3.0})

# named log buff -> (priced item, units required for 100% coverage over this raid)
BUFF={
 'Flask of Relentless Assault':('Flask of Relentless Assault',2),
 'Flask of Pure Death':('Flask of Pure Death',2),
 'Flask of Blinding Light':('Flask of Blinding Light',2),
 'Chromatic Wonder':('Flask of Chromatic Wonder',2),
 'Relentless Assault of Shattrath':('__MARK__',2),
 'Blinding Light of Shattrath':('__MARK__',2),
 'Major Agility':('Elixir of Major Agility',6),
 'Major Strength':('Elixir of Major Strength',6),
 'Healing Power':('Elixir of Healing Power',6),
 "Adept's Elixir":("Adept's Elixir",6),
 'Elixir of Draenic Wisdom':('Elixir of Draenic Wisdom',6),
 'Elixir of Major Fortitude':('Elixir of Major Fortitude',6),
 'Elixir of the Mongoose':('Elixir of the Mongoose',6),
 'Elixir of Demonslaying':('Elixir of Demonslaying',6),
 'Gift of Arthas':('Gift of Arthas',6),
 'Greater Versatility':('Greater Versatility',6),
 'Agility':('Scroll of Agility V',6), 'Strength':('Scroll of Strength V',6),
 'Spirit':('Scroll of Spirit V',6),   'Armor':('Scroll of Protection V',6),
 'Well Fed':('__FOOD__',8),
 "Kreeg's Stout Beatdown":("Kreeg's Stout Beatdown",8),
 'Noggenfogger Elixir':('Noggenfogger Elixir',8),
 'Scourgebane Draught':('Scourgebane Draught',6),
 'Flip Out':('Noggenfogger Elixir',8), 'Yaaarrrr':('Noggenfogger Elixir',8),
}
FOOD=round(sum(L[k] for k in ['Spicy Hot Talbuk',"Fisherman's Feast",'Ravager Dog','Blackened Basilisk',
        'Golden Fish Sticks','Roasted Clefthoof','Grilled Mudfish','Spicy Crawdad'])/8,2)
# weapon enhancement priced by what the role actually applies (per 30-min application)
WEAP={'Rogue':L['Deadly Poison VII'],
      'caster':round(L['Superior Wizard Oil']/5,2), 'healer':round(L['Superior Mana Oil']/5,2),
      'melee':L['Adamantite Sharpening Stone']}
ROLE={'Bmztilt':'healer','Caicey':'healer','Likapally':'healer','Plánet':'healer','Splïff':'healer',
 'Pierogï':'caster','Azzblast':'caster','Kapisce':'caster','Õhm':'caster','Junnox':'caster',
 'Novick':'caster','Zèv':'caster','Orixon':'Rogue'}

rows=[]
for p in P:
    n=p['name']; cov=0.0; lines=[]
    for name,cnt,upt in buffs.get(n,[]):
        if name not in BUFF: continue
        item,full=BUFF[name]
        price = MARK if item=='__MARK__' else (FOOD if item=='__FOOD__' else L.get(item,0))
        units = min(cnt,F)/F*full
        c=units*price
        if c>0: cov+=c; lines.append((name,round(units,2),round(price,2),round(c,1)))
    w=WEAP.get(ROLE.get(n,'melee'))
    wc=p['weapon']/100*6*w
    cov+=wc; lines.append(('weapon enhancement',round(p['weapon']/100*6,2),w,round(wc,1)))
    cnts=sum(v*d['price'].get(k,0) for k,v in p['counts'].items())
    p['gold']=round(cov+cnts); p['goldCov']=round(cov); p['goldCnt']=round(cnts); p['costLines']=lines
    rows.append(p)
rows.sort(key=lambda x:-x['gold'])
old={p['name']:p for p in json.load(open('page_data4.json'))['players']}
print(f"{'Player':<13}{'NEW':>7}{'OLD':>7}{'  cov':>7}{'cnt':>7}   biggest coverage lines")
for p in rows:
    top=sorted(p['costLines'],key=lambda x:-x[3])[:3]
    print(f"{p['name']:<13}{p['gold']:>7}{old[p['name']]['gold']:>7}{p['goldCov']:>7}{p['goldCnt']:>7}   "
          +", ".join(f"{t[0]} {t[3]}g" for t in top))
print("\nraid total:", sum(p['gold'] for p in rows))
d['price']['__mark__']=round(MARK,2)
json.dump(d, open('page_data5.json','w'), ensure_ascii=False, separators=(',',':'))
