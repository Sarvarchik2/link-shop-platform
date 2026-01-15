<template>
    <div class="min-h-screen bg-white">
        <LandingHeader />

        <main class="pt-32 pb-20">
            <div class="max-w-4xl mx-auto px-6">
                <h1 class="text-4xl md:text-5xl font-bold tracking-tight text-zinc-900 mb-8">
                    {{ $t('footer.legal.privacy') }}
                </h1>

                <div class="prose prose-zinc max-w-none space-y-8 text-zinc-600 leading-relaxed">
                    <section>
                        <h2 class="text-2xl font-bold text-zinc-900 mb-4">1. {{ $t('legal.general.intro') }}</h2>
                        <p>{{ $t('legal.privacy.intro_text') }}</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-zinc-900 mb-4">2. {{ $t('legal.general.data_collection') }}
                        </h2>
                        <p>{{ $t('legal.privacy.data_collection_text') }}</p>
                        <ul class="list-disc pl-6 mt-4 space-y-2">
                            <li v-for="item in $tm('legal.privacy.data_items')" :key="item">{{ $rt(item) }}</li>
                        </ul>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-zinc-900 mb-4">3. {{ $t('legal.general.data_usage') }}</h2>
                        <p>{{ $t('legal.privacy.data_usage_text') }}</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-zinc-900 mb-4">4. {{ $t('legal.general.data_protection') }}
                        </h2>
                        <p>{{ $t('legal.privacy.data_protection_text') }}</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-zinc-900 mb-4">5. {{ $t('legal.general.rights') }}</h2>
                        <p>{{ $t('legal.privacy.rights_text') }}</p>
                    </section>
                </div>
            </div>
        </main>

        <AppFooter />
    </div>
</template>

<script setup>
// No extra logic needed
</script>

<style scoped>
.prose section+section {
    margin-top: 3rem;
    padding-top: 3rem;
    border-top: 1px solid #f4f4f5;
}
</style>
