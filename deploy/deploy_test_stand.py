#!/usr/bin/env python3
"""Deploy the test stand (repository claypnw/test-stand) to Cloudflare Pages.

The test stand moved from GitHub Pages to Cloudflare Pages on 2026-11-20
(move record: ~/workspace/goals/github-minutes-reduction/hidden_files/
test-stand-move-2026-11-20.md). The repository stays the source of the
files; GitHub Pages is off, so a publish to the repository alone no longer
reaches the live address. This program is the deploy step that closes that
gap. Jobs that publish to the test stand call it after their GitHub publish
passes.

What it does:
  1. Downloads the repository's current files (branch main) through the
     GitHub API into a fresh staging folder beside this program, verifying
     every file's git blob SHA-1 against the repository's tree record.
  2. Deploys that folder to the Cloudflare Pages project `test-stand`
     (live address https://test-stand-6ku.pages.dev) with wrangler 4 via
     npx — the road proven in the move. The raw direct-upload endpoint is
     not used: it failed with HTTP 500 "error code: 1101" on every variant
     tried on 2026-11-20.

Credentials: neither key is read by this program. The GitHub key rides as
an hsurr: surrogate that Muse swaps in only on requests to
api.github.com; the Cloudflare token rides the same way, passed to
wrangler through its environment only — never printed, never on a command
line, never written to a file.

Ends with one line: VERDICT: PASS (exit 0) or VERDICT: FAIL (exit 1).
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import (
    add_surrogate_to_request,
    dynamic_credential_entry,
    read_json_response,
)

GH_HOST = "api.github.com"
REPO = "claypnw/test-stand"
BRANCH = "main"
CF_ACCOUNT_ID = "ff015afa0634d0159522bdc5094c5d08"
CF_PROJECT = "test-stand"
HERE = os.path.dirname(os.path.abspath(__file__))
STAGING = os.path.join(HERE, "staging")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise RuntimeError("redirect refused")


def api_get(path, raw=False):
    headers = {
        "Accept": "application/vnd.github.raw" if raw else "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "claypnw-test-stand-deploy",
    }
    request = urllib.request.Request(
        f"https://{GH_HOST}{path}", headers=headers, method="GET"
    )
    add_surrogate_to_request(request, "custom.github", allowed_hosts=[GH_HOST])
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=180) as response:
            if raw:
                return response.status, response.read()
            return response.status, read_json_response(response)
    except urllib.error.HTTPError as err:
        return err.code, err.read()[:500]


def stage_repository():
    """Download every file on BRANCH into a fresh STAGING folder, verifying
    each file's git blob SHA-1. Returns (file_count, total_bytes)."""
    status, tree = api_get(
        f"/repos/{REPO}/git/trees/{BRANCH}?recursive=1"
    )
    if status != 200 or not isinstance(tree, dict) or "tree" not in tree:
        raise RuntimeError(f"tree read failed: HTTP {status}")
    if tree.get("truncated"):
        raise RuntimeError("tree read came back truncated; cannot stage safely")
    blobs = [e for e in tree["tree"] if e.get("type") == "blob"]
    if os.path.isdir(STAGING):
        shutil.rmtree(STAGING)
    os.makedirs(STAGING)
    total = 0
    for entry in blobs:
        path = entry["path"]
        status, data = api_get(
            f"/repos/{REPO}/git/blobs/{entry['sha']}", raw=True
        )
        if status != 200 or not isinstance(data, bytes):
            raise RuntimeError(f"download failed for {path}: HTTP {status}")
        digest = hashlib.sha1(
            b"blob " + str(len(data)).encode() + b"\0" + data
        ).hexdigest()
        if digest != entry["sha"]:
            raise RuntimeError(f"SHA-1 mismatch for {path}")
        dest = os.path.join(STAGING, path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as fh:
            fh.write(data)
        total += len(data)
    print(f"staged {len(blobs)} files, {total} bytes, every SHA-1 matched")
    return len(blobs), total


def deploy():
    """Run wrangler pages deploy of STAGING. Returns wrangler's exit code."""
    entry = dynamic_credential_entry("custom.cloudflare", "access_token")
    surrogate = str(entry["surrogate"]).strip()
    assert surrogate.startswith("hsurr:"), "not a surrogate"
    env = dict(os.environ)
    env["CLOUDFLARE_API_TOKEN"] = surrogate
    env["CLOUDFLARE_ACCOUNT_ID"] = CF_ACCOUNT_ID
    env["WRANGLER_SEND_METRICS"] = "false"
    env["CI"] = "true"
    cmd = [
        "npx", "--yes", "wrangler@4",
        "pages", "deploy", STAGING,
        "--project-name", CF_PROJECT,
        "--branch", BRANCH,
        "--commit-dirty=true",
        "--commit-message", "Test stand deploy from repository claypnw/test-stand",
    ]
    print("launching wrangler pages deploy (token value not shown)")
    result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=1200)
    out = (result.stdout or "") + (result.stderr or "")
    out = out.replace(surrogate, "<redacted>")
    print(out[-4000:])
    print("wrangler exit code:", result.returncode)
    return result.returncode


def main():
    try:
        stage_repository()
    except Exception as err:
        print(f"staging failed: {err}")
        print("VERDICT: FAIL")
        return 1
    try:
        code = deploy()
    except Exception as err:
        print(f"deploy failed: {err}")
        print("VERDICT: FAIL")
        return 1
    if code != 0:
        print("VERDICT: FAIL")
        return 1
    # The change-control gate (Hearth ITIL 2.11; Clay's ruling,
    # 2026-11-20): the deploy is a production movement — the files
    # themselves landed in the repository through the gated shop
    # publisher, and this deploy of them to their live address is
    # recorded as a change-control movement with its change-log
    # entry. A failed record is printed loudly; it never un-deploys
    # a deploy that passed.
    try:
        proc = subprocess.run(
            [sys.executable,
             os.path.expanduser("~/workspace/change-control/change_control.py"),
             "record", "--piece", "Test stand deploy",
             "--repo", "test-stand", "--path", "",
             "--by", os.environ.get("CC_BY", "Muggy"),
             "--note", "The test stand's standing files, deployed "
                       "from repository claypnw/test-stand to "
                       "https://test-stand-6ku.pages.dev by the "
                       "standing deploy program."],
            capture_output=True, text=True, timeout=1200)
        for out_line in (proc.stdout or "").splitlines():
            print(f"change control: {out_line}")
        if proc.returncode != 0:
            print("CHANGE CONTROL: the deploy's record did not fully "
                  "land — its change-log entry is queued for retry")
    except Exception as err:
        print(f"CHANGE CONTROL: the record step could not run: {err}")
    print("VERDICT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
