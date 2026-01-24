<template>
  <div class="platform-admin-offers">
    <PlatformAdminSidebar :current-route="'offers'" :model-value="sidebarOpen"
      @update:model-value="sidebarOpen = $event" @logout="handleLogout" />

    <main class="admin-main">
      <!-- Header -->
      <header class="top-nav">
        <div class="nav-left">
          <button class="mobile-menu-btn" @click="sidebarOpen = true">
            <iconify-icon icon="lucide:menu" />
          </button>
          <div class="page-info">
            <h1 class="page-title">{{ $t('platformAdmin.offers.title') }}</h1>
            <p class="page-subtitle">{{ $t('platformAdmin.offers.subtitle') }}</p>
          </div>
        </div>

        <div class="nav-right">
          <button @click="refresh" class="refresh-btn" :class="{ loading: pending }">
            <iconify-icon icon="lucide:rotate-cw" />
          </button>
          <button @click="openCreateModal" class="primary-btn">
            <iconify-icon icon="lucide:plus-circle" />
            <span>{{ $t('platformAdmin.offers.add') }}</span>
          </button>
        </div>
      </header>

      <div class="admin-scroll">
        <div v-if="pending" class="loading-state">
          <div class="loader"></div>
        </div>

        <div v-else-if="!offers || offers.length === 0" class="empty-state">
          <iconify-icon icon="lucide:sparkles" />
          <h2>{{ $t('platformAdmin.offers.noOffers') }}</h2>
          <p>{{ $t('platformAdmin.offers.createFirst') }}</p>
          <button @click="openCreateModal" class="primary-btn mt-6">{{ $t('platformAdmin.offers.add') }}</button>
        </div>

        <div v-else class="offers-grid">
          <div v-for="offer in offers" :key="offer.id" class="offer-card" :class="{ inactive: !offer.is_active }">
            <div class="card-header">
              <div class="offer-icon"><iconify-icon icon="lucide:gift" /></div>
              <div class="card-actions">
                <button @click="editOffer(offer)" class="card-act-btn"><iconify-icon icon="lucide:edit-3" /></button>
                <button @click="deleteOffer(offer)" class="card-act-btn delete"><iconify-icon
                    icon="lucide:trash-2" /></button>
              </div>
            </div>

            <div class="offer-body">
              <h3 class="offer-title">{{ getLocalizedValue(offer, 'title') }}</h3>
              <div class="offer-price">
                <span v-if="offer.price" class="p-val">{{ formatPrice(offer.price) }}</span>
                <span v-else class="p-text">{{ getLocalizedValue(offer, 'price_text') ||
                  $t('platformAdmin.offers.priceOnRequest') }}</span>
              </div>
              <p class="offer-desc">{{ getLocalizedValue(offer, 'description') }}</p>

              <div class="offer-contacts">
                <div v-if="offer.contact_email" class="c-item">
                  <iconify-icon icon="lucide:mail" /> {{ offer.contact_email }}
                </div>
                <div v-if="offer.contact_phone" class="c-item">
                  <iconify-icon icon="lucide:phone" /> {{ offer.contact_phone }}
                </div>
              </div>
            </div>

            <div class="card-footer">
              <div class="order-tag">{{ $t('platformAdmin.offers.order', { n: offer.display_order }) }}</div>
              <button @click="toggleActive(offer)" class="status-btn" :class="{ active: offer.is_active }">
                {{ offer.is_active ? $t('platformAdmin.offers.active') : $t('platformAdmin.offers.hidden') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Modal -->
    <Transition name="scale">
      <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal-win large" @click.stop>
          <div class="modal-header">
            <div class="modal-title-wrap">
              <h3>{{ editingOffer ? $t('platformAdmin.offers.edit') : $t('platformAdmin.offers.new') }}</h3>
              <div class="lang-pills">
                <button v-for="l in ['ru', 'en', 'uz']" :key="l" @click="activeLang = l"
                  :class="{ active: activeLang === l }">
                  {{ l.toUpperCase() }}
                </button>
              </div>
            </div>
            <button @click="closeModal" class="close-modal"><iconify-icon icon="lucide:x" /></button>
          </div>

          <form @submit.prevent="saveOffer" class="offer-form">
            <div class="form-scroll">
              <div class="form-grid">
                <div class="f-group span-2">
                  <label>{{ $t('platformAdmin.offers.titleLabel', { lang: activeLang.toUpperCase() }) }}</label>
                  <input v-if="activeLang === 'ru'" v-model="offerForm.title_ru" type="text" class="modern-input"
                    required />
                  <input v-if="activeLang === 'en'" v-model="offerForm.title_en" type="text" class="modern-input"
                    required />
                  <input v-if="activeLang === 'uz'" v-model="offerForm.title_uz" type="text" class="modern-input"
                    required />
                </div>

                <div class="f-group span-2">
                  <label>{{ $t('platformAdmin.offers.descriptionLabel', { lang: activeLang.toUpperCase() }) }}</label>
                  <textarea v-if="activeLang === 'ru'" v-model="offerForm.description_ru" class="modern-input" rows="3"
                    required></textarea>
                  <textarea v-if="activeLang === 'en'" v-model="offerForm.description_en" class="modern-input" rows="3"
                    required></textarea>
                  <textarea v-if="activeLang === 'uz'" v-model="offerForm.description_uz" class="modern-input" rows="3"
                    required></textarea>
                </div>

                <div class="f-group">
                  <label>{{ $t('platformAdmin.offers.priceLabel') }}</label>
                  <input v-model.number="offerForm.price" type="number" class="modern-input"
                    :placeholder="$t('platformAdmin.offers.pricePlaceholder')" />
                </div>

                <div class="f-group">
                  <label>{{ $t('platformAdmin.offers.priceTextLabel', { lang: activeLang.toUpperCase() }) }}</label>
                  <input v-if="activeLang === 'ru'" v-model="offerForm.price_text_ru" type="text" class="modern-input"
                    :placeholder="$t('platformAdmin.offers.priceTextPlaceholder')" />
                  <input v-if="activeLang === 'en'" v-model="offerForm.price_text_en" type="text"
                    class="modern-input" />
                  <input v-if="activeLang === 'uz'" v-model="offerForm.price_text_uz" type="text"
                    class="modern-input" />
                </div>

                <div class="f-group">
                  <label>{{ $t('platformAdmin.offers.emailLabel') }}</label>
                  <input v-model="offerForm.contact_email" type="email" class="modern-input" />
                </div>

                <div class="f-group">
                  <label>{{ $t('platformAdmin.offers.phoneLabel') }}</label>
                  <input v-model="offerForm.contact_phone" type="tel" class="modern-input" />
                </div>

                <div class="f-group">
                  <label>{{ $t('platformAdmin.offers.orderLabel') }}</label>
                  <input v-model.number="offerForm.display_order" type="number" class="modern-input" />
                </div>

                <div class="f-group mt-6">
                  <label class="sw-row">
                    <input v-model="offerForm.is_active" type="checkbox" />
                    <span>{{ $t('platformAdmin.offers.activeLabel') }}</span>
                  </label>
                </div>
              </div>
            </div>

            <div class="modal-footer">
              <button type="button" @click="closeModal" class="btn-cancel">{{ $t('platformAdmin.offers.cancel')
                }}</button>
              <button type="submit" class="btn-save" :disabled="saving">
                <span v-if="saving" class="loader-xs"></span>
                <span v-else>{{ editingOffer ? $t('platformAdmin.offers.save') : $t('platformAdmin.offers.create')
                  }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
const { t, locale } = useI18n()
const { token, logout } = useAuth()
const { formatPrice } = useCurrency()
const toast = useToast()
const config = useRuntimeConfig()

// Use internal URL for SSR, public URL for client
const apiBase = process.server ? config.apiBaseInternal : config.public.apiBase


definePageMeta({ middleware: 'platform-admin' })

const sidebarOpen = ref(false)
const showModal = ref(false)
const editingOffer = ref(null)
const saving = ref(false)
const activeLang = ref('ru')

const offerForm = reactive({
  title_ru: '', title_en: '', title_uz: '',
  description_ru: '', description_en: '', description_uz: '',
  price: null,
  price_text_ru: '', price_text_en: '', price_text_uz: '',
  contact_text_ru: '', contact_text_en: '', contact_text_uz: '',
  contact_email: '', contact_phone: '',
  is_active: true, display_order: 0
})

const { data: offers, pending, refresh } = useFetch(apiBase + '/platform/admin/offers', {
  lazy: true, watch: [token],
  headers: computed(() => ({ 'Authorization': `Bearer ${token.value}` }))
})

const handleLogout = () => { logout(); toast.success(t('auth.loggedOut')) }

const getLocalizedValue = (obj, k) => {
  if (locale.value === 'ru' && obj[k + '_ru']) return obj[k + '_ru']
  if (locale.value === 'en' && obj[k + '_en']) return obj[k + '_en']
  if (locale.value === 'uz' && obj[k + '_uz']) return obj[k + '_uz']
  return obj[k] || obj[k + '_ru'] || ''
}

const openCreateModal = () => { editingOffer.value = null; resetForm(); showModal.value = true }

const editOffer = (offer) => {
  editingOffer.value = offer
  Object.keys(offerForm).forEach(k => offerForm[k] = offer[k] ?? offerForm[k])
  // Fallbacks
  offerForm.title_ru = offer.title_ru || offer.title
  offerForm.description_ru = offer.description_ru || offer.description
  showModal.value = true
}

const closeModal = () => { showModal.value = false; editingOffer.value = null }

const resetForm = () => {
  Object.assign(offerForm, {
    title_ru: '', title_en: '', title_uz: '',
    description_ru: '', description_en: '', description_uz: '',
    price: null, price_text_ru: '', price_text_en: '', price_text_uz: '',
    contact_text_ru: t('platformAdmin.offers.contactDefault'), contact_email: '', contact_phone: '',
    is_active: true, display_order: 0
  })
}

const saveOffer = async () => {
  saving.value = true
  try {
    const body = {
      ...offerForm,
      title: offerForm.title_ru || offerForm.title_en || offerForm.title_uz,
      description: offerForm.description_ru || offerForm.description_en || offerForm.description_uz
    }
    const url = editingOffer.value ? `${config.public.apiBase}/platform/admin/offers/${editingOffer.value.id}` : `${config.public.apiBase}/platform/admin/offers`
    await $fetch(url, {
      method: editingOffer.value ? 'PUT' : 'POST',
      headers: { 'Authorization': `Bearer ${token.value}` },
      body
    })
    toast.success(t('platformAdmin.offers.saved'))
    closeModal(); refresh()
  } catch (e) { toast.error(t('platformAdmin.offers.saveError')) } finally { saving.value = false }
}

const toggleActive = async (o) => {
  try {
    await $fetch(`${config.public.apiBase}/platform/admin/offers/${o.id}`, {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token.value}` },
      body: { is_active: !o.is_active }
    })
    refresh()
  } catch (e) { toast.error(t('platformAdmin.offers.error')) }
}

const deleteOffer = async (o) => {
  if (!confirm(t('platformAdmin.offers.deleteConfirm', { title: getLocalizedValue(o, 'title') }))) return
  try {
    await $fetch(`${config.public.apiBase}/platform/admin/offers/${o.id}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token.value}` }
    })
    toast.success(t('platformAdmin.offers.deleted'))
    refresh()
  } catch (e) { toast.error(t('platformAdmin.offers.deleteError')) }
}
</script>

<style scoped>
/* Page specific styles */
.admin-scroll {
  padding: 32px;
  flex: 1;
  overflow-y: auto;
}

/* Offers Grid */
.offers-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
  padding-bottom: 40px;
}

.offer-card {
  background: white;
  border-radius: 32px;
  padding: 32px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.03);
  border: 2px solid transparent;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
}

.offer-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.08);
}

.offer-card.inactive {
  opacity: 0.6;
  filter: grayscale(1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.offer-icon {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  background: #f1f5f9;
  color: #111;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.card-act-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background: #f1f5f9;
  color: #64748b;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.card-act-btn:hover {
  background: #111;
  color: white;
}

.card-act-btn.delete:hover {
  background: #ef4444;
  color: white;
}

.offer-body {
  flex: 1;
}

.offer-title {
  font-size: 1.5rem;
  font-weight: 950;
  color: #111;
  margin: 0 0 12px 0;
  letter-spacing: -0.5px;
}

.offer-price {
  margin-bottom: 20px;
}

.p-val {
  font-size: 1.5rem;
  font-weight: 950;
  color: #6366f1;
}

.p-text {
  font-size: 1.1rem;
  font-weight: 800;
  color: #94a3b8;
}

.offer-desc {
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 600;
  line-height: 1.6;
  margin-bottom: 24px;
}

.offer-contacts {
  background: #f8fafc;
  padding: 16px;
  border-radius: 20px;
  display: grid;
  gap: 8px;
}

.c-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.85rem;
  font-weight: 750;
  color: #475569;
}

.c-item iconify-icon {
  color: #94a3b8;
  font-size: 1.2rem;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1.5px dashed #f1f5f9;
  padding-top: 24px;
  margin-top: 24px;
}

.order-tag {
  font-size: 0.75rem;
  font-weight: 850;
  color: #94a3b8;
  text-transform: uppercase;
}

.status-btn {
  padding: 6px 14px;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 900;
  border: 1.5px solid #e2e8f0;
  background: transparent;
  cursor: pointer;
  transition: all 0.2s;
}

.status-btn.active {
  background: #dcfce7;
  color: #166534;
  border-color: #dcfce7;
}

.empty-state {
  text-align: center;
  padding: 100px 0;
  grid-column: 1 / -1;
}

.empty-state iconify-icon {
  font-size: 4rem;
  color: #cbd5e1;
  margin-bottom: 24px;
}

.empty-state h2 {
  font-weight: 950;
  font-size: 1.75rem;
  margin-bottom: 12px;
}

.empty-state p {
  font-weight: 600;
  color: #64748b;
  max-width: 400px;
  margin: 0 auto;
}

.modal-win.large {
  max-width: 600px;
}

.modal-title-wrap {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.lang-pills {
  display: flex;
  background: #f1f5f9;
  padding: 4px;
  border-radius: 10px;
  width: fit-content;
}

.lang-pills button {
  padding: 4px 12px;
  border: none;
  border-radius: 8px;
  font-size: 0.7rem;
  font-weight: 900;
  cursor: pointer;
  background: transparent;
  color: #64748b;
}

.lang-pills button.active {
  background: white;
  color: #111;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.offer-form {
  display: flex;
  flex-direction: column;
  max-height: 80vh;
}

.form-scroll {
  overflow-y: auto;
  padding: 32px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.span-2 {
  grid-column: span 2;
}

.modern-input {
  width: 100%;
  padding: 14px 20px;
  border-radius: 16px;
  border: 1.5px solid #e2e8f0;
  font-weight: 700;
  outline: none;
  transition: all 0.2s;
}

.modern-input:focus {
  border-color: #111;
}

.f-group {
  display: grid;
  gap: 8px;
}

.f-group label {
  font-size: 0.8rem;
  font-weight: 850;
  color: #1e293b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.sw-row {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 800;
  cursor: pointer;
}

.sw-row input {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.modal-footer {
  padding: 24px 32px;
  border-top: 1px solid #f1f5f9;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn-save {
  padding: 14px 28px;
  border-radius: 16px;
  background: #111;
  color: white;
  border: none;
  font-weight: 900;
  cursor: pointer;
}

.loader {
  width: 40px;
  height: 40px;
  border: 4px solid #f1f5f9;
  border-top-color: #111;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1024px) {
  /* Inherits from platform-admin.css */
}

@media (max-width: 640px) {
  .offers-grid {
    grid-template-columns: 1fr;
  }
}
</style>
