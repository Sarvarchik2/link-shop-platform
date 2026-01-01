<template>
  <div class="antialiased selection:bg-zinc-900 selection:text-white">
    <nav class="fixed top-0 w-full z-50 glass border-b border-zinc-100/50 transition-all duration-300">
      <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <div class="flex items-center gap-8">
          <NuxtLink to="/" class="text-lg font-semibold tracking-tight flex items-center gap-2">
            <div class="w-5 h-5 bg-black rounded-md flex items-center justify-center text-white">
              <iconify-icon icon="lucide:box" width="12"></iconify-icon>
            </div>
            LinkShop
          </NuxtLink>
          <div class="hidden md:flex items-center gap-6 text-sm font-medium text-zinc-500">
            <a href="#features" class="hover:text-black transition-colors">Функции</a>
            <a href="#solutions" class="hover:text-black transition-colors">Решения</a>
            <a href="#pricing" class="hover:text-black transition-colors">Цены</a>
            <a href="#clients" class="hover:text-black transition-colors">Клиенты</a>
          </div>
        </div>
        <div class="flex items-center gap-4">
          <NuxtLink v-if="!user" to="/login"
            class="text-sm font-medium text-zinc-500 hover:text-black transition-colors">Войти</NuxtLink>
          <NuxtLink v-else :to="profileLink"
            class="text-sm font-medium text-zinc-500 hover:text-black transition-colors">Профиль</NuxtLink>
          <NuxtLink to="/register-shop"
            class="bg-black text-white px-4 py-2 rounded-full text-sm font-medium hover:bg-zinc-800 transition-all shadow-lg shadow-zinc-200/50">
            Создать магазин
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
            LinkShop 2.0 уже доступен
          </div> -->

          <h1 class="text-5xl md:text-7xl font-semibold tracking-tight text-zinc-900 mb-8 leading-[1.1]">
            Ваш магазин. Мгновенно. <br>
            <span class="text-zinc-400">Профессионально.</span>
          </h1>

          <p class="text-lg md:text-xl text-zinc-500 max-w-2xl mx-auto mb-10 leading-relaxed font-normal">
            Единая платформа для управления продажами, складом и аналитикой. Замените Excel таблицы и рутину на
            интеллектуальную автоматизацию Commerce OS.
          </p>

          <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-20">
            <NuxtLink to="/register-shop"
              class="w-full sm:w-auto px-8 py-3.5 bg-black text-white rounded-full font-medium shadow-xl shadow-zinc-900/10 hover:shadow-2xl hover:bg-zinc-800 transition-all flex items-center justify-center gap-2 group">
              Начать бесплатно
              <iconify-icon icon="lucide:arrow-right"
                class="group-hover:translate-x-1 transition-transform"></iconify-icon>
            </NuxtLink>
            <button
              class="w-full sm:w-auto px-8 py-3.5 bg-white border border-zinc-200 text-zinc-700 rounded-full font-medium hover:bg-zinc-50 hover:border-zinc-300 transition-all flex items-center justify-center gap-2">
              <iconify-icon icon="lucide:play-circle" width="18"></iconify-icon>
              Демо видео
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
              linkshop.uz/dashboard
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
                  <div class="text-2xl font-semibold text-zinc-900">$12,402</div>
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
      </div>
    </section>



    <section id="features" class="py-32 bg-zinc-50/50">
      <div class="max-w-7xl mx-auto px-6">
        <div class="mb-20 max-w-2xl reveal" :class="{ active: featuresRevealed }">
          <h2 class="text-3xl md:text-5xl font-semibold tracking-tight text-zinc-900 mb-6">Всё, что нужно для
            роста. <br>В одной системе.</h2>
          <p class="text-lg text-zinc-500">Наш набор инструментов покрывает каждый аспект современной электронной
            коммерции.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 auto-rows-[minmax(300px,auto)]">
          <div
            class="md:col-span-2 bg-white rounded-2xl border border-zinc-200/80 p-8 shadow-sm hover:shadow-xl transition-all duration-300 group overflow-hidden relative reveal"
            :class="{ active: featuresRevealed }">
            <div class="relative z-10">
              <div class="w-10 h-10 rounded-lg bg-zinc-100 flex items-center justify-center mb-6 text-zinc-700">
                <iconify-icon icon="lucide:layers" width="20"></iconify-icon>
              </div>
              <h3 class="text-xl font-semibold mb-2">Умный склад</h3>
              <p class="text-zinc-500 text-sm max-w-sm">Отслеживание остатков в реальном времени.
                Автоматические уведомления о низком запасе.</p>
            </div>

            <div
              class="absolute right-0 bottom-0 w-3/4 md:w-1/2 h-4/5 bg-zinc-50 border-t border-l border-zinc-200 rounded-tl-2xl p-6 shadow-inner group-hover:scale-[1.02] transition-transform duration-500 origin-bottom-right">
              <table class="w-full text-xs text-left">
                <thead class="text-zinc-400 border-b border-zinc-200">
                  <tr>
                    <th class="pb-2 font-medium">SKU</th>
                    <th class="pb-2 font-medium">Товар</th>
                    <th class="pb-2 font-medium">Stock</th>
                    <th class="pb-2 font-medium text-right">Status</th>
                  </tr>
                </thead>
                <tbody class="text-zinc-700">
                  <tr class="border-b border-zinc-100">
                    <td class="py-3 font-mono text-[10px] text-zinc-400">#8021</td>
                    <td class="py-3 font-medium">Cotton Tee</td>
                    <td class="py-3">124</td>
                    <td class="py-3 text-right">
                      <span class="bg-green-100 text-green-700 px-2 py-0.5 rounded-full text-[10px]">OK</span>
                    </td>
                  </tr>
                  <tr class="border-b border-zinc-100">
                    <td class="py-3 font-mono text-[10px] text-zinc-400">#8022</td>
                    <td class="py-3 font-medium">Linen Pants</td>
                    <td class="py-3">12</td>
                    <td class="py-3 text-right">
                      <span class="bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded-full text-[10px]">Low</span>
                    </td>
                  </tr>
                  <tr>
                    <td class="py-3 font-mono text-[10px] text-zinc-400">#8023</td>
                    <td class="py-3 font-medium">Wool Hat</td>
                    <td class="py-3">0</td>
                    <td class="py-3 text-right">
                      <span class="bg-red-100 text-red-700 px-2 py-0.5 rounded-full text-[10px]">Out</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <div
            class="md:col-span-1 bg-white rounded-2xl border border-zinc-200/80 p-8 shadow-sm hover:shadow-xl transition-all duration-300 group overflow-hidden relative reveal"
            :class="{ active: featuresRevealed }">
            <div class="relative z-10">
              <div class="w-10 h-10 rounded-lg bg-zinc-100 flex items-center justify-center mb-6 text-zinc-700">
                <iconify-icon icon="lucide:bar-chart-2" width="20"></iconify-icon>
              </div>
              <h3 class="text-xl font-semibold mb-2">Аналитика</h3>
              <p class="text-zinc-500 text-sm">Глубокие инсайты.</p>
            </div>

            <div class="absolute bottom-6 left-6 right-6 h-32 group-hover:scale-105 transition-transform duration-500">
              <svg class="w-full h-full overflow-visible" viewBox="0 0 100 50" preserveAspectRatio="none">
                <path d="M0,50 L20,35 L40,42 L60,15 L80,25 L100,5" fill="none" stroke="black" stroke-width="1.5"
                  class="animate-draw" />
                <circle cx="100" cy="5" r="3" fill="white" stroke="black" stroke-width="1.5" />
              </svg>
            </div>
          </div>

          <div
            class="md:col-span-1 bg-zinc-900 text-white rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 group overflow-hidden relative reveal"
            :class="{ active: featuresRevealed }">
            <div class="relative z-10">
              <div
                class="w-10 h-10 rounded-lg bg-zinc-800 flex items-center justify-center mb-6 text-white border border-zinc-700">
                <iconify-icon icon="lucide:zap" width="20"></iconify-icon>
              </div>
              <h3 class="text-xl font-semibold mb-2">Скорость</h3>
              <p class="text-zinc-400 text-sm">Оптимизирован для молниеносной загрузки.</p>
            </div>
            <div
              class="absolute bottom-4 right-4 text-6xl font-bold text-zinc-800 select-none opacity-20 group-hover:opacity-40 transition-opacity">
              99
            </div>
          </div>

          <!-- Card 4: Sync -->
          <div
            class="md:col-span-2 bg-white rounded-2xl border border-zinc-200/80 p-8 shadow-sm hover:shadow-xl transition-all duration-300 group overflow-hidden relative flex items-center justify-between reveal"
            :class="{ active: featuresRevealed }">
            <div class="relative z-10 max-w-xs">
              <div class="w-10 h-10 rounded-lg bg-zinc-100 flex items-center justify-center mb-6 text-zinc-700">
                <iconify-icon icon="lucide:refresh-ccw" width="20"></iconify-icon>
              </div>
              <h3 class="text-xl font-semibold mb-2">Авто-Синхронизация</h3>
              <p class="text-zinc-500 text-sm">Изменения на складе мгновенно отражаются в витрине. Никаких
                задержек.</p>
            </div>

            <!-- Visual: Sync Animation -->
            <div class="hidden md:flex items-center gap-8 pr-12 opacity-80 group-hover:opacity-100 transition-opacity">
              <div
                class="w-24 h-32 bg-zinc-50 border border-zinc-200 rounded-lg flex flex-col items-center justify-center shadow-sm">
                <iconify-icon icon="lucide:store" width="32" class="text-zinc-400 mb-2"></iconify-icon>
                <span class="text-[10px] font-mono text-zinc-400 uppercase">Storefront</span>
              </div>

              <div class="flex flex-col items-center gap-2 text-zinc-300">
                <iconify-icon icon="lucide:arrow-right" width="24"
                  class="group-hover:translate-x-2 transition-transform duration-500"></iconify-icon>
                <iconify-icon icon="lucide:arrow-left" width="24"
                  class="group-hover:-translate-x-2 transition-transform duration-500 delay-75"></iconify-icon>
              </div>

              <div
                class="w-24 h-32 bg-zinc-900 border border-zinc-800 rounded-lg flex flex-col items-center justify-center shadow-lg">
                <iconify-icon icon="lucide:database" width="32" class="text-zinc-500 mb-2"></iconify-icon>
                <span class="text-[10px] font-mono text-zinc-500 uppercase">Admin</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section id="solutions" class="py-32 bg-white relative">
      <div class="max-w-4xl mx-auto px-6">
        <h2 class="text-center text-3xl md:text-5xl font-semibold tracking-tight text-zinc-900 mb-24 reveal"
          :class="{ active: timelineRevealed }">Путь к
          продажам</h2>

        <div class="relative">
          <div class="absolute left-8 md:left-1/2 top-0 bottom-0 w-px bg-zinc-100 -translate-x-1/2"></div>
          <div ref="timelineLine"
            class="absolute left-8 md:left-1/2 top-0 w-px bg-black -translate-x-1/2 transition-all duration-300"
            :style="{ height: timelineProgress + '%' }"></div>

          <div class="relative flex flex-col md:flex-row items-center  md:gap-24 mb-32 group reveal"
            :class="{ active: timelineRevealed }">
            <div class="md:w-1/2 text-left md:text-right order-2 md:order-1">
              <h3 class="text-2xl font-semibold mb-2">Создайте аккаунт</h3>
              <p class="text-zinc-500">Зарегистрируйтесь за 30 секунд. Кредитная карта не требуется.</p>
            </div>
            <div
              class="absolute left-8 md:left-1/2 -translate-x-1/2 w-16 h-16 bg-white border border-zinc-200 rounded-full flex items-center justify-center z-10 shadow-lg group-hover:scale-110 transition-transform duration-300 order-1 md:order-2">
              <iconify-icon icon="lucide:user" width="24"></iconify-icon>
            </div>
            <div class="md:w-1/2 order-3 pl-16 md:pl-0"></div>
          </div>

          <div class="relative flex flex-col md:flex-row items-center  md:gap-24 mb-32 group reveal"
            :class="{ active: timelineRevealed }">
            <div class="md:w-1/2 order-2 md:order-1"></div>
            <div
              class="absolute left-8 md:left-1/2 -translate-x-1/2 w-16 h-16 bg-white border border-zinc-200 rounded-full flex items-center justify-center z-10 shadow-lg group-hover:scale-110 transition-transform duration-300 order-1 md:order-2">
              <iconify-icon icon="lucide:upload-cloud" width="24"></iconify-icon>
            </div>
            <div class="md:w-1/2 text-left order-2 md:order-3">
              <h3 class="text-2xl font-semibold mb-2">Загрузите товары</h3>
              <p class="text-zinc-500">Импортируйте через Excel или добавьте вручную. Загрузите фото.</p>
            </div>
          </div>

          <div class="relative flex flex-col md:flex-row items-center  md:gap-24 group reveal"
            :class="{ active: timelineRevealed }">
            <div class="md:w-1/2 text-left md:text-right order-2 md:order-1">
              <h3 class="text-2xl font-semibold mb-2">Начните продавать</h3>
              <p class="text-zinc-500">Опубликуйте магазин и принимайте первые заказы мгновенно.</p>
            </div>
            <div
              class="absolute left-8 md:left-1/2 -translate-x-1/2 w-16 h-16 bg-black text-white border border-black rounded-full flex items-center justify-center z-10 shadow-lg group-hover:scale-110 transition-transform duration-300 order-1 md:order-2">
              <iconify-icon icon="lucide:rocket" width="24"></iconify-icon>
            </div>
            <div class="md:w-1/2 order-3 pl-16 md:pl-0"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Section -->
    <section id="pricing" class="py-32 bg-zinc-50 border-t border-zinc-200">
      <div class="max-w-7xl mx-auto px-6">
        <h2 class="text-3xl md:text-5xl font-semibold tracking-tight text-center mb-6 reveal"
          :class="{ active: pricingRevealed }">Тарифные планы</h2>
        <p class="text-center text-zinc-500 mb-20 reveal" :class="{ active: pricingRevealed }">Прозрачное
          ценообразование. Без скрытых комиссий.</p>

        <div v-if="plansPending" class="text-center py-12">
          <div class="loading-spinner"></div>
          <p class="mt-4 text-zinc-400">Загрузка тарифов...</p>
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
              <span v-if="plan.price === 0 || plan.is_trial">$0</span>
              <span v-else>${{ plan.price }}</span>
              <span class="text-base font-normal text-zinc-500">/мес</span>
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
                  <strong>{{ plan.max_products === null ? 'Неограниченно' : plan.max_products }}</strong> товаров
                </span>
              </div>
            </div>

            <NuxtLink :to="plan.slug === 'business' ? '/register-shop?plan=business' : '/register-shop'"
              class="w-full py-3 rounded-lg text-sm font-semibold transition-colors block text-center" :class="plan.slug === 'basic' || index === Math.floor(plans.length / 2)
                ? 'bg-black text-white hover:bg-zinc-800 shadow-lg'
                : 'border border-zinc-200 hover:border-black hover:bg-zinc-50'">
              <span v-if="plan.slug === 'business'">Связаться с нами</span>
              <span v-else>Выбрать {{ plan.name }}</span>
            </NuxtLink>
          </div>
        </div>

        <div v-else class="text-center py-12 text-zinc-400">
          <p>Тарифные планы временно недоступны</p>
        </div>

        <!-- Offers Section -->
        <div v-if="offers && offers.length > 0" class="mt-20">
          <h2 class="text-2xl md:text-4xl font-semibold tracking-tight text-center mb-6">Специальные предложения</h2>
          <p class="text-center text-zinc-500 mb-12">Дополнительные услуги и решения</p>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="offer in offers" :key="offer.id"
              class="bg-white rounded-2xl p-8 border-2 border-zinc-900 shadow-lg hover:shadow-xl transition-all">
              <div class="flex justify-between items-start mb-4">
                <h3 class="text-xl font-semibold">{{ offer.title }}</h3>
                <div v-if="offer.price || offer.price_text" class="text-right">
                  <div v-if="offer.price" class="text-2xl font-bold">${{ offer.price.toFixed(2) }}</div>
                  <div v-else class="text-sm font-medium text-zinc-600">{{ offer.price_text }}</div>
                </div>
              </div>
              <p class="text-sm text-zinc-600 mb-6">{{ offer.description }}</p>
              <div class="pt-6 border-t border-zinc-200">
                <p class="text-xs text-zinc-500 mb-4">{{ offer.contact_text }}</p>
                <div class="flex gap-3">
                  <a v-if="offer.contact_email" :href="`mailto:${offer.contact_email}`"
                    class="flex-1 py-2.5 px-4 bg-zinc-100 hover:bg-zinc-900 hover:text-white rounded-lg text-sm font-semibold transition-colors text-center">
                    Email
                  </a>
                  <a v-if="offer.contact_phone" :href="`tel:${offer.contact_phone}`"
                    class="flex-1 py-2.5 px-4 bg-zinc-100 hover:bg-zinc-900 hover:text-white rounded-lg text-sm font-semibold transition-colors text-center">
                    Телефон
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-white border-t border-zinc-200 pt-20 pb-12">
      <div class="max-w-7xl mx-auto px-6">
        <div class="grid grid-cols-2 md:grid-cols-5 gap-12 mb-20">
          <div class="col-span-2">
            <NuxtLink to="/" class="text-xl font-bold tracking-tight flex items-center gap-2 mb-6">
              <div class="w-6 h-6 bg-black rounded-md flex items-center justify-center text-white">
                <iconify-icon icon="lucide:box" width="14"></iconify-icon>
              </div>
              LinkShop
            </NuxtLink>
            <p class="text-zinc-500 text-sm max-w-xs leading-relaxed">
              Операционная система для современной торговли. Создаем инструменты, которые помогают
              предпринимателям расти быстрее.
            </p>
          </div>
          <div>
            <h4 class="font-semibold mb-6 text-sm">Продукт</h4>
            <ul class="space-y-4 text-sm text-zinc-500">
              <li><a href="#features" class="hover:text-black transition-colors">Функции</a></li>
              <li><a href="#solutions" class="hover:text-black transition-colors">Интеграции</a></li>
              <li><a href="#" class="hover:text-black transition-colors">Шаблоны</a></li>
              <li><a href="#" class="hover:text-black transition-colors">Roadmap</a></li>
            </ul>
          </div>
          <div>
            <h4 class="font-semibold mb-6 text-sm">Компания</h4>
            <ul class="space-y-4 text-sm text-zinc-500">
              <li><a href="#" class="hover:text-black transition-colors">О нас</a></li>
              <li><a href="#" class="hover:text-black transition-colors">Карьера</a></li>
              <li><a href="#" class="hover:text-black transition-colors">Блог</a></li>
              <li><a href="#" class="hover:text-black transition-colors">Бренд</a></li>
            </ul>
          </div>
          <div>
            <h4 class="font-semibold mb-6 text-sm">Legal</h4>
            <ul class="space-y-4 text-sm text-zinc-500">
              <li><a href="#" class="hover:text-black transition-colors">Privacy</a></li>
              <li><a href="#" class="hover:text-black transition-colors">Terms</a></li>
              <li><a href="#" class="hover:text-black transition-colors">Cookie Policy</a></li>
            </ul>
          </div>
        </div>

        <div
          class="flex flex-col md:flex-row justify-between items-center pt-8 border-t border-zinc-100 text-sm text-zinc-400">
          <p>&copy; 2024 LinkShop Technologies Inc. All rights reserved.</p>
          <div class="flex gap-6 mt-4 md:mt-0">
            <a href="#" class="hover:text-black transition-colors">
              <iconify-icon icon="lucide:twitter" width="20"></iconify-icon>
            </a>
            <a href="#" class="hover:text-black transition-colors">
              <iconify-icon icon="lucide:github" width="20"></iconify-icon>
            </a>
            <a href="#" class="hover:text-black transition-colors">
              <iconify-icon icon="lucide:linkedin" width="20"></iconify-icon>
            </a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
const { user, token } = useAuth()

// Fetch subscription plans from API
const { data: plans, pending: plansPending } = await useFetch('http://localhost:8000/subscription-plans', {
  server: false,
  transform: (data) => {
    // Sort by display_order and filter active plans
    const filteredPlans = data
      ?.filter(plan => plan.is_active)
      ?.sort((a, b) => (a.display_order || 0) - (b.display_order || 0)) || []

    // Ensure features_list is parsed if features exists
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
const { data: offers } = await useFetch('http://localhost:8000/offers', {
  server: false
})

// Get user's shops to determine profile link
const { data: myShops } = await useFetch('http://localhost:8000/platform/shops/me', {
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
  if (user.value.role === 'platform_admin') return '/platform/admin'
  if (myShops.value && myShops.value.length > 0) return '/profile'
  return '/profile'
})

// Animation states
const heroRevealed = ref(false)
const featuresRevealed = ref(false)
const timelineRevealed = ref(false)
const pricingRevealed = ref(false)
const timelineProgress = ref(0)

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

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>
