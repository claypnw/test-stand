# Cloud Work GitHub access test

- UTC start (Work mode tool clock, before first GitHub read) `2026-11-28T04:27:57.652Z`.
- UTC end of pre-write checks (evidence sealed for the single create) `2026-11-28T04:29:05.375Z`. The create and independent read-back finish after these bytes are fixed.
- Assistant and runtime exposed: Codex (GPT-6 family) in ChatGPT Work mode, using the GitHub connector from the Work mode tool runtime. Exact model variant, execution host, native task or run ID, and authenticated GitHub principal were not independently exposed or verified.
- Authorization: direct instruction in the active Work chat for this bounded test and one retained file in the GitHub test stand.
- Governing sources read: Standing Instructions 0.2, production supplement 0.2, SOP-OPS-AIT-003 v1.5, and Hearth ITIL v2.0 (including 2.6, 2.7, 2.11 and 3.5). Hearth ITIL checked at commit `6f6b0919ae9c200490650b9a03029f48f9332d45`, blob `8f2c256e5800c3714d68eba85e9bb30a9d221a8b`.
- Source read PASS: `github_fetch_file` returned UTF-8 content for `claypnw/system-documentation/ChatGPT Scheduled Work/validation/validation-pass-1.1.md` on the default branch. The returned blob SHA `99b0be760797d53692ecb6add85db51e52a461e0` matched the required SHA exactly.
- Target pre-check PASS: repository access and default branch `main` confirmed. `github_fetch_file` on `claypnw/test-stand/scheduler-cloud-work-validation-20261128T043000Z.md` returned GitHub API 404 `NOT_FOUND` (message: `Not Found`).
- Checked create: one `github_create_file` request on `main`, with no replacement SHA. It can create the path only if absent. The evidence path was the sole write target.
- Independent read-back criterion: fetch this path at the returned commit, compare all bytes to the submitted text, and compare the returned blob SHA to the Git blob SHA computed from those bytes. The active Work chat records the observed create and read-back results, commit, blob, and final UTC end after verification.
- Scope: interactive Work mode GitHub access only. Scheduled triggering, timing, duty execution, duplicate prevention, concurrency and cutover require separate tests. This test uses no scheduled-duty jobs, automation controls, claims, production outputs, personal or health data, PC, browser control, local files, paid services or supplied secrets.
