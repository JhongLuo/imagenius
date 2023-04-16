# ImaGenius

Web frontend for ImaGenius.

ImaGenius supports the following functionalities:

- Generating images from a given prompt

- Saving selected generated images to the library

- Retouching the images with new prompts

- Visualizing the edit history of the image

- Showing aggregate statistics about the library

Built on top of Vue 3 Composition API with Vite and UnoCSS.

## Usage

Run the following commands to start the development server:

```bash
npm install   # if using npm
pnpm install  # if using pnpm
```

and then

```bash
npm run dev   # or
pnpm run dev
```

Or, if having [`ni`](https://www.npmjs.com/package/@antfu/ni) installed, run the following command:

```bash
ni
```

and

```bash
nr dev --open
```

### Default Port

The default port is `5174`. You can change it by passing the `--port` flag to the `dev` script.

```bash
nr dev --port 2333
```

## Features

- [Vue 3](https://github.com/vuejs/core) + [Vite 4](https://github.com/vitejs/vite) + [pnpm](https://pnpm.io/)

- [TypeScript](https://www.typescriptlang.org/)

- [File based routing](./src/pages) and [Components auto importing](./src/components)

- [UnoCSS](https://github.com/antfu/unocss) - The instant on-demand atomic CSS engine.

## Pre-packed

### UI Frameworks

- [UnoCSS](https://github.com/antfu/unocss) - The instant on-demand atomic CSS engine.

### Icons

- [Iconify](https://iconify.design) - use icons from any icon sets [🔍Icônes](https://icones.netlify.app/)
- [Pure CSS Icons via UnoCSS](https://github.com/antfu/unocss/tree/main/packages/preset-icons)

### Plugins

- [Vue Router](https://github.com/vuejs/vue-router)
- [`vite-plugin-pages`](https://github.com/hannoeru/vite-plugin-pages) - file system based routing
- [`unplugin-auto-import`](https://github.com/antfu/unplugin-auto-import) - Directly use Vue Composition API and others without importing
- [`unplugin-vue-components`](https://github.com/antfu/unplugin-vue-components) - components auto import
- [`unplugin-vue-macros`](https://github.com/sxzz/unplugin-vue-macros) - Explore and extend more macros and syntax sugar to Vue.
- [VueUse](https://github.com/antfu/vueuse) - collection of useful composition APIs

## Acknowledgements

Style and plug-in integrations inspired by [Vitesse Lite](https://github.com/antfu/vitesse-lite) from [@antfu](https://github.com/antfu/).
