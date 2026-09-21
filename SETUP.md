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
