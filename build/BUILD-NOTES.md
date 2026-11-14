# Build notes — effort log page

- `build/build_page.py` — builds the effort log page (effort-log.html in this repository) from effort-data.csv: one table per day, newest first — each job's runs, minutes, and token counts. It runs on Muse's side in the nightly effort log job (04:40). `build/queries.md` holds the standing questions the log answers.
