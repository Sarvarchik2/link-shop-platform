<template>
    <div class="min-h-screen bg-white">
        <LandingHeader />

        <!-- Hero Section -->
        <section class="relative pt-32 pb-20 overflow-hidden">
            <div
                class="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[600px] bg-gradient-to-b from-zinc-100/50 to-transparent rounded-[100%] blur-3xl -z-10 opacity-60">
            </div>

            <div class="max-w-7xl mx-auto px-6 text-center relative z-10">
                <div class="reveal active">
                    <h1 class="text-5xl md:text-7xl font-bold tracking-tight text-zinc-900 mb-8 leading-[1.1]">
                        {{ $t('features_page.hero.title') }}
                    </h1>
                    <p class="text-xl text-zinc-500 max-w-3xl mx-auto mb-12 leading-relaxed">
                        {{ $t('features_page.hero.subtitle') }}
                    </p>
                </div>

                <!-- Abstract Feature Visualization -->
                <div
                    class="relative mx-auto max-w-5xl aspect-[21/9] bg-zinc-900 rounded-3xl overflow-hidden shadow-2xl reveal active border border-white/10 group">
                    <div
                        class="absolute inset-0 bg-gradient-to-tr from-blue-500/10 via-transparent to-pink-500/10 opacity-50">
                    </div>

                    <div class="absolute inset-0 flex items-center justify-center">
                        <div class="grid grid-cols-3 gap-8 w-full px-12">
                            <div v-for="i in 3" :key="i"
                                class="h-40 bg-white/5 rounded-2xl border border-white/10 backdrop-blur-sm p-6 transform transition-all duration-500 group-hover:scale-105 group-hover:-translate-y-2"
                                :style="{ transitionDelay: (i * 100) + 'ms' }">
                                <div class="w-10 h-10 rounded-lg bg-white/10 mb-4 animate-pulse"></div>
                                <div class="h-4 w-3/4 bg-white/10 rounded mb-2"></div>
                                <div class="h-3 w-1/2 bg-white/5 rounded"></div>
                            </div>
                        </div>
                    </div>

                    <div class="absolute bottom-8 left-1/2 -translate-x-1/2 flex gap-4">
                        <div
                            class="px-4 py-2 rounded-full bg-white/10 border border-white/20 text-white text-xs font-medium backdrop-blur-md">
                            Cloud Architecture</div>
                        <div
                            class="px-4 py-2 rounded-full bg-white/10 border border-white/20 text-white text-xs font-medium backdrop-blur-md">
                            Real-time Sync</div>
                        <div
                            class="px-4 py-2 rounded-full bg-white/10 border border-white/20 text-white text-xs font-medium backdrop-blur-md">
                            API Enabled</div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Main Features Grid -->
        <section class="py-32">
            <div class="max-w-7xl mx-auto px-6">
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    <div v-for="feature in features" :key="feature.titleKey"
                        class="group p-8 rounded-3xl border border-zinc-100 bg-zinc-50/50 hover:bg-white hover:shadow-2xl hover:shadow-zinc-200/50 transition-all duration-500 reveal active">
                        <div
                            class="w-14 h-14 rounded-2xl bg-white shadow-sm flex items-center justify-center text-zinc-900 mb-8 border border-zinc-100 group-hover:scale-110 transition-transform duration-500">
                            <iconify-icon :icon="feature.icon" width="28"></iconify-icon>
                        </div>
                        <h3 class="text-2xl font-bold mb-4 text-zinc-900">{{
                            $t(`features_page.items.${feature.titleKey}.title`) }}</h3>
                        <p class="text-zinc-500 leading-relaxed mb-6">{{
                            $t(`features_page.items.${feature.titleKey}.desc`) }}</p>

                        <ul class="space-y-3">
                            <li v-for="point in 3" :key="point" class="flex items-center gap-2 text-sm text-zinc-600">
                                <div class="w-1.5 h-1.5 rounded-full bg-zinc-300"></div>
                                {{ $t(`features_page.items.${feature.titleKey}.points.${point}`) }}
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- Detailed Section: Telegram Web App -->
        <section class="py-32 bg-zinc-950 text-white overflow-hidden relative">
            <div class="absolute -right-64 top-0 w-[800px] h-[800px] bg-blue-500/10 blur-[120px] rounded-full"></div>

            <div class="max-w-7xl mx-auto px-6 relative z-10">
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
                    <div>
                        <div
                            class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-bold mb-8 uppercase tracking-widest">
                            Killer Feature
                        </div>
                        <h2 class="text-4xl md:text-6xl font-bold mb-8 tracking-tight leading-[1.1]">
                            {{ $t('features_page.telegram.title') }}
                        </h2>
                        <p class="text-xl text-zinc-400 mb-12 leading-relaxed">
                            {{ $t('features_page.telegram.subtitle') }}
                        </p>

                        <div class="space-y-6">
                            <div v-for="i in 3" :key="i"
                                class="flex gap-6 p-6 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/10 transition-colors">
                                <div
                                    class="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center text-blue-400 flex-shrink-0">
                                    <iconify-icon :icon="['lucide:zap', 'lucide:layout', 'lucide:message-square'][i - 1]"
                                        width="24"></iconify-icon>
                                </div>
                                <div>
                                    <h4 class="text-lg font-bold mb-2">{{
                                        $t(`features_page.telegram.features.${i}.title`) }}</h4>
                                    <p class="text-sm text-zinc-400">{{ $t(`features_page.telegram.features.${i}.desc`)
                                        }}</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="relative flex items-center justify-center">
                        <div
                            class="w-[300px] md:w-[400px] aspect-[1/2] bg-zinc-800 rounded-[60px] border-[12px] border-zinc-700 shadow-2xl relative overflow-hidden transform lg:rotate-6 hover:rotate-0 transition-transform duration-700 select-none">
                            <div class="absolute inset-0 bg-white">
                                <div class="h-16 bg-[#517da2] flex items-center px-6 gap-4">
                                    <div class="w-10 h-10 rounded-full bg-white/20"></div>
                                    <div class="h-3 w-32 bg-white/40 rounded"></div>
                                </div>
                                <div class="p-6">
                                    <div class="w-full aspect-[16/9] bg-zinc-100 rounded-xl mb-6"></div>
                                    <div class="h-4 w-3/4 bg-zinc-100 rounded mb-4"></div>
                                    <div class="h-4 w-1/2 bg-zinc-100 rounded mb-8"></div>
                                    <div
                                        class="h-12 w-full bg-[#2481cc] rounded-xl flex items-center justify-center text-white font-bold text-sm shadow-lg shadow-blue-500/20">
                                        Open Shop
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Floating Data Points -->
                        <div
                            class="absolute -left-10 top-1/4 p-4 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20 animate-float">
                            <div class="text-2xl font-bold text-white">95%</div>
                            <div class="text-[10px] text-zinc-400 uppercase tracking-widest">Conversion Rate</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- CTA Section -->
        <section class="py-32">
            <div class="max-w-4xl mx-auto px-6 text-center">
                <h2 class="text-4xl font-bold mb-8">{{ $t('features_page.cta.title') }}</h2>
                <NuxtLink :to="localePath('/register-shop')"
                    class="inline-flex items-center gap-2 px-10 py-5 bg-black text-white rounded-full font-bold text-lg hover:bg-zinc-800 transition-all hover-lift shadow-xl shadow-zinc-200">
                    {{ $t('features_page.cta.button') }}
                    <iconify-icon icon="lucide:arrow-right"></iconify-icon>
                </NuxtLink>
            </div>
        </section>

        <AppFooter />
    </div>
</template>

<script setup>
const localePath = useLocalePath()

const features = [
    { titleKey: 'catalog', icon: 'lucide:grid' },
    { titleKey: 'orders', icon: 'lucide:shopping-bag' },
    { titleKey: 'analytics', icon: 'lucide:bar-chart-2' },
    { titleKey: 'marketing', icon: 'lucide:megaphone' },
    { titleKey: 'inventory', icon: 'lucide:package' },
    { titleKey: 'teams', icon: 'lucide:users' }
]

onMounted(() => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active')
            }
        })
    }, { threshold: 0.1 })

    document.querySelectorAll('.reveal').forEach(el => observer.observe(el))
})
</script>

<style scoped>
.reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.reveal.active {
    opacity: 1;
    transform: translateY(0);
}

.animate-float {
    animation: float 6s ease-in-out infinite;
}

@keyframes float {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-20px);
    }
}

.hover-lift:hover {
    transform: translateY(-4px);
}
</style>
