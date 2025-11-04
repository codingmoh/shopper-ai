import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    fs: {
      // allow serving files from one level up to access /img during dev
      allow: ['..']
    }
  }
})
