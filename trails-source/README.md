# Trails and Finds — source home

This folder holds the production source for the Trails and Finds page
(`trails-and-finds.html` at the root of this repository, live at
https://test-stand-6ku.pages.dev/trails-and-finds.html).

## What stands here

- `build_page.py` — the builder that makes the page. It reads the last
  reviewed sample page (sample 78, 2026-10-25, kept in the local trails
  home at `~/workspace/trails-page/` on Muggy's machine, with the source
  list `trail-and-finds-list.md` and the `photos/` folder beside it),
  applies the standing changes named in its own header, and writes the
  finished page. The local working copy stands at
  `~/workspace/trails-page/build/build_page.py`; this copy is the
  escrow copy, kept identical.
- `trails-existing-source.json` — the page's 27 entries and picture
  keys exactly as recovered from the live page on 2026-11-23 (Maggie's
  recovery, Raven's Reach, Trails-Work-For-Maggie). Nothing in it was
  retyped.
- `Trails-Living-Record-0.1.md` — Maggie's living working record built
  from those 27 entries: what each entry says, what is not yet checked,
  and the working process for keeping it current.

## The 2026-11-23 change (CHG-20261123-trails-preview)

The tale form on the page only ever showed a visitor's tale on the
open page — nothing was saved and the keeper was not told — while its
words claimed the tale stood live for every traveler and that the
keeper had been told. Eight strings were changed so the form names
itself a page-only preview that a reload removes. No other words, no
entry, and no picture changed.

- Baseline page blob: dee2507538181dae731622d81d544a895688946d (rollback
  restores this blob through the same publish road).
- Fixed page blob: 9ac1b45f2e1289cf963c738686b7be5fc9661912 — Maggie's
  tested patch and a fresh run of this builder produce the identical
  file, checked byte for byte on 2026-11-23.
- The builder carries the same eight changes as its step 6, each
  guarded to exactly one match, so a rebuild cannot bring the false
  claim back.
