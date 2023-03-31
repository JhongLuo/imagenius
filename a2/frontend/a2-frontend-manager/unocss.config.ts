import {
  defineConfig,
  presetAttributify,
  presetIcons,
  presetUno,
  presetWebFonts,
  // transformerDirectives,
  // transformerVariantGroup,
} from 'unocss'

export default defineConfig({
  shortcuts: [
    // icons
    ['icon-btn', 'text-[0.9em] inline-block cursor-pointer select-none opacity-75 transition duration-2 ease-in-out hover:opacity-100 hover:text-teal-6 !outline-none'],
    ['icon-plain', 'text-[0.9em] inline-block cursor-default select-none opacity-75'],
    // styles
    ['my-outline-none', 'outline-none focus:outline-none ring-none focus:ring-none'],
    ['my-border', 'border border-1.5 border-rounded-md border-gray-4 dark:border-gray-5 border-op-20 dark:border-op-20 focus:border-gray-4 focus:dark:border-gray-5 focus:border-op-40 focus:dark:border-op-30 my-outline-none'],
    ['my-shadow', 'shadow-lg shadow-gray-5 shadow-op-50 dark:shadow-gray-8 dark:shadow-op-60'],
    ['my-shadow-light', 'shadow-lg shadow-gray-5 shadow-op-30 dark:shadow-gray-8 dark:shadow-op-60'],
    ['my-shadow-heavy', 'shadow-lg shadow-gray-5 dark:shadow-gray-8'],
    // colors
    ['my-text-color-primary', 'text-gray-8 placeholder-gray-4 dark:text-gray-2 dark:placeholder-gray-7'],
    ['my-text-color-secondary', 'text-gray-5 placeholder-gray-5 dark:text-gray-4'],
    ['my-text-color-tertiary', 'text-gray-4 placeholder-gray-5 dark:text-gray-6'],
    ['my-bg-primary', 'bg-white dark:bg-black'],
    ['my-bg-secondary', 'bg-#FAFAFA dark:bg-#181A22'],
    ['my-bg-tertiary', 'bg-#FAFAFA dark:bg-gray-8'],
    // components
    ['my-input', 'text-sm font-medium rounded-md my-text-color-primary my-bg-primary my-border pla disabled:text-op-15 disabled:placeholder-op-15'],
    ['my-text-input', 'w-full px-4 py-2 my-input'],
    ['my-title', 'mb-5 text-xl font-extrabold my-text-color-primary select-none'],
    ['my-label', 'mb-2 text-sm font-medium my-text-color-primary'],
    ['my-helper-text', 'mt-1 text-xs font-medium my-text-color-secondary'],
    ['my-btn', 'px-3 py-1 rounded inline-block text-white cursor-pointer disabled:cursor-default disabled:bg-gray-6 disabled:opacity-50 my-border'],
    ['my-btn-primary', 'my-btn bg-teal-6 hover:bg-teal-7 dark:bg-teal-7 dark:hover:bg-teal-8'],
    ['my-btn-danger', 'my-btn bg-red-6 hover:bg-red-7 dark:bg-red-7 dark:hover:bg-red-8'],
    ['my-card', 'rounded-lg my-shadow'],

  ],
  presets: [
    presetUno(),
    presetAttributify(),
    presetIcons({
      scale: 1.2,
      warn: true,
    }),
    presetWebFonts({
      fonts: {
        sans: 'DM Sans',
        serif: 'DM Serif Display',
        mono: 'DM Mono',
      },
    }),
  ],
  // transformers: [
  //   transformerDirectives(),
  //   transformerVariantGroup(),
  // ],
})
