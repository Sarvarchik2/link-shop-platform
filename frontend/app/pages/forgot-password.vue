<template>
    <div class="login-page">
        <div class="login-container">
            <div class="login-card">
                <div class="login-header">
                    <h1 class="login-title">{{ $t('auth.reset_password_title') }}</h1>
                    <p class="login-subtitle">{{ $t('auth.login_subtitle') }}</p>
                </div>

                <form @submit.prevent="handleRequestReset" class="login-form">
                    <div class="form-group">
                        <label class="form-label">{{ $t('profile.info.email_label') }}</label>
                        <input v-model="email" type="email" required class="form-input"
                            placeholder="example@mail.com" />
                    </div>

                    <button type="submit" :disabled="loading" class="btn-submit">
                        <span v-if="loading">{{ $t('common.sending') }}</span>
                        <span v-else>{{ $t('common.confirm') }}</span>
                    </button>

                    <div class="form-footer">
                        <NuxtLink :to="localePath('/login')" class="footer-link">{{ $t('auth.login_link_text') }}
                        </NuxtLink>
                    </div>
                </form>
            </div>
        </div>

        <!-- Unverified Email Modal -->
        <div v-if="showUnverifiedModal" class="modal-overlay">
            <div class="modal-card">
                <h3>{{ $t('common.error') }}</h3>
                <p>{{ $t('auth.email_not_verified_error') }}</p>
                <div class="modal-actions" style="margin-top: 24px;">
                    <button @click="showUnverifiedModal = false" class="btn-confirm">{{ $t('common.close') }}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
definePageMeta({
    layout: false
})

const { t } = useI18n()
const localePath = useLocalePath()
const toast = useToast()
const email = ref('')
const loading = ref(false)
const showUnverifiedModal = ref(false)

const handleRequestReset = async () => {
    if (loading.value) return
    if (!email.value) return

    loading.value = true
    try {
        const config = useRuntimeConfig()
        await $fetch(`${config.public.apiBase}/password-reset/request`, {
            method: 'POST',
            body: { email: email.value }
        })
        toast.success(t('auth.request_reset_success'))
    } catch (e: any) {
        console.error('Reset request error:', e)
        if (e?.data?.detail?.includes('подтверждена') || e?.data?.detail?.includes('verified')) {
            showUnverifiedModal.value = true
        } else {
            let errorMessage = t('common.error')
            if (e?.data?.detail) {
                errorMessage = e.data.detail
            }
            toast.error(errorMessage)
        }
    } finally {
        loading.value = false
    }
}
</script>

<style scoped>
.login-page {
    min-height: 100vh;
    background: #FAFAFA;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.login-container {
    width: 100%;
    max-width: 440px;
}

.login-card {
    background: white;
    border-radius: 24px;
    padding: 48px 40px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.login-header {
    text-align: center;
    margin-bottom: 40px;
}

.login-title {
    font-size: 2.5rem;
    font-weight: 900;
    color: #111;
    margin: 0;
    letter-spacing: -0.02em;
}

.login-subtitle {
    font-size: 0.875rem;
    color: #6B7280;
    margin-top: 8px;
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-label {
    font-size: 0.875rem;
    font-weight: 600;
    color: #374151;
    letter-spacing: 0.025em;
}

.form-input {
    padding: 16px 20px;
    border: 2px solid #E5E7EB;
    border-radius: 12px;
    font-size: 1rem;
    transition: all 0.3s;
    background: #F9FAFB;
    color: #111;
}

.form-input:focus {
    outline: none;
    border-color: #111;
    background: white;
    box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.05);
}

.btn-submit {
    padding: 18px;
    background: #111;
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s;
    margin-top: 8px;
}

.btn-submit:hover:not(:disabled) {
    background: #000;
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.btn-submit:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.form-footer {
    text-align: center;
    margin-top: 8px;
}

.footer-link {
    color: #111;
    font-weight: 600;
    margin-left: 4px;
    text-decoration: none;
    transition: color 0.2s;
    font-size: 0.875rem;
}

.footer-link:hover {
    text-decoration: underline;
}

/* Modal styles */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-card {
    background: white;
    padding: 32px;
    border-radius: 24px;
    width: 100%;
    max-width: 400px;
    text-align: center;
}

.modal-actions {
    display: flex;
    gap: 12px;
}

.modal-actions button {
    flex: 1;
    padding: 14px;
    border-radius: 12px;
    font-weight: 700;
    border: none;
    cursor: pointer;
}

.btn-confirm {
    background: #111;
    color: white;
}
</style>
