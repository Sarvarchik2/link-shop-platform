// https://nuxt.com/docs/api/configuration/nuxt-config
// Force restart - updated locales
export default defineNuxtConfig({
  compatibilityDate: '2025-12-09', // Latest stable Nuxt 3 Release date as a safe baseline
  future: {
    compatibilityVersion: 4,
  },
  srcDir: 'app',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss', '@nuxtjs/i18n'],

  experimental: {
    // autoImportTranslationFunctions: true // Removed as it is not a valid option in this version
  },

  runtimeConfig: {
    apiBaseInternal: process.env.NUXT_API_BASE_INTERNAL || 'http://localhost:8000',
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
    }
  },

  devServer: {
    host: '0.0.0.0',
    port: process.env.PORT ? parseInt(process.env.PORT) : 3000
  },

  nitro: {
    preset: 'node-server',
    compatibilityDate: '2026-01-13',
    // host and port are strictly environment/preset specific in newer Nitro versions
  },

  css: ['~/assets/css/main.css', '~/assets/css/platform-admin.css'],
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    }
  },
  vue: {
    compilerOptions: {
      isCustomElement: (tag) => tag === 'iconify-icon' || tag.startsWith('swiper-')
    }
  },

  i18n: {
    locales: [
      { code: 'uz', iso: 'uz-UZ', file: 'uz.json', name: "O'zbek" },
      { code: 'ru', iso: 'ru-RU', file: 'ru.json', name: 'Русский' },
      { code: 'en', iso: 'en-US', file: 'en.json', name: 'English' }
    ],
    defaultLocale: 'uz',
    strategy: 'prefix_except_default',
    langDir: '../i18n/locales',
    detectBrowserLanguage: {
      useCookie: true,
      cookieKey: 'i18n_redirected',
      redirectOn: 'root',
    }
  },

  app: {
    pageTransition: { name: 'page', mode: 'out-in' },
    head: {
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ],
      link: [
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap' }
      ],
      script: [
        { src: 'https://telegram.org/js/telegram-web-app.js' },
        { src: 'https://code.iconify.design/iconify-icon/1.0.7/iconify-icon.min.js', defer: true }
      ]
    }
  }
})
