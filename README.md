# Cape Jaffa Marine Fishing Planner

Static website ready for GitHub Pages. Forecasts require an internet connection.

## Publish on GitHub Pages

1. Sign in to https://github.com and create a **public** repository named `cape-jaffa-wind` (do not initialize with a README).
2. Choose **Add file → Upload files**, and upload `index.html` and `.nojekyll` from this folder (README optional). Commit changes.
3. Go to **Settings → Pages → Build and deployment**. Set **Source** to **Deploy from a branch**, **Branch** to `main`, folder `/ (root)`, and save.
4. Wait a few minutes for publication. Visit `https://YOUR-USERNAME.github.io/cape-jaffa-wind/` (replace YOUR-USERNAME).
5. Click **Refresh live forecast**. Verify that wind and wave readings load. If not, copy the status message and inspect the browser developer console for the failed request.

## Important limitations

- The forecast uses third-party Open-Meteo endpoints from the browser; HTTPS hosting does not guarantee the APIs will respond. Browser extensions, firewall, rate limits, and API outages can still block requests.
- Forecast accuracy tracking is stored in **this browser only**. It does not automatically fetch BOM observations or collect data while closed. Export accuracy CSV regularly. Different browsers/devices do not share the tracker.
- The app is a planning aid, **not** an official marine forecast or safety determination. Always check BOM warnings, local conditions, and your vessel's limits.
- Before using commercially, review Open-Meteo licensing and usage conditions.
