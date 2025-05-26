# handicap-calculator

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

## Android Project

Capacitor ist das neue Runtime-Layer von Ionic, funktioniert aber framework-agnostisch und spielt super mit Vite/Vue zusammen.

1. **Installiere Capacitor**

   ```bash
   npm install @capacitor/core @capacitor/cli --save
   ```

2. **Initialisiere dein Capacitor-Projekt**
   Im Projekt-Root:

   ```bash
   npx cap init
   ```

   * **Name:** z. B. `HandicapCalculator`
   * **App-ID:** z. B. `com.deinname.handicapcalculator`
   * **Web-dir:** `dist` (Vite-Build-Output)

3. **Baue dein Vue-Projekt**

   ```bash
   npm run build
   ```

4. **Platform Android hinzufügen**

   ```bash
   npx cap add android
   ```

5. **Assets synchronisieren**
   Jedes Mal, wenn du neu baust:

   ```bash
   npm run build
   npx cap copy
   ```

6. **Android Studio öffnen & APK erzeugen**

   ```bash
   npx cap open android
   ```

   – In Android Studio wählst du dein virtuelles Gerät oder verbindest ein reales, und klickst auf **Run** (oder **Build → Generate Signed Bundle / APK** für Release-Builds).

Das Ergebnis ist eine vollwertige Android-App mit WebView, in der dein Vue-Frontend läuft. Capacitor bietet außerdem Plugins für Kamera, Filesystem, Geolocation etc., falls du später native APIs brauchst.

### Sync

Nach Anpassungen am Vue-Projekt die App synchen:

`npx cap sync android`

Release-Package erstellen:

```zsh
cd android
./gradlew assembleRelease
```

Und das APK-File signieren:
```zsh
$ANDROID_SDK_ROOT/build-tools/$(ls $ANDROID_SDK_ROOT/build-tools | sort -V | tail -n1)/apksigner \
  sign \
  --ks /Users/brigittebohm/Workspace/golf/handicap-calculator/android/my-release-key.jks \
  --ks-key-alias bri-b-dev \
  --out android/app/build/outputs/apk/release/app-release-signed.apk \
  android/app/build/outputs/apk/release/app-release-unsigned.apk
```

