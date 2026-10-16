#!/usr/bin/env python3
"""Aktualizuje Casks/freetube.rb do najnowszego wydania FreeTube starszego niż MIN_AGE_DAYS.

FreeTube publikuje wszystkie wydania jako „prerelease” (sufiks -beta), więc są brane pod uwagę.
"""
import hashlib
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = "FreeTubeApp/FreeTube"
CASK = Path(__file__).resolve().parent.parent / "Casks" / "freetube.rb"
MIN_AGE_DAYS = int(os.environ.get("MIN_AGE_DAYS", "7"))
TAG_RE = re.compile(r"^v(\d+\.\d+\.\d+)-beta$")


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "homebrew-tap-updater"})
    token = os.environ.get("GITHUB_TOKEN")
    if token and "api.github.com" in url:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=300) as r:
        return r.read()


def pick_release() -> tuple[str, dict]:
    releases = json.loads(get(f"https://api.github.com/repos/{REPO}/releases?per_page=20"))
    cutoff = datetime.now(timezone.utc) - timedelta(days=MIN_AGE_DAYS)
    for rel in releases:  # API zwraca od najnowszych
        m = TAG_RE.match(rel["tag_name"])
        if rel["draft"] or not m:
            continue
        published = datetime.fromisoformat(rel["published_at"].replace("Z", "+00:00"))
        if published <= cutoff:
            return m.group(1), rel
    sys.exit("Brak wydania spełniającego warunek wieku.")


def main() -> None:
    version, rel = pick_release()
    text = CASK.read_text()
    current = re.search(r'version "([^"]+)"', text).group(1)
    if current == version:
        print(f"Bez zmian: {version}")
        return

    assets = {a["name"]: a["browser_download_url"] for a in rel["assets"]}
    sums = {}
    for arch in ("arm64", "x64"):
        name = f"freetube-{version}-beta-mac-{arch}.dmg"
        if name not in assets:
            sys.exit(f"Brak pliku {name} w wydaniu {rel['tag_name']}")
        sums[arch] = hashlib.sha256(get(assets[name])).hexdigest()

    text = re.sub(r'version "[^"]+"', f'version "{version}"', text, count=1)
    text = re.sub(r'(sha256 arm:\s+)"[0-9a-f]{64}"', rf'\1"{sums["arm64"]}"', text, count=1)
    text = re.sub(r'(intel:\s+)"[0-9a-f]{64}"', rf'\1"{sums["x64"]}"', text, count=1)
    CASK.write_text(text)
    print(f"Zaktualizowano {current} -> {version}")
    if out := os.environ.get("GITHUB_OUTPUT"):
        with open(out, "a") as f:
            f.write(f"version={version}\n")


if __name__ == "__main__":
    main()
