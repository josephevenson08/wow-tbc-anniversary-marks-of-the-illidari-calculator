# WoW TBC Anniversary — Marks of the Illidari Calculator

A raid-night consumable audit and Marks distributor for **The Burning Crusade Anniversary**,
built from a real Black Temple log.

It answers two questions a raid lead actually has to settle:

1. **Who brought consumables, and who didn't?** Every raider is scored 1–25 on flasks, both
   elixir slots, food, weapon enhancements, scrolls, combat and mana potions, drums, utility
   items and engineering consumables — bosses only.
2. **How do we split the Marks of the Illidari fairly?** Marks redeem for consumables, so the
   split is a reimbursement. Enter the raid's Mark total and the page distributes it by gold spent
   alone: by default every raider gets back the same share of their own outlay. Raiders can be
   excluded from the pool, and the whole result exports as a PNG.

The whole thing is one self-contained `index.html`. No build step, no dependencies, no server.

---

## Why Marks are the right thing to redistribute

A Mark of the Illidari redeems for **exactly one** of:

| Redemption | Value at the bundled prices |
|---|---|
| One Shattrath flask (Blinding Light) | **92.27g** |
| Ten Haste Potions | **82.10g** |
| Ten Destruction Potions | **81.90g** |

Never a combination — you pick one. That makes a Mark worth roughly 82–92g of consumables
depending on which redemption you take, and it makes the distribution question simple:
Marks are the raid paying back the people who funded the raid.

The Shattrath flasks are restricted to SSC, TK, Hyjal, Black Temple and Sunwell, and require
Exalted with The Sha'tar, Cenarion Expedition, and Aldor or Scryers.

## The scoring model

The score ranks preparation. It does **not** feed the Mark split — that runs on gold spent alone
(see [The Mark split](#the-mark-split) below). The two answer different questions: who prepared
well, and who is owed money.

100 points every raider controls, plus bonuses for consumables only some professions can bring,
minus flags for using the wrong item.

| Component | Weight | Measure |
|---|---:|---|
| Battle elixir slot | 18 | Share of boss fights with a battle elixir **or** flask up |
| Guardian elixir slot | 18 | Share with a guardian elixir **or** flask up |
| Food buff | 12 | Share of fights Well Fed |
| Weapon enhancement | 12 | Oil, stone or poison on the weapon |
| Scrolls | 10 | Share of fights with any scroll active |
| Active potions | 22 | Haste, Destruction, Ironshield, mana potions, runes, Mana Emerald, Thistle Tea, Super Healing — per fight, full credit at 2.0/fight |
| Utility items | 8 | Healthstones, Nightmare Seed, Flame Cap, Fel Blossom, Free Action, bandages — per fight, full credit at 0.8/fight |
| Drums bonus | +8 | Party haste applications actually delivered (drums × buffs landed) |
| Engineering bonus | +3 | Damage from bombs, sappers, grenades |
| Gift of Arthas bonus | +2 | Uptime of the raid-wide +8 damage-taken disease |
| Suboptimal flag | −1.5 each | Wrong item for the slot |

**A flask fills both elixir slots.** The battle and guardian columns are combined slot coverage;
the separate flask column is informational, and a low number there is not a fault.

**Combat and mana potions share one 22-point pool** rather than being scored separately. A warrior
can never drink a mana potion and a healer has no use for a Destruction Potion, so splitting them
would hand every role a category it structurally cannot win.

### Is the ranking robust?

`scripts/sensitivity.py` re-rolls every weight, cap and bonus ceiling 4,000 times at ±40% and
re-sorts. 23 of 25 raiders land within two places of their listed rank in at least 86% of runs.

## The Mark split

Marks are distributed on estimated gold spent — no score, no parse, no role. Every raider in the
pool lands in one of three bands by what they spent:

| Band | Default cut | Raiders | Spend | Share of raid | Derived share |
|---|---|---:|---:|---:|---:|
| Top | 500g and up | 7 | 4,729g | 49.6% | 4.9× |
| Middle | 250–499g | 10 | 3,707g | 38.9% | 2.7× |
| Bottom | under 250g | 8 | 1,095g | 11.5% | 1.0× |

**Share counts are derived, not typed in.** Each raider carries their band's mean spend as their
weight, so every band is reimbursed at the same rate as every other and everyone inside a band is
paid alike. Change the mark total, the prices, or who is in the pool and the shares recompute.
Marks that don't divide evenly go to the biggest spender first, which — because gold order is band
order — hands them to the top band first and keeps the bands ordered.

### The cut points find themselves

**Cut points are derived too, on `Auto`.** They come from a three-class
[Jenks natural breaks](https://en.wikipedia.org/wiki/Jenks_natural_breaks_optimization)
fit — the pair of splits leaving the least variation inside each band — rounded to the nearest
tidy figure that still sits inside the gap. On the bundled log that lands on **500 / 200**, a
7 / 11 / 7 split with 45g and 64g of clear air either side of the cuts.

This matters because a raid's spend shape changes every week, and hand-picked cut points go stale
immediately. Exclude the top spender and the cuts move to 450 / 200 on their own. `Manual` unlocks
the two boxes and hands over whatever Auto last worked out, so you start from a sane place.

A warning about tuning cuts by hand: it is tempting to pick the cuts that land closest to the
per-gold split, but that objective is unstable. It chases integer rounding, so it moves with the
mark total — 660 / 315 at 30 marks, 350 / 185 at 40, 500 / 350 at 80. Jenks reads the shape of the
spend instead and ignores the mark total, which is why Auto uses it.

### Bands or per gold

The **Split shape** toggle picks how those weights get spent:

- **Per gold** *(default)* — each raider is reimbursed on their own spend. Every raider gets back
  the same percentage, the ordering can never invert, and there is nothing to re-tune week to week.
  The easiest to defend one-on-one: "you spent 446g, he spent 543g, everyone got 39% back."
- **Bands** — everyone in a band gets the same number of marks, at the rate that band averaged. A
  tidier rule to announce, at the cost of a cliff on each cut point: at 40 marks Junnox on 498g
  gets 2 while Donkin on 543g gets 3, so 45g of spend costs a whole mark.

Per gold is the fairer per gold spent — by construction it is exactly proportional, where even the
best-fitting bands move a couple of marks away from it. Bands are the more announceable. Both run
off the same gold figures and neither touches the score.

### Floors

Two guarantees sit on top of the bands: a **tank floor** (1 by default) and a **floor for
everyone** (0 by default). Both are true minimums, not bonuses — a raider whose own band share
already earns more keeps the larger figure. Tanking costs money the log does not always show,
which is what the tank floor is for.

They are applied by re-splitting rather than by reservation. Anyone the share split leaves under
their floor is pinned at it and dropped out of the weighted pool, then the remaining marks are
re-split over whoever is left, repeating until nobody is short. That keeps the total exact and the
bands ordered: with everyone floored at 1 the split still comes out 3 / 1–2 / 1, where simply
reserving a mark per head would flatten it to 2 / 1–2 / 1. Rows lifted this way are tagged `min`
in the table.

On the defaults that means the two bottom-band tanks are lifted to one Mark each, taken out of the
middle band, while the top-band tank keeps the three her spend earns.

### Picking a total

The mark total is the constraint that actually decides how this feels, and it is worth being blunt
about the arithmetic. At 92g a Mark, **40 marks is 3,690g of value against 9,531g of spend — the
raid can only give back 39% of what it cost.** Spread over 25 raiders that is 1.6 marks each, so
any scheme is going to leave the bottom of the roster on nought or one.

That is why the bottom of the roster rounds to zero: it is not the shares or the cuts being
harsh, it is that those raiders put in about a tenth of the gold, and a tenth of 40 marks is four
marks between them. The levers that change it are the mark total and the floors, not the shares
and not the cut points:

- **Raise the total.** More marks, less rounding, everyone moves up.
- **Floor for everyone = 1.** Nobody leaves with nothing. The re-splitting floor keeps the bands
  ordered while it does this — the split still comes out 3 / 1–2 / 1.
- **Leave it.** Faithful reimbursement: you get back a share of what you put in, and if you put in
  little you get little.

If the floors themselves overrun the total, the split falls back to an even one and says so in a
banner.

Raiders can be checked out of the pool entirely with the **In** column; their shares are
redistributed among everyone left, and they are dropped from both PNG exports.

## The gold estimate

Counted consumables are quantity × unit price. Coverage percentages are converted to units first,
using how long each buff lasts against the raid's length: a flask runs two hours and survives death
(2 per raid at 100%), elixirs run an hour and are lost on death (6), food and scrolls run 30 minutes
(8 and 6), weapon enhancement 6.

Conjured items — Healthstones from the warlocks, a mage's Mana Emeralds — are priced at zero,
because nobody bought them.

### Prices

`data/live-prices-2026-09-06.json` holds 58 real TBC Anniversary auction prices (US region, Horde
market value, hourly from TradeSkillMaster via BootyBayBroker).

There is no first-party price API. Blizzard's Classic auction house endpoints have returned 404 for
the `dynamic-classic1x` namespaces since late 2024; the issue was acknowledged in March 2025 and is
still open. Nothing available is realm-specific either, so these are region-wide figures.

Because of that the page takes prices from you three ways: edit any field, paste a list in any
reasonable format (`Flask of Relentless Assault 132g`, `Super Mana Potion, 14`, `Haste Potion 15g 50s`),
or restore the bundled snapshot. Whatever you set travels in the share link.

Prices move hourly. Re-run `scripts/scrape_prices.js` when they drift.

## The data

| File | What it is |
|---|---|
| `data/wcl-boss-buffs.json` | Every named consumable buff per raider, with applications and uptime, boss fights only |
| `data/live-prices-2026-09-06.json` | 58 auction prices with source and pull date |
| `data/page-data.json` | The assembled payload the page renders from |

The buff data was read out of the report's own boss-only buff tables, one raider at a time, and
cross-checked against the CLA and RPB analyzer workbooks. The counts agree: Destruction Potions
20 / 21 / 23 for the three casters, haste potions 29 and 21 for the two top melee.

The fight list confirms **17 boss encounters — 9 kills and 8 wipes**. Every coverage percentage on
the analyzer sheets is an exact seventeenth, and 17 fits with about a sixth the error of any other
denominator from 15 to 19 (`scripts/verify_fight_count.py`).

## Scripts

| Script | Purpose |
|---|---|
| `scripts/scrape_wcl_buffs.js` | Pull per-raider boss-only buff tables from a Warcraft Logs report (browser console) |
| `scripts/scrape_prices.js` | Pull current Anniversary auction prices (browser console) |
| `scripts/parse_cla_pdf.py` | Read the CLA analyzer workbook's coverage table out of its PDF |
| `scripts/parse_rpb_pdf.py` | Read the RPB workbook's consumable counts out of its PDF |
| `scripts/score.py` | Build the 1–25 ranking |
| `scripts/gold_live.py` | Convert consumable usage to gold at live prices |
| `scripts/sensitivity.py` | Monte-Carlo the weights to test rank stability |
| `scripts/build_payload.py` | Assemble `data/page-data.json` |

Python scripts need `pdfplumber` for the PDF parsers; everything else is standard library.

## Using it for your own raid

1. Open your report on Warcraft Logs, signed in.
2. Run `scripts/scrape_wcl_buffs.js` in the console with `REPORT` set to your report code.
3. Run the CLA and RPB analyzer sheets on the same log and export them.
4. Run `scripts/scrape_prices.js` for current prices.
5. Rebuild with `scripts/build_payload.py`, then open `index.html`.

Or just open `index.html`, ignore the roster, and use the Marks distributor and price panel —
the settings all live in the URL.

## Caveats worth reading

- **Windfury and weapon enhancement.** Windfury Totem occupies the same weapon imbue slot as a
  sharpening stone, so melee parked with an enhancement shaman can read near-zero weapon coverage
  through no fault of their own. Check party layout before treating it as a prep failure.
- **Missing combatant info.** Some Tier 6 fights drop the `combatantInfo` block carrying consumable
  data when a logger is far from the boss at pull. A raider at 94% rather than 100% may be a logging
  artefact rather than a missed flask.
- **Prices are region-wide and hourly**, not your realm and not live.
- **Engineering, drums and Gift of Arthas are bonuses only.** Nobody is penalised for not having the
  profession.

## Credits

Consumable and gear analysis workbooks by the Classic Log Analyzer (CLA) and Raid Performance Board
(RPB) community tools. Log data from Warcraft Logs. Price data from BootyBayBroker's TradeSkillMaster
feed. Item mechanics from Wowhead.
