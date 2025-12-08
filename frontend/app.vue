<template>
  <div>
    <NuxtRouteAnnouncer />
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
    <ToastContainer />
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #FAFAFA;
  color: #111;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

a {
  text-decoration: none;
  color: inherit;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

/* Utility Classes */
.grid {
  display: grid;
}
.flex {
  display: flex;
}
.justify-between {
  justify-content: space-between;
}
.justify-center {
  justify-content: center;
}
.items-center {
  align-items: center;
}
.items-start {
  align-items: flex-start;
}
.items-end {
  align-items: flex-end;
}
.gap-2 { gap: 0.5rem; }
.gap-3 { gap: 0.75rem; }
.gap-4 { gap: 1rem; }
.gap-6 { gap: 1.5rem; }
.gap-8 { gap: 2rem; }

.mb-0 { margin-bottom: 0; }
.mb-1 { margin-bottom: 0.25rem; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-3 { margin-bottom: 0.75rem; }
.mb-4 { margin-bottom: 1rem; }
.mb-6 { margin-bottom: 1.5rem; }
.mb-8 { margin-bottom: 2rem; }
.mt-2 { margin-top: 0.5rem; }
.mt-4 { margin-top: 1rem; }
.ml-auto { margin-left: auto; }

.py-4 { padding-top: 1rem; padding-bottom: 1rem; }
.py-8 { padding-top: 2rem; padding-bottom: 2rem; }
.py-12 { padding-top: 3rem; padding-bottom: 3rem; }
.px-2 { padding-left: 0.5rem; padding-right: 0.5rem; }
.px-3 { padding-left: 0.75rem; padding-right: 0.75rem; }
.px-4 { padding-left: 1rem; padding-right: 1rem; }
.px-8 { padding-left: 2rem; padding-right: 2rem; }
.p-2 { padding: 0.5rem; }
.p-3 { padding: 0.75rem; }
.p-4 { padding: 1rem; }

.w-full { width: 100%; }
.h-full { height: 100%; }

.text-center { text-align: center; }
.text-xs { font-size: 0.75rem; }
.text-sm { font-size: 0.875rem; }
.text-lg { font-size: 1.125rem; }
.text-xl { font-size: 1.25rem; }
.text-2xl { font-size: 1.5rem; }

.font-medium { font-weight: 500; }
.font-semibold { font-weight: 600; }
.font-bold { font-weight: 700; }

.text-gray-400 { color: #9CA3AF; }
.text-gray-500 { color: #6B7280; }
.text-gray-600 { color: #4B5563; }
.text-white { color: white; }
.text-black { color: #111; }
.text-red-500 { color: #EF4444; }
.text-green-500 { color: #10B981; }

.bg-white { background: white; }
.bg-black { background: #111; }
.bg-gray-50 { background: #F9FAFB; }
.bg-gray-100 { background: #F3F4F6; }
.bg-red-50 { background: #FEF2F2; }

.rounded-full { border-radius: 9999px; }
.rounded-xl { border-radius: 0.75rem; }
.rounded-2xl { border-radius: 1rem; }
.rounded-3xl { border-radius: 1.5rem; }

.border { border: 1px solid #E5E7EB; }
.border-gray-100 { border-color: #F3F4F6; }
.border-gray-200 { border-color: #E5E7EB; }

.shadow-sm { box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); }
.shadow-lg { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }

.cursor-pointer { cursor: pointer; }
.relative { position: relative; }
.absolute { position: absolute; }
.fixed { position: fixed; }

.overflow-hidden { overflow: hidden; }
.overflow-x-auto { overflow-x: auto; }

.space-y-4 > * + * { margin-top: 1rem; }
.space-y-6 > * + * { margin-top: 1.5rem; }

.grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }

@media (min-width: 768px) {
  .md\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .md\:grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
  .md\:relative { position: relative; }
  .md\:border-none { border: none; }
  .md\:p-0 { padding: 0; }
  .md\:bg-transparent { background: transparent; }
}

@media (min-width: 1024px) {
  .lg\:col-span-2 { grid-column: span 2 / span 2; }
  .lg\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}

/* Smooth Transitions */
button, a, .card {
  transition: all 0.2s ease;
}

button:hover, a:hover {
  opacity: 0.9;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
