<template>
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
                        <NuxtLink :to="localePath('/')" class="flex items-center mb-6">
                            <img src="/img/logo.jpg" alt="Storely" class="h-10 w-auto brightness-0 invert" />
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
                                <a :href="`tel:${$t('footer.phone').replace(/\s/g, '')}`" class="text-sm">{{
                                    $t('footer.phone') }}</a>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Links Grid -->
                <div class="lg:col-span-7 grid grid-cols-2 md:grid-cols-3 gap-12">
                    <div>
                        <h4 class="text-white font-semibold mb-8 text-sm uppercase tracking-wider">{{
                            $t('footer.product.title') }}
                        </h4>
                        <ul class="space-y-4 text-sm">
                            <li>
                                <NuxtLink :to="localePath('/features')" class="hover:text-white transition-colors">{{
                                    $t('footer.product.features') }}</NuxtLink>
                            </li>
                            <li>
                                <NuxtLink :to="localePath('/integrations')" class="hover:text-white transition-colors">
                                    {{
                                        $t('footer.product.integrations')
                                    }}</NuxtLink>
                            </li>
                            <li>
                                <NuxtLink :to="localePath('/templates')" class="hover:text-white transition-colors">{{
                                    $t('footer.product.templates')
                                }}</NuxtLink>
                            </li>
                            <li>
                                <NuxtLink :to="localePath('/roadmap')" class="hover:text-white transition-colors">{{
                                    $t('footer.product.roadmap')
                                }}</NuxtLink>
                            </li>
                        </ul>
                    </div>
                    <div>
                        <h4 class="text-white font-semibold mb-8 text-sm uppercase tracking-wider">{{
                            $t('footer.company.title') }}
                        </h4>
                        <ul class="space-y-4 text-sm">
                            <li><a href="https://linkdigital.uz" target="_blank"
                                    class="hover:text-white transition-colors">{{
                                        $t('footer.company.about') }}</a></li>
                            <li><a href="https://linkdigital.uz" target="_blank"
                                    class="hover:text-white transition-colors">{{
                                        $t('footer.company.careers') }}</a></li>
                            <li><a href="https://linkdigital.uz" target="_blank"
                                    class="hover:text-white transition-colors">{{
                                        $t('footer.company.blog') }}</a></li>
                            <li><a href="https://linkdigital.uz" target="_blank"
                                    class="hover:text-white transition-colors">{{
                                        $t('footer.company.brand') }}</a></li>
                        </ul>
                    </div>
                    <div>
                        <h4 class="text-white font-semibold mb-8 text-sm uppercase tracking-wider">{{
                            $t('footer.legal.title') }}
                        </h4>
                        <ul class="space-y-4 text-sm">
                            <li>
                                <NuxtLink :to="localePath('/privacy-policy')"
                                    class="hover:text-white transition-colors">{{
                                        $t('footer.legal.privacy') }}</NuxtLink>
                            </li>
                            <li>
                                <NuxtLink :to="localePath('/terms-of-use')" class="hover:text-white transition-colors">
                                    {{
                                        $t('footer.legal.terms') }}</NuxtLink>
                            </li>
                            <li>
                                <NuxtLink :to="localePath('/cookie-policy')" class="hover:text-white transition-colors">
                                    {{
                                        $t('footer.legal.cookie') }}</NuxtLink>
                            </li>
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
                    <a href="https://www.youtube.com/@storelyuz" target="_blank"
                        class="w-10 h-10 rounded-full bg-zinc-900 border border-zinc-800 flex items-center justify-center hover:bg-red-600 hover:text-white hover:border-red-600 transition-all duration-300"
                        title="YouTube">
                        <iconify-icon icon="lucide:youtube" width="18"></iconify-icon>
                    </a>
                </div>
            </div>
        </div>
    </footer>
</template>

<script setup>
const localePath = useLocalePath()
</script>
