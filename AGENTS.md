# AGENTS.md — HandyCap

Guidelines for AI agents working in this repository.

## Project overview

**HandyCap** is a mobile-first golf handicap tracker (Vue 3 + Vite + TypeScript + Capacitor).
Version: **1.1.0** | License: Apache 2.0

The app runs as a PWA in any browser and can be compiled to a native Android APK/AAB via Capacitor.
All data is stored locally in IndexedDB (Dexie). There is no backend or cloud sync.

---

## Repository layout

```
src/
  assets/          # CSS (base, global, main)
  components/
    FaqItem.vue        # Collapsible FAQ accordion item
    HandicapChart.vue  # Chart.js time-series chart (HCPI over time)
    IconLogo.vue       # App logo SVG
    InfoTooltip.vue    # Hover/tap tooltip wrapper
  locales/
    de.ts              # German translations (incl. HTML content for FAQs)
    en.ts              # English translations
  router/
    index.ts           # Vue Router v4 — 4 routes (see below)
  utils/
    calculations.ts    # Core WHS handicap calculation logic
    pdfParser.ts       # In-browser DGV Scoring Record PDF parser (pdfjs-dist)
  views/
    CalculatorView.vue # Round entry form → computes & saves Score Differential
    HistoryView.vue    # Statistics dashboard + chart + results table + PDF import
    FAQ.vue            # FAQ page (accordion)
    SettingsView.vue   # Language toggle + about/version info
  App.vue              # Root app shell with bottom navigation bar
  db.ts                # Dexie schema (Result, Setting tables)
  main.ts              # App entry point (Vue 3 + vue-i18n initialisation)
android/               # Capacitor-managed Android project (do not edit manually)
.github/workflows/     # build-release.yaml.yml — tag-triggered Android CI/CD
Dockerfile             # Multi-stage: Node 24 build → nginx:stable-alpine serve
nginx.conf             # SPA fallback routing for NGINX
capacitor.config.ts    # appId: com.bribdev.HandyCap | webDir: dist
vite.config.ts         # @vitejs/plugin-vue, alias @ → src/
```

---

## Routes

| Path        | View               | Purpose                                    |
|-------------|--------------------|--------------------------------------------|
| `/`         | CalculatorView     | Enter a round, compute Score Differential  |
| `/history`  | HistoryView        | Stats, HCPI chart, full results table      |
| `/settings` | SettingsView       | Language selector, app info                |
| `/faq`      | FAQ                | Accordion FAQ (i18n content)               |

---

## Database schema (src/db.ts)

Dexie v4, IndexedDB. Two tables:

**results** — one row per golf round
`id` (auto) | `date` (ISO string) | `courseName` | `grossScore` | `scoreDifferential` | `storedHandicap`

**settings** — key/value store
`id` (auto) | `key` (unique string, e.g. `"locale"`) | `value`

Schema is versioned (v1 → v2). Add new versions with `db.version(n).stores(...)` — never modify existing version definitions.

---

## Core calculation logic (src/utils/calculations.ts)

### Score Differential
```
SD = (GBE − CR) × 113 / Slope ± PCC
```
For 9-hole rounds the result is doubled before storing (converted to 18-hole equivalent).

### computeBaseHandicap(diffs, prevHC)
Selects the best N differentials from the most recent 20 rounds per WHS rules:

| Rounds | Best N | Adjustment |
|--------|--------|------------|
| 1      | 1      | −2.0       |
| 2      | 1      | −1.0       |
| 3      | 1      | 0.0        |
| 4      | 1      | 0.0        |
| 5      | 1      | 0.0        |
| 6      | 2      | −1.0       |
| 7–8    | 2      | 0.0        |
| 9–11   | 3      | 0.0        |
| 12–14  | 4      | 0.0        |
| 15–16  | 5      | 0.0        |
| 17–18  | 6      | 0.0        |
| 19     | 7      | 0.0        |
| 20+    | 8      | 0.0        |

Previous HC Cap: if `prevHC` is between 26.5 and 54, the new HI is capped at `prevHC`.
Result is rounded to 1 decimal.

### applyCap(newHC, allRecords, currentIndex)
Implements WHS Soft/Hard Cap using the lowest `storedHandicap` in the past 365 days:
- **Soft Cap**: growth beyond +3.0 from lowest HI is halved
- **Hard Cap**: absolute ceiling of lowest HI + 5.0

---

## PDF import (src/utils/pdfParser.ts)

Parses a **DGV Scoring Record (Detailliert)** PDF (not the Handicap History Sheet).
Uses `pdfjs-dist` for in-browser text extraction — no server call, no file upload.

Extracted per round: `date`, `courseName` (club + tournament), `holes` (9/18), `cr`, `slope`, `hcpi`, `gbe`, `sd`
SD is taken directly from the PDF value — it is **not** recalculated.

Entry point: `parsePdf(file: File): Promise<ImportedRound[]>`

The `ImportedRound` interface is defined in `pdfParser.ts`; use it when passing data between the parser and the database layer.

---

## Internationalisation (src/locales/)

vue-i18n v12. Two locales: `de` (default), `en`.
Locale is persisted in the `settings` table under key `"locale"`.

Translation keys include rich HTML strings (used in FAQ tooltips). When adding keys, add them to **both** `de.ts` and `en.ts`.

---

## Tech stack

| Layer         | Library / Tool                  | Version  |
|---------------|---------------------------------|----------|
| Framework     | Vue 3                           | ~3.5     |
| Routing       | vue-router                      | ~4.5     |
| i18n          | vue-i18n                        | ~12.0    |
| Storage       | Dexie (IndexedDB)               | ~4.0     |
| Charts        | Chart.js + chartjs-adapter-date-fns | ~4.4 / ~3.0 |
| PDF parsing   | pdfjs-dist                      | ~5.5     |
| Icons         | material-design-icons-iconfont  | ~6.7     |
| Mobile        | Capacitor + @capacitor/android  | ~7.2     |
| Build         | Vite                            | ~6.2     |
| Language      | TypeScript                      | ~5.8     |

---

## Development

```bash
npm install       # install deps
npm run dev       # start Vite dev server at http://localhost:5173
npm run type-check  # run vue-tsc
npm run build     # type-check + production build → dist/
npm run preview   # preview production build locally
```

### Android
```bash
npm run build
npx cap sync android
npx cap open android   # open in Android Studio
```

### Docker
```bash
docker build -t HandyCap:latest .
docker run --rm -p 8080:80 HandyCap:latest
```

---

## CI/CD (.github/workflows/build-release.yaml.yml)

Triggered on version tags (`v*`). Two jobs:

1. **build-release**: builds the Vue app, syncs Capacitor, builds a signed AAB + APK via Gradle, uploads artifacts.
2. **github-release**: creates a GitHub Release with the AAB and APK attached.

Signing secrets required (stored in GitHub repository secrets):
- `KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD`

---

## Conventions & constraints

- **TypeScript strict mode** — avoid `any`; use proper interfaces.
- **No backend** — all persistence goes through Dexie (`src/db.ts`). Never introduce a network call for data storage.
- **pdfjs worker** — the worker is resolved via `import.meta.url` in `pdfParser.ts`. Do not change this pattern; it is required for Vite's asset bundling.
- **i18n keys** — always add translations to both `de.ts` and `en.ts` in the same commit.
- **Dexie schema versions** — only append new `db.version(n)` blocks; never mutate existing ones.
- **android/ directory** — managed by Capacitor CLI. Do not hand-edit files inside it; run `npx cap sync android` after web changes.
- **Environment variable** — `VITE_APP_VERSION` is injected at build time for the About page. Update it when bumping the version.
- **Secrets** — never commit keystore files, `.env` with real secrets, or `android/local.properties`.
