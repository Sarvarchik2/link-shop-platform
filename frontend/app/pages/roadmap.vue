<template>
    <div class="min-h-screen bg-white">
        <LandingHeader />

        <!-- Hero -->
        <section class="pt-32 pb-20 relative overflow-hidden">
            <div class="absolute top-0 right-0 w-1/2 h-full bg-zinc-50 -z-10 skew-x-[-12deg] translate-x-32"></div>

            <div class="max-w-7xl mx-auto px-6">
                <div class="max-w-2xl reveal active">
                    <div
                        class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-zinc-100 border border-zinc-200 text-xs font-bold text-zinc-500 mb-8 uppercase tracking-widest">
                        Our Path
                    </div>
                    <h1 class="text-5xl md:text-7xl font-bold tracking-tight text-zinc-900 mb-8">
                        {{ $t('roadmap.hero.title') }}
                    </h1>
                    <p class="text-xl text-zinc-500 leading-relaxed mb-10">
                        {{ $t('roadmap.hero.subtitle') }}
                    </p>
                </div>
            </div>
        </section>

        <!-- Timeline -->
        <section class="py-24">
            <div class="max-w-5xl mx-auto px-6 relative">
                <!-- Central Line -->
                <div class="absolute left-1/2 top-0 bottom-0 w-px bg-zinc-200 -translate-x-1/2 hidden md:block"></div>

                <div class="space-y-32">
                    <div v-for="(phase, i) in roadmapPhases" :key="phase.id"
                        class="relative flex flex-col md:flex-row items-center gap-12 reveal active"
                        :class="i % 2 === 1 ? 'md:flex-row-reverse' : ''">

                        <!-- Content -->
                        <div class="flex-1 w-full">
                            <div
                                class="p-8 rounded-3xl border border-zinc-100 bg-white shadow-xl shadow-zinc-200/50 hover:border-black transition-all group">
                                <div
                                    class="text-xs font-bold text-zinc-400 uppercase tracking-widest mb-4 flex items-center gap-2">
                                    <span class="w-2 h-2 rounded-full"
                                        :class="phase.status === 'completed' ? 'bg-green-500' : phase.status === 'current' ? 'bg-blue-500 animate-pulse' : 'bg-zinc-300'"></span>
                                    {{ phase.period }}
                                </div>
                                <h3 class="text-2xl font-bold mb-4 group-hover:text-black transition-colors">{{
                                    phase.title }}</h3>
                                <p class="text-zinc-500 leading-relaxed mb-6">{{ phase.desc }}</p>

                                <div class="flex flex-wrap gap-2">
                                    <div v-for="tag in phase.items" :key="tag"
                                        class="px-3 py-1 bg-zinc-50 rounded-lg text-xs font-medium text-zinc-600 border border-zinc-100">
                                        {{ tag }}
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Connector Point -->
                        <div
                            class="absolute left-1/2 -translate-x-1/2 w-12 h-12 bg-white rounded-full border-4 border-zinc-100 z-10 hidden md:flex items-center justify-center">
                            <iconify-icon
                                :icon="phase.status === 'completed' ? 'lucide:check-circle' : phase.status === 'current' ? 'lucide:zap' : 'lucide:circle'"
                                width="24"
                                :class="phase.status === 'completed' ? 'text-green-500' : phase.status === 'current' ? 'text-blue-500' : 'text-zinc-300'"></iconify-icon>
                        </div>

                        <!-- Future Space -->
                        <div class="flex-1 hidden md:block"></div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Contribution CTA -->
        <section class="py-32 bg-zinc-950 text-white overflow-hidden relative">
            <div class="max-w-4xl mx-auto px-6 text-center relative z-10">
                <h2 class="text-4xl font-bold mb-8">{{ $t('roadmap.cta.title') }}</h2>
                <p class="text-zinc-400 mb-12 max-w-xl mx-auto">{{ $t('roadmap.cta.subtitle') }}</p>
                <a href="https://t.me/storely_uz" target="_blank"
                    class="inline-flex items-center gap-2 px-10 py-5 bg-white text-black rounded-full font-bold hover:bg-zinc-200 transition-all hover-lift">
                    {{ $t('roadmap.cta.button') }}
                    <iconify-icon icon="lucide:send"></iconify-icon>
                </a>
            </div>
        </section>

        <AppFooter />
    </div>
</template>

<script setup>
const localePath = useLocalePath()

const roadmapPhases = [
    {
        id: 1,
        period: '2025 Q3-Q4',
        status: 'completed',
        title: 'Platform Foundation',
        desc: 'Storely platformasining asosiy yadrosini yaratish, mahsulotlar katalogi va buyurtma berish tizimini ishga tushirish.',
        items: ['Core Platform', 'Payment APIs', 'Mobile Web UI']
    },
    {
        id: 2,
        period: '2026 Q1',
        status: 'current',
        title: 'Telegram Ecosystem',
        desc: 'Hozirgi vaqtda biz Telegram Web App imkoniyatlarini maksimal darajaga chiqarish va kuryerlik tizimini integratsiya qilish ustida ishlayapmiz.',
        items: ['Telegram Web Apps', 'Courier Dashboard', 'Multi-currency']
    },
    {
        id: 3,
        period: '2026 Q2',
        status: 'upcoming',
        title: 'Marketing & Growth',
        desc: 'Sotuvchilarga sotuvlarni oshirishda yordam beradigan avtomatlashtirilgan marketing vositalari va AI yordamchisi.',
        items: ['AI Copilot', 'Advanced Promo Tools', 'SEO Suite']
    },
    {
        id: 4,
        period: '2026 Q3-Q4',
        status: 'future',
        title: 'Global Expansion',
        desc: 'Platformani xalqaro bozorlarga moslashtirish, ko\'p tilli do\'konlar va xalqaro kuryerlik xizmatlari.',
        items: ['Cross-border Sales', 'Mobile App (iOS/Android)', 'API Marketplace']
    }
]
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

.hover-lift:hover {
    transform: translateY(-4px);
}
</style>
