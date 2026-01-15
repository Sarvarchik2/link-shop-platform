<template>
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
                    <NuxtLink :to="localePath('/') + '#features'" class="hover:text-black transition-colors">{{
                        $t('nav.features') }}</NuxtLink>
                    <NuxtLink :to="localePath('/') + '#solutions'" class="hover:text-black transition-colors">{{
                        $t('nav.solutions') }}</NuxtLink>
                    <NuxtLink :to="localePath('/') + '#pricing'" class="hover:text-black transition-colors">{{
                        $t('nav.pricing') }}</NuxtLink>
                    <NuxtLink :to="localePath('/') + '#clients'" class="hover:text-black transition-colors">{{
                        $t('nav.clients') }}</NuxtLink>
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
</template>

<script setup>
const localePath = useLocalePath()
const { user } = useAuth()

const profileLink = computed(() => {
    if (!user.value) return '/login'
    if (user.value.role === 'platform_admin' || user.value.roles?.includes('admin')) return '/platform/admin'
    return '/profile'
})
</script>

<style scoped>
.glass {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}

.transition-smooth {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.hover-lift:hover {
    transform: translateY(-2px);
}
</style>
