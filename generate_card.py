#!/usr/bin/env python3
"""
Updates the live-stats badge row in README.md for a GitHub profile.

Live mode (used by the GitHub Action): reads GITHUB_TOKEN + GH_USERNAME env
vars, pulls public profile + contribution data from the GitHub API, builds
a row of shields.io flat-square badges (visually identical to the other
badges already in the README), and rewrites the section of README.md
between the STATS:START / STATS:END markers.

Offline/preview mode (used for local iteration, e.g. in a sandbox):
run with --preview to skip all network calls and use fixed sample data.

Usage:
    python3 generate_card.py --preview                # local preview, no network
    GITHUB_TOKEN=... GH_USERNAME=... python3 generate_card.py   # live, in Actions
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

API_ROOT = "https://api.github.com"
BADGE_COLOR = "3a3a3a"
START_MARKER = "<!-- STATS:START -->"
END_MARKER = "<!-- STATS:END -->"


def _get(url, token):
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "User-Agent": "profile-dashboard-script",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _graphql(query, variables, token):
    body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(
        API_ROOT + "/graphql",
        data=body,
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "User-Agent": "profile-dashboard-script",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def longest_streak(days):
    """days: list of {'date': 'YYYY-MM-DD', 'contributionCount': int}, chronological."""
    longest = 0
    running = 0
    for d in days:
        if d["contributionCount"] > 0:
            running += 1
            longest = max(longest, running)
        else:
            running = 0
    return longest


def fetch_live_stats(username, token):
    user = _get(API_ROOT + "/users/" + username, token)
    repos = _get(API_ROOT + "/users/" + username + "/repos?sort=pushed&per_page=1", token)
    last_commit = repos[0]["pushed_at"][:10] if repos else "n/a"

    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            weeks { contributionDays { date contributionCount } }
          }
        }
      }
    }
    """
    gql = _graphql(query, {"login": username}, token)
    weeks = (
        gql.get("data", {})
        .get("user", {})
        .get("contributionsCollection", {})
        .get("contributionCalendar", {})
        .get("weeks", [])
    )
    days = [d for w in weeks for d in w["contributionDays"]]
    streak = longest_streak(days) if days else 0

    return {
        "PUBLIC_REPOS": user.get("public_repos", 0),
        "FOLLOWERS": user.get("followers", 0),
        "LONGEST_STREAK": streak,
        "LAST_COMMIT": last_commit,
    }


def sample_stats():
    return {
        "PUBLIC_REPOS": 2,
        "FOLLOWERS": 4,
        "LONGEST_STREAK": 11,
        "LAST_COMMIT": "2026-07-10",
    }


def _escape_badge_part(part):
    # shields.io uses "-" as the field delimiter, so any literal "-" inside
    # a label/value must be doubled, and spaces become underscores.
    part = part.replace("-", "--").replace(" ", "_")
    return urllib.parse.quote(part)


def _badge_url(label, value):
    label_part = _escape_badge_part(label)
    value_part = _escape_badge_part(value)
    url = "https://img.shields.io/badge/"
    url += label_part + "-" + value_part + "-" + BADGE_COLOR
    url += "?style=flat-square"
    return url


def build_badges_line(stats):
    fields = [
        ("public repos", str(stats["PUBLIC_REPOS"])),
        ("followers", str(stats["FOLLOWERS"])),
        ("longest streak", str(stats["LONGEST_STREAK"]) + "d"),
        ("last commit", str(stats["LAST_COMMIT"])),
    ]
    parts = []
    for label, value in fields:
        parts.append("![" + label + "](" + _badge_url(label, value) + ")")
    badges = " ".join(parts)
    return START_MARKER + "\n" + badges + "\n" + END_MARKER


def update_readme(readme_path, stats):
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    if START_MARKER not in content or END_MARKER not in content:
        print("Could not find STATS markers in " + readme_path + "; leaving file untouched.", file=sys.stderr)
        return

    before = content.split(START_MARKER)[0]
    after = content.split(END_MARKER)[1]
    new_content = before + build_badges_line(stats) + after

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("updated " + readme_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="skip network calls, use sample data")
    parser.add_argument("--readme", default="README.md")
    args = parser.parse_args()

    username = os.environ.get("GH_USERNAME", "d1d2dopamine")

    if args.preview:
        stats = sample_stats()
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not token:
            print("GITHUB_TOKEN is not set; use --preview for a local dry run.", file=sys.stderr)
            return 1
        stats = fetch_live_stats(username, token)

    update_readme(args.readme, stats)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
    
