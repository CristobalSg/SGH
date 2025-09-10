/// <reference types="vitest" />

import legacy from '@vitejs/plugin-legacy'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    legacy()
  ],
  server: {
    host: '0.0.0.0',
    port: 8100,
    hmr: {
      port: 8100
    }
  },
  define: {
    'import.meta.env.VITE_API_URL': JSON.stringify(process.env.API_URL),
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/setupTests.ts',
  }
})
