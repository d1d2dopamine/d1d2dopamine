# Setup

1. This repository must be named exactly `d1d2dopamine`, the same as the GitHub username, so GitHub renders `README.md` on the profile page.
2. Push the repository to `main`.
3. In **Settings -> Actions -> General -> Workflow permissions**, enable **Read and write permissions**. The workflow needs this only to refresh the small stats row in `README.md`.
4. The workflow runs on pushes to `main`, once a day, and manually from the Actions tab.

## How the stats row works

`generate_card.py` reads public GitHub data and replaces only the block between:

```text
<!-- STATS:START -->
...
<!-- STATS:END -->
```

Everything else in `README.md` is left untouched.

For an offline test without GitHub API calls:

```bash
python3 generate_card.py --preview --readme README.md
```

This writes fixed sample values into the stats block. Do this on a temporary copy if you do not want sample numbers committed.

## Notes

- The workflow uses GitHub's built-in `GITHUB_TOKEN`. No personal token is required.
- If the GitHub username changes, update `GH_USERNAME` in `.github/workflows/update-card.yml`.

## Badge definitions

- `public repos`: GitHub's public repository count for this account.
- `followers`: GitHub's follower count for this account.
- `longest streak (365d)`: the longest sequence of days with at least one contribution within the 365 UTC calendar dates ending today. This is not an all-time record. The API request specifies the date window explicitly.
- `last push`: the date of the most recent push to a public repository owned by this account, using GitHub's `pushed_at` field. It can include automated pushes, including updates to this profile. It is not the date of the latest authored commit.

The values shipped in README are the last snapshot from the supplied archive. The workflow refreshes them after publication; preview mode must only be run on a temporary copy. API errors or an incomplete contribution calendar fail the update rather than replacing real values with zeroes.

`assets/card.svg` is an unused legacy asset. The current workflow updates README badges only and does not regenerate that SVG.

## Local verification

Run the offline checks without a token:

```bash
python3 -m unittest discover -s tests -v
```

## Profile fields

Bio, website, public email, social links and pinned repositories belong to GitHub account settings. Replacing this repository cannot change those fields. Use the separately supplied profile text for the account settings.
