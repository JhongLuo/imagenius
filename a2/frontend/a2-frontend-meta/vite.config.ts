/// <reference types="vitest" />

import path from 'path'
import { defineConfig } from 'vite'
import Vue from '@vitejs/plugin-vue'
import Pages from 'vite-plugin-pages'
import Components from 'unplugin-vue-components/vite'
import AutoImport from 'unplugin-auto-import/vite'
import Unocss from 'unocss/vite'
import VueMacros from 'unplugin-vue-macros/vite'

export default defineConfig({
  server: {
    port: 5176,
    strictPort: true,
  },
  resolve: {
    alias: {
      '~/': `${path.resolve(__dirname, 'src')}/`,
    },
  },
  plugins: [
    VueMacros({
      plugins: {
        vue: Vue({
          reactivityTransform: true,
        }),
      },
    }),

    // https://github.com/hannoeru/vite-plugin-pages
    Pages(),

    // https://github.com/antfu/unplugin-auto-import
    AutoImport({
      imports: [
        'vue',
        'vue/macros',
        'vue-router',
        '@vueuse/core',
        // custom
        {
          // 'package-name': [
          //   'import-name',    // import { import-name } from 'package-name',
          //   ['from', 'alias'], // import { from as alias } from 'package-name',
          // ],
          axios: [
            ['default', 'axios'],
          ],
          uuid: [
            ['v4', 'uuidv4'],
          ],
          flowbite: [
            'initTooltips',
          ],
        },
        {
          from: 'apexcharts',
          imports: ['ApexOptions'],
          type: true,
        },
        // custom types
        {
          from: '~/composables/useToasts',
          imports: ['ToastModel', 'ToastType'],
          type: true,
        },
        {
          from: '~/composables/utils',
          imports: ['StatsData', 'RawStatsData', 'CacheConfigOptions'],
          type: true,
        },
      ],
      dts: true,
      dirs: [
        './src/composables/**',
        './src/stores/**',
      ],
      vueTemplate: true,
    }),

    // https://github.com/antfu/vite-plugin-components
    Components({
      dts: true,
    }),

    // https://github.com/antfu/unocss
    // see unocss.config.ts for config
    Unocss(),
  ],

  // https://github.com/vitest-dev/vitest
  test: {
    environment: 'jsdom',
  },
})