# Setup

1. This goes in your GitHub **profile repo** — the one named exactly
   `d1d2dopamine` (same as your username). Create it if it doesn't exist yet
   (GitHub Settings prompts you to when a repo name matches your username).
2. Copy these files/folders into the root of that repo, preserving structure:
   - `README.md`
   - `generate_card.py`
   - `assets/card.svg` (a pre-generated sample so the card shows up immediately,
     before the Action has run even once)
   - `.github/workflows/update-card.yml`
3. Push to `main`.
4. In the repo, go to **Settings → Actions → General → Workflow permissions**
   and select **Read and write permissions**. This lets the Action commit the
   refreshed `assets/card.svg` back to the repo. Without this the push step
   in the workflow will fail with a permissions error.
5. That's it — the Action runs on every push to `main`, once a day at 03:00 UTC,
   and on demand from the **Actions** tab ("Run workflow").

## Local preview / editing

To tweak colors, spacing, or copy without waiting on GitHub Actions:

```bash
python3 generate_card.py --preview
```

This writes `assets/card.svg` using fixed sample numbers (no network calls),
so you can open it in a browser and iterate on the design directly in
`generate_card.py` (look for `SVG_TEMPLATE`).

## Notes

- Numbers on the card (repos, followers, streak, last commit) come from the
  public GitHub REST + GraphQL APIs, authenticated with the Action's built-in
  `GITHUB_TOKEN` — no personal access token or secret needs to be created.
- If you ever rename your GitHub username, update `GH_USERNAME` in
  `.github/workflows/update-card.yml`.
