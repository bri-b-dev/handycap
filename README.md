# Handycap

[![Version](https://img.shields.io/badge/version-1.0.0-informational.svg)](#)
[![Vue 3](https://img.shields.io/badge/Vue-3-42b883?logo=vue.js)](https://vuejs.org/)
[![Vite](https://img.shields.io/badge/Bundler-Vite-646cff?logo=vite)](https://vitejs.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?logo=typescript)](https://www.typescriptlang.org/)
[![Capacitor](https://img.shields.io/badge/Capacitor-7.x-119EFF?logo=capacitor)](https://capacitorjs.com/)
[![Android](https://img.shields.io/badge/Platform-Android-3DDC84?logo=android)](https://developer.android.com/)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue?logo=githubactions)](#)
[![License](https://img.shields.io/badge/license-Apache_2.0-lightgrey.svg)](./LICENSE)

A mobile‑first web app built with Vue 3 + Vite and Capacitor. It uses IndexedDB (via Dexie) for offline data and Chart.js for visualizations. The project can be deployed as a static site (dist) or packaged as a native Android app via Capacitor.

* [About](#about)
* [Features](#features)
* [Tech stack](#tech-stack)
* [Prerequisites](#prerequisites)
* [Getting started](#getting-started)
* [Configuration](#configuration)
* [Development](#development)
* [Build & production](#build--production)
* [Android build & release](#android-build--release)
* [Docker usage](#docker-usage)
* [Project scripts](#project-scripts)
* [Troubleshooting](#troubleshooting)
* [Contributing](#contributing)
* [License](#license)

## About
Handycap is a Vue 3 + Capacitor application. It is designed to run in the browser as a PWA and can be compiled to a native Android application. The app leverages IndexedDB for persistent offline storage and provides charts for insights.

## Features
- Modern Vue 3 single‑page app using Vite for fast dev/build
- Fully strict Type‑safe codebase with TypeScript
- Premium modern UI with glassmorphism, responsive animations, and 'Inter' typography
- Offline‑first local storage with Dexie (IndexedDB)
- Charts and time‑series via Chart.js and date‑fns adapter
- Internationalization via vue‑i18n (English & German)
- Android packaging with Capacitor
- Dockerfile for static hosting with NGINX

## Tech stack
- Framework: Vue 3, vue‑router
- Build tooling: Vite
- Language: TypeScript
- Offline storage: Dexie (IndexedDB)
- Charts: Chart.js + chartjs‑adapter‑date‑fns
- Mobile: Capacitor (Android platform included)

## Prerequisites
- Node.js 20 or 22 (recommended) and npm
- Git
- Optional for Android builds:
  - Java 21 (as used by the helper script)
  - Android Studio (latest) + Android SDK/NDK
  - Capacitor CLI
- Optional for Docker:
  - Docker Engine 24+

Verify versions:
- node -v
- npm -v
- java -version (for Android)

## Getting started
1) Clone the repository
- git clone https://github.com/bri-b-dev/handycap.git
- cd handycap

2) Install dependencies
- npm install

3) Start the dev server
- npm run dev

4) Open the app
- Visit http://localhost:5173 (default Vite dev port)

## Configuration
- Vite config: vite.config.ts
- TypeScript config: tsconfig.json and tsconfig.app.json
- Capacitor config: capacitor.config.ts
  - appId: com.bribdev.handycap
  - appName: Handycap
  - webDir: dist
- Android project: android/ directory (generated/managed by Capacitor)
- NGINX config for static hosting: nginx.conf

Environment variables
- `VITE_APP_VERSION`: Used to dynamically inject the app version into the "About" page (e.g. `VITE_APP_VERSION=1.1.0`). Note that Vite evaluates this **at build time**, so any changes to this variable require a fresh `npm run build` and `npx cap sync android` to propagate into the Android APK.
- If you add more custom environment variables, prefix them with `VITE_` and document them here.

Android signing
- An example helper script exists at setup-android-release.sh which exports signing‑related environment variables. Adjust paths and secrets to your environment; do not commit actual secrets.

## Development
- Run dev server with HMR:
  - npm run dev
- Type checking in watch/build pipelines:
  - npm run type-check

Project entry points
- index.html
- src/ (application source)

## Build & production
Create a production build:
- npm run build

Preview the production build locally:
- npm run preview

The build outputs static files in dist/ suitable for serving by any static server or via the included Dockerfile/NGINX.

## Android build & release
Capacitor workflows typically follow these steps:
1) Build the web assets
- npm run build

2) Sync web assets to native platform
- npx cap sync android

3) Open Android Studio to build/run/sign
- npx cap open android

4) Configure signing
- Use Android Studio or environment variables/gradle properties. The helper script setup-android-release.sh illustrates exporting:
  - ANDROID_KEYSTORE_PATH
  - ANDROID_KEYSTORE_PASSWORD
  - ANDROID_KEY_ALIAS
  - ANDROID_KEY_PASSWORD
  - JAVA_HOME

5) Build an APK/AAB in Android Studio (Build > Generate Signed Bundle/APK)

Notes
- Keep android/local.properties and private keystores out of version control.
- If the Android project becomes out of sync, re‑run npx cap sync android.

## Docker usage
Build a production image:
- docker build -t handycap:latest .

Run the container (serves dist/ via NGINX):
- docker run --rm -p 8080:80 handycap:latest

Then open http://localhost:8080

## Project scripts
From package.json:
- npm run dev — start Vite dev server
- npm run build — type‑check then build
- npm run build-only — build without type checking
- npm run type-check — run vue-tsc in build mode
- npm run preview — preview built app locally

## Troubleshooting
- After upgrading dependencies, delete node_modules and package-lock.json, then reinstall:
  - rm -rf node_modules package-lock.json && npm install
- Vite dev server port conflicts: use PORT=5174 npm run dev or configure in vite.config.ts
- Capacitor Android build errors:
  - Ensure Java 21 is configured (JAVA_HOME)
  - Open the Android project from the android/ folder in Android Studio
  - Re‑run npx cap sync android after web code changes that affect native assets

## Contributing
Contributions, issues, and feature requests are welcome. Please open a GitHub issue or pull request.

## License
This project is licensed under the Apache License, Version 2.0.

- See the LICENSE file for details.
- You may obtain a copy at http://www.apache.org/licenses/LICENSE-2.0
