<template>
    <div class="min-h-screen bg-white">
        <LandingHeader />

        <!-- Hero -->
        <section class="pt-32 pb-24 bg-zinc-950 text-white overflow-hidden relative">
            <!-- Gradient background -->
            <div class="absolute inset-0 bg-gradient-to-b from-blue-600/10 to-transparent"></div>

            <div class="max-w-7xl mx-auto px-6 relative z-10 text-center">
                <div class="reveal active">
                    <h1 class="text-5xl md:text-8xl font-bold tracking-tight mb-8">
                        {{ $t('templates.hero.title') }}
                    </h1>
                    <p class="text-xl text-zinc-400 max-w-2xl mx-auto mb-16 leading-relaxed">
                        {{ $t('templates.hero.subtitle') }}
                    </p>
                </div>

                <!-- Simulated Gallery Slider (Visual) -->
                <div class="flex gap-8 justify-center overflow-hidden h-[400px]">
                    <div v-for="i in 5" :key="i"
                        class="w-[300px] flex-shrink-0 bg-zinc-900 rounded-2xl border border-white/10 p-4 transform transition-all duration-700 hover:-translate-y-8"
                        :style="{ transitionDelay: (i * 100) + 'ms' }">
                        <div class="h-full bg-zinc-800 rounded-xl overflow-hidden relative group">
                            <div
                                class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-6">
                                <div class="text-left">
                                    <div class="text-xs font-bold uppercase tracking-widest text-blue-400 mb-1">Modern
                                        UI</div>
                                    <div class="text-sm font-medium">Business Template {{ i }}</div>
                                </div>
                            </div>
                            <div class="p-4 space-y-3">
                                <div class="h-2 w-1/2 bg-white/10 rounded"></div>
                                <div class="aspect-square bg-white/5 rounded-lg"></div>
                                <div class="grid grid-cols-2 gap-2">
                                    <div class="h-20 bg-white/5 rounded-lg"></div>
                                    <div class="h-20 bg-white/5 rounded-lg"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Template Showcases -->
        <section class="py-32">
            <div class="max-w-7xl mx-auto px-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-16">
                    <div v-for="temp in templateCategories" :key="temp.id" class="group reveal active">
                        <div
                            class="aspect-[16/10] bg-zinc-100 rounded-3xl overflow-hidden mb-8 border border-zinc-200 relative group-hover:shadow-2xl transition-all duration-500">
                            <!-- Decorative elements for the category -->
                            <div class="absolute inset-0 flex items-center justify-center">
                                <iconify-icon :icon="temp.icon" width="120"
                                    class="text-zinc-200 group-hover:scale-110 transition-transform duration-700"></iconify-icon>
                            </div>
                            <div
                                class="absolute bottom-6 left-6 right-6 p-6 bg-white/90 backdrop-blur-md rounded-2xl border border-zinc-100 shadow-sm translate-y-4 opacity-0 group-hover:translate-y-0 group-hover:opacity-100 transition-all duration-500">
                                <div class="flex justify-between items-center">
                                    <div>
                                        <div class="text-xs font-bold text-zinc-400 uppercase tracking-widest mb-1">{{
                                            temp.industry }}</div>
                                        <div class="text-lg font-bold">{{ temp.name }}</div>
                                    </div>
                                    <div
                                        class="w-10 h-10 rounded-full bg-black text-white flex items-center justify-center">
                                        <iconify-icon icon="lucide:arrow-right"></iconify-icon>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <h3 class="text-2xl font-bold mb-4">{{ temp.name }}</h3>
                        <p class="text-zinc-500 mb-6 leading-relaxed">{{ temp.desc }}</p>
                        <div class="flex gap-4">
                            <div v-for="tag in temp.tags" :key="tag"
                                class="px-3 py-1 rounded-full bg-zinc-100 text-[10px] font-bold text-zinc-500 uppercase tracking-wider">
                                {{ tag }}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Bottom CTA -->
        <section class="py-24 bg-zinc-50 border-t border-zinc-100">
            <div class="max-w-3xl mx-auto px-6 text-center">
                <h2 class="text-3xl font-bold mb-8">{{ $t('templates.cta.title') }}</h2>
                <NuxtLink :to="localePath('/register-shop')"
                    class="inline-flex items-center gap-2 px-8 py-4 bg-black text-white rounded-full font-bold hover:bg-zinc-800 transition-all hover-lift">
                    {{ $t('templates.cta.button') }}
                    <iconify-icon icon="lucide:sparkles"></iconify-icon>
                </NuxtLink>
            </div>
        </section>

        <AppFooter />
    </div>
</template>

<script setup>
const localePath = useLocalePath()

const templateCategories = [
    {
        id: 1,
        name: 'Elegant Fashion',
        industry: 'Lifestyle',
        icon: 'lucide:shirt',
        desc: 'Kiyim-kechak va aksessuarlar do\'konlari uchun minimalist va chiroyli dizayn.',
        tags: ['Mobile First', 'High Conversion', 'Lookbook']
    },
    {
        id: 2,
        name: 'Tech & Gadgets',
        industry: 'Electronics',
        icon: 'lucide:cpu',
        desc: 'Texnika va gadjetlar uchun yuqori texnologiyali va qulay interfeys.',
        tags: ['Spec Tables', 'Dark Mode', 'Filter Rich']
    },
    {
        id: 3,
        name: 'Fresh Food',
        industry: 'Grocery',
        icon: 'lucide:apple',
        desc: 'Oziq-ovqat va yetkazib berish xizmatlari uchun yorqin va ishtahani ochuvchi dizayn.',
        tags: ['Speedy Checkout', 'Categories Maps', 'Live Tracking']
    },
    {
        id: 4,
        name: 'Beauty Lab',
        industry: 'Cosmetics',
        icon: 'lucide:sparkles',
        desc: 'Go\'zallik va parvarish mahsulotlari uchun nafis va yumshoq ranglardagi dizayn.',
        tags: ['Grid Gallery', 'Video Support', 'Reviews Focus']
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
