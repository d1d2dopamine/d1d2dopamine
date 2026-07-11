#!/usr/bin/env python3
"""
Generates assets/card.svg for a GitHub profile README.

Live mode (used by the GitHub Action): reads GITHUB_TOKEN + GH_USERNAME env
vars, pulls public profile + contribution data from the GitHub API, and
writes a dark, minimal SVG "research panel" card.

Offline/preview mode (used for local iteration, e.g. in a sandbox):
run with --preview to skip all network calls and use fixed sample data.

Usage:
    python3 generate_card.py --preview                # local preview, no network
    GITHUB_TOKEN=... GH_USERNAME=... python3 generate_card.py   # live, in Actions
"""
import argparse
import datetime
import json
import os
import sys
import urllib.request

API_ROOT = "https://api.github.com"


def _get(url: str, token: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "profile-dashboard-script",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _graphql(query: str, variables: dict, token: str) -> dict:
    body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(
        f"{API_ROOT}/graphql",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "profile-dashboard-script",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def longest_streak(days: list) -> int:
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


def fetch_live_stats(username: str, token: str) -> dict:
    user = _get(f"{API_ROOT}/users/{username}", token)
    repos = _get(
        f"{API_ROOT}/users/{username}/repos?sort=pushed&per_page=1", token
    )
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


def sample_stats() -> dict:
    return {
        "PUBLIC_REPOS": 2,
        "FOLLOWERS": 4,
        "LONGEST_STREAK": 11,
        "LAST_COMMIT": "2026-07-10",
    }


# NOTE: uses __TOKEN__ placeholders + str.replace, not str.format, so the
# literal curly braces in the embedded CSS don't need any escaping.
SVG_TEMPLATE = """<svg width="880" height="320" viewBox="0 0 880 320" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .name { font: 700 26px 'Segoe UI', Helvetica, Arial, sans-serif; fill: #E6EDF3; }
      .subtitle { font: 400 13px 'SFMono-Regular', Consolas, Menlo, monospace; fill: rgba(255,255,255,0.55); }
      .live { font: 400 12px 'SFMono-Regular', Consolas, Menlo, monospace; fill: rgba(255,255,255,0.65); }
      .bio { font: 400 14.5px 'Segoe UI', Helvetica, Arial, sans-serif; fill: rgba(255,255,255,0.78); }
      .label { font: 600 11px 'SFMono-Regular', Consolas, Menlo, monospace; fill: rgba(255,255,255,0.45); letter-spacing: 1px; }
      .value { font: 700 23px 'SFMono-Regular', Consolas, Menlo, monospace; fill: #5E9FE8; }
      .footer { font: 400 10.5px 'SFMono-Regular', Consolas, Menlo, monospace; fill: rgba(255,255,255,0.4); }
    </style>
  </defs>

  <rect x="0.5" y="0.5" width="879" height="319" rx="14" fill="#0D1117" stroke="rgba(255,255,255,0.12)" />

  <text x="32" y="52" class="name">__USERNAME__</text>
  <text x="32" y="76" class="subtitle">independent researcher &#183; computational behavior</text>

  <circle cx="744" cy="48" r="4" fill="#72BC8F" />
  <text x="756" y="52" class="live">building in public</text>

  <line x1="32" y1="96" x2="848" y2="96" stroke="rgba(255,255,255,0.12)" />

  <text x="32" y="126" class="bio">No lab, no institution, no degree &#8212; self-taught, working from open</text>
  <text x="32" y="150" class="bio">datasets. I publish whatever's left standing, including what isn't.</text>

  <line x1="32" y1="178" x2="848" y2="178" stroke="rgba(255,255,255,0.12)" />

  <line x1="234" y1="196" x2="234" y2="254" stroke="rgba(255,255,255,0.10)" />
  <line x1="438" y1="196" x2="438" y2="254" stroke="rgba(255,255,255,0.10)" />
  <line x1="642" y1="196" x2="642" y2="254" stroke="rgba(255,255,255,0.10)" />

  <text x="32" y="204" class="label">PUBLIC REPOS</text>
  <text x="32" y="236" class="value">__PUBLIC_REPOS__</text>

  <text x="254" y="204" class="label">FOLLOWERS</text>
  <text x="254" y="236" class="value">__FOLLOWERS__</text>

  <text x="458" y="204" class="label">LONGEST STREAK</text>
  <text x="458" y="236" class="value">__LONGEST_STREAK__d</text>

  <text x="662" y="204" class="label">LAST COMMIT</text>
  <text x="662" y="236" class="value">__LAST_COMMIT__</text>

  <text x="32" y="296" class="footer">generated automatically &#183; updated __GENERATED_AT__</text>
</svg>
"""


def render(username: str, stats: dict) -> str:
    svg = SVG_TEMPLATE
    svg = svg.replace("__USERNAME__", username)
    svg = svg.replace("__PUBLIC_REPOS__", str(stats["PUBLIC_REPOS"]))
    svg = svg.replace("__FOLLOWERS__", str(stats["FOLLOWERS"]))
    svg = svg.replace("__LONGEST_STREAK__", str(stats["LONGEST_STREAK"]))
    svg = svg.replace("__LAST_COMMIT__", str(stats["LAST_COMMIT"]))
    svg = svg.replace("__GENERATED_AT__", datetime.date.today().isoformat())
    return svg


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preview", action="store_true", help="skip network calls, use sample data")
    parser.add_argument("--out", default="assets/card.svg")
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

    svg = render(username, stats)
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
