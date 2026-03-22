# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

-

### Fixed

-

### Changed

-

### Removed

-

## [1.2.2] - 2026-03-22

### Fixed

- Force full `vue-i18n` build (`vue-i18n/dist/vue-i18n.esm-bundler.js`) instead of the runtime-only build, so `{n}` placeholders compile correctly in production and on Android

## [1.2.1] - 2026-03-22

### Fixed

- Improved table view layout in history
- Duplicate detection on PDF import now matches by `importKey` (stable key derived from date + course name) with a fallback to date-only matching for manually entered or legacy records
- Delete action is now accessible from the detail view
- Date formatting always uses DD.MM.YYYY to prevent timezone off-by-one errors on ISO date strings
- Updated package lockfile to resolve install issues

## [1.2.0] - 2026-03-22

### Added

- Scoring Record (Stammblatt) PDF import: upload a DGV scoring record PDF to bulk-import round results into the history
- Import preview modal showing parsed rounds before confirming, with duplicate highlighting
- New `pdfParser.ts` utility for extracting round data from scoring record PDFs
- Locale strings for import flow (German and English)

### Fixed

- Build configuration (`tsconfig.app.json`) to resolve TypeScript compilation errors
