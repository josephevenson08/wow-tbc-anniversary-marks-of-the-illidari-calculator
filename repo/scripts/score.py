# -*- coding: utf-8 -*-
import json
F = 17  # boss fights (verified: all CLA percentages are exact multiples of 1/17)

# ---- CLA: buff coverage (% of 17 boss fights) ----
# name: [battle%, guardian%, flask%, food%, scroll%, weapon%, scroll_types, suboptimal_flags]
cla = {
"Bmztilt":      [94, 94,   6, 100,  82, 100, "Spi", []],
"Captrawr":     [88, 76,  12, 100,  53,  94, "Agi*,Prot*,Str*", []],
"Oddbird":      [76, 76,  12,  88,  35,  88, "Prot", []],
"Pierogi":      [ 0,  0, 100, 100,   0, 100, "-", []],
"Cowboy":       [ 0,  0, 100, 100, 100, 100, "Agi", []],
"Grazzyknoll":  [88, 59,   0, 100,  41,  59, "Agi,Spi", []],
"Thundaqt":     [35, 35,  53,  94,  94,  88, "Agi,Str", []],
"Azzblast":     [ 0,  0, 100,  94,   0, 100, "-", []],
"Celions":      [ 0,  0, 100, 100,  24,   6, "Agi,Str", []],
"Likapally":    [100,35,   0,  94,  65, 100, "Spi", []],
"Thotiana":     [ 0,  0,  88, 100,  82,  65, "Agi,Prot", ["Well Fed (weak food)"]],
"Caicey":       [100,100,  0, 100, 100, 100, "Spi", []],
"Kapisce":      [ 0,  0, 100, 100,  94,  94, "Spi", []],
"Orixon":       [41, 41,  59, 100,  71, 100, "Agi,Str", []],
"Donkin":       [53, 47,  35, 100,  94, 100, "Agi,Str,Str*", ["Elixir of the Mongoose"]],
"Masun":        [100,100,  0, 100,   0, 100, "-", []],
"Planet":       [100,100,  0, 100, 100, 100, "Prot,Spi", []],
"Spliff":       [100,100,  0, 100,  94, 100, "Spi", ["Superior Wizard Oil","Superior Mana Oil"]],
"Ohm":          [82,  0,   0,  94,   0, 100, "-", ["Superior Wizard Oil"]],
"Junnox":       [ 0,  0, 100, 100,   0, 100, "-", []],
"Novick":       [ 0,  0,  94,  88,   0,  94, "-", []],
"Zev":          [ 0,  0, 100, 100,   0, 100, "-", []],
"Shoutofearth": [41,  0,  59, 100,   0, 100, "-", ["Elixir of Major Strength"]],
"Threatbull":   [41,  0,  59, 100,  94, 100, "Agi,Str", []],
"Woksauce":     [ 6,  0,  94, 100,  94, 100, "Agi,Str", []],
}

# ---- RPB: raw active consumable counts ----
# perf = Haste/Destruction/Ironshield ; sustain = mana pots/runes/emerald/thistle/super heal ; util = free & situational
rpb = {
#                haste destr iron  | smana omana felmana rune emerald thistle sheal | hs seed flame felbl freeact bandage lei | GoA_uptime
"Bmztilt":      dict(haste=0,destr=0,iron=0, smana=13,omana=0,felmana=0,rune=12,emerald=0,thistle=0,sheal=0, hs=0,seed=0,flame=0,felbl=0,freeact=0,band=0,lei=0, goa=0.0),
"Captrawr":     dict(haste=4,destr=0,iron=2, smana=0,omana=0,felmana=0,rune=0,emerald=0,thistle=0,sheal=0, hs=2,seed=0,flame=0,felbl=0,freeact=0,band=0,lei=0, goa=0.40),
"Oddbird":      dict(haste=0,destr=0,iron=0, smana=0,omana=0,felmana=0,rune=0,emerald=0,thistle=0,sheal=0, hs=1,seed=0,flame=0,felbl=0,freeact=0,band=0,lei=0, goa=0.33),
"Pierogi":      dict(haste=0,destr=20,iron=0, smana=9,omana=9,felmana=0,rune=15,emerald=0,thistle=0,sheal=0, hs=1,seed=0,flame=0,felbl=0,freeact=0,band=0,lei=0, goa=0.0),
"Cowboy":       dict(haste=19,destr=0,iron=0, smana=4,omana=0,felmana=8,rune=0,emerald=0,thistle=0,sheal=0, hs=10,seed=0,flame=0,felbl=0,freeact=0,band=0,lei=0, goa=0.0),
"Grazzyknoll":  dict(haste=0,destr=0,iron=0, smana=0,omana=0,felmana=0,rune=0,emerald=0,thistle=0,sheal=0, hs=9,seed=0,flame=0,felbl=0,freeact=0,band=1,lei=0, goa=0.0),
"Thundaqt":     dict(haste=27,destr=0,iron=0, smana=6,omana=0,felmana=0,rune=7,emerald=0,thistle=0,sheal=0, hs=4,seed=0,flame=18,felbl=0,freeact=0,band=1,lei=0, goa=0.0),
"Azzblast":     dict(haste=0,destr=21,iron=0, smana=12,omana=0,felmana=0,rune=0,emerald=37,thistle=0,sheal=0, hs=0,seed=0,flame=0,felbl=0,freeact=0,band=0,lei=0, goa=0.0),
"Celions":      dict(haste=10,destr=0,iron=0, smana=2,omana=0,felmana=0,rune=1,emerald=0,thistle=0,sheal=0, hs=5,seed=2,flame=0,felbl=0,freeact=0,band=1,lei=0, goa=0.0),
"Likapally":    dict(haste=0,destr=0,iron=0, smana=16,omana=0,felmana=0,rune=0,emerald=0,thistle=0,sheal=0, hs=7,seed=0,flame=0,felbl=0,freeact=0,band=0,lei=2, goa=0.0),
"Thotiana":     dict(haste=4,destr=0,iron=4, smana=2,omana=0,felmana=0,rune=0,emerald=0,thistle=0,sheal=0, hs=0,seed=8,flame=0,felbl=0,freeact=0,band=0,lei=0, goa=0.0),
"Caicey":       dict(haste=0,destr=0,iron=0, smana=16,omana=0,felmana=0,rune=7,emerald=0,thistle=0,sheal=0, hs=0,seed=0,flame=0,felbl=0,freeact=0,band=0,lei=0, goa=0.0),
"Kapisce":      dict(haste=0,destr=23,iron=0, smana=8,omana=0,felmana=0,rune=0,emerald=0,thistle=0,sheal=0, hs=7,seed=0,flame=0,felbl=0,freeact=0,band=0,lei=0, goa=0.0),
"Orixon":       dict(haste=13,destr=0,iron=0, smana=0,omana=0,felmana=0,rune=0,emerald=0,thistle=10,sheal=9, hs=16,seed=0,flame=0,felbl=1,freeact=2,band=4,lei=0, goa=0.0),
"Donkin":       dict(haste=29,destr=0,iron=0, smana=7,omana=0,felmana=0,rune=0,emerald=0,thistle=0,sheal=0, hs=13,seed=0,flame=0,felbl=0,freeact=0,band=0,lei=0, goa=0.0),
"Masun":        dict(haste=0,destr=0,iron=0, smana=8,omana=0,felmana=0,rune=0,emerald=0,thistle=0,sheal=0, hs=3,seed=0,flame=0,felbl=0,freeact=0,band=0,lei=0, goa=0.0),
"Planet":       dict(haste=0,destr=0,iron=0, smana=12,omana=0,felmana=0,rune=12,emerald=0,thistle=0,sheal=0, hs=0,seed=0,flame=0,felbl=0,freeact=0,band=0,lei=0, goa=0.0),
"Spliff":       dict(haste=0,destr=0,iron=0, smana=27,omana=0,felmana=0,rune=6,emerald=0,thistle=0,sheal=0, hs=6,seed=0,flame=0,felbl=0,freeact=0,band=0,lei=0, goa=0.0),
"Ohm":          dict(haste=0,destr=0,iron=0, smana=0,omana=7,felmana=0,rune=0,emerald=0,thistle=0,sheal=0, hs=8,seed=0,flame=0,felbl=0,freeact=0,band=0,lei=0, goa=0.0),
"Junnox":       dict(haste=0,destr=11,iron=0, smana=16,omana=0,felmana=0,rune=5,emerald=0,thistle=0,sheal=0, hs=8,seed=0,flame=0,felbl=0,freeact=1,band=3,lei=0, goa=0.0),
"Novick":       dict(haste=0,destr=5,iron=0, smana=5,omana=0,felmana=0,rune=0,emerald=0,thistle=0,sheal=0, hs=6,seed=0,flame=0,felbl=0,freeact=0,band=1,lei=0, goa=0.0),
"Zev":          dict(haste=0,destr=21,iron=0, smana=0,omana=0,felmana=0,rune=5,emerald=0,thistle=0,sheal=0, hs=5,seed=0,flame=0,felbl=0,freeact=0,band=0,lei=0, goa=0.0),
"Shoutofearth": dict(haste=0,destr=0,iron=0, smana=0,omana=0,felmana=0,rune=0,emerald=0,thistle=0,sheal=1, hs=10,seed=0,flame=0,felbl=0,freeact=0,band=0,lei=0, goa=0.0),
"Threatbull":   dict(haste=21,destr=0,iron=0, smana=0,omana=0,felmana=0,rune=0,emerald=0,thistle=0,sheal=1, hs=7,seed=0,flame=0,felbl=0,freeact=0,band=0,lei=0, goa=0.0),
"Woksauce":     dict(haste=23,destr=0,iron=0, smana=0,omana=0,felmana=0,rune=0,emerald=0,thistle=0,sheal=0, hs=11,seed=0,flame=0,felbl=0,freeact=0,band=0,lei=0, goa=0.0),
}

# drums: CLA weighted score (party-buffs actually delivered)
drums = {"Cowboy":22,"Grazzyknoll":89,"Donkin":237,"Masun":144,"Planet":105,"Spliff":49}
drum_counts = {"Cowboy":18,"Grazzyknoll":51,"Donkin":60,"Masun":38,"Planet":34,"Spliff":32}
drum_waste  = {"Grazzyknoll":4,"Spliff":9}
# engineering consumable damage
engi = {"Pierogi":67679,"Thundaqt":102567,"Thotiana":107315,"Junnox":65588,"Threatbull":60779,"Woksauce":64017}

roles = {
"Bmztilt":"Resto Druid (heal)","Captrawr":"Druid tank","Oddbird":"Druid tank","Pierogi":"Balance Druid",
"Cowboy":"Hunter","Grazzyknoll":"Hunter","Thundaqt":"Hunter","Azzblast":"Mage","Celions":"Ret Paladin",
"Likapally":"Holy Paladin","Thotiana":"Prot Paladin (tank)","Caicey":"Priest (heal)","Kapisce":"Shadow Priest",
"Orixon":"Rogue","Donkin":"Enh Shaman","Masun":"Enh Shaman","Planet":"Resto Shaman","Spliff":"Resto Shaman",
"Ohm":"Ele Shaman","Junnox":"Warlock","Novick":"Warlock","Zev":"Warlock",
"Shoutofearth":"Warrior","Threatbull":"Warrior","Woksauce":"Warrior",
}

W = dict(battle=18, guard=18, food=12, weap=12, scroll=10, active=22, util=8)

rows=[]
for n,(b,g,fl,fd,sc,wp,st,sub) in cla.items():
    r=rpb[n]
    battle_slot=min(100,b+fl); guard_slot=min(100,g+fl)
    perf_n=r['haste']+r['destr']+r['iron']
    sust_n=r['smana']+r['omana']+r['felmana']+r['rune']+r['emerald']+r['thistle']+r['sheal']
    util_n=r['hs']+r['seed']+r['flame']+r['felbl']+r['freeact']+r['band']+r['lei']
    perf_r, sust_r, util_r = perf_n/F, sust_n/F, util_n/F
    A=battle_slot/100*W['battle']; B=guard_slot/100*W['guard']; C=fd/100*W['food']
    D=wp/100*W['weap']; E=sc/100*W['scroll']
    act_r=(perf_n+sust_n)/F
    P=min(act_r/2.0,1)*W['active']; S=0.0; U=min(util_r/0.8,1)*W['util']
    core=A+B+C+D+E+P+U
    bd=min(drums.get(n,0)/237,1)*8.0
    be=min(engi.get(n,0)/107315,1)*3.0
    bg=r['goa']/0.40*2.0 if r['goa'] else 0.0
    bonus=bd+be+bg
    pen=1.5*len(sub)
    rows.append(dict(name=n,role=roles[n],battle_slot=battle_slot,guard_slot=guard_slot,food=fd,weap=wp,scroll=sc,
        perf_n=perf_n,sust_n=sust_n,util_n=util_n,perf_r=round(perf_r,2),sust_r=round(sust_r,2),util_r=round(util_r,2),act_r=round((perf_n+sust_n)/F,2),
        A=A,B=B,C=C,D=D,E=E,P=P,S=S,U=U,core=core,bonus=bonus,bd=bd,be=be,bg=bg,pen=pen,
        total=core+bonus-pen, sub=sub, scroll_types=st,
        drums=drum_counts.get(n,0), drum_score=drums.get(n,0), drum_waste=drum_waste.get(n,0), engi=engi.get(n,0)))

rows.sort(key=lambda x:-x['total'])
for i,r in enumerate(rows,1):
    r['rank']=i
json.dump(rows,open('/home/claude/wow/ranked.json','w'),indent=1)
print(f"{'#':>3} {'Player':<13}{'Role':<20}{'Tot':>6} {'Core':>6} {'Bon':>5} {'Pen':>5} | {'Btl':>4}{'Grd':>4}{'Food':>5}{'Wpn':>5}{'Scr':>5} | {'act/f':>6}{'util/f':>7} {'drums':>6}{'engi':>7}")
print("-"*115)
for r in rows:
    print(f"{r['rank']:>3} {r['name']:<13}{r['role']:<20}{r['total']:>6.1f} {r['core']:>6.1f} {r['bonus']:>5.1f} {-r['pen']:>5.1f} | "
          f"{r['battle_slot']:>4}{r['guard_slot']:>4}{r['food']:>5}{r['weap']:>5}{r['scroll']:>5} | {r['act_r']:>6}{r['util_r']:>7} {r['drum_score']:>6}{r['engi']:>7}")
