<template>
    <div class="min-h-screen bg-zinc-50">
        <LandingHeader />

        <!-- Hero -->
        <section class="pt-32 pb-20 overflow-hidden bg-white">
            <div class="max-w-7xl mx-auto px-6">
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
                    <div class="reveal active">
                        <h1 class="text-5xl md:text-7xl font-bold tracking-tight text-zinc-900 mb-8 leading-[1.1]">
                            {{ $t('integrations.hero.title') }}
                        </h1>
                        <p class="text-xl text-zinc-500 leading-relaxed mb-10">
                            {{ $t('integrations.hero.subtitle') }}
                        </p>
                        <div class="flex gap-4">
                            <NuxtLink :to="localePath('/register-shop')"
                                class="px-8 py-4 bg-black text-white rounded-full font-bold hover:bg-zinc-800 transition-all hover-lift">
                                {{ $t('integrations.hero.cta') }}
                            </NuxtLink>
                        </div>
                    </div>

                    <div class="relative reveal active">
                        <!-- Animated Integration Web -->
                        <div class="w-full aspect-square relative">
                            <div
                                class="absolute inset-0 bg-gradient-to-tr from-zinc-100 to-transparent rounded-full border border-zinc-100 animate-pulse-slow">
                            </div>
                            <!-- Central Logo -->
                            <div
                                class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-24 h-24 bg-white rounded-3xl shadow-2xl flex items-center justify-center z-20 border border-zinc-100">
                                <img src="/img/logo.jpg" class="w-16 h-auto" />
                            </div>

                            <!-- Orbiting Icons -->
                            <div v-for="(icon, i) in orbitingIcons" :key="i"
                                class="absolute w-16 h-16 bg-white rounded-2xl shadow-xl border border-zinc-100 flex items-center justify-center text-zinc-900 transition-all duration-700 hover:scale-110 cursor-pointer z-10"
                                :style="getOrbitStyle(i)">
                                <iconify-icon :icon="icon" width="32"></iconify-icon>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Categories -->
        <section v-for="category in categories" :key="category.id" class="py-24 border-t border-zinc-100">
            <div class="max-w-7xl mx-auto px-6">
                <div class="mb-16">
                    <h2 class="text-3xl font-bold mb-4">{{ $t(`integrations.categories.${category.id}.title`) }}</h2>
                    <p class="text-zinc-500">{{ $t(`integrations.categories.${category.id}.subtitle`) }}</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    <div v-for="tool in category.tools" :key="tool.name"
                        class="p-6 bg-white rounded-2xl border border-zinc-200 hover:border-black transition-all group reveal active">
                        <div class="w-12 h-12 mb-6 grayscale group-hover:grayscale-0 transition-all duration-500">
                            <iconify-icon :icon="tool.icon" width="48" :style="{ color: tool.color }"></iconify-icon>
                        </div>
                        <h4 class="text-lg font-bold mb-2">{{ tool.name }}</h4>
                        <p class="text-sm text-zinc-500 mb-4">{{ tool.desc }}</p>
                        <div
                            class="inline-flex items-center gap-1 text-xs font-bold text-zinc-400 group-hover:text-black transition-colors uppercase tracking-widest">
                            {{ $t('integrations.active') }}
                            <iconify-icon icon="lucide:check-circle" width="14"></iconify-icon>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <AppFooter />
    </div>
</template>

<script setup>
const localePath = useLocalePath()

const orbitingIcons = [
    'logos:telegram',
    'logos:google-analytics',
    'logos:facebook',
    'logos:whatsapp-icon',
    'simple-icons:payme'
]

const categories = [
    {
        id: 'payments',
        tools: [
            { name: 'Payme', icon: 'simple-icons:payme', color: '#00BAE0', desc: 'Sotuvlarni avtomatlashtiring' },
            { name: 'Click', icon: 'mingcute:card-pay-fill', color: '#007DFE', desc: 'Eng mashhur to\'lov tizimi' },
            { name: 'Uzum Bank', icon: 'lucide:credit-card', color: '#7E33FF', desc: 'Zamonaviy fintex yechim' },
            { name: 'Cash', icon: 'lucide:banknote', color: '#10B981', desc: 'Naqd pul bilan ishlash' }
        ]
    },
    {
        id: 'marketing',
        tools: [
            { name: 'Facebook Pixel', icon: 'logos:facebook', color: '#1877F2', desc: 'Reklama samaradorligi' },
            { name: 'Google Analytics', icon: 'logos:google-analytics', color: '#E37400', desc: 'Trafik tahlili' },
            { name: 'JivoChat', icon: 'lucide:message-square', color: '#25C960', desc: 'Jonli muloqot' }
        ]
    }
]

const getOrbitStyle = (i) => {
    const angle = (i * 72) * (Math.PI / 180)
    const radius = 200
    const x = Math.cos(angle) * radius
    const y = Math.sin(angle) * radius
    return {
        left: `calc(50% + ${x}px)`,
        top: `calc(50% + ${y}px)`,
        transform: 'translate(-50%, -50%)'
    }
}
</script>

<style scoped>
@keyframes pulse-slow {

    0%,
    100% {
        transform: scale(1);
        opacity: 0.3;
    }

    50% {
        transform: scale(1.1);
        opacity: 0.5;
    }
}

.animate-pulse-slow {
    animation: pulse-slow 8s ease-in-out infinite;
}

.reveal {
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.6s cubic-bezier(0.2, 1, 0.2, 1);
}

.reveal.active {
    opacity: 1;
    transform: translateY(0);
}

.hover-lift:hover {
    transform: translateY(-2px);
}
</style>
