<template>
  <div class="platform-admin-page">
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
      <span class="mobile-title">{{ $t('platformAdmin.offers.title') }}</span>
      <NuxtLink :to="localePath('/')" class="home-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
          <polyline points="9 22 9 12 15 12 15 22"></polyline>
        </svg>
      </NuxtLink>
    </header>

    <PlatformAdminSidebar :current-route="currentRoute" :model-value="sidebarOpen"
      @update:model-value="sidebarOpen = $event" @logout="handleLogout" />

    <!-- Main Content -->
    <main class="admin-main">
      <div class="admin-header">
        <div class="header-content">
          <div>
            <h1 class="admin-title">{{ $t('platformAdmin.offers.title') }}</h1>
            <p class="admin-subtitle">{{ $t('platformAdmin.offers.subtitle') }}</p>
          </div>
          <button @click="openCreateModal" class="create-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            <span>{{ $t('platformAdmin.offers.add') }}</span>
          </button>
        </div>
      </div>

      <div class="admin-content">
        <!-- Error State -->
        <div v-if="error" class="error-state">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <p class="error-message">{{ $t('platformAdmin.dashboard.error') }}: {{ error.message || 'Unknown' }}</p>
          <button @click="refresh" class="retry-btn">{{ $t('platformAdmin.dashboard.refresh') }}</button>
        </div>

        <!-- Loading State -->
        <div v-else-if="pending" class="loading-state">
          <div class="loading-spinner"></div>
          <p>{{ $t('platformAdmin.dashboard.loading') }}</p>
        </div>

        <!-- Offers Grid -->
        <div v-else class="offers-grid">
          <div v-for="offer in offers" :key="offer.id" class="offer-card" :class="{ 'inactive': !offer.is_active }">
            <div class="offer-header">
              <div class="offer-title-section">
                <h3 class="offer-name">{{ getLocalizedValue(offer, 'title') }}</h3>
                <div class="offer-badges">
                  <span v-if="!offer.is_active" class="badge inactive-badge">{{ $t('platformAdmin.plans.card.inactive')
                  }}</span>
                </div>
              </div>
              <div class="offer-actions">
                <button @click="editOffer(offer)" class="icon-btn" :title="$t('platformAdmin.offers.edit')">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                </button>
                <button @click="deleteOffer(offer)" class="icon-btn delete" :title="$t('platformAdmin.offers.delete')">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  </svg>
                </button>
              </div>
            </div>

            <div class="offer-price-section">
              <div v-if="offer.price" class="offer-price-value">
                {{ formatPrice(offer.price) }}
              </div>
              <div v-else class="offer-price-text">
                {{ getLocalizedValue(offer, 'price_text') || $t('platformAdmin.offers.card.priceByRequest') }}
              </div>
            </div>

            <p class="offer-description">{{ getLocalizedValue(offer, 'description') }}</p>

            <div class="offer-contact-info">
              <div v-if="offer.contact_email" class="contact-info-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                  <polyline points="22,6 12,13 2,6"></polyline>
                </svg>
                <span>{{ offer.contact_email }}</span>
              </div>
              <div v-if="offer.contact_phone" class="contact-info-item">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path
                    d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z">
                  </path>
                </svg>
                <span>{{ offer.contact_phone }}</span>
              </div>
            </div>

            <div class="offer-footer">
              <div class="offer-meta">
                <span>{{ $t('platformAdmin.plans.card.order') }} {{ offer.display_order }}</span>
              </div>
              <button @click="toggleActive(offer)" :class="['toggle-btn', offer.is_active ? 'active' : 'inactive']">
                {{ offer.is_active ? $t('platformAdmin.plans.card.active') : $t('platformAdmin.plans.card.inactive') }}
              </button>
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="offers && offers.length === 0" class="empty-state">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
              <path d="M2 17l10 5 10-5"></path>
              <path d="M2 12l10 5 10-5"></path>
            </svg>
            <p>{{ $t('platformAdmin.offers.empty') }}</p>
            <p class="empty-subtitle">{{ $t('platformAdmin.offers.emptySubtitle') }}</p>
            <button @click="openCreateModal" class="create-first-btn">{{ $t('platformAdmin.offers.create') }}</button>
          </div>
        </div>

        <!-- Create/Edit Modal -->
        <div v-if="showModal" class="modal-overlay" @click="closeModal">
          <div class="modal-content" @click.stop>
            <div class="modal-header">
              <h2 class="modal-title">{{ editingOffer ? $t('platformAdmin.offers.edit') :
                $t('platformAdmin.offers.create') }}</h2>
              <button @click="closeModal" class="modal-close">×</button>
            </div>

            <div class="lang-switcher">
              <button v-for="lang in ['ru', 'en', 'uz']" :key="lang" class="lang-btn"
                :class="{ active: activeLang === lang }" @click="activeLang = lang">
                {{ lang.toUpperCase() }}
              </button>
            </div>

            <form @submit.prevent="saveOffer" class="modal-form">
              <div class="form-grid">
                <div class="form-group full-width">
                  <label>{{ $t('platformAdmin.offers.form.title') }} ({{ activeLang.toUpperCase() }}) *</label>
                  <input v-if="activeLang === 'ru'" v-model="offerForm.title_ru" type="text" class="form-input"
                    required />
                  <input v-if="activeLang === 'en'" v-model="offerForm.title_en" type="text" class="form-input"
                    required />
                  <input v-if="activeLang === 'uz'" v-model="offerForm.title_uz" type="text" class="form-input"
                    required />
                </div>

                <div class="form-group full-width">
                  <label>{{ $t('platformAdmin.offers.form.description') }} ({{ activeLang.toUpperCase() }}) *</label>
                  <textarea v-if="activeLang === 'ru'" v-model="offerForm.description_ru" class="form-input" rows="4"
                    required></textarea>
                  <textarea v-if="activeLang === 'en'" v-model="offerForm.description_en" class="form-input" rows="4"
                    required></textarea>
                  <textarea v-if="activeLang === 'uz'" v-model="offerForm.description_uz" class="form-input" rows="4"
                    required></textarea>
                </div>

                <div class="form-group">
                  <label>{{ $t('platformAdmin.offers.form.price') }}</label>
                  <input v-model.number="offerForm.price" type="number" step="0.01" min="0" class="form-input"
                    placeholder="0.00" />
                  <small class="form-hint">{{ $t('platformAdmin.offers.form.hints.price') }}</small>
                </div>

                <div class="form-group">
                  <label>{{ $t('platformAdmin.offers.form.priceText') }} ({{ activeLang.toUpperCase() }})</label>
                  <input v-if="activeLang === 'ru'" v-model="offerForm.price_text_ru" type="text" class="form-input" />
                  <input v-if="activeLang === 'en'" v-model="offerForm.price_text_en" type="text" class="form-input" />
                  <input v-if="activeLang === 'uz'" v-model="offerForm.price_text_uz" type="text" class="form-input" />
                </div>

                <div class="form-group full-width">
                  <label>{{ $t('platformAdmin.offers.form.contactText') }} ({{ activeLang.toUpperCase() }})</label>
                  <input v-if="activeLang === 'ru'" v-model="offerForm.contact_text_ru" type="text"
                    class="form-input" />
                  <input v-if="activeLang === 'en'" v-model="offerForm.contact_text_en" type="text"
                    class="form-input" />
                  <input v-if="activeLang === 'uz'" v-model="offerForm.contact_text_uz" type="text"
                    class="form-input" />
                </div>

                <div class="form-group">
                  <label>{{ $t('platformAdmin.offers.form.email') }}</label>
                  <input v-model="offerForm.contact_email" type="email" class="form-input" />
                </div>

                <div class="form-group">
                  <label>{{ $t('platformAdmin.offers.form.phone') }}</label>
                  <input v-model="offerForm.contact_phone" type="tel" class="form-input" />
                </div>

                <div class="form-group">
                  <label class="checkbox-label">
                    <input v-model="offerForm.is_active" type="checkbox" class="checkbox-input" />
                    <span>{{ $t('platformAdmin.plans.form.isActive') }}</span>
                  </label>
                </div>

                <div class="form-group">
                  <label>{{ $t('platformAdmin.plans.form.order') }}</label>
                  <input v-model.number="offerForm.display_order" type="number" min="0" class="form-input" />
                  <small class="form-hint">{{ $t('platformAdmin.plans.form.hints.order') }}</small>
                </div>
              </div>

              <div class="modal-actions">
                <button type="button" @click="closeModal" class="btn-secondary">{{ $t('platformAdmin.plans.cancel')
                }}</button>
                <button type="submit" class="btn-primary" :disabled="saving">
                  {{ saving ? $t('common.saving') : (editingOffer ? $t('platformAdmin.plans.save') :
                    $t('platformAdmin.plans.create')) }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'platform-admin'
})

const route = useRoute()
const sidebarOpen = ref(false)
const { token, logout } = useAuth()
const toast = useToast()
const { t, locale } = useI18n()
const { formatPrice } = useCurrency()
const localePath = useLocalePath()

const handleLogout = () => {
  logout()
  toast.success(t('common.logout'))
}

const currentRoute = computed(() => {
  if (route.path.includes('/offers')) return 'offers'
  if (route.path.includes('/subscription-plans')) return 'subscription-plans'
  if (route.path.includes('/shops')) return 'shops'
  if (route.path.includes('/users')) return 'users'
  return 'dashboard'
})

const { data: offers, pending, error, refresh } = await useFetch(useRuntimeConfig().public.apiBase + '/platform/admin/offers', {
  server: false,
  headers: {
    'Authorization': `Bearer ${token.value}`
  }
})

const showModal = ref(false)
const editingOffer = ref(null)
const saving = ref(false)
const activeLang = ref('ru') // 'ru', 'en', 'uz'

const offerForm = reactive({
  title_ru: '',
  title_en: '',
  title_uz: '',
  description_ru: '',
  description_en: '',
  description_uz: '',
  price: null,
  price_text_ru: '',
  price_text_en: '',
  price_text_uz: '',
  contact_text_ru: 'Свяжитесь с нами для покупки',
  contact_text_en: 'Contact us to buy',
  contact_text_uz: 'Sotib olish uchun biz bilan bog\'laning',
  contact_email: '',
  contact_phone: '',
  is_active: true,
  display_order: 0
})

const getLocalizedValue = (obj, key) => {
  const currentLocale = locale.value
  if (currentLocale === 'ru' && obj[key + '_ru']) return obj[key + '_ru']
  if (currentLocale === 'en' && obj[key + '_en']) return obj[key + '_en']
  if (currentLocale === 'uz' && obj[key + '_uz']) return obj[key + '_uz']
  // Fallback to default fields (legacy support)
  return obj[key] || obj[key + '_ru'] || ''
}

const openCreateModal = () => {
  editingOffer.value = null
  resetForm()
  showModal.value = true
}

const editOffer = (offer) => {
  editingOffer.value = offer
  offerForm.title_ru = offer.title_ru || offer.title
  offerForm.title_en = offer.title_en || offer.title
  offerForm.title_uz = offer.title_uz || offer.title

  offerForm.description_ru = offer.description_ru || offer.description
  offerForm.description_en = offer.description_en || offer.description
  offerForm.description_uz = offer.description_uz || offer.description

  offerForm.price = offer.price ?? null

  offerForm.price_text_ru = offer.price_text_ru || offer.price_text || ''
  offerForm.price_text_en = offer.price_text_en || offer.price_text || ''
  offerForm.price_text_uz = offer.price_text_uz || offer.price_text || ''

  offerForm.contact_text_ru = offer.contact_text_ru || offer.contact_text || 'Свяжитесь с нами для покупки'
  offerForm.contact_text_en = offer.contact_text_en || offer.contact_text || 'Contact us to buy'
  offerForm.contact_text_uz = offer.contact_text_uz || offer.contact_text || 'Sotib olish uchun biz bilan bog\'laning'

  offerForm.contact_email = offer.contact_email || ''
  offerForm.contact_phone = offer.contact_phone || ''
  offerForm.is_active = offer.is_active
  offerForm.display_order = offer.display_order
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingOffer.value = null
  resetForm()
}

const resetForm = () => {
  offerForm.title_ru = ''
  offerForm.title_en = ''
  offerForm.title_uz = ''
  offerForm.description_ru = ''
  offerForm.description_en = ''
  offerForm.description_uz = ''
  offerForm.price = null
  offerForm.price_text_ru = ''
  offerForm.price_text_en = ''
  offerForm.price_text_uz = ''
  offerForm.contact_text_ru = 'Свяжитесь с нами для покупки'
  offerForm.contact_text_en = 'Contact us to buy'
  offerForm.contact_text_uz = 'Sotib olish uchun biz bilan bog\'laning'
  offerForm.contact_email = ''
  offerForm.contact_phone = ''
  offerForm.is_active = true
  offerForm.display_order = 0
}

const saveOffer = async () => {
  saving.value = true
  try {
    // Fill required default fields with RU values as fallback
    const payload = {
      ...offerForm,
      title: offerForm.title_ru || offerForm.title_en || offerForm.title_uz,
      description: offerForm.description_ru || offerForm.description_en || offerForm.description_uz,
      price_text: offerForm.price_text_ru,
      contact_text: offerForm.contact_text_ru,
      price: offerForm.price === null || offerForm.price === '' ? null : Number(offerForm.price)
    }

    if (editingOffer.value) {
      await $fetch(`${useRuntimeConfig().public.apiBase}/platform/admin/offers/${editingOffer.value.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token.value}`
        },
        body: payload
      })
      toast.success(t('common.saved'))
    } else {
      await $fetch(useRuntimeConfig().public.apiBase + '/platform/admin/offers', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token.value}`
        },
        body: payload
      })
      toast.success(t('common.saved'))
    }

    closeModal()
    refresh()
  } catch (e) {
    toast.error(e.data?.detail || t('platformAdmin.dashboard.error'))
  } finally {
    saving.value = false
  }
}

const toggleActive = async (offer) => {
  try {
    await $fetch(`${useRuntimeConfig().public.apiBase}/platform/admin/offers/${offer.id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token.value}`
      },
      body: {
        is_active: !offer.is_active
      }
    })
    toast.success(t('common.saved'))
    refresh()
  } catch (e) {
    toast.error(e.data?.detail || t('platformAdmin.dashboard.error'))
  }
}

const deleteOffer = async (offer) => {
  if (!confirm(`${t('platformAdmin.offers.delete')} "${getLocalizedValue(offer, 'title')}"?`)) {
    return
  }

  try {
    await $fetch(`${useRuntimeConfig().public.apiBase}/platform/admin/offers/${offer.id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token.value}`
      },
    })
    toast.success(t('common.deleted'))
    refresh()
  } catch (e) {
    toast.error(e.data?.detail || t('platformAdmin.dashboard.error'))
  }
}
</script>

<style scoped>
/* Same styles as subscription-plans.vue */
.platform-admin-page {
  min-height: 100vh;
  display: flex;
  background: #F5F7FA;
  width: 100%;
}

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
}

@media (max-width: 1024px) {
  .admin-main {
    margin-left: 0;
    padding-top: 60px;
  }
}

.admin-header {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
  color: white;
  padding: 40px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
  }

  .create-btn {
    width: 100%;
    justify-content: center;
  }
}

.admin-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: white;
  margin: 0 0 8px 0;
}

@media (max-width: 640px) {
  .admin-title {
    font-size: 1.25rem !important;
    line-height: 1.2 !important;
  }

  .admin-header {
    padding: 20px !important;
  }

  .admin-content {
    padding: 16px !important;
  }
}

.admin-subtitle {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 24px;
  background: #10B981;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.create-btn:hover {
  background: #059669;
  transform: translateY(-2px);
}

.admin-content {
  padding: 40px;
}

@media (max-width: 640px) {
  .admin-content {
    padding: 16px !important;
  }
}

/* Offers Grid */
.offers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

@media (max-width: 640px) {
  .offers-grid {
    grid-template-columns: 1fr;
  }
}

.offer-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 2px solid #E5E7EB;
  display: flex;
  flex-direction: column;
  transition: all 0.3s;
}

.offer-card:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.offer-card.inactive {
  opacity: 0.6;
}

.offer-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.offer-title-section {
  flex: 1;
}

.offer-name {
  font-size: 1.25rem;
  font-weight: 800;
  color: #111;
  margin: 0 0 8px 0;
}

.offer-badges {
  display: flex;
  gap: 8px;
}

.badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.inactive-badge {
  background: #FEE2E2;
  color: #991B1B;
}

.offer-actions {
  display: flex;
  gap: 8px;
}

.icon-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F3F4F6;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  color: #6B7280;
  transition: all 0.2s;
}

.icon-btn:hover {
  background: #E5E7EB;
  color: #111;
}

.icon-btn.delete:hover {
  background: #FEE2E2;
  color: #DC2626;
}

.offer-price-section {
  margin-bottom: 16px;
}

.offer-price-value {
  font-size: 2rem;
  font-weight: 800;
  color: #6366F1;
}

.offer-price-text {
  font-size: 1.25rem;
  font-weight: 700;
  color: #6B7280;
}

.offer-description {
  color: #6B7280;
  line-height: 1.6;
  margin-bottom: 20px;
  flex: 1;
}

.offer-contact-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
  padding: 12px;
  background: #F9FAFB;
  border-radius: 12px;
}

.contact-info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.875rem;
  color: #6B7280;
}

.contact-info-item svg {
  color: #9CA3AF;
  flex-shrink: 0;
}

.offer-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 2px solid #F3F4F6;
}

.offer-meta {
  font-size: 0.75rem;
  color: #6B7280;
}

.toggle-btn {
  padding: 6px 16px;
  border-radius: 8px;
  font-size: 0.8125rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.toggle-btn.active {
  background: #D1FAE5;
  color: #065F46;
}

.toggle-btn.inactive {
  background: #FEE2E2;
  color: #991B1B;
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 60px 20px;
}

.empty-state svg {
  color: #9CA3AF;
  margin: 0 auto 20px;
}

.empty-state p {
  font-size: 1.125rem;
  font-weight: 700;
  color: #6B7280;
  margin: 0 0 8px 0;
}

.empty-subtitle {
  font-size: 0.875rem;
  color: #9CA3AF;
  margin-bottom: 24px !important;
}

.create-first-btn {
  padding: 12px 24px;
  background: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.create-first-btn:hover {
  background: #000;
}

.error-state,
.loading-state {
  text-align: center;
  padding: 60px 20px;
}

.error-state svg,
.loading-state svg {
  color: #EF4444;
  margin: 0 auto 20px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #111;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.retry-btn {
  padding: 12px 24px;
  background: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  margin-top: 16px;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 20px;
  width: 100%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.modal-header {
  padding: 24px;
  border-bottom: 1px solid #E5E7EB;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 2rem;
  color: #6B7280;
  cursor: pointer;
  line-height: 1;
}

.lang-switcher {
  display: flex;
  gap: 8px;
  padding: 16px 24px 0;
}

.lang-btn {
  padding: 8px 16px;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  font-weight: 600;
  color: #6B7280;
  transition: all 0.2s;
}

.lang-btn.active {
  background: #111;
  color: white;
  border-color: #111;
}

.modal-form {
  padding: 24px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #D1D5DB;
  border-radius: 8px;
  font-size: 0.9375rem;
  transition: all 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #111;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.1);
}

.form-hint {
  display: block;
  font-size: 0.75rem;
  color: #6B7280;
  margin-top: 4px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
}

.checkbox-input {
  width: 18px;
  height: 18px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #E5E7EB;
}

.btn-primary,
.btn-secondary {
  padding: 12px 24px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  font-size: 0.9375rem;
  transition: all 0.2s;
}

.btn-primary {
  background: #111;
  color: white;
}

.btn-primary:hover {
  background: #000;
}

.btn-primary:disabled {
  background: #9CA3AF;
  cursor: not-allowed;
}

.btn-secondary {
  background: #F3F4F6;
  color: #374151;
}

.btn-secondary:hover {
  background: #E5E7EB;
}

@media (max-width: 640px) {
  .form-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}

.modal-content {
  background: white;
  border-radius: 24px;
  max-width: 700px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    border-radius: 20px;
    padding: 0;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .modal-header,
  .modal-form,
  .modal-actions {
    padding: 20px;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px;
  border-bottom: 1px solid #E5E7EB;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111;
  margin: 0;
}

.modal-close {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F3F4F6;
  border: none;
  border-radius: 10px;
  font-size: 24px;
  cursor: pointer;
  color: #6B7280;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #E5E7EB;
  color: #111;
}

.modal-form {
  padding: 32px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-weight: 600;
  color: #111;
  margin-bottom: 8px;
  font-size: 0.875rem;
}

.form-input {
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.2s;
  font-family: inherit;
}

.form-input:focus {
  outline: none;
  border-color: #111;
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
}

.form-hint {
  font-size: 0.75rem;
  color: #9CA3AF;
  margin-top: 4px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  margin: 0;
}

.checkbox-input {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 32px;
  padding-top: 32px;
  border-top: 1px solid #E5E7EB;
}

.btn-primary {
  padding: 12px 24px;
  background: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #000;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  padding: 12px 24px;
  background: #F3F4F6;
  color: #111;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #E5E7EB;
}

@media (max-width: 1024px) {
  .admin-main {
    margin-left: 0;
  }

  .mobile-header {
    display: flex;
  }

  .offers-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .admin-content {
    padding: 20px;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .admin-header {
    padding: 24px 20px;
  }

  .header-content {
    flex-direction: column;
    gap: 20px;
  }

  .create-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>

<style scoped>
/* Responsive improvements */
@media (max-width: 640px) {
  .offer-header {
    flex-direction: column;
    gap: 12px;
  }

  .offer-badges {
    margin-top: 8px;
  }

  .offer-actions {
    margin-top: 0;
    justify-content: flex-end;
    width: 100%;
  }

  .offer-footer {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .toggle-btn {
    width: 100%;
  }
}
</style>
