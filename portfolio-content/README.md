# Obsidian Portfolio Vault

This folder is the content source for the ProtoSem section of the portfolio.

## Workflow
1. Open `portfolio-content/` as an Obsidian vault.
2. Add notes and images inside the appropriate `Week_XX/NN_DayName/` folder.
3. In Obsidian, paste images normally; they stay beside the note because attachments are configured for the current folder.
4. Push the repository (Obsidian Git can do this automatically).
5. GitHub Actions runs `scripts/build-templates.js` and regenerates `content/protosem/weeks.json` plus copied weekly images.

The public website reads the generated JSON automatically, so the ProtoSem journey updates without editing `index.html`.
