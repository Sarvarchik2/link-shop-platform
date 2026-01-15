<template>
    <div class="min-h-screen bg-white">
        <LandingHeader />

        <main class="pt-32 pb-20">
            <div class="max-w-4xl mx-auto px-6">
                <h1 class="text-4xl md:text-5xl font-bold tracking-tight text-zinc-900 mb-8">
                    {{ $t('footer.legal.cookie') }}
                </h1>

                <div class="prose prose-zinc max-w-none space-y-8 text-zinc-600 leading-relaxed">
                    <section>
                        <h2 class="text-2xl font-bold text-zinc-900 mb-4">1. {{ $t('legal.general.what_are_cookies') }}
                        </h2>
                        <p>{{ $t('legal.cookie.what_are_cookies_text') }}</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-zinc-900 mb-4">2. {{ $t('legal.general.how_we_use_cookies')
                            }}</h2>
                        <p>{{ $t('legal.cookie.how_we_use_cookies_text') }}</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-zinc-900 mb-4">3. {{ $t('legal.general.types_of_cookies') }}
                        </h2>
                        <p>{{ $t('legal.cookie.types_of_cookies_text') }}</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-zinc-900 mb-4">4. {{ $t('legal.general.managing_cookies') }}
                        </h2>
                        <p>{{ $t('legal.cookie.managing_cookies_text') }}</p>
                    </section>
                </div>
            </div>
        </main>

        <AppFooter />
    </div>
</template>

<script setup>
</script>

<style scoped>
.prose section+section {
    margin-top: 3rem;
    padding-top: 3rem;
    border-top: 1px solid #f4f4f5;
}
</style>
