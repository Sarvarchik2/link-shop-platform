<template>
  <div class="shop-admin-page">
    <!-- Mobile Header -->
    <header class="mobile-header">
      <button class="menu-btn" @click="sidebarOpen = !sidebarOpen">
        <svg v-if="!sidebarOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor"
          stroke-width="2">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
        <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
      <span class="mobile-title">{{ $t('admin.telegram.title') }}</span>
      <NuxtLink :to="localePath(`/${shopSlug}`)" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <ShopAdminSidebar :shop-slug="shopSlug" :current-route="currentRoute" v-model="sidebarOpen" />

    <!-- Main Content -->
    <main class="admin-main">
      <div class="telegram-settings-page">
        <div class="page-header">
          <div class="header-content">
            <h1 class="page-title">{{ $t('admin.telegram.pageTitle') }}</h1>
            <p class="page-subtitle">{{ $t('admin.telegram.pageSubtitle') }}</p>
          </div>
          <div class="header-actions">
            <!-- Status Badge -->
            <div v-if="shop?.telegram_bot_token" class="status-badge" :class="{ active: shop?.is_bot_active }">
              <div class="status-dot"></div>
              <span>{{ shop?.is_bot_active ? $t('admin.telegram.botActive') : $t('admin.telegram.botStatus') }}</span>
            </div>
          </div>
        </div>

        <div class="settings-grid">
          <!-- Left Column: Bot Settings -->
          <div class="settings-card main-card">
            <div class="card-header">
              <div class="card-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 2L11 13"></path>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                </svg>
              </div>
              <h2 class="card-title">{{ $t('admin.telegram.title') }}</h2>
            </div>

            <div class="form-group">
              <label class="form-label">{{ $t('admin.telegram.tokenLabel') }}</label>
              <div class="input-with-action">
                <input 
                  v-model="botToken" 
                  type="password" 
                  class="form-input" 
                  placeholder="123456789:ABCDefGhIJKlmNoPQRsTUVwxyZ"
                />
                <button 
                  @click="handleTestToken" 
                  class="test-btn" 
                  :disabled="!botToken || testing"
                >
                  <span v-if="!testing">{{ $t('admin.telegram.testBtn') }}</span>
                  <div v-else class="loader-sm"></div>
                </button>
              </div>
              <p class="input-hint">Enter the token received from @BotFather</p>
            </div>

            <!-- Bot Result Info -->
            <div v-if="testResult" class="test-result" :class="{ success: testResult.valid, error: !testResult.valid }">
              <div class="result-icon">
                <svg v-if="testResult.valid" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </div>
              <div class="result-content">
                <div class="result-title">{{ testResult.valid ? $t('admin.telegram.botValid') : $t('admin.telegram.botInvalid') }}</div>
                <div v-if="testResult.valid && testResult.bot_name" class="result-details">
                  <strong>@{{ testResult.username }}</strong> ({{ testResult.bot_name }})
                </div>
              </div>
            </div>

            <div class="form-actions">
              <button 
                @click="handleSaveSettings" 
                class="save-btn" 
                :disabled="saving || !botToken"
              >
                <span v-if="!saving">{{ $t('admin.telegram.saveBtn') }}</span>
                <div v-else class="loader-sm"></div>
              </button>
            </div>
          </div>

          <!-- Right Column: Instructions -->
          <div class="settings-card info-card">
            <div class="card-header">
              <div class="card-icon info-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="16" x2="12" y2="12"></line>
                  <line x1="12" y1="8" x2="12.01" y2="8"></line>
                </svg>
              </div>
              <h2 class="card-title">{{ $t('admin.telegram.instructionsTitle') }}</h2>
            </div>

            <div class="steps-list">
              <div class="step-item">
                <div class="step-num">1</div>
                <div class="step-text">{{ $t('admin.telegram.step1') }}</div>
              </div>
              <div class="step-item">
                <div class="step-num">2</div>
                <div class="step-text">{{ $t('admin.telegram.step2') }}</div>
              </div>
              <div class="step-item">
                <div class="step-num">3</div>
                <div class="step-text">{{ $t('admin.telegram.step3') }}</div>
              </div>
              <div class="step-item highlight">
                <div class="step-num">4</div>
                <div class="step-text">
                  {{ $t('admin.telegram.step4', { slug: shopSlug }) }}
                  <div class="copy-box" @click="copyToClipboard(`https://storely.uz/s/${shopSlug}`)">
                    <code>https://storely.uz/s/{{ shopSlug }}</code>
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            <div v-if="shop?.telegram_bot_token" class="webapp-info">
              <div class="webapp-label">{{ $t('admin.telegram.webAppLink') }}</div>
              <a :href="`https://t.me/${testResult?.username || 'bot'}`" target="_blank" class="webapp-link">
                t.me/{{ testResult?.username || 'your_bot' }}
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

const botToken = ref('')
const testing = ref(false)
const saving = ref(false)
const testResult = ref(null)
const sidebarOpen = ref(false)

const currentRoute = computed(() => {
  if (route.path.includes('/telegram')) return 'telegram'
  return ''
})

// Fetch current shop data
const { data: shop, refresh } = await useFetch(`${config.public.apiBase}/platform/shops/${shopSlug}`, {
  headers: computed(() => ({
    'Authorization': `Bearer ${token.value}`
  }))
})

watch(shop, (newShop) => {
  if (newShop?.telegram_bot_token) {
    botToken.value = newShop.telegram_bot_token
    // Don't auto-test - only set the value
    // User will click "Test Token" button manually
  }
}, { immediate: true })

const handleTestToken = async () => {
  if (!botToken.value) return
  
  testing.value = true
  try {
    const res = await $fetch(`${config.public.apiBase}/shop/${shopSlug}/admin/telegram/test`, {
      method: 'POST',
      body: { token: botToken.value },
      headers: {
        'Authorization': `Bearer ${token.value}`
      }
    })
    testResult.value = res
  } catch (e) {
    testResult.value = { valid: false }
    toast.error(t('admin.telegram.botInvalid'))
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
        is_bot_active: testResult.value?.valid || false
      },
      headers: {
        'Authorization': `Bearer ${token.value}`
      }
    })
    toast.success(t('common.saved'))
    await refresh()
  } catch (e) {
    toast.error(e.data?.detail || 'Error saving settings')
  } finally {
    saving.value = false
  }
}

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text)
  toast.success(t('common.copied'))
}
</script>

<style scoped>
.shop-admin-page {
  min-height: 100vh;
  display: flex;
  background: #FAFAFA;
}

/* Mobile Header */
.mobile-header {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: white;
  border-bottom: 1px solid #E5E7EB;
  padding: 0 16px;
  align-items: center;
  justify-content: space-between;
  z-index: 1000;
}

.menu-btn,
.home-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F3F4F6;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  color: #111;
  transition: all 0.2s;
}

.menu-btn:hover,
.home-btn:hover {
  background: #111;
  color: white;
}

.mobile-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111;
}

/* Main Content */
.admin-main {
  flex: 1;
  margin-left: 280px;
  min-height: 100vh;
  padding: 40px;
}

@media (max-width: 1024px) {
  .mobile-header {
    display: flex;
  }

  .admin-main {
    margin-left: 0;
    padding: 24px 16px;
    padding-top: 80px;
  }
}

.telegram-settings-page {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.page-title {
  font-size: 2rem;
  font-weight: 900;
  color: #111;
  margin-bottom: 8px;
}

.page-subtitle {
  color: #6B7280;
  font-size: 1rem;
}

/* Status Badge */
.status-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(255, 68, 68, 0.1);
  border: 1px solid rgba(255, 68, 68, 0.2);
  border-radius: 100px;
  color: #FF4444;
  font-weight: 600;
  font-size: 0.9rem;
}

.status-badge.active {
  background: rgba(16, 185, 129, 0.1);
  border-color: rgba(16, 185, 129, 0.2);
  color: #10B981;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: currentColor;
  box-shadow: 0 0 10px currentColor;
}

/* Grid & Cards */
.settings-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 24px;
}

@media (max-width: 1024px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }
}

.settings-card {
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 20px;
  padding: 28px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
}

.card-icon {
  width: 48px;
  height: 48px;
  background: #EEF2FF;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3B82F6;
}

.info-icon {
  background: #F5F3FF;
  color: #8B5CF6;
}

.card-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: #111;
}

/* Forms */
.form-group {
  margin-bottom: 24px;
}

.form-label {
  display: block;
  font-size: 0.9rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.input-with-action {
  display: flex;
  gap: 12px;
}

.form-input {
  flex: 1;
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  padding: 12px 16px;
  color: #111;
  font-family: inherit;
  transition: all 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #3B82F6;
  background: white;
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
}

.test-btn {
  padding: 0 20px;
  background: #F3F4F6;
  border: 1px solid #E5E7EB;
  border-radius: 12px;
  color: #111;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.test-btn:hover:not(:disabled) {
  background: #111;
  color: white;
}

.test-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.input-hint {
  font-size: 0.8rem;
  color: #9CA3AF;
  margin-top: 8px;
}

/* Test Result */
.test-result {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-radius: 12px;
  margin-bottom: 24px;
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.test-result.success {
  background: #ECFDF5;
  border: 1px solid #10B981;
}

.test-result.error {
  background: #FEF2F2;
  border: 1px solid #EF4444;
}

.result-icon {
  flex-shrink: 0;
  margin-top: 2px;
}

.success .result-icon { color: #10B981; }
.error .result-icon { color: #EF4444; }

.result-title {
  font-weight: 700;
  margin-bottom: 4px;
  color: #111;
}

.result-details {
  font-size: 0.9rem;
  color: #6B7280;
}

.save-btn {
  width: 100%;
  height: 48px;
  background: #111;
  border: none;
  border-radius: 12px;
  color: white;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.save-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  background: #000;
}

.save-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Steps */
.steps-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.step-item {
  display: flex;
  gap: 16px;
}

.step-num {
  width: 32px;
  height: 32px;
  background: #F3F4F6;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #111;
  flex-shrink: 0;
  font-size: 0.9rem;
}

.step-text {
  color: #4B5563;
  line-height: 1.6;
  padding-top: 4px;
}

.step-item.highlight .step-num {
  background: #8B5CF6;
  color: white;
}

.copy-box {
  margin-top: 8px;
  padding: 10px 14px;
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s;
}

.copy-box:hover {
  background: #F3F4F6;
  border-color: #D1D5DB;
}

.copy-box code {
  font-family: 'Fira Code', 'Courier New', monospace;
  color: #8B5CF6;
  font-size: 0.85rem;
}

.copy-box svg {
  color: #9CA3AF;
}

.webapp-info {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #E5E7EB;
}

.webapp-label {
  font-size: 0.85rem;
  color: #6B7280;
  margin-bottom: 8px;
  font-weight: 500;
}

.webapp-link {
  color: #3B82F6;
  text-decoration: none;
  font-weight: 600;
  display: block;
}

.webapp-link:hover {
  text-decoration: underline;
}

.loader-sm {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
