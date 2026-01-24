<template>
  <div class="shop-telegram-settings">
    <ShopAdminSidebar :shop-slug="shopSlug" :current-route="'telegram'" v-model="sidebarOpen" />

    <main class="admin-main">
      <!-- Header -->
      <header class="top-nav">
        <div class="nav-left">
          <button class="mobile-menu-btn" @click="sidebarOpen = true">
            <iconify-icon icon="lucide:menu" />
          </button>
          <div class="page-info">
            <h1 class="page-title">{{ $t('admin.telegram.title') }}</h1>
            <p class="page-subtitle">{{ $t('admin.telegram.subtitle') }}</p>
          </div>
        </div>

        <div class="nav-right">
          <div v-if="shop?.telegram_bot_token" class="status-pill" :class="{ active: shop?.is_bot_active }">
            <div class="dot"></div>
            <span>{{ shop?.is_bot_active ? $t('admin.telegram.statusConnected') : $t('admin.telegram.statusNotActive')
              }}</span>
          </div>
        </div>
      </header>

      <div class="admin-scroll">
        <div class="settings-layout">
          <!-- Main Form Card -->
          <div class="card-glass main-card">
            <div class="card-header">
              <div class="icon-box"><iconify-icon icon="lucide:bot" /></div>
              <div class="title-wrap">
                <h2>{{ $t('admin.telegram.botSettings') }}</h2>
                <p>{{ $t('admin.telegram.tokenInstruction') }}</p>
              </div>
            </div>

            <div class="form-body">
              <div class="input-group">
                <label>{{ $t('admin.telegram.tokenLabel') }}</label>
                <div class="input-act-wrap">
                  <input v-model="botToken" @input="isValid = false" type="password"
                    placeholder="123456789:ABCDefGhIJKlmNoPQRsTUVwxyZ" class="modern-input password" />
                  <button @click="handleTestToken" class="test-btn" :disabled="!botToken || testing">
                    <span v-if="!testing">{{ $t('admin.telegram.checkBtn') }}</span>
                    <div v-else class="loader-xs"></div>
                  </button>
                </div>
                <p class="hint">{{ $t('admin.telegram.securityWarning') }}</p>
              </div>

              <!-- Test Result Overlay -->
              <Transition name="fade-slide">
                <div v-if="testResult" class="result-banner"
                  :class="{ success: testResult.valid, error: !testResult.valid }">
                  <div class="rb-icon">
                    <iconify-icon :icon="testResult.valid ? 'lucide:check-circle' : 'lucide:alert-circle'" />
                  </div>
                  <div class="rb-content">
                    <div class="rb-title">{{ testResult.valid ? $t('admin.telegram.botFound') :
                      $t('admin.telegram.invalidToken') }}</div>
                    <div v-if="testResult.valid" class="rb-name">@{{ testResult.username }} ({{ testResult.bot_name }})
                    </div>
                    <div v-else class="rb-desc">{{ $t('admin.telegram.checkAndTryAgain') }}</div>
                  </div>
                </div>
              </Transition>

              <div v-if="isValid" class="action-hint">
                <iconify-icon icon="lucide:info" />
                <p>{{ $t('admin.telegram.saveHint') }}</p>
              </div>
            </div>

            <div class="card-footer">
              <button @click="handleSaveSettings" class="save-btn" :disabled="saving || !botToken">
                <span v-if="!saving">{{ $t('admin.telegram.saveBtn') }}</span>
                <span v-else class="loader-xs"></span>
              </button>
            </div>
          </div>

          <!-- Instructions Card -->
          <div class="card-glass side-card">
            <div class="card-header">
              <div class="icon-box info"><iconify-icon icon="lucide:help-circle" /></div>
              <h2>{{ $t('admin.telegram.howToCreate') }}</h2>
            </div>

            <div class="guide-steps">
              <div class="step">
                <div class="num">1</div>
                <div class="txt"
                  v-html="$t('admin.telegram.step1', { link: `<a href='https://t.me/BotFather' target='_blank'>@BotFather</a>` })">
                </div>
              </div>
              <div class="step">
                <div class="num">2</div>
                <div class="txt" v-html="$t('admin.telegram.step2')"></div>
              </div>
              <div class="step">
                <div class="num">3</div>
                <div class="txt">{{ $t('admin.telegram.step3') }}</div>
              </div>
              <div class="step highlight">
                <div class="num">4</div>
                <div class="txt">
                  {{ $t('admin.telegram.step4') }}
                  <div class="copy-url" @click="copyToClipboard(`https://storely.uz/s/${shopSlug}`)">
                    <code>https://storely.uz/s/{{ shopSlug }}</code>
                    <iconify-icon icon="lucide:copy" />
                  </div>
                </div>
              </div>
            </div>

            <div v-if="shop?.telegram_bot_token && testResult?.username" class="bot-link-box">
              <label>{{ $t('admin.telegram.botReady') }}</label>
              <a :href="`https://t.me/${testResult.username}`" target="_blank" class="t-me-link">
                t.me/{{ testResult.username }}
                <iconify-icon icon="lucide:external-link" />
              </a>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
const { t } = useI18n()
const localePath = useLocalePath()
const route = useRoute()
const shopSlug = route.params.slug
const config = useRuntimeConfig()
const { token } = useAuth()
const toast = useToast()

const sidebarOpen = ref(false)
const botToken = ref('')
const testing = ref(false)
const isValid = ref(false)
const saving = ref(false)
const testResult = ref(null)

// Current Route for sidebar
const currentRoute = computed(() => 'telegram')

// Fetch current shop data
const { data: shop, refresh } = await useFetch(`${config.public.apiBase}/platform/shops/${shopSlug}`, {
  headers: computed(() => ({ 'Authorization': `Bearer ${token.value}` }))
})

// Sync form with data
watch(shop, (newShop) => {
  if (newShop?.telegram_bot_token) {
    botToken.value = newShop.telegram_bot_token
    if (newShop.is_bot_active) isValid.value = true
  }
}, { immediate: true })

onMounted(() => {
  if (botToken.value) handleTestToken()
})

const handleTestToken = async () => {
  if (!botToken.value) return
  testing.value = true
  try {
    const res = await $fetch(`${config.public.apiBase}/shop/${shopSlug}/admin/telegram/test`, {
      method: 'POST',
      body: { token: botToken.value },
      headers: { 'Authorization': `Bearer ${token.value}` }
    })
    testResult.value = res
    isValid.value = res.valid
    if (res.valid) toast.success(t('admin.telegram.checkSuccess'))
  } catch (e) {
    testResult.value = { valid: false }
    isValid.value = false
    toast.error(t('admin.telegram.checkError'))
  } finally {
    testing.value = false
  }
}

const handleSaveSettings = async () => {
  saving.value = true
  try {
    await $fetch(`${config.public.apiBase}/shop/${shopSlug}/admin/info`, {
      method: 'PUT',
      body: {
        telegram_bot_token: botToken.value,
        is_bot_active: isValid.value
      },
      headers: { 'Authorization': `Bearer ${token.value}` }
    })
    toast.success(t('admin.telegram.saveSuccess'))
    await refresh()
  } catch (e) {
    toast.error(e.data?.detail || t('admin.telegram.saveError'))
  } finally {
    saving.value = false
  }
}

const copyToClipboard = (txt) => {
  navigator.clipboard.writeText(txt)
  toast.success(t('admin.telegram.copied'))
}
</script>

<style scoped>
.shop-telegram-settings {
  background: #f8fafc;
  min-height: 100vh;
  display: flex;
}

.admin-main {
  flex: 1;
  margin-left: 280px;
  display: flex;
  flex-direction: column;
  transition: all 0.4s;
}

.top-nav {
  padding: 32px;
  background: #fff;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mobile-menu-btn {
  display: none;
  width: 44px;
  height: 44px;
  background: #f1f5f9;
  border: none;
  border-radius: 12px;
  font-size: 1.5rem;
  cursor: pointer;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 950;
  margin: 0;
  letter-spacing: -1px;
}

.page-subtitle {
  font-size: 0.85rem;
  color: #64748b;
  margin-top: 4px;
  font-weight: 600;
}

.status-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 100px;
  background: #fee2e2;
  color: #991b1b;
  font-size: 0.8rem;
  font-weight: 800;
}

.status-pill.active {
  background: #dcfce7;
  color: #166534;
}

.status-pill .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
}

.admin-scroll {
  padding: 32px;
  flex: 1;
  overflow-y: auto;
}

.settings-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 32px;
  max-width: 1300px;
}

.card-glass {
  background: white;
  border-radius: 32px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.02);
  overflow: hidden;
}

.card-header {
  padding: 32px;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  gap: 20px;
  align-items: center;
}

.icon-box {
  width: 60px;
  height: 60px;
  border-radius: 20px;
  background: #e0e7ff;
  color: #4338ca;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
}

.icon-box.info {
  background: #fef3c7;
  color: #92400e;
}

.title-wrap h2 {
  font-weight: 900;
  font-size: 1.4rem;
  margin: 0;
}

.title-wrap p {
  font-size: 0.85rem;
  color: #64748b;
  margin-top: 4px;
  font-weight: 600;
}

.form-body {
  padding: 32px;
  display: grid;
  gap: 24px;
}

.input-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 850;
  color: #1e293b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
}

.input-act-wrap {
  display: flex;
  gap: 12px;
}

.modern-input {
  flex: 1;
  padding: 14px 20px;
  border-radius: 16px;
  border: 1.5px solid #e2e8f0;
  font-weight: 700;
  font-family: monospace;
}

.modern-input:focus {
  border-color: #111;
  outline: none;
}

.test-btn {
  padding: 0 24px;
  border-radius: 16px;
  background: #f1f5f9;
  border: none;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.test-btn:hover:not(:disabled) {
  background: #111;
  color: white;
}

.hint {
  font-size: 0.75rem;
  color: #94a3b8;
  font-weight: 600;
  margin-top: 8px;
}

.result-banner {
  display: flex;
  gap: 16px;
  padding: 20px;
  border-radius: 20px;
  margin-top: 8px;
}

.result-banner.success {
  background: #ecfdf5;
  border: 1.5px solid #10b981;
}

.result-banner.error {
  background: #fef2f2;
  border: 1.5px solid #ef4444;
}

.rb-icon {
  font-size: 1.5rem;
}

.success .rb-icon {
  color: #10b981;
}

.error .rb-icon {
  color: #ef4444;
}

.rb-title {
  font-weight: 900;
  color: #111;
}

.rb-name {
  font-family: monospace;
  font-size: 0.9rem;
  color: #166534;
  margin-top: 4px;
  font-weight: 800;
}

.rb-desc {
  font-size: 0.85rem;
  color: #991b1b;
  margin-top: 4px;
  font-weight: 600;
}

.action-hint {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: #eff6ff;
  border-radius: 16px;
  color: #1e40af;
  align-items: flex-start;
}

.action-hint iconify-icon {
  font-size: 1.2rem;
}

.action-hint p {
  font-size: 0.85rem;
  line-height: 1.5;
  font-weight: 600;
}

.card-footer {
  padding: 24px 32px;
  background: #f8fafc;
  border-top: 1px solid #f1f5f9;
}

.save-btn {
  width: 100%;
  height: 56px;
  border-radius: 18px;
  background: #111;
  color: white;
  border: none;
  font-weight: 900;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.save-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.guide-steps {
  padding: 32px;
  display: grid;
  gap: 20px;
}

.step {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.step .num {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #f1f5f9;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 900;
  flex-shrink: 0;
}

.step .txt {
  font-size: 0.9rem;
  font-weight: 650;
  color: #475569;
  line-height: 1.5;
  padding-top: 4px;
}

.step .txt a {
  color: #6366f1;
  text-decoration: underline;
}

.step.highlight .num {
  background: #6366f1;
  color: white;
}

.copy-url {
  margin-top: 12px;
  padding: 12px 16px;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.copy-url code {
  font-family: monospace;
  color: #6366f1;
  font-size: 0.8rem;
}

.copy-url:hover {
  border-color: #111;
}

.bot-link-box {
  padding: 0 32px 32px;
}

.bot-link-box label {
  display: block;
  font-size: 0.75rem;
  font-weight: 900;
  color: #94a3b8;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.t-me-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: #111;
  color: #fff;
  border-radius: 16px;
  font-weight: 800;
  text-decoration: none;
  font-size: 0.95rem;
}

.loader-xs {
  width: 18px;
  height: 18px;
  border: 2.5px solid rgba(255, 255, 255, 0.2);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1024px) {
  .admin-main {
    margin-left: 0;
  }

  .mobile-menu-btn {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .settings-layout {
    grid-template-columns: 1fr;
  }
}

.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
