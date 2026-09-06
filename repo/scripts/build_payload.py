# -*- coding: utf-8 -*-
import json, runpy
ns=runpy.run_path('gold3.py')
d=json.load(open('page_data5.json')); P=d['players']
L=json.load(open('live_prices.json'))
prices=dict(L['items'])
prices.update({'Gift of Arthas':4.13,'Deadly Poison VII':0.40,"Kreeg's Stout Beatdown":1.0,
 'Noggenfogger Elixir':1.0,'Scourgebane Draught':2.0,'Demonic Rune':prices['Dark Rune'],
 'Thornling Seed':4.0,'Stratholme Holy Water':1.0,'Greater Versatility':3.0,
 'Buff food (average)':round(sum(prices[k] for k in ['Spicy Hot Talbuk',"Fisherman's Feast",'Ravager Dog',
   'Blackened Basilisk','Golden Fish Sticks','Roasted Clefthoof','Grilled Mudfish','Spicy Crawdad'])/8,2),
 'Shattrath flask (1 Mark)':round(max(prices['Flask of Blinding Light'],10*prices['Haste Potion'],10*prices['Destruction Potion']),2), 'Healthstone (conjured)':0, 'Mana Emerald (conjured)':0,
 'Drums of Battle (per charge)':round(prices['Drums of Battle']/50,2)})
CNT={'haste':'Haste Potion','destr':'Destruction Potion','iron':'Ironshield Potion',
 'smana':'Super Mana Potion','omana':'Major Mana Potion','felmana':'Fel Mana Potion',
 'sheal':'Super Healing Potion','rune':'Dark Rune','emerald':'Mana Emerald (conjured)',
 'thistle':'Thistle Tea','hs':'Healthstone (conjured)','seed':'Nightmare Seed','flame':'Flame Cap',
 'felbl':'Fel Blossom','freeact':'Free Action Potion','band':'Heavy Netherweave Bandage',
 'lei':'Lei of Lilies','drum':'Drums of Battle (per charge)','felbomb':'Fel Iron Bomb',
 'ssap':'Super Sapper Charge','gsap':'Goblin Sapper Charge','arcbomb':'Arcane Bomb',
 'adagren':'Adamantite Grenade','mine':'Goblin Land Mine','thorn':'Thornling Seed',
 'holywater':'Stratholme Holy Water'}
WEAPITEM={'Rogue':'Deadly Poison VII','caster':'Superior Wizard Oil','healer':'Superior Mana Oil',
          'melee':'Adamantite Sharpening Stone'}
ROLE=ns['ROLE']
GROUP={}
for k in prices:
    if 'Flask' in k or 'Shattrath' in k: GROUP[k]='Flasks'
    elif 'Elixir' in k or k in ('Gift of Arthas','Greater Versatility','Adept’s Elixir'): GROUP[k]='Elixirs'
    elif k.startswith('Scroll'): GROUP[k]='Scrolls'
    elif 'Potion' in k or 'Rune' in k or 'Emerald' in k or k=='Thistle Tea': GROUP[k]='Potions & runes'
    elif 'Oil' in k or 'Stone' in k or 'Poison' in k: GROUP[k]='Weapon'
    elif 'Bomb' in k or 'Sapper' in k or 'Grenade' in k or 'Mine' in k or 'Holy Water' in k: GROUP[k]='Engineering'
    elif 'Drums' in k: GROUP[k]='Drums'
    else: GROUP[k]='Food & utility'
GROUP["Adept's Elixir"]='Elixirs'

for p in P:
    items=[]
    for name,units,price,cost in p['costLines']:
        if name=='weapon enhancement':
            items.append([WEAPITEM[ROLE.get(p['name'],'melee')], round(units,2)]); continue
        item,full=ns['BUFF'][name]
        key = 'Shattrath flask (1 Mark)' if item=='__MARK__' else ('Buff food (average)' if item=='__FOOD__' else item)
        items.append([key, round(units,2)])
    for k,v in p['counts'].items():
        if k in CNT and v: items.append([CNT[k], v])
    merged={}
    for k,q in items: merged[k]=round(merged.get(k,0)+q,2)
    p['items2']=sorted(merged.items(), key=lambda x:-x[1]*prices.get(x[0],0))
    p.pop('costLines',None); p.pop('cov',None)
d['prices']=prices; d['groups']=GROUP
d['markItems']={'flask':'Flask of Blinding Light','haste':'Haste Potion','destr':'Destruction Potion'}
d.pop('price',None); d.pop('units',None)
P.sort(key=lambda x:x['rank'])
json.dump(d, open('page_data6.json','w'), ensure_ascii=False, separators=(',',':'))
print("bytes",len(open('page_data6.json').read()),"| priced items",len(prices))
tot=0
for p in P:
    g=sum(q*prices.get(k,0) for k,q in p['items2']); tot+=g
    if p['name'] in ('Donkin','Thundaqt','Cowboy'):
        print(f"\n{p['name']} = {g:.0f}g")
        for k,q in p['items2'][:6]: print(f"   {k:<34}{q:>7} x {prices.get(k,0):>6.2f} = {q*prices.get(k,0):>7.1f}")
print("\nraid total %.0fg"%tot)
