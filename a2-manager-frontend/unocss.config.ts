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
    ['icon-btn', 'text-[0.9em] inline-block cursor-pointer select-none opacity-75 transition duration-2 ease-in-out hover:opacity-100 hover:text-teal-6 !outline-none'],
    ['icon-plain', 'text-[0.9em] inline-block cursor-default select-none opacity-75'],
    ['my-outline-none', 'outline-none focus:outline-none ring-none focus:ring-none'],
    ['my-border', 'border border-1 border-rounded border-gray-4 dark:border-gray-5 border-op-20 dark:border-op-20 focus:border-gray-4 focus:dark:border-gray-5 focus:border-op-40 focus:dark:border-op-30 my-outline-none'],
    ['my-text-color-primary', 'text-gray-8 placeholder-gray-6 dark:text-gray-2 dark:placeholder-gray-4'],
    ['my-text-color-secondary', 'text-gray-5 placeholder-gray-5 dark:text-gray-4'],
    ['my-text-color-tertiary', 'text-gray-4 placeholder-gray-5 dark:text-gray-6'],
    ['my-bg-primary', 'bg-white dark:bg-black'],
    ['my-bg-secondary', 'bg-gray-1 dark:bg-true-gray-9'],
    ['my-bg-tertiary', 'bg-gray-2 dark:bg-true-gray-8'],
    ['my-input-style', 'text-sm font-medium rounded-lg my-text-color-primary my-bg-primary my-border'],
    ['my-text-input-style', 'w-full px-4 py-2 my-input-style'],
    ['my-title-style', 'block mb-5 text-xl font-extrabold my-text-color-primary select-none'],
    ['my-label-style', 'block mb-2 text-sm font-medium my-text-color-primary'],
    ['my-helper-text-style', 'mt-1 text-xs font-medium my-text-color-secondary'],
    ['my-btn-primary', 'px-4 py-1 rounded inline-block bg-teal-6 text-white cursor-pointer hover:bg-teal-7 disabled:cursor-default disabled:bg-gray-6 disabled:opacity-50 my-border'],
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
