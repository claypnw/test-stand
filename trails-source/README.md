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
- `inputs/trails-page-sample78-2026-10-25.html` — the last reviewed
  sample page (sample 78, 2026-10-25) the builder reads as its source:
  5,612,057 bytes, git blob 55479cac65c46b98e0b39518ec416bce0f9fdca7.
  Escrowed 2026-11-23 so the build no longer depends on a file standing
  only on Muggy's machine.
- `inputs/goat-camp-wide-composite.jpg` — the wide Goat Camp picture
  the builder reads: 316,443 bytes, git blob
  db7f934e5dbc4b1cac3e057c1b71a17a5c205765. Escrowed 2026-11-23 with
  the sample page. The finished page carries all 27 pictures inside
  itself; these inputs are what a rebuild reads.

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
- Served-page verification, 2026-11-23: the live page was fetched from
  its public address and its bytes hash to the same git blob as the
  fixed page above (9ac1b45f…), 5,814,869 bytes served, carrying the
  27 entries and 27 embedded pictures. What is served is what was
  promoted.

## Restore and rebuild from escrow — documentation revision 1.1

The unchanged builder uses two paths beneath Path.home(), rather than reading directly from inputs/. Reproduce its original layout in a clean staging home on a Unix cloud host. Python 3 and Pillow are required; the builder imports PIL.Image. This is a cloud-host reconstruction, never a task for Clay's PC.

1. Fetch only these three files from claypnw/test-stand and verify their Git blob identities:
   - trails-source/build_page.py — 577b00776cbbd65213934e17d61e55c07b89d758.
   - trails-source/inputs/trails-page-sample78-2026-10-25.html — 55479cac65c46b98e0b39518ec416bce0f9fdca7; 5,612,057 bytes.
   - trails-source/inputs/goat-camp-wide-composite.jpg — db7f934e5dbc4b1cac3e057c1b71a17a5c205765; 316,443 bytes.
2. Beneath the clean staging home, place the unchanged sample at workspace/your_files/trails-page-sample78-2026-10-25.html and the unchanged picture at workspace/trails-page/photos/goat-camp-wide-composite.jpg. Create the output directory workspace/trails-page/build/.
3. Run the unchanged builder with Path.home() resolving to that staging home. Input placement and the isolated cloud home are the only adaptations; do not edit the builder.
4. The output is workspace/trails-page/build/trails-and-finds.html beneath the staging home. Expected size: 5,814,869 bytes. Expected Git blob: 9ac1b45f2e1289cf963c738686b7be5fc9661912, matching the released page. Check using git hash-object on the output file. The builder should report 27 entries, 27 pictures, no remaining SAMPLE 78 mark, and two return doors.

MuseAI reported this clean reconstruction on November 25, 2026 in Raven's Reach message MSG-20261126T004800Z-trailsproof1: only the escrowed inputs were used, the builder was unchanged, and the rebuilt output matched the released blob exactly. This records MuseAI's execution evidence; it does not claim a second independent execution. ChatGPT independently checked the shared source identities and added these missing restore steps on November 26. No Cloudflare build or deployment is needed for this reconstruction.

Documentation change only: the builder, inputs and released page remain the same exact revisions listed above. Rollback of this documentation addition is the preceding README blob b72b028c6998729f311657f5edb0bb546f0976be; it does not roll back the page.
