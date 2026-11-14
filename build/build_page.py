#!/usr/bin/env python3
"""Build effort-log.html from effort-data.csv (same folder)."""
import csv, os
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, 'effort-data.csv'))))

def mins(sec):
    s = float(sec or 0)
    if s <= 0: return '—'
    m = s / 60.0
    return f'{m:,.1f}' if m < 100 else f'{m:,.0f}'

def tok(n):
    n = int(n or 0)
    return f'{n:,}' if n > 0 else '—'

days = OrderedDict()
for r in rows:
    days.setdefault(r['date'], []).append(r)

parts = []
parts.append('''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Effort log</title>
<style>
  body { background:#f3efe4; color:#111; font-family: Georgia, serif; margin:0; padding:24px 16px; }
  .page { background:#fffdf5; max-width:820px; margin:0 auto; padding:24px 28px 28px; border:1px solid #d8d2c0; }
  h1 { font-size:30px; margin:0 0 6px; }
  h2 { font-size:21px; margin:26px 0 8px; border-bottom:2px solid #111; padding-bottom:4px; }
  p, li { font-size:16px; line-height:1.5; }
  table { border-collapse:collapse; width:100%; margin:6px 0 4px; }
  th, td { text-align:left; font-size:15px; padding:5px 8px; border-bottom:1px solid #d8d2c0; }
  th { border-bottom:2px solid #111; }
  td.n, th.n { text-align:right; }
  .note { font-size:13.5px; color:#444; }
  .total td { font-weight:bold; border-top:2px solid #111; }
</style></head><body><div class="page">
<h1>Effort log</h1>
<p>What each job costs to run, day by day: how many times it ran, how many minutes it took, and how much it read in and wrote out, in tokens. A token is a small piece of a word — the meter Muse's work is counted in.</p>
<p>How to read the token counts: "read in" counts the standing pages a job reads again at every step, so a long job's count runs into the millions without meaning millions of new words. Some jobs run with no agent and leave no token record; those lines say so. Your plan's own meter — the weekly percent — does not split by job, so it is not on this page.</p>
''')

for date, drows in reversed(list(days.items())):
    parts.append(f'<h2>{date}</h2><table><tr><th>Job</th><th class="n">Runs</th><th class="n">Minutes</th><th class="n">Tokens read in</th><th class="n">Tokens written out</th></tr>')
    t_runs = t_sec = t_in = t_out = 0
    for r in drows:
        t_runs += int(r['runs']); t_sec += float(r['run_seconds'] or 0)
        t_in += int(r['in_tok'] or 0); t_out += int(r['out_tok'] or 0)
        note = f' <span class="note">({r["note"]})</span>' if r['note'] else ''
        parts.append(f'<tr><td>{r["job"]}{note}</td><td class="n">{r["runs"]}</td><td class="n">{mins(r["run_seconds"])}</td><td class="n">{tok(r["in_tok"])}</td><td class="n">{tok(r["out_tok"])}</td></tr>')
    parts.append(f'<tr class="total"><td>Day total so far</td><td class="n">{t_runs}</td><td class="n">{mins(t_sec)}</td><td class="n">{tok(t_in)}</td><td class="n">{tok(t_out)}</td></tr></table>')

# First-week self-count: what the effort log itself costs
self_rows = [r for r in rows if r['job'] == 'Effort log nightly' and '2026-11-11' <= r['date'] <= '2026-11-18']
s_sec = sum(float(r['run_seconds'] or 0) for r in self_rows)
s_in = sum(int(r['in_tok'] or 0) for r in self_rows)
s_out = sum(int(r['out_tok'] or 0) for r in self_rows)
parts.append('<h2>First week self-count — what this log itself costs</h2>')
parts.append('<p>Clay asked for this count for the first week, November 10–17, so the cost of keeping the log stands next to the log.</p><ul>')
parts.append('<li>Setup, November 10, done by hand in chat: about 15 minutes of chat work, shared with other work in the same stretch. No separate token record stands for chat work, so this line is minutes only.</li>')
if self_rows:
    parts.append(f'<li>The nightly log job itself: {len(self_rows)} run(s) so far, {mins(s_sec)} minutes, {tok(s_in)} tokens read in, {tok(s_out)} written out. Its newest run always lands in the next day\'s table, so this count runs one day behind.</li>')
else:
    parts.append('<li>The nightly log job itself: no runs yet — its first run is the morning of November 11, and each run lands in the next day\'s table.</li>')
parts.append('</ul>')
parts.append('</div></body></html>')
open(os.path.join(HERE, 'effort-log.html'), 'w').write('\n'.join(parts))
print('built effort-log.html')
