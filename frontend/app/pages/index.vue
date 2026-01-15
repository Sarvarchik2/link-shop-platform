<template>
  <div class="antialiased selection:bg-zinc-900 selection:text-white">
    <nav class="fixed top-0 w-full z-50 glass border-b border-zinc-100/50 transition-all duration-300">
      <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <div class="flex items-center gap-8">
          <NuxtLink :to="localePath('/')" class="text-lg font-semibold tracking-tight flex items-center gap-2">
            <div class="w-5 h-5 bg-black rounded-md flex items-center justify-center text-white">
              <iconify-icon icon="lucide:box" width="12"></iconify-icon>
            </div>
            Storely
          </NuxtLink>
          <div class="hidden md:flex items-center gap-6 text-sm font-medium text-zinc-500">
            <a href="#features" class="hover:text-black transition-colors">{{ $t('nav.features') }}</a>
            <a href="#solutions" class="hover:text-black transition-colors">{{ $t('nav.solutions') }}</a>
            <a href="#pricing" class="hover:text-black transition-colors">{{ $t('nav.pricing') }}</a>
            <a href="#clients" class="hover:text-black transition-colors">{{ $t('nav.clients') }}</a>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <LanguageSwitcher />
          <NuxtLink v-if="!user" :to="localePath('/login')"
            class="text-sm font-medium text-zinc-500 hover:text-black transition-colors">{{ $t('nav.login') }}
          </NuxtLink>
          <NuxtLink v-else :to="localePath(profileLink)"
            class="text-sm font-medium text-zinc-500 hover:text-black transition-colors">{{ $t('nav.profile') }}
          </NuxtLink>
          <NuxtLink :to="localePath('/register-shop')"
            class="registr-shop-btn bg-black text-white px-4 py-2 rounded-full text-sm font-medium hover:bg-zinc-800 shadow-lg shadow-zinc-200/50 transition-smooth hover-lift">
            {{ $t('nav.create_shop') }}
          </NuxtLink>
        </div>
      </div>
    </nav>

    <section class="relative pt-32 pb-20 overflow-hidden perspective-container">
      <div
        class="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[500px] bg-gradient-to-b from-zinc-100/50 to-transparent rounded-[100%] blur-3xl -z-10 opacity-60">
      </div>

      <div class="max-w-5xl mx-auto px-6 text-center z-10 relative">
        <div :class="['reveal', { active: heroRevealed }]">
          <!-- <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-50 border border-zinc-200 text-xs font-medium text-zinc-600 mb-8 animate-float">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
            </span>
            Storely 2.0 yaqin kunda
          </div> -->

          <h1 class="text-5xl md:text-7xl font-semibold tracking-tight text-zinc-900 mb-8 leading-[1.1]">
            {{ $t('home.hero.title_1') }} <br>
            <span class="text-zinc-400">{{ $t('home.hero.title_2') }}</span>
          </h1>

          <p class="text-lg md:text-xl text-zinc-500 max-w-2xl mx-auto mb-10 leading-relaxed font-normal">
            {{ $t('home.hero.subtitle') }}
          </p>

          <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-20">
            <NuxtLink :to="localePath('/register-shop')"
              class="w-full sm:w-auto px-8 py-3.5 bg-black text-white rounded-full font-medium shadow-xl shadow-zinc-900/10 hover:shadow-2xl hover:bg-zinc-800 flex items-center justify-center gap-2 group transition-smooth hover-lift">
              {{ $t('home.hero.start_free') }}
              <iconify-icon icon="lucide:arrow-right"
                class="group-hover:translate-x-1 transition-smooth"></iconify-icon>
            </NuxtLink>
            <button
              class="w-full sm:w-auto px-8 py-3.5 bg-white border border-zinc-200 text-zinc-700 rounded-full font-medium hover:bg-zinc-50 hover:border-zinc-300 flex items-center justify-center gap-2 transition-smooth hover-lift">
              <iconify-icon icon="lucide:play-circle" width="18"></iconify-icon>
              {{ $t('home.hero.demo_video') }}
            </button>
          </div>
        </div>

        <div ref="heroDashboard"
          class="relative mx-auto w-full max-w-[1000px] aspect-[16/10] bg-white rounded-xl border border-zinc-200 shadow-2xl overflow-hidden transition-transform duration-100 ease-out origin-bottom select-none">
          <div class="h-8 bg-zinc-50 border-b border-zinc-100 flex items-center px-4 gap-2">
            <div class="flex gap-1.5">
              <div class="w-2.5 h-2.5 rounded-full bg-zinc-300"></div>
              <div class="w-2.5 h-2.5 rounded-full bg-zinc-300"></div>
              <div class="w-2.5 h-2.5 rounded-full bg-zinc-300"></div>
            </div>
            <div
              class="mx-auto w-1/3 h-4 bg-white rounded flex items-center justify-center text-[10px] text-zinc-400 font-medium shadow-sm border border-zinc-100">
              storely.uz/dashboard
            </div>
          </div>

          <div class="p-6 grid grid-cols-4 gap-6 h-full bg-zinc-50/30">
            <div class="hidden md:flex col-span-1 flex-col gap-2 border-r border-zinc-100 pr-4">
              <div class="h-8 w-full bg-zinc-100 rounded mb-4"></div>
              <div class="h-6 w-3/4 bg-zinc-100 rounded"></div>
              <div class="h-6 w-full bg-zinc-100 rounded"></div>
              <div class="h-6 w-5/6 bg-zinc-100 rounded"></div>
              <div class="mt-auto h-20 w-full bg-zinc-100 rounded"></div>
            </div>
            <!-- Main Area -->
            <div class="col-span-4 md:col-span-3 flex flex-col gap-6">
              <!-- Stats Row -->
              <div class="grid grid-cols-3 gap-4">
                <div class="bg-white p-4 rounded-lg border border-zinc-100 shadow-sm">
                  <div class="text-xs text-zinc-400 mb-1">Total Revenue</div>
                  <div class="text-2xl font-semibold text-zinc-900">{{ formatPrice(12402) }}</div>
                  <div class="mt-2 h-1 w-full bg-zinc-100 rounded-full overflow-hidden">
                    <div class="h-full w-[70%] bg-zinc-900 rounded-full"></div>
                  </div>
                </div>
                <div class="bg-white p-4 rounded-lg border border-zinc-100 shadow-sm">
                  <div class="text-xs text-zinc-400 mb-1">Orders</div>
                  <div class="text-2xl font-semibold text-zinc-900">156</div>
                  <div class="mt-2 h-1 w-full bg-zinc-100 rounded-full overflow-hidden">
                    <div class="h-full w-[45%] bg-zinc-900 rounded-full"></div>
                  </div>
                </div>
                <div class="bg-white p-4 rounded-lg border border-zinc-100 shadow-sm">
                  <div class="text-xs text-zinc-400 mb-1">Active Now</div>
                  <div class="text-2xl font-semibold text-zinc-900">24</div>
                  <div class="flex gap-1 mt-2">
                    <div class="h-4 w-1 bg-green-400 rounded-full"></div>
                    <div class="h-2 w-1 bg-green-200 rounded-full"></div>
                    <div class="h-3 w-1 bg-green-300 rounded-full"></div>
                  </div>
                </div>
              </div>
              <!-- Chart Area -->
              <div class="flex-1 bg-white rounded-lg border border-zinc-100 shadow-sm p-6 relative overflow-hidden">
                <div class="flex justify-between items-center mb-6">
                  <div class="h-4 w-32 bg-zinc-100 rounded"></div>
                  <div class="h-8 w-24 bg-zinc-50 rounded border border-zinc-100"></div>
                </div>
                <!-- Simulated Chart Line -->
                <svg class="w-full h-[200px] text-zinc-900" preserveAspectRatio="none">
                  <path
                    d="M0,150 C50,150 50,100 100,100 C150,100 150,180 200,180 C250,180 250,40 300,40 C350,40 350,120 400,120 C450,120 450,80 500,80 C550,80 550,160 600,160 C650,160 650,20 700,20"
                    fill="none" stroke="currentColor" stroke-width="2" vector-effect="non-scaling-stroke"
                    opacity="0.8" />
                  <defs>
                    <linearGradient id="gradient" x1="0" x2="0" y1="0" y2="1">
                      <stop offset="0%" stop-color="rgba(0,0,0,0.1)" />
                      <stop offset="100%" stop-color="rgba(0,0,0,0)" />
                    </linearGradient>
                  </defs>
                  <path
                    d="M0,150 C50,150 50,100 100,100 C150,100 150,180 200,180 C250,180 250,40 300,40 C350,40 350,120 400,120 C450,120 450,80 500,80 C550,80 550,160 600,160 C650,160 650,20 700,20 V200 H0 Z"
                    fill="url(#gradient)" stroke="none" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <!-- Stats Bar -->
        <div class="mt-24 border-t border-zinc-100 pt-16 reveal" :class="{ active: heroRevealed }">
          <div class="grid grid-cols-2 md:grid-cols-3 gap-8 text-center max-w-4xl mx-auto">
            <div>
              <div class="text-3xl font-bold mb-1">1,200+</div>
              <div class="text-sm text-zinc-500">{{ $t('home.stats.active_shops') }}</div>
            </div>
            <div>
              <div class="text-3xl font-bold mb-1">25k+</div>
              <div class="text-sm text-zinc-500">{{ $t('home.stats.daily_orders') }}</div>
            </div>
            <div class="col-span-2 md:col-span-1">
              <div class="text-3xl font-bold mb-1">98%</div>
              <div class="text-sm text-zinc-500">{{ $t('home.stats.happy_merchants') }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>



    <section id="features" class="py-32 bg-zinc-50/50">
      <div class="max-w-7xl mx-auto px-6">
        <div class="mb-20 max-w-2xl reveal" :class="{ active: featuresRevealed }">
          <h2 class="text-3xl md:text-5xl font-semibold tracking-tight text-zinc-900 mb-6"
            v-html="$t('home.features_new.title')"></h2>
          <p class="text-lg text-zinc-500">{{ $t('home.features_new.subtitle') }}</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 auto-rows-auto">
          <!-- Block 1: Analitika -->
          <div
            class="md:col-span-1 bg-white rounded-2xl border border-zinc-200/80 p-8 shadow-sm hover:shadow-xl transition-all duration-300 group overflow-hidden relative reveal"
            :class="{ active: featuresRevealed }">
            <div class="relative z-10 flex flex-col h-full">
              <div class="flex justify-between items-start mb-6">
                <div class="w-10 h-10 rounded-lg bg-zinc-100 flex items-center justify-center text-zinc-700">
                  <iconify-icon icon="lucide:bar-chart-3" width="20"></iconify-icon>
                </div>
                <!-- Period Switcher -->
                <div class="flex bg-zinc-100 p-1 rounded-lg text-[10px] font-medium transition-smooth">
                  <button v-for="p in ['Bugun', 'Bu hafta', 'Barcha vaqt']" :key="p" @click="analyticsPeriod = p"
                    :class="['px-2 py-1 rounded-md transition-all', analyticsPeriod === p ? 'bg-white shadow-sm text-black' : 'text-zinc-400 hover:text-zinc-600']">
                    {{ p === 'Bugun' ? $t('periods.today') : p === 'Bu hafta' ? $t('periods.week') : $t('periods.all')
                    }}
                  </button>
                </div>
              </div>

              <h3 class="text-xl font-semibold mb-2">{{ $t('home.features_new.analytics_v2.title') }}</h3>
              <p class="text-zinc-500 text-sm mb-8 leading-relaxed">{{ $t('home.features_new.analytics_v2.desc') }}
              </p>

              <div class="mt-auto space-y-6">
                <div>
                  <div class="text-[10px] uppercase tracking-wider text-zinc-400 font-bold mb-1">{{
                    $t('home.features_new.analytics_v2.revenue') }}</div>
                  <div class="text-3xl font-bold text-zinc-900 transition-all duration-500 tabular-nums">
                    {{ formatPrice(analyticsData.revenue) }}
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-4">
                  <div class="bg-zinc-50 p-3 rounded-xl border border-zinc-100">
                    <div class="text-[10px] uppercase text-zinc-400 font-bold mb-0.5">{{
                      $t('home.features_new.analytics_v2.customers') }}</div>
                    <div class="text-xl font-bold tabular-nums">{{ analyticsData.customers }}</div>
                  </div>
                  <div class="bg-zinc-50 p-3 rounded-xl border border-zinc-100">
                    <div class="text-[10px] uppercase text-zinc-400 font-bold mb-0.5">{{
                      $t('home.features_new.analytics_v2.orders') }}</div>
                    <div class="text-xl font-bold tabular-nums">{{ analyticsData.orders }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Block 2: KILLER-FEATURE - Telegram Web App Integration -->
          <div
            class="md:col-span-2 bg-zinc-900 text-white rounded-2xl p-8 shadow-xl hover:shadow-2xl transition-all duration-500 group overflow-hidden relative reveal overflow-hidden"
            :class="{ active: featuresRevealed }">
            <!-- Background Glow -->
            <div
              class="absolute -right-20 -top-20 w-80 h-80 bg-blue-500/10 rounded-full blur-[100px] group-hover:bg-blue-500/20 transition-all duration-700">
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 h-full relative z-10">
              <div class="flex flex-col justify-center">
                <div
                  class="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center mb-6 text-blue-400 border border-blue-500/30">
                  <iconify-icon icon="lucide:send" width="24"></iconify-icon>
                </div>
                <h2 class="text-2xl md:text-3xl font-bold mb-4 tracking-tight">{{
                  $t('home.features_new.telegram.title') }}</h2>
                <p class="text-zinc-400 text-sm md:text-base leading-relaxed mb-8">
                  {{ $t('home.features_new.telegram.desc') }}
                </p>
                <div class="flex items-center gap-4">
                  <div class="flex -space-x-2">
                    <div v-for="i in 3" :key="i"
                      class="w-8 h-8 rounded-full border-2 border-zinc-900 bg-zinc-800 flex items-center justify-center text-[10px] font-bold">
                      <iconify-icon :icon="['lucide:user', 'lucide:zap', 'lucide:star'][i - 1]"></iconify-icon>
                    </div>
                  </div>
                  <span class="text-xs text-zinc-500 font-medium">+1,200 stores integrated</span>
                </div>
              </div>

              <div class="relative flex items-center justify-center perspective-1000">
                <!-- Phone Mockup -->
                <div
                  class="w-[240px] h-[480px] bg-zinc-800 rounded-[40px] border-[8px] border-zinc-700 shadow-2xl relative overflow-hidden transform rotate-6 group-hover:rotate-3 transition-transform duration-700 group-hover:scale-105">
                  <!-- Screen Content -->
                  <div class="absolute inset-0 bg-white">
                    <!-- Telegram Header -->
                    <div class="h-14 bg-[#517da2] flex items-center px-4 gap-3">
                      <div class="w-8 h-8 rounded-full bg-white/20"></div>
                      <div class="flex-1">
                        <div class="h-2 w-20 bg-white/40 rounded"></div>
                        <div class="h-1.5 w-12 bg-white/20 rounded mt-1"></div>
                      </div>
                    </div>
                    <!-- Chat Area -->
                    <div class="p-4 space-y-4">
                      <div class="w-3/4 h-20 bg-zinc-50 rounded-2xl rounded-tl-none border border-zinc-100 p-3">
                        <div class="h-2 w-full bg-zinc-200 rounded"></div>
                        <div class="h-2 w-2/3 bg-zinc-100 rounded mt-2"></div>
                        <div class="h-2 w-1/2 bg-zinc-100 rounded mt-2"></div>
                      </div>
                    </div>
                    <!-- Bottom Menu Button Overlay -->
                    <div class="absolute bottom-0 inset-x-0 p-4 bg-white/80 backdrop-blur-md border-t border-zinc-100">
                      <div
                        class="w-full py-3 bg-[#2481cc] text-white rounded-xl text-center text-sm font-bold shadow-lg shadow-blue-500/20 animate-pulse-slow">
                        {{ $t('home.features_new.telegram.button') }}
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Floating Labels -->
                <div
                  class="absolute -left-4 top-1/4 bg-white text-black p-3 rounded-2xl shadow-xl border border-zinc-100 opacity-0 group-hover:opacity-100 transition-all duration-500 translate-x-4 group-hover:translate-x-0">
                  <div class="flex items-center gap-2">
                    <div class="w-2 h-2 rounded-full bg-green-500"></div>
                    <span class="text-[10px] font-bold">Menu Button API</span>
                  </div>
                </div>
                <div
                  class="absolute -right-8 bottom-1/4 bg-white text-black p-3 rounded-2xl shadow-xl border border-zinc-100 opacity-0 group-hover:opacity-100 transition-all duration-500 delay-100 -translate-x-4 group-hover:translate-x-0">
                  <div class="flex items-center gap-2">
                    <iconify-icon icon="lucide:link-2" width="12" class="text-blue-500"></iconify-icon>
                    <span class="text-[10px] font-bold">t.me/your_bot</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Block 3: Order Lifecycle -->
          <div
            class="md:col-span-1 bg-white rounded-2xl border border-zinc-200/80 p-8 shadow-sm hover:shadow-xl transition-all duration-300 group overflow-hidden relative reveal"
            :class="{ active: featuresRevealed }">
            <div class="relative z-10 flex flex-col h-full">
              <div class="w-10 h-10 rounded-lg bg-zinc-100 flex items-center justify-center mb-6 text-zinc-700">
                <iconify-icon icon="lucide:workflow" width="20"></iconify-icon>
              </div>
              <h3 class="text-xl font-semibold mb-2">{{ $t('home.features_new.orders_v2.title') }}</h3>
              <p class="text-zinc-500 text-sm mb-10 leading-relaxed">{{ $t('home.features_new.orders_v2.desc') }}
              </p>

              <!-- Vertical Timeline -->
              <div class="space-y-4">
                <div v-for="(step, idx) in orderSteps" :key="step.key" class="relative">
                  <div v-if="idx < orderSteps.length - 1"
                    class="absolute left-5 top-10 bottom-0 w-0.5 bg-zinc-100 -mb-4"></div>
                  <div class="flex items-center gap-4 group/item">
                    <div
                      :class="[step.bg, step.color, 'w-10 h-10 rounded-full flex items-center justify-center transition-all duration-300 group-hover/item:scale-110 z-10 border-2 border-white shadow-sm']">
                      <iconify-icon :icon="step.icon" width="18"></iconify-icon>
                    </div>
                    <div class="flex-1">
                      <div class="flex justify-between items-center">
                        <span class="text-xs font-bold text-zinc-900">{{ $t(`status.${step.key}`) }}</span>
                        <span class="text-[10px] font-bold bg-zinc-100 px-2 py-0.5 rounded-full text-zinc-500"
                          v-if="step.count > 0">{{ step.count }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Block 4: Catalog and Limits -->
          <div
            class="md:col-span-1 bg-white rounded-2xl border border-zinc-200/80 p-8 shadow-sm hover:shadow-xl transition-all duration-300 group overflow-hidden relative reveal"
            :class="{ active: featuresRevealed }">
            <div class="relative z-10 flex flex-col h-full">
              <div class="w-10 h-10 rounded-lg bg-zinc-100 flex items-center justify-center mb-6 text-zinc-700">
                <iconify-icon icon="lucide:layout-grid" width="20"></iconify-icon>
              </div>
              <h3 class="text-xl font-semibold mb-2">{{ $t('home.features_new.catalog.title') }}</h3>
              <p class="text-zinc-500 text-sm mb-8 leading-relaxed">{{ $t('home.features_new.catalog.desc') }}</p>

              <div class="mt-auto space-y-6">
                <!-- Limit Bar -->
                <div class="bg-zinc-50 p-4 rounded-xl border border-zinc-100">
                  <div class="flex justify-between text-[10px] font-bold text-zinc-400 uppercase mb-2">
                    <span>{{ $t('home.features_new.catalog.products') }}</span>
                    <span>2 / 100</span>
                  </div>
                  <div class="h-2 w-full bg-zinc-200 rounded-full overflow-hidden">
                    <div class="h-full w-[2%] bg-black rounded-full transition-all duration-1000 ease-out"></div>
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-4">
                  <div
                    class="border border-zinc-100 p-4 rounded-xl flex flex-col items-center gap-2 hover:bg-zinc-50 transition-colors cursor-default group/btn">
                    <iconify-icon icon="lucide:folder-tree" width="20"
                      class="text-zinc-400 group-hover/btn:text-black transition-colors"></iconify-icon>
                    <span class="text-[10px] font-bold uppercase tracking-wider text-zinc-500">{{
                      $t('home.features_new.catalog.categories') }}</span>
                  </div>
                  <div
                    class="border border-zinc-100 p-4 rounded-xl flex flex-col items-center gap-2 hover:bg-zinc-50 transition-colors cursor-default group/btn">
                    <iconify-icon icon="lucide:award" width="20"
                      class="text-zinc-400 group-hover/btn:text-black transition-colors"></iconify-icon>
                    <span class="text-[10px] font-bold uppercase tracking-wider text-zinc-500">{{
                      $t('home.features_new.catalog.brand') }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Block 5: Logistics and Branding -->
          <div
            class="md:col-span-1 bg-white rounded-2xl border border-zinc-200/80 p-8 shadow-sm hover:shadow-xl transition-all duration-300 group overflow-hidden relative reveal"
            :class="{ active: featuresRevealed }">
            <div class="relative z-10 flex flex-col h-full">
              <div class="w-10 h-10 rounded-lg bg-zinc-100 flex items-center justify-center mb-6 text-zinc-700">
                <iconify-icon icon="lucide:settings-2" width="20"></iconify-icon>
              </div>
              <h3 class="text-xl font-semibold mb-2">{{ $t('home.features_new.settings.title') }}</h3>
              <p class="text-zinc-500 text-sm mb-8 leading-relaxed">{{ $t('home.features_new.settings.desc') }}</p>

              <div class="grid grid-cols-1 gap-4 mt-auto">
                <div
                  class="bg-zinc-50 rounded-xl p-4 border border-zinc-100 relative overflow-hidden group/card shadow-sm">
                  <div class="flex items-center gap-4 relative z-10">
                    <div class="w-10 h-10 rounded-lg bg-white shadow-sm flex items-center justify-center text-zinc-900">
                      <iconify-icon icon="lucide:map-pin" width="20"></iconify-icon>
                    </div>
                    <div>
                      <div class="text-xs font-bold">{{ $t('home.features_new.settings.delivery') }}</div>
                      <div class="text-[10px] text-zinc-400">12 ta viloyat sozlangan</div>
                    </div>
                  </div>
                  <iconify-icon icon="lucide:chevron-right"
                    class="absolute right-4 top-1/2 -translate-y-1/2 text-zinc-300 group-hover/card:translate-x-1 transition-transform"></iconify-icon>
                </div>

                <div
                  class="bg-zinc-900 rounded-xl p-4 border border-zinc-800 relative overflow-hidden group/card shadow-sm">
                  <div class="flex items-center gap-4 relative z-10">
                    <div class="w-10 h-10 rounded-lg bg-zinc-800 flex items-center justify-center text-white">
                      <iconify-icon icon="lucide:image" width="20"></iconify-icon>
                    </div>
                    <div>
                      <div class="text-xs font-bold text-white">{{ $t('home.features_new.settings.banner') }}</div>
                      <div class="text-[10px] text-zinc-500">2 ta faol promo bannerlar</div>
                    </div>
                  </div>
                  <iconify-icon icon="lucide:chevron-right"
                    class="absolute right-4 top-1/2 -translate-y-1/2 text-zinc-700 group-hover/card:translate-x-1 transition-transform"></iconify-icon>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="solutions" class="py-32 bg-white relative overflow-hidden">
      <div class="max-w-7xl mx-auto px-6">
        <div class="text-center mb-24">
          <h2 class="text-3xl md:text-5xl font-semibold tracking-tight text-zinc-900 mb-6 reveal"
            :class="{ active: timelineRevealed }">{{ $t('home.timeline.title') }}</h2>
          <div class="h-1.5 w-24 bg-black mx-auto rounded-full reveal" :class="{ active: timelineRevealed }"></div>
        </div>

        <div class="relative">
          <!-- Desktop Connecting Line -->
          <div
            class="hidden md:block absolute top-[120px] left-[15%] right-[15%] h-px border-t-2 border-dashed border-zinc-200 z-0">
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-12 md:gap-8 relative z-10 transition-smooth">
            <!-- Step 1 -->
            <div class="flex flex-col items-center text-center group reveal" :class="{ active: timelineRevealed }">
              <div class="relative mb-10 w-24 h-24 flex items-center justify-center">
                <div
                  class="absolute inset-0 bg-zinc-50 rounded-3xl border border-zinc-200 rotate-6 group-hover:rotate-12 transition-transform duration-500 shadow-sm">
                </div>
                <div
                  class="absolute inset-0 bg-white rounded-3xl border border-zinc-200 group-hover:-rotate-3 transition-transform duration-500 shadow-md flex items-center justify-center text-zinc-900">
                  <iconify-icon icon="lucide:user-plus" width="32"></iconify-icon>
                </div>
                <div
                  class="absolute -top-3 -right-3 w-8 h-8 bg-black text-white rounded-full flex items-center justify-center text-xs font-bold border-4 border-white">
                  01</div>
              </div>
              <h3 class="text-2xl font-bold mb-4 group-hover:text-black transition-colors">{{
                $t('home.timeline.step1.title') }}</h3>
              <p class="text-zinc-500 text-sm leading-relaxed max-w-[280px]">{{ $t('home.timeline.step1.desc') }}</p>
            </div>

            <!-- Step 2 -->
            <div class="flex flex-col items-center text-center group reveal delay-200"
              :class="{ active: timelineRevealed }">
              <div class="relative mb-10 w-24 h-24 flex items-center justify-center">
                <div
                  class="absolute inset-0 bg-zinc-50 rounded-3xl border border-zinc-200 -rotate-6 group-hover:-rotate-12 transition-transform duration-500 shadow-sm">
                </div>
                <div
                  class="absolute inset-0 bg-white rounded-3xl border border-zinc-200 group-hover:rotate-3 transition-transform duration-500 shadow-md flex items-center justify-center text-zinc-900">
                  <iconify-icon icon="lucide:upload-cloud" width="32"></iconify-icon>
                </div>
                <div
                  class="absolute -top-3 -right-3 w-8 h-8 bg-black text-white rounded-full flex items-center justify-center text-xs font-bold border-4 border-white">
                  02</div>
              </div>
              <h3 class="text-2xl font-bold mb-4 group-hover:text-black transition-colors">{{
                $t('home.timeline.step2.title') }}</h3>
              <p class="text-zinc-500 text-sm leading-relaxed max-w-[280px]">{{ $t('home.timeline.step2.desc') }}</p>
            </div>

            <!-- Step 3 -->
            <div class="flex flex-col items-center text-center group reveal delay-400"
              :class="{ active: timelineRevealed }">
              <div class="relative mb-10 w-24 h-24 flex items-center justify-center">
                <div
                  class="absolute inset-0 bg-black rounded-3xl rotate-12 group-hover:rotate-6 transition-transform duration-500 shadow-xl">
                </div>
                <div
                  class="absolute inset-0 bg-zinc-900 rounded-3xl border border-zinc-800 group-hover:rotate-0 transition-transform duration-500 shadow-2xl flex items-center justify-center text-white">
                  <iconify-icon icon="lucide:rocket" width="32"></iconify-icon>
                </div>
                <div
                  class="absolute -top-3 -right-3 w-8 h-8 bg-white text-black rounded-full flex items-center justify-center text-xs font-bold border-4 border-zinc-900">
                  03</div>
              </div>
              <h3 class="text-2xl font-bold mb-4 group-hover:text-black transition-colors">{{
                $t('home.timeline.step3.title') }}</h3>
              <p class="text-zinc-500 text-sm leading-relaxed max-w-[280px]">{{ $t('home.timeline.step3.desc') }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Section -->
    <section id="pricing" class="py-32 bg-zinc-50 border-t border-zinc-200">
      <div class="max-w-7xl mx-auto px-6">
        <h2 class="text-3xl md:text-5xl font-semibold tracking-tight text-center mb-6 reveal"
          :class="{ active: pricingRevealed }">{{ $t('home.pricing.title') }}</h2>
        <p class="text-center text-zinc-500 mb-20 reveal" :class="{ active: pricingRevealed }">{{
          $t('home.pricing.subtitle') }}</p>

        <div v-if="plansPending" class="text-center py-12">
          <div class="loading-spinner"></div>
          <p class="mt-4 text-zinc-400">{{ $t('home.pricing.loading') }}</p>
        </div>

        <div v-else-if="plans && plans.length > 0" class="grid grid-cols-1 md:grid-cols-3 gap-8 items-start">
          <div v-for="(plan, index) in plans" :key="plan.id"
            class="bg-white rounded-2xl p-8 border shadow-sm hover:shadow-lg transition-all reveal relative" :class="{
              'active': pricingRevealed,
              'border-zinc-900 shadow-2xl md:-mt-8 md:mb-8': plan.slug === 'basic' || index === Math.floor(plans.length / 2)
            }">
            <div v-if="plan.slug === 'basic' || index === Math.floor(plans.length / 2)"
              class="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-black text-white px-3 py-1 rounded-full text-xs font-medium tracking-wide">
              POPULAR
            </div>

            <h3 class="text-xl font-medium mb-2">{{ plan.name }}</h3>
            <div class="text-4xl font-bold mb-6">
              <span v-if="plan.price === 0 || plan.is_trial">{{ formatPrice(0) }}</span>
              <span v-else>{{ formatPrice(plan.price) }}</span>
              <span v-if="plan.is_trial" class="text-base font-normal text-zinc-500">/{{ plan.period_days }} {{
                $t('home.pricing.days') }}</span>
              <span v-else class="text-base font-normal text-zinc-500">/{{ $t('home.pricing.month') }}</span>
            </div>
            <p v-if="plan.description" class="text-sm text-zinc-500 mb-8 border-b border-zinc-100 pb-8">{{
              plan.description }}</p>

            <ul v-if="plan.features_list && plan.features_list.length > 0" class="space-y-4 mb-6">
              <li v-for="(feature, idx) in plan.features_list" :key="idx" class="flex items-center gap-3 text-sm">
                <template v-if="feature.startsWith('✗') || feature.startsWith('-') || feature.startsWith('×')">
                  <iconify-icon icon="lucide:x" class="text-zinc-300"></iconify-icon>
                  <span class="text-zinc-400">{{ feature.replace(/^[✗\-×]\s*/, '') }}</span>
                </template>
                <template v-else>
                  <iconify-icon icon="lucide:check"
                    :class="plan.slug === 'basic' || index === Math.floor(plans.length / 2) ? 'text-black' : 'text-green-500'"></iconify-icon>
                  <span :class="{ 'font-semibold': plan.slug === 'basic' || index === Math.floor(plans.length / 2) }">{{
                    feature.replace(/^[✓√]\s*/, '') }}</span>
                </template>
              </li>
            </ul>

            <!-- Product Limit -->
            <div class="mb-6 p-3 bg-zinc-50 rounded-lg border border-zinc-200">
              <div class="flex items-center gap-2 text-sm text-zinc-600">
                <iconify-icon icon="lucide:package" width="16"></iconify-icon>
                <span>
                  <strong>{{ plan.max_products === null ? $t('home.pricing.unlimited') : plan.max_products }}</strong>
                  {{ $t('home.pricing.products') }}
                </span>
              </div>
            </div>

            <NuxtLink :to="localePath(plan.slug === 'business' ? '/register-shop?plan=business' : '/register-shop')"
              class="w-full py-3 rounded-lg text-sm font-semibold block text-center transition-smooth hover-lift"
              :class="plan.slug === 'basic' || index === Math.floor(plans.length / 2)
                ? 'bg-black text-white hover:bg-zinc-800 shadow-lg'
                : 'border border-zinc-200 hover:border-black hover:bg-zinc-50'">
              <span v-if="plan.slug === 'business'">{{ $t('home.pricing.contact') }}</span>
              <span v-else>{{ $t('home.pricing.select') }} {{ plan.name }}</span>
            </NuxtLink>
          </div>
        </div>

        <div v-else class="text-center py-12 text-zinc-400">
          <p>{{ $t('home.pricing.unavailable') }}</p>
        </div>

        <!-- Offers Section -->
        <div v-if="offers && offers.length > 0" class="mt-20">
          <h2 class="text-2xl md:text-4xl font-semibold tracking-tight text-center mb-6">{{ $t('home.offers.title') }}
          </h2>
          <p class="text-center text-zinc-500 mb-12">{{ $t('home.offers.subtitle') }}</p>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="offer in offers" :key="offer.id"
              class="bg-white rounded-2xl p-8 border-2 border-zinc-900 shadow-lg hover:shadow-xl transition-smooth hover-lift">
              <div class="flex justify-between items-start mb-4 offer-title">
                <h3 class="text-xl font-semibold">{{ getField(offer, 'title') }}</h3>
                <div v-if="offer.price || getField(offer, 'price_text')" class="text-right">
                  <div v-if="offer.price" class="text-2xl font-bold">{{ formatPrice(offer.price) }}</div>
                  <div v-else class="text-sm font-medium text-zinc-600">{{ getField(offer, 'price_text') }}</div>
                </div>
              </div>
              <p class="text-sm text-zinc-600 mb-6">{{ getField(offer, 'description') }}</p>
              <div class="pt-6 border-t border-zinc-200">
                <p class="text-xs text-zinc-500 mb-4">{{ getField(offer, 'contact_text') }}</p>
                <div class="flex gap-3">
                  <a v-if="offer.contact_email" :href="`mailto:${offer.contact_email}`"
                    class="flex-1 py-2.5 px-4 bg-zinc-100 hover:bg-zinc-900 hover:text-white rounded-lg text-sm font-semibold transition-colors text-center">
                    {{ $t('home.offers.email') }}
                  </a>
                  <a v-if="offer.contact_phone" :href="`tel:${offer.contact_phone}`"
                    class="flex-1 py-2.5 px-4 bg-zinc-100 hover:bg-zinc-900 hover:text-white rounded-lg text-sm font-semibold transition-colors text-center">
                    {{ $t('home.offers.phone') }}
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- FAQ Section -->
        <div class="mt-40 max-w-3xl mx-auto px-6 mb-40 reveal" :class="{ active: pricingRevealed }">
          <div class="text-center mb-16">
            <h2 class="text-3xl md:text-5xl font-semibold tracking-tight text-zinc-900 mb-6">{{ $t('home.faq.title') }}
            </h2>
            <p class="text-lg text-zinc-500">{{ $t('home.faq.subtitle') }}</p>
          </div>

          <div class="space-y-4">
            <div v-for="i in 4" :key="i"
              class="border border-zinc-100 rounded-2xl overflow-hidden transition-all duration-300"
              :class="activeFaq === i ? 'bg-zinc-50 shadow-sm border-zinc-200' : 'bg-white hover:bg-zinc-50'">
              <button @click="toggleFaq(i)" class="w-full h-full p-6 text-left flex justify-between items-center group">
                <span class="font-medium text-lg pr-8">{{ $t(`home.faq.q${i}.q`) }}</span>
                <iconify-icon icon="lucide:chevron-down" width="20"
                  class="transition-transform duration-300 flex-shrink-0 text-zinc-400 group-hover:text-black"
                  :class="{ 'rotate-180': activeFaq === i }"></iconify-icon>
              </button>
              <div v-show="activeFaq === i"
                class="px-6 pb-6 text-zinc-500 text-sm leading-relaxed animate-in fade-in slide-in-from-top-2 duration-300">
                {{ $t(`home.faq.q${i}.a`) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-zinc-950 text-zinc-300 pt-24 pb-12 border-t border-zinc-900 relative overflow-hidden">
      <!-- Decorative background blur -->
      <div
        class="absolute top-0 right-0 w-[500px] h-[500px] bg-zinc-900/20 blur-[120px] rounded-full pointer-events-none">
      </div>

      <div class="max-w-7xl mx-auto px-6 relative z-10">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-16 mb-20">
          <!-- Brand and Newsletter -->
          <div class="lg:col-span-5 space-y-10">
            <div>
              <NuxtLink :to="localePath('/')"
                class="text-2xl font-bold tracking-tight flex items-center gap-2 mb-6 text-white group">
                <div
                  class="w-8 h-8 bg-white rounded-lg flex items-center justify-center text-black group-hover:scale-110 transition-transform">
                  <iconify-icon icon="lucide:box" width="18"></iconify-icon>
                </div>
                Storely
              </NuxtLink>
              <p class="text-zinc-400 text-base max-w-sm leading-relaxed mb-8">
                {{ $t('footer.desc') }}
              </p>

              <div class="space-y-4">
                <div class="flex items-center gap-3 text-zinc-400 hover:text-white transition-colors">
                  <iconify-icon icon="lucide:map-pin" width="20"></iconify-icon>
                  <span class="text-sm">{{ $t('footer.address') }}</span>
                </div>
                <div class="flex items-center gap-3 text-zinc-400 hover:text-white transition-colors">
                  <iconify-icon icon="lucide:phone" width="20"></iconify-icon>
                  <a :href="`tel:${$t('footer.phone').replace(/\s/g, '')}`" class="text-sm">{{ $t('footer.phone') }}</a>
                </div>
              </div>
            </div>
          </div>

          <!-- Links Grid -->
          <div class="lg:col-span-7 grid grid-cols-2 md:grid-cols-3 gap-12">
            <div>
              <h4 class="text-white font-semibold mb-8 text-sm uppercase tracking-wider">{{ $t('footer.product.title')
              }}
              </h4>
              <ul class="space-y-4 text-sm">
                <li><a href="#features" class="hover:text-white transition-colors">{{ $t('footer.product.features')
                }}</a>
                </li>
                <li><a href="#solutions" class="hover:text-white transition-colors">{{ $t('footer.product.integrations')
                }}</a></li>
                <li><a href="#" class="hover:text-white transition-colors">{{ $t('footer.product.templates') }}</a></li>
                <li><a href="#" class="hover:text-white transition-colors">{{ $t('footer.product.roadmap') }}</a></li>
              </ul>
            </div>
            <div>
              <h4 class="text-white font-semibold mb-8 text-sm uppercase tracking-wider">{{ $t('footer.company.title')
                }}
              </h4>
              <ul class="space-y-4 text-sm">
                <li><a href="https://linkdigital.uz" target="_blank" class="hover:text-white transition-colors">{{
                  $t('footer.company.about') }}</a></li>
                <li><a href="https://linkdigital.uz" target="_blank" class="hover:text-white transition-colors">{{
                  $t('footer.company.careers') }}</a></li>
                <li><a href="https://linkdigital.uz" target="_blank" class="hover:text-white transition-colors">{{
                  $t('footer.company.blog') }}</a></li>
                <li><a href="https://linkdigital.uz" target="_blank" class="hover:text-white transition-colors">{{
                  $t('footer.company.brand') }}</a></li>
              </ul>
            </div>
            <div>
              <h4 class="text-white font-semibold mb-8 text-sm uppercase tracking-wider">{{ $t('footer.legal.title') }}
              </h4>
              <ul class="space-y-4 text-sm">
                <li><a href="#" class="hover:text-white transition-colors">{{ $t('footer.legal.privacy') }}</a></li>
                <li><a href="#" class="hover:text-white transition-colors">{{ $t('footer.legal.terms') }}</a></li>
                <li><a href="#" class="hover:text-white transition-colors">{{ $t('footer.legal.cookie') }}</a></li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Bottom Strip -->
        <div
          class="pt-10 border-t border-zinc-900 flex flex-col md:flex-row justify-between items-center gap-6 text-sm text-zinc-500">
          <p>{{ $t('footer.rights') }}</p>
          <div class="flex gap-4">
            <a href="https://linkdigital.uz" target="_blank"
              class="w-10 h-10 rounded-full bg-zinc-900 border border-zinc-800 flex items-center justify-center hover:bg-white hover:text-black hover:border-white transition-all duration-300"
              title="LinkDigital">
              <iconify-icon icon="lucide:globe" width="18"></iconify-icon>
            </a>
            <a href="https://www.instagram.com/storely.uz/" target="_blank"
              class="w-10 h-10 rounded-full bg-zinc-900 border border-zinc-800 flex items-center justify-center hover:bg-pink-500 hover:text-white hover:border-pink-500 transition-all duration-300"
              title="Instagram">
              <iconify-icon icon="lucide:instagram" width="18"></iconify-icon>
            </a>
            <a href="https://t.me/storely_uz" target="_blank"
              class="w-10 h-10 rounded-full bg-zinc-900 border border-zinc-800 flex items-center justify-center hover:bg-blue-500 hover:text-white hover:border-blue-500 transition-all duration-300"
              title="Telegram">
              <iconify-icon icon="lucide:send" width="18"></iconify-icon>
            </a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
const route = useRoute()
const localePath = useLocalePath()
const { user, token } = useAuth()
const { formatPrice } = useCurrency()
const { getField } = useMultilingual()
const config = useRuntimeConfig()

const { data: plans, pending: plansPending } = useFetch(config.public.apiBase + '/subscription-plans', {
  server: false,
  transform: (data) => {
    const filteredPlans = data
      ?.filter(plan => plan.is_active)
      ?.sort((a, b) => (a.display_order || 0) - (b.display_order || 0)) || []

    return filteredPlans.map(plan => {
      if (plan.features && !plan.features_list) {
        try {
          plan.features_list = JSON.parse(plan.features)
        } catch (e) {
          plan.features_list = []
        }
      }
      return plan
    })
  }
})

// Fetch active offers from API
const { data: offers } = useFetch(config.public.apiBase + '/offers', {
  server: false
})

// Get user's shops to determine profile link
const { data: myShops } = useFetch(config.public.apiBase + '/platform/shops/me', {
  server: false,
  headers: token.value ? {
    'Authorization': `Bearer ${token.value}`
  } : {},
  watch: [token],
  immediate: false,
  lazy: true
})

const profileLink = computed(() => {
  if (!user.value) return '/login'
  if (user.value.role === 'platform_admin' || user.value.roles?.includes('admin')) return '/platform/admin'
  return '/profile'
})

// Animation states
const heroRevealed = ref(false)
const featuresRevealed = ref(false)
const timelineRevealed = ref(false)
const pricingRevealed = ref(false)
const timelineProgress = ref(0)

// Analytics state for v2 block
const analyticsPeriod = ref('Bugun')
const analyticsData = computed(() => {
  const data = {
    'Bugun': { revenue: 3820100, customers: 2, orders: 8 },
    'Bu hafta': { revenue: 24500000, customers: 14, orders: 42 },
    'Barcha vaqt': { revenue: 852000000, customers: 156, orders: 1240 }
  }
  return data[analyticsPeriod.value]
})

// Order lifecycle steps
const orderSteps = [
  { key: 'pending', count: 2, icon: 'lucide:clock-4', color: 'text-amber-500', bg: 'bg-amber-50' },
  { key: 'processing', count: 0, icon: 'lucide:package', color: 'text-blue-500', bg: 'bg-blue-50' },
  { key: 'shipping', count: 0, icon: 'lucide:truck', color: 'text-indigo-500', bg: 'bg-indigo-50' },
  { key: 'delivered', count: 6, icon: 'lucide:check-circle-2', color: 'text-green-500', bg: 'bg-green-50' },
  { key: 'cancelled', count: 0, icon: 'lucide:x-circle', color: 'text-red-500', bg: 'bg-red-50' }
]

// FAQ State
const activeFaq = ref(null)
const toggleFaq = (idx) => {
  activeFaq.value = activeFaq.value === idx ? null : idx
}

// Refs for DOM elements
const heroDashboard = ref(null)
const timelineLine = ref(null)

// Scroll reveal observer
onMounted(() => {
  // Hero reveal
  heroRevealed.value = true

  // Features reveal
  const featuresObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        featuresRevealed.value = true
      }
    })
  }, { threshold: 0.1 })

  const featuresSection = document.querySelector('#features')
  if (featuresSection) {
    featuresObserver.observe(featuresSection)
  }

  // Timeline reveal
  const timelineObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        timelineRevealed.value = true
      }
    })
  }, { threshold: 0.1 })

  const timelineSection = document.querySelector('#solutions')
  if (timelineSection) {
    timelineObserver.observe(timelineSection)
  }

  // Pricing reveal
  const pricingObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        pricingRevealed.value = true
      }
    })
  }, { threshold: 0.1 })

  const pricingSection = document.querySelector('#pricing')
  if (pricingSection) {
    pricingObserver.observe(pricingSection)
  }

  // Hero Dashboard 3D Tilt Effect on Scroll
  const handleScroll = () => {
    const scrollY = window.scrollY
    if (window.innerWidth > 768 && scrollY < 800 && heroDashboard.value) {
      const rotation = Math.min(scrollY * 0.05, 10)
      const translate = scrollY * 0.1
      heroDashboard.value.style.transform = `perspective(1000px) rotateX(${rotation}deg) translateY(${translate}px)`
    }

    // Timeline Progress Bar
    const timelineSectionEl = document.querySelector('#solutions')
    if (timelineSectionEl && timelineLine.value) {
      const rect = timelineSectionEl.getBoundingClientRect()
      const windowHeight = window.innerHeight

      if (rect.top < windowHeight / 2 && rect.bottom > windowHeight / 2) {
        const totalHeight = rect.height
        let progress = ((windowHeight / 2 - rect.top) / totalHeight) * 100
        progress = Math.min(Math.max(progress, 0), 100)
        timelineProgress.value = progress
      } else if (rect.top > windowHeight / 2) {
        timelineProgress.value = 0
      } else {
        timelineProgress.value = 100
      }
    }
  }

  window.addEventListener('scroll', handleScroll)
  handleScroll() // Initial call

  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
  })
})
</script>

<style scoped>
body {
  font-family: 'Inter', sans-serif;
  background-color: #ffffff;
  color: #09090b;
}

/* Hide scrollbar for clean UI */
:global(::-webkit-scrollbar) {
  width: 8px;
}

:global(::-webkit-scrollbar-track) {
  background: #ffffff;
}

:global(::-webkit-scrollbar-thumb) {
  background: #e4e4e7;
  border-radius: 4px;
}

:global(::-webkit-scrollbar-thumb:hover) {
  background: #a1a1aa;
}

/* Scroll Reveal Utility Classes */
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

.reveal.active {
  opacity: 1;
  transform: translateY(0);
}

/* Glassmorphism */
.glass {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(228, 228, 231, 0.6);
}

/* Gradient Text */
.text-gradient {
  background: linear-gradient(to bottom right, #18181b 0%, #52525b 100%);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* 3D Perspective Container */
.perspective-container {
  perspective: 2000px;
}

/* Glow effects */
.glow-hover:hover {
  box-shadow: 0 0 40px -10px rgba(0, 0, 0, 0.1);
}

/* Loading Spinner */
.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #111;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

.offer-title {
  display: flex;
  flex-direction: column;
}

@media (max-width:600px) {
  .registr-shop-btn {
    font-size: 12px;
  }
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.perspective-1000 {
  perspective: 1000px;
}

@keyframes pulse-slow {

  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }

  50% {
    opacity: 0.8;
    transform: scale(0.98);
  }
}

.animate-pulse-slow {
  animation: pulse-slow 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
