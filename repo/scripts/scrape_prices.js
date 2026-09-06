/*
 * Pulls current TBC Anniversary auction prices from BootyBayBroker.
 * Run in the browser devtools console on https://bootybaybroker.com/tbc-classic/ah
 *
 * Their pages are server-rendered, so a same-origin fetch returns the table.
 * Prices are US region, hourly from TradeSkillMaster. There is no realm-level
 * filter and no first-party Blizzard API: the Classic auction endpoints have
 * returned 404 for the dynamic-classic1x namespaces since late 2024.
 */
const WANTED = [
  'Flask of Relentless Assault', 'Flask of Pure Death', 'Flask of Blinding Light',
  'Elixir of Major Agility', 'Elixir of Draenic Wisdom', 'Elixir of Demonslaying',
  'Haste Potion', 'Destruction Potion', 'Super Mana Potion', 'Dark Rune',
  'Superior Wizard Oil', 'Adamantite Sharpening Stone', 'Scroll of Agility V',
  'Drums of Battle', 'Flame Cap', 'Nightmare Seed', 'Free Action Potion',
];

const toGold = s => {
  if (!s) return null;
  const g = (s.match(/(\d[\d,]*)\s*g/) || [])[1];
  const si = (s.match(/(\d+)\s*s/) || [])[1];
  const c = (s.match(/(\d+)\s*c/) || [])[1];
  if (g === undefined && si === undefined && c === undefined) return null;
  return +(g || 0).toString().replace(/,/g, '') + +(si || 0) / 100 + +(c || 0) / 10000;
};

async function query(q) {
  const r = await fetch(`/tbc-classic/ah?region=us&q=${encodeURIComponent(q)}`, { credentials: 'include' });
  const doc = new DOMParser().parseFromString(await r.text(), 'text/html');
  const rows = [];
  doc.querySelectorAll('table tr').forEach(tr => {
    const c = [...tr.cells].map(x => x.innerText.replace(/\s+/g, ' ').trim());
    if (c.length < 5) return;
    const name = (c[0] || '').replace(/ (common|uncommon|rare|epic|poor) quality$/, '').trim();
    if (!name || /^ITEM/i.test(name)) return;
    rows.push({ name, alliance: toGold(c[1]), horde: toGold(c[4]) });   // horde is column 5
  });
  return rows;
}

const found = {};
for (const q of ['flask', 'elixir', 'potion', 'scroll', 'oil', 'sharpening', 'drums', 'rune', 'cap']) {
  (await query(q)).forEach(r => { if (WANTED.includes(r.name)) found[r.name] = r.horde; });
}
console.log(JSON.stringify(found, null, 1));
