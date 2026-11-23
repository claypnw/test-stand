#!/usr/bin/env python3
"""Build the live Trails and Finds page for the test stand from the last
reviewed sample (sample 78, 2026-10-25), applying the standing deltas:

- the SAMPLE badge and title prefix come off (this is the built page);
- the Goat Camp Trail picture becomes the wide composite — the widened
  scene with the TRUE trail marker joined onto it by hand (the settled
  fix of 2026-10-25: the widened paintings turned the marker's arrow
  the wrong way three times; the composite keeps the arrow true) —
  and Goat Camp joins the WIDE picture set;
- a return door to the Guest Menu stands at the top and the foot of
  the sheet, in the page's own Georgia hand;
- the finder's zero state (Clay, 2026-11-03, after hitting it himself
  with art + bird watching in "and" mode): when nothing matches, the
  count line stands large and bold and a plain helper line stands
  with it — "Nothing matched both picks — try dropping one." Any
  nonzero count renders exactly as before. At Clay's word later the
  same day, the zero count line also stands in the masthead's ember
  red — var(--ember), #b54f24, the color at the very top of the sheet
  (the kicker and the return door both wear it).

- the tale form tells the truth (2026-11-23, CHG-20261123-trails-preview,
  settled with Maggie on Raven's Reach): leaving a tale only shows it on
  the open page — nothing is saved and the keeper is not told — so the
  eight strings that claimed a live posting and a told keeper now say
  it is a page-only preview that a reload removes. The same eight
  changes stand in Maggie's tested patch (blob 9ac1b45f); a rebuild
  must produce that same page.

Everything else stands exactly as sample 78 was reviewed and gated.
Output: ~/workspace/trails-page/build/trails-and-finds.html
"""
import base64
import io
import json
import re
from pathlib import Path

from PIL import Image

SRC = Path.home() / "workspace/your_files/trails-page-sample78-2026-10-25.html"
GOAT = Path.home() / "workspace/trails-page/photos/goat-camp-wide-composite.jpg"
OUT = Path.home() / "workspace/trails-page/build/trails-and-finds.html"

s = SRC.read_text(encoding="utf-8")

# 1. Title: the owner's word, no sample mark.
old_title = "<title>SAMPLE 78 — Trails and Finds in the Holds</title>"
assert s.count(old_title) == 1
s = s.replace(old_title, "<title>Trails and Finds in the Holds</title>")

# 2. The badge comes off; the return door stands in its place at the top.
badge = '<span class="sample">SAMPLE 78 — MORE DETAIL, WORDS IN THE BUBBLES, NOT THE BUILT PAGE</span>'
assert s.count(badge) == 1
top_link = ('<p style="margin:0 0 10px;font-size:1.15rem;">'
            '<a href="guest-menu.html" style="color:#b54f24;">&#8592; Back to the Guest Menu</a></p>')
s = s.replace(badge, top_link)

# 3. The same return door at the foot of the sheet, after the Law.
law_close = '— Sworn by the word of the Hearth, with thanks.</p>\n  </div>\n</div>'
assert s.count(law_close) == 1
foot_link = ('— Sworn by the word of the Hearth, with thanks.</p>\n  </div>\n'
             '  <p style="margin:22px 0 4px;font-size:1.15rem;">'
             '<a href="guest-menu.html" style="color:#b54f24;">&#8592; Back to the Guest Menu</a></p>\n</div>')
s = s.replace(law_close, foot_link)

# 4. Goat Camp: the wide composite picture, and its place in the WIDE set.
goat_bytes = GOAT.read_bytes()
im = Image.open(io.BytesIO(goat_bytes))
assert im.size == (1400, 560), f"composite size {im.size}"
goat_uri = "data:image/jpeg;base64," + base64.b64encode(goat_bytes).decode()
pat = re.compile(r'"Goat Camp Trail":\s*"data:image/jpeg;base64,[A-Za-z0-9+/=]+"')
assert len(pat.findall(s)) == 1
s = pat.sub('"Goat Camp Trail": "' + goat_uri + '"', s)

wide = re.search(r'var WIDE = \{(.*?)\};', s, re.S)
assert wide and "Goat Camp Trail" not in wide.group(1)
s = s.replace('var WIDE = {"Rumsey Park": 1,', 'var WIDE = {"Goat Camp Trail": 1, "Rumsey Park": 1,', 1)

# 5. The finder's zero state: large, bold count line plus the helper line.
css_anchor = '  #count { font-family:Georgia, "Times New Roman", serif; font-size:.9rem; color:var(--muted); }'
assert s.count(css_anchor) == 1
s = s.replace(css_anchor, css_anchor + '\n'
              '  #count.zero { font-size:1.6rem; font-weight:bold; color:#b54f24; }\n'
              '  #noMatch { font-size:1.05rem; color:#2f1a12; margin:2px 0 10px; }')

count_anchor = '  <p id="count"></p>'
assert s.count(count_anchor) == 1
s = s.replace(count_anchor, count_anchor + '\n'
              '  <p id="noMatch" style="display:none;">Nothing matched both picks — try dropping one.</p>')

js_anchor = '    countEl.textContent = "Showing " + shown.length + " of " + ENTRIES.length + " entries" + (showThrift ? ", and the Gilded Pages pointer" : "");'
assert s.count(js_anchor) == 1
s = s.replace(js_anchor, js_anchor + '\n'
              '    var zeroHit = shown.length === 0 && !showThrift;\n'
              '    countEl.classList.toggle("zero", zeroHit);\n'
              '    document.getElementById("noMatch").style.display = zeroHit ? "" : "none";')

# 6. The tale form tells the truth: a page-only preview, honestly named
# (CHG-20261123-trails-preview — the eight changes, each guarded to
# exactly one match, so a rebuild can never bring the false claim back).
tale_changes = [
    (" Leave a tale</span>", " Preview a tale</span>"),
    ("<h3>Leave your tale</h3>", "<h3>Preview your tale</h3>"),
    (">See it as it will stand</button>", ">Preview on this page</button>"),
    ("<h3>As it will stand</h3>", "<h3>Your preview</h3>"),
    ('<p class="facts">Read it as the next traveler will read it. If it stands true, publish it.</p>',
     '<p class="facts">This is a preview only. Your tale is not saved or sent to the keeper.</p>'),
    (">Yes, publish</button>", ">Show on this page</button>"),
    ("<h3>It stands.</h3>", "<h3>Shown on this page only</h3>"),
    ("<p>Your tale is live on this place, for every traveler who comes after. The keeper of the Hearth has been told of it.</p>",
     "<p>Your tale is shown only in this open page. It has not been saved or sent to the keeper. Reloading this page will remove it.</p>"),
]
for old_tale, new_tale in tale_changes:
    assert s.count(old_tale) == 1, f"tale change anchor not unique: {old_tale[:40]}"
    s = s.replace(old_tale, new_tale)

OUT.write_text(s, encoding="utf-8")

# Proof lines
E = json.loads(re.search(r'var ENTRIES = (\[.*?\]);', s, re.S).group(1))
pics = re.findall(r'"([^"]+)":\s*"data:image', re.search(r'var PICS = \{(.*?)\};', s, re.S).group(1))
print(f"entries: {len(E)}")
print(f"pictures: {len(pics)}")
print(f"SAMPLE 78 left: {s.count('SAMPLE 78')}")
print(f"return doors: {s.count('Back to the Guest Menu')}")
print(f"zero style: {s.count('#count.zero')}, helper line: {s.count('Nothing matched both picks')}, zero logic: {s.count('zeroHit')}")
print(f"tale truth: preview named: {s.count('Preview a tale')}, false claims left: {s.count('has been told of it') + s.count('Yes, publish')}")
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
