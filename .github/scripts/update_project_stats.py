#!/usr/bin/env python3
"""Update README star/fork totals for repositories and public organizations."""

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

README = Path("README.md")

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

ORGANIZATIONS = (
    "Automercatorum",
    "AirBook-for-CrossPoint",
)


def api_get(url: str, token: str):
    request = urllib.request.Request(
        url,
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
        raise RuntimeError(f"GitHub API request failed: {error.code} {details}") from error


def repository_totals(repository: str, token: str) -> tuple[int, int]:
    data = api_get(f"https://api.github.com/repos/{repository}", token)
    return int(data.get("stargazers_count", 0)), int(data.get("forks_count", 0))


def organization_totals(organization: str, token: str) -> tuple[int, int]:
    stars = 0
    forks = 0
    page = 1
    while True:
        query = urllib.parse.urlencode({"type": "public", "per_page": 100, "page": page})
        repos = api_get(f"https://api.github.com/orgs/{organization}/repos?{query}", token)
        if not repos:
            break
        stars += sum(int(repo.get("stargazers_count", 0)) for repo in repos)
        forks += sum(int(repo.get("forks_count", 0)) for repo in repos)
        if len(repos) < 100:
            break
        page += 1
    return stars, forks


def render(stars: int, forks: int) -> str:
    items = []
    if stars > 0:
        items.append(
            f'<span title="{stars} {"star" if stars == 1 else "stars"}">'
            f'<img src="https://api.iconify.design/octicon:star-16.svg?color=%23F1C40F" '
            f'width="16" height="16" alt="Stars">&nbsp;<strong>{stars}</strong></span>'
        )
    if forks > 0:
        items.append(
            f'<span title="{forks} {"fork" if forks == 1 else "forks"}">'
            f'<img src="https://api.iconify.design/octicon:repo-forked-16.svg?color=%238B949E" '
            f'width="16" height="16" alt="Forks">&nbsp;<strong>{forks}</strong></span>'
        )
    return "&nbsp;&nbsp;&nbsp;".join(items)


def update_block(readme: str, key: str, url: str, rendered: str) -> str:
    start = f"<!-- repo-stats:{key}:start -->"
    end = f"<!-- repo-stats:{key}:end -->"
    replacement = f"{start}{rendered}{end}"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    updated, count = pattern.subn(replacement, readme)
    if count == 1:
        return updated
    if count > 1:
        raise RuntimeError(f"Duplicate stats blocks for {key}")

    link_pattern = re.compile(rf'(<a href="{re.escape(url)}"><strong>.*?</strong></a>)')
    updated, count = link_pattern.subn(rf"\1&nbsp;&nbsp;&nbsp;{replacement}", readme, count=1)
    if count != 1:
        raise RuntimeError(f"Could not find README link for {key}")
    return updated


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        print("GITHUB_TOKEN is not set", file=sys.stderr)
        return 1

    original = README.read_text(encoding="utf-8")
    updated = original

    for repository in REPOSITORIES:
        stars, forks = repository_totals(repository, token)
        updated = update_block(
            updated,
            repository,
            f"https://github.com/{repository}",
            render(stars, forks),
        )
        print(f"{repository}: {stars} stars, {forks} forks")

    for organization in ORGANIZATIONS:
        stars, forks = organization_totals(organization, token)
        updated = update_block(
            updated,
            organization,
            f"https://github.com/{organization}",
            render(stars, forks),
        )
        print(f"{organization}: {stars} stars, {forks} forks")

    if updated != original:
        README.write_text(updated, encoding="utf-8")
        print("README.md updated")
    else:
        print("README.md already up to date")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
