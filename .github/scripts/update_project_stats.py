#!/usr/bin/env python3
"""Update README project stars and forks using the GitHub REST API."""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

README_PATH = Path("README.md")

REPOSITORIES = (
    "Yoddikko/kasetPlus",
    "Yoddikko/terminal_portfolio",
    "Yoddikko/GulliverWeb",
    "Yoddikko/yoddChatGPT",
    "Yoddikko/TokenMaxxxxing-Claude-Code-X-Deepseek",
    "Yoddikko/GetGyroAndAccelerometerData",
    "Yoddikko/Now",
    "Yoddikko/ASL-Recognizer",
    "Yoddikko/Be-Charge-Host-Hackaton2022",
    "Yoddikko/DropDown",
)


def fetch_repository(repository: str, token: str) -> dict[str, object]:
    request = urllib.request.Request(
        f"https://api.github.com/repos/{repository}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "Yoddikko-profile-stats",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API request failed for {repository}: {error.code} {details}") from error


def render_stats(repository: str, stars: int, forks: int) -> str:
    items: list[str] = []
    if stars > 0:
        items.append(
            f'<a href="https://github.com/{repository}/stargazers" title="{stars} stars">'
            f'<img src="https://api.iconify.design/lucide:star.svg?color=%23F1C40F" width="15" height="15" alt="Stars">'
            f'&nbsp;<sub><strong>{stars}</strong></sub></a>'
        )
    if forks > 0:
        items.append(
            f'<a href="https://github.com/{repository}/forks" title="{forks} forks">'
            f'<img src="https://api.iconify.design/lucide:git-fork.svg?color=%238B949E" width="15" height="15" alt="Forks">'
            f'&nbsp;<sub><strong>{forks}</strong></sub></a>'
        )
    return "&nbsp;&nbsp;".join(items)


def update_block(readme: str, repository: str, rendered: str) -> str:
    start = f"<!-- repo-stats:{repository}:start -->"
    end = f"<!-- repo-stats:{repository}:end -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    replacement = f"{start}{rendered}{end}"
    updated, count = pattern.subn(replacement, readme)
    if count != 1:
        raise RuntimeError(f"Expected exactly one stats block for {repository}, found {count}")
    return updated


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        print("GITHUB_TOKEN is not set", file=sys.stderr)
        return 1

    readme = README_PATH.read_text(encoding="utf-8")
    updated = readme

    for repository in REPOSITORIES:
        data = fetch_repository(repository, token)
        stars = int(data.get("stargazers_count", 0))
        forks = int(data.get("forks_count", 0))
        updated = update_block(updated, repository, render_stats(repository, stars, forks))
        print(f"{repository}: {stars} stars, {forks} forks")

    if updated != readme:
        README_PATH.write_text(updated, encoding="utf-8")
        print("README.md updated")
    else:
        print("README.md already up to date")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
