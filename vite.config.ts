import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      // Force the full vue-i18n build (includes message compiler) instead of
      // the runtime-only build, so {n} placeholders work in production/Android.
      'vue-i18n': 'vue-i18n/dist/vue-i18n.esm-bundler.js'
    },
  },
})
