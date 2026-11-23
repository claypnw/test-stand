# Test stand deploy program

Placed 2026-11-23 through change control (Hearth ITIL 2.11), closing part of gap 2 of the pickup check's first run (2026-11-23): this deploy program stood only on the working machine, so the test-stand Pages project could not be re-made from GitHub alone.

- The program: `deploy/deploy_test_stand.py` (7,452 bytes). Working copy it was placed from: `~/workspace/test-stand-deploy/deploy_test_stand.py`. The two stand byte-identical at placement.
- What it does: downloads this repository's current files (branch main) through the GitHub API into a fresh staging folder, verifying every file's git blob SHA-1 against the repository's tree record, then deploys that folder to the Cloudflare Pages project `test-stand` (live address https://test-stand-6ku.pages.dev) with wrangler 4 via npx. GitHub Pages for this repository is off; a publish to the repository alone does not reach the live address — this program is the step that closes that gap, and jobs that publish to the test stand call it after their GitHub publish passes.
- Credentials: neither key is read by the program; both ride as surrogates Muse swaps in only for their own services. Full notes stand in the program's own header.
