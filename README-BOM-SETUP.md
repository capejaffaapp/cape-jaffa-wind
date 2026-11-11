# Cape Jaffa BOM automatic observations — installation

Upload **all files and folders** in this package to the **root** of your existing `capejaffaapp/cape-jaffa-wind` repository. Keep the `.github/workflows/observations.yml` and `scripts/update_bom.py` paths intact. GitHub web upload may not easily preserve nested folders; easiest is to upload with GitHub Desktop, git, or create those two files individually using GitHub **Add file → Create new file** and enter the full path.

1. In GitHub repository **Settings → Actions → General → Workflow permissions**, select **Read and write permissions** (if your account allows it), then save.
2. Open **Actions → Update Cape Jaffa BOM observations → Run workflow**. If prompted, enable Actions first.
3. Wait for a successful run and confirm `data/cape-jaffa-observations.json` exists in the repository. If the action fails, inspect its logs. BOM may block the GitHub runner or change its public feed; do not assume it worked.
4. Visit `https://capejaffaapp.github.io/cape-jaffa-wind/` after Pages republishes, then reload. The live observation panel should show the latest **measured** station reading and timestamp.
5. The job is scheduled approximately every 30 minutes, but GitHub may delay or skip scheduled runs. A stale-data warning is shown when measurements are over 90 minutes old. GitHub may disable scheduled workflows after prolonged repository inactivity.

**Important:** GitHub Pages only publishes static files. Scheduled GitHub Actions fetches observations and commits the JSON. This is not a guaranteed real-time service. The archive begins collecting after the first successful workflow run. The tracker stores forecasts in each browser and matches them against shared BOM observations; it does not retroactively generate old forecasts. Existing manually entered observations are ignored by the updated app. Always consult BOM marine forecasts and warnings before departure.

BOM station: Cape Jaffa (The Limestone) 026095; JSON feed: https://www.bom.gov.au/fwo/IDS60801/IDS60801.94813.json
