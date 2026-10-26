# TOOLS.md - Local Notes

Short, durable notes that make external tools work reliably in this
particular setup: device nicknames, host aliases, preferred voices, and
environment-specific quirks. Skills describe how tools work in general; this
file holds only what is unique here. Leave it empty until there is something
worth recording.

- Anycubic Slicer Next: consolidating a multi-plate 3MF must be done by exporting individual models as STL files first — importing 3MFs directly overwrites the workspace (Clay's note, 2026-09-25).
- Voice-note pronunciation: "Mogollon" is pronounced MUGGY-yohn (M-U-G-G-Y + Y-glide "YOHN" ending) — spelled out and confirmed by Clay 2026-10-14 after voice-transcription garbled his spoken corrections repeatedly. `~/workspace/bin/voice-note.sh` substitutes "MUGGY-yohn" for "Mogollon" in the TTS feed only; written text keeps the true spelling.
- Headless Chrome for page screenshots lives at /opt/meta-chromium/chrome (found 2026-10-15) — usable to render a local HTML draft to a real PNG instead of drawing a mock by hand.
- Android home-screen shortcuts (2026-10-09): a pasted muse.ai menu link ended up as a shortcut pointing at news.ai — a real, unrelated Anguilla news site — because the address got mangled during shortcut creation. For links he needs daily, use a Chrome bookmark instead of a home-screen/desktop shortcut; it's one tap inside Chrome and can't get the address wrong.
