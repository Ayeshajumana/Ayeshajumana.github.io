# Obsidian → ProtoSem Portfolio Sync

This repository now uses `portfolio-content/` as the Obsidian vault and keeps the public site as a static HTML portfolio.

### Daily workflow
Open `portfolio-content/` as your Obsidian vault. Add a note to the correct week/day folder and paste images there. Commit/push the repo; the GitHub Action compiles the notes into `content/protosem/weeks.json` and copies images into `assets/weekly/`. The ProtoSem UI in `index.html` fetches that generated JSON on page load.

### GitHub Pages
The repo can continue serving the static site from the repository root. The new generated `content/` and `assets/` folders are normal static files, so no React/Vite migration is required.

### GitHub Action permission
Repository Settings → Actions → General → Workflow permissions → Read and write permissions.

### Obsidian Git (optional)
Install the Obsidian Git community plugin and enable a periodic auto-commit/auto-push interval. The guide’s suggested 30-minute cadence is fine.
