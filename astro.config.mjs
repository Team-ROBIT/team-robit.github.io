// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

import mdx from '@astrojs/mdx';
import remarkGallery from './src/plugins/remark-gallery.mjs';

// https://astro.build/config
export default defineConfig({
  site: 'https://team-robit.github.io',

  vite: {
    plugins: [tailwindcss()],
  },

  markdown: {
    remarkPlugins: [remarkGallery],
  },

  integrations: [mdx()],
});
