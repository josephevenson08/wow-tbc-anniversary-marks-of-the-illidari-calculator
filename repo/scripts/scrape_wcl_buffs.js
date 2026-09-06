/*
 * Pulls per-raider, boss-only buff tables out of a Warcraft Logs report.
 *
 * Run it in the browser devtools console with the report open and you signed in.
 * It works by fetching each raider's Buffs view same-origin and reading the
 * rendered table, because the report's own JSON endpoint is not documented.
 *
 * boss=-2&difficulty=0  ->  "All Encounters" = every boss pull, trash excluded.
 */
const REPORT = 'HTxgKGcWPkN67LmZ';

async function participants() {
  const r = await fetch(`/reports/fights-and-participants/${REPORT}/0`, { credentials: 'include' });
  const j = await r.json();
  return (j.friendlies || [])
    .filter(f => !['Pet', 'NPC', 'Boss'].includes(f.type))
    .map(f => ({ id: f.id, name: f.name, cls: f.type }));
}

function grab(sourceId) {
  return new Promise(resolve => {
    const fr = document.createElement('iframe');
    fr.style.cssText = 'position:fixed;left:-9999px;width:1400px;height:900px';
    fr.src = `/reports/${REPORT}?type=auras&hostility=0&boss=-2&difficulty=0&source=${sourceId}`;
    document.body.appendChild(fr);
    let tries = 0;
    const iv = setInterval(() => {
      tries++;
      const d = fr.contentDocument;
      const ready = d && d.querySelector('table.auras-table')?.rows.length > 1;
      if (!ready && tries < 40) return;
      clearInterval(iv);
      const seen = new Set(), rows = [];
      d?.querySelectorAll('table.auras-table').forEach(tb => {
        [...tb.rows].slice(1).forEach(tr => {
          const c = [...tr.cells].map(x => x.innerText.trim().replace(/\s+/g, ' '));
          if (c.length < 4 || !c[0]) return;
          const key = c.slice(0, 3).join('|');
          if (seen.has(key)) return;
          seen.add(key);
          rows.push({ buff: c[0], count: +c[1], uptime: parseFloat(c[2]), source: c[3] });
        });
      });
      fr.remove();
      resolve(rows);
    }, 700);
  });
}

const out = {};
for (const p of await participants()) out[p.name] = await grab(p.id);
console.log(JSON.stringify(out, null, 1));
