# AgInsight Site — Password Gate for Saved Locations

**Date:** 2026-08-04
**Scope:** Front-end change to the deployed AgInsight site
**Production URL:** https://jolie-walker-shipday.netlify.app
**Site source:** `/workspaces/collective-assignment-walk0504/agri-ai-site/`
**Commit:** `59e1d00` (AgInsight: gate saved locations behind password on every visit)

## Problem (what happened)

On every page load the site read saved locations straight from `localStorage` and
rendered them immediately — no password required. It also auto-seeded a default
"Weatherford, OK" pin so the page was never empty. The existing "🔐 Save My Locations"
feature only offered *optional* cloud backup; it never gated what was shown on open.
Result: locations were visible to anyone who opened the URL.

## Solution

Added a **lock gate**: saved locations stay hidden on every visit until the user types
the correct password, which then pulls the locations up (from the encrypted vault).

### New behavior
- **Page load:** locations are no longer auto-rendered, and the default pin is no longer
  seeded. A gate panel is shown instead; the map, search bar, saved-locations list, and
  monitor area are hidden behind it. The gate offers two clear paths:
  - **Returning user:** enter your password and press "🔓 Pull up saved locations" to
    decrypt and display the locations saved under that password.
  - **New user:** press "＋ New here — start with a clean slate" to skip the password and
    start with an empty set of locations.
- **Unlock:** looks up the encrypted vault (local encrypted cache first, then the cloud
  Netlify function), decrypts it with the password-derived key (PBKDF2 + AES-GCM), and
  renders the saved locations + nicknames.
- **First run / no vault for that password:** shows a friendly notice and unlocks to an
  empty state so the user can add locations and press **💾 Save** to store them.
- **Save:** the encrypted blob is now also cached in `localStorage`
  (`aginsight_vault_cache`) in addition to being POSTed to the cloud, so unlocking works
  even offline / on repeat visits.

## Commodity selection (added 2026-08-04)

Users can now **select which commodity** to include in every monitoring cycle:
- A "📦 Monitor commodity" dropdown sits in the **Live Monitoring Results** section.
- Options: Wheat ($5.72/bu), Corn ($4.18/bu), Soybeans ($12.10/bu), Cotton ($0.85/lb), Oats ($3.40/bu), stored in `COMMODITIES` in `index.html`.
- The chosen commodity's name + price replace the old hardcoded wheat line in alerts and is shown as a "Commodity" row on each monitor card.
- The selection is **persisted in the password vault** (saved/restored with the locations), so a returning user gets their commodity back on unlock.
- Prices are labeled sample/demo constants (front-end has no Alpha Vantage key); the backend `capstone-aginsight/main.py` fetches live wheat via Alpha Vantage when a key is present.

## Files changed

| File | Change |
|------|--------|
| `agri-ai-site/index.html` | Added lock-gate HTML/CSS, gate JS (`unlockLocations`, `showGate`/`hideGate`), empty-on-load state, local encrypted cache on save, gate wire-up, and the commodity selector (`commoditySel` + `COMMODITIES`). `dist/` is generated from this. |
| `agri-ai-site/dist/index.html` | Rebuilt via `node scripts/build.js` (copies `index.html`; `dist/` is git-ignored build output). |
| `agri-ai-site/netlify/functions/vault.mjs` | Unchanged — pre-existing Netlify Function for storing/retrieving encrypted vault blobs. |

Untracked files added as part of the site deployment pipeline (pre-existing before this
change, not authored here): `netlify.toml`, `netlify/functions/vault.mjs`,
`package.json`, `package-lock.json`.

## How the existing encryption works (unchanged)

- Client derives a key from the password via PBKDF2 (150k iterations, SHA-256) → AES-GCM-256.
- Vault lookup key = `SHA-256('aginsight:' + pw)` (hex) — server only ever sees opaque ciphertext.
- Cloud store: Netlify Blobs (`getStore("aginsight-vault")`), keyed by that hex hash.
- Server never sees the password or plaintext.

## The new gate logic (summary)

```
on load:
  locations = []
  show gate; hide #locArea

unlock(password):
  hex = sha256('aginsight:' + password)
  1. try local cache  (aginsight_vault_cache) where cache.hex === hex
  2. else GET /.netlify/functions/vault?key=<hex>
  if no vault found → unlock to empty (first-run / new password) with notice
  else decrypt → set locations → render markers + saved list → hide gate
```

## Verification

- `node scripts/build.js` → "Built dist/index.html"; `dist/index.html` byte-identical to `index.html`.
- `<div>` / `</div>` counts balanced (44 / 44).
- Inline `<script>` passes `node --check` (JS syntax OK).
- Deployed to Netlify production; live HTML confirmed to contain the gate
  (`id="locGate"`, `id="btnUnlock"`, `id="gatePw"`) and the new lead copy.

## Deployment

```bash
cd /workspaces/collective-assignment-walk0504/agri-ai-site
node scripts/build.js            # regenerate dist/index.html
netlify deploy --dir dist --prod # pushed to jolie-walker-shipday
```

Note: the Netlify CLI session and the env `NETLIFY_AUTH_TOKEN` were stale
(`401 Access Denied`); deployment succeeded using a fresh access token supplied by the
author (`nfp_...`). That token was used inline only and not stored.

## What this means for existing data

Previously saved locations were stored in `localStorage` as plaintext and are now
**ignored** (hidden behind the gate). The user must re-save their locations under a
password (add locations → 💾 Save) so future visits can pull them up.

## Manual test checklist

1. Open the production URL → confirm the 🔒 gate shows and the map/list are hidden.
2. Enter a new password → confirm it unlocks to an empty state with the first-run notice.
3. Add a location (click map or search), optionally set a nickname.
4. Press 💾 Save in "Save My Locations".
5. Reload the page → confirm gate reappears; enter the same password → confirm the
   saved location(s) + nickname are pulled up.
6. Enter a wrong/different password → confirm it does not reveal data.

### Two-path gate checklist (new-user vs returning-user)
1. Open the production URL on a clean browser → gate shows both options.
2. Click "＋ New here — start with a clean slate" → unlocks with an empty saved list,
   no password required; add a location and press 💾 Save.
3. Reload → gate reappears → enter that same password → saved location(s) are pulled up.
4. On a fresh browser, click "＋ New here" again → confirm it does NOT auto-load any
   previously saved locations (starts empty).
