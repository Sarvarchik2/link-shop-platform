<template>
  <div class="platform-admin-plans">
    <PlatformAdminSidebar :current-route="'subscription-plans'" :model-value="sidebarOpen"
      @update:model-value="sidebarOpen = $event" @logout="handleLogout" />

    <main class="admin-main">
      <!-- Header -->
      <header class="top-nav">
        <div class="nav-left">
          <button class="mobile-menu-btn" @click="sidebarOpen = true">
            <iconify-icon icon="lucide:menu" />
          </button>
          <div class="page-info">
            <h1 class="page-title">{{ $t('platformAdmin.plans.title') }}</h1>
            <p class="page-subtitle">{{ $t('platformAdmin.plans.subtitle') }}</p>
          </div>
        </div>

        <div class="nav-right">
          <button @click="refresh" class="refresh-btn" :class="{ loading: pending }">
            <iconify-icon icon="lucide:rotate-cw" />
          </button>
          <button @click="openCreateModal" class="primary-btn">
            <iconify-icon icon="lucide:plus-circle" />
            <span>{{ $t('platformAdmin.plans.add') }}</span>
          </button>
        </div>
      </header>

      <div class="admin-scroll">
        <div v-if="pending" class="loading-state">
          <div class="loader"></div>
        </div>

        <div v-else class="plans-grid">
          <div v-for="plan in plans" :key="plan.id" class="plan-card"
            :class="{ inactive: !plan.is_active, trial: plan.is_trial }">
            <div class="card-header">
              <div class="plan-type-icon" :class="{ trial: plan.is_trial }">
                <iconify-icon :icon="plan.is_trial ? 'lucide:test-tube' : 'lucide:zap'" />
              </div>
              <div class="card-actions">
                <button @click="editPlan(plan)" class="card-act-btn"><iconify-icon icon="lucide:edit-3" /></button>
                <button @click="deletePlan(plan)" class="card-act-btn delete"><iconify-icon
                    icon="lucide:trash-2" /></button>
              </div>
            </div>

            <div class="plan-main-info">
              <h3 class="plan-name">{{ getLocalizedValue(plan, 'name') }}</h3>
              <div class="plan-price">
                <span class="price-val">{{ plan.price === 0 ? $t('platformAdmin.plans.free') : formatPrice(plan.price)
                  }}</span>
                <span class="price-period">/ {{ plan.is_trial ? (plan.trial_period_days || 0) : plan.period_days }} {{
                  $t('platformAdmin.plans.days') }}</span>
              </div>
              <div class="plan-slug"><code>{{ plan.slug }}</code></div>
            </div>

            <div class="plan-description-s">
              {{ getLocalizedValue(plan, 'description') || $t('platformAdmin.plans.noDesc') }}
            </div>

            <div class="plan-limits">
              <div class="limit-row">
                <iconify-icon icon="lucide:package" />
                <span>{{ $t('platformAdmin.plans.products') }}:</span>
                <strong>{{ plan.max_products || '∞' }}</strong>
              </div>
              <div class="limit-row">
                <iconify-icon icon="lucide:image" />
                <span>{{ $t('platformAdmin.plans.banners') }}:</span>
                <strong>{{ plan.max_banners || 1 }}</strong>
              </div>
              <div class="limit-row" :class="{ ok: plan.has_telegram }">
                <iconify-icon icon="lucide:message-circle" />
                <span>{{ $t('platformAdmin.plans.telegram') }}</span>
                <iconify-icon :icon="plan.has_telegram ? 'lucide:check' : 'lucide:x'" class="status-ico" />
              </div>
              <div class="limit-row" :class="{ ok: plan.can_broadcast }">
                <iconify-icon icon="lucide:send" />
                <span>{{ $t('platformAdmin.plans.broadcasts') }}</span>
                <iconify-icon :icon="plan.can_broadcast ? 'lucide:check' : 'lucide:x'" class="status-ico" />
              </div>
            </div>

            <div class="card-footer">
              <div class="order-badge">{{ $t('platformAdmin.plans.order') }}: {{ plan.display_order }}</div>
              <button @click="toggleActive(plan)" class="status-toggle" :class="{ active: plan.is_active }">
                {{ plan.is_active ? $t('platformAdmin.plans.active') : $t('platformAdmin.plans.draft') }}
              </button>
            </div>
          </div>

          <!-- Add plan empty card -->
          <button class="add-plan-card" @click="openCreateModal">
            <iconify-icon icon="lucide:plus" />
            <span>{{ $t('platformAdmin.plans.createFirst') }}</span>
          </button>
        </div>
      </div>
    </main>

    <!-- Create/Edit Modal -->
    <Transition name="scale">
      <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal-win large" @click.stop>
          <div class="modal-header">
            <div class="modal-title-wrap">
              <h3>{{ editingPlan ? $t('platformAdmin.plans.edit') : $t('platformAdmin.plans.new') }}</h3>
              <div class="lang-pills">
                <button v-for="l in ['ru', 'en', 'uz']" :key="l" @click="activeLang = l"
                  :class="{ active: activeLang === l }">
                  {{ l.toUpperCase() }}
                </button>
              </div>
            </div>
            <button @click="closeModal" class="close-modal"><iconify-icon icon="lucide:x" /></button>
          </div>

          <form @submit.prevent="savePlan" class="plan-form">
            <div class="form-scroll">
              <div class="form-grid">
                <div class="f-group">
                  <label>{{ $t('platformAdmin.plans.form.name') }} ({{ activeLang.toUpperCase() }})</label>
                  <input v-if="activeLang === 'ru'" v-model="planForm.name_ru" type="text" class="modern-input"
                    required />
                  <input v-if="activeLang === 'en'" v-model="planForm.name_en" type="text" class="modern-input"
                    required />
                  <input v-if="activeLang === 'uz'" v-model="planForm.name_uz" type="text" class="modern-input"
                    required />
                </div>

                <div class="f-group">
                  <label>{{ $t('platformAdmin.plans.form.slug') }}</label>
                  <input v-model="planForm.slug" type="text" class="modern-input" required
                    placeholder="example: premium" />
                </div>

                <div class="f-group">
                  <label>{{ $t('platformAdmin.plans.form.price') }}</label>
                  <input v-model.number="planForm.price" type="number" class="modern-input" required />
                </div>

                <div class="f-group">
                  <label>{{ $t('platformAdmin.plans.form.period') }}</label>
                  <input v-model.number="planForm.period_days" type="number" class="modern-input" required />
                </div>

                <div class="f-group">
                  <label>{{ $t('platformAdmin.plans.form.maxProducts') }}</label>
                  <input v-model.number="planForm.max_products" type="number" class="modern-input" />
                </div>

                <div class="f-group">
                  <label>{{ $t('platformAdmin.plans.form.maxBanners') }}</label>
                  <input v-model.number="planForm.max_banners" type="number" class="modern-input" />
                </div>

                <div class="f-group span-2">
                  <label>{{ $t('platformAdmin.plans.form.description') }} ({{ activeLang.toUpperCase() }})</label>
                  <textarea v-if="activeLang === 'ru'" v-model="planForm.description_ru" class="modern-input"
                    rows="2"></textarea>
                  <textarea v-if="activeLang === 'en'" v-model="planForm.description_en" class="modern-input"
                    rows="2"></textarea>
                  <textarea v-if="activeLang === 'uz'" v-model="planForm.description_uz" class="modern-input"
                    rows="2"></textarea>
                </div>

                <div class="f-group span-2">
                  <label>{{ $t('platformAdmin.plans.form.features') }}</label>
                  <textarea v-if="activeLang === 'ru'" v-model="features_ru_string" class="modern-input"
                    placeholder="Умный поиск, Личный кабинет, Без рекламы"></textarea>
                  <textarea v-if="activeLang === 'en'" v-model="features_en_string" class="modern-input"></textarea>
                  <textarea v-if="activeLang === 'uz'" v-model="features_uz_string" class="modern-input"></textarea>
                </div>

                <div class="f-group">
                  <label>{{ $t('platformAdmin.plans.form.sort') }}</label>
                  <input v-model.number="planForm.display_order" type="number" class="modern-input" />
                </div>

                <div v-if="planForm.is_trial" class="f-group">
                  <label>{{ $t('platformAdmin.plans.form.trialPeriod') }}</label>
                  <input v-model.number="planForm.trial_period_days" type="number" class="modern-input" required />
                </div>

                <div class="f-switches">
                  <label class="sw-row">
                    <input v-model="planForm.is_active" type="checkbox" />
                    {{ $t('platformAdmin.plans.form.isActive') }}
                  </label>
                  <label class="sw-row">
                    <input v-model="planForm.is_trial" type="checkbox" />
                    {{ $t('platformAdmin.plans.form.isTrial') }}
                  </label>
                  <label class="sw-row">
                    <input v-model="planForm.has_telegram" type="checkbox" />
                    {{ $t('platformAdmin.plans.form.hasTelegram') }}
                  </label>
                  <label class="sw-row">
                    <input v-model="planForm.can_broadcast" type="checkbox" />
                    {{ $t('platformAdmin.plans.form.canBroadcast') }}
                  </label>
                </div>
              </div>
            </div>

            <div class="modal-footer">
              <button type="button" @click="closeModal" class="btn-cancel">{{ $t('platformAdmin.plans.cancel')
                }}</button>
              <button type="submit" class="btn-save" :disabled="saving">
                <span v-if="saving" class="loader-xs"></span>
                <span v-else>{{ editingPlan ? $t('platformAdmin.plans.save') : $t('platformAdmin.plans.create')
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
const editingPlan = ref(null)
const saving = ref(false)
const activeLang = ref('ru')

const planForm = reactive({
  name_ru: '', name_en: '', name_uz: '',
  slug: '', price: 0, period_days: 30,
  description_ru: '', description_en: '', description_uz: '',
  features_ru: [], features_en: [], features_uz: [],
  is_active: true, is_trial: false, can_broadcast: false, has_telegram: false,
  display_order: 0, max_products: 0, max_banners: 1, trial_period_days: 0
})

const features_ru_string = computed({
  get: () => planForm.features_ru.join(', '),
  set: (v) => planForm.features_ru = v.split(',').map(s => s.trim()).filter(s => s)
})
const features_en_string = computed({
  get: () => planForm.features_en.join(', '),
  set: (v) => planForm.features_en = v.split(',').map(s => s.trim()).filter(s => s)
})
const features_uz_string = computed({
  get: () => planForm.features_uz.join(', '),
  set: (v) => planForm.features_uz = v.split(',').map(s => s.trim()).filter(s => s)
})

const { data: plans, pending, refresh } = useFetch(apiBase + '/platform/admin/subscription-plans', {
  lazy: true,
  watch: [token],
  headers: computed(() => ({ 'Authorization': `Bearer ${token.value}` }))
})

const handleLogout = () => { logout(); toast.success(t('auth.loggedOut')) }

const getLocalizedValue = (obj, k) => {
  if (locale.value === 'ru' && obj[k + '_ru']) return obj[k + '_ru']
  if (locale.value === 'en' && obj[k + '_en']) return obj[k + '_en']
  if (locale.value === 'uz' && obj[k + '_uz']) return obj[k + '_uz']
  return obj[k] || obj[k + '_ru'] || ''
}

const openCreateModal = () => { editingPlan.value = null; resetForm(); showModal.value = true }

const editPlan = (plan) => {
  editingPlan.value = plan
  Object.keys(planForm).forEach(k => {
    if (k.startsWith('features')) {
      planForm[k] = plan[k] ? plan[k].split(',') : []
    } else {
      planForm[k] = plan[k] ?? planForm[k]
    }
  })
  // Fallbacks for localized names if empty
  planForm.name_ru = plan.name_ru || plan.name
  planForm.description_ru = plan.description_ru || plan.description
  showModal.value = true
}

const closeModal = () => { showModal.value = false; editingPlan.value = null }

const resetForm = () => {
  Object.assign(planForm, {
    name_ru: '', name_en: '', name_uz: '',
    slug: '', price: 0, period_days: 30,
    description_ru: '', description_en: '', description_uz: '',
    features_ru: [], features_en: [], features_uz: [],
    is_active: true, is_trial: false, can_broadcast: false, has_telegram: false,
    display_order: 0, max_products: 0, max_banners: 1, trial_period_days: 0
  })
}

const savePlan = async () => {
  saving.value = true
  try {
    const body = {
      ...planForm,
      features_ru: planForm.features_ru.join(','),
      features_en: planForm.features_en.join(','),
      features_uz: planForm.features_uz.join(','),
      name: planForm.name_ru || planForm.name_en || planForm.name_uz,
      description: planForm.description_ru || planForm.description_en || planForm.description_uz
    }
    const url = editingPlan.value ? `${config.public.apiBase}/platform/admin/subscription-plans/${editingPlan.value.id}` : `${config.public.apiBase}/platform/admin/subscription-plans`
    await $fetch(url, {
      method: editingPlan.value ? 'PUT' : 'POST',
      headers: { 'Authorization': `Bearer ${token.value}` },
      body
    })
    toast.success(t('platformAdmin.plans.saved'))
    closeModal(); refresh()
  } catch (e) { toast.error(e.data?.detail || t('platformAdmin.plans.error')) } finally { saving.value = false }
}

const toggleActive = async (plan) => {
  try {
    await $fetch(`${config.public.apiBase}/platform/admin/subscription-plans/${plan.id}`, {
      method: 'PUT',
      headers: { 'Authorization': `Bearer ${token.value}` },
      body: { is_active: !plan.is_active }
    })
    refresh()
  } catch (e) { toast.error(t('platformAdmin.plans.error')) }
}

const deletePlan = async (plan) => {
  if (!confirm(t('platformAdmin.plans.deleteConfirm', { name: getLocalizedValue(plan, 'name') }))) return
  try {
    await $fetch(`${config.public.apiBase}/platform/admin/subscription-plans/${plan.id}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token.value}` }
    })
    toast.success(t('platformAdmin.plans.deleted'))
    refresh()
  } catch (e) { toast.error(t('platformAdmin.plans.error')) }
}
</script>

<style scoped>
.platform-admin-plans {
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

.nav-right {
  display: flex;
  gap: 12px;
}

.refresh-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  border: 1.5px solid #e2e8f0;
  background: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  transition: all 0.2s;
}

.refresh-btn:hover {
  border-color: #111;
}

.primary-btn {
  padding: 0 24px;
  height: 44px;
  border-radius: 12px;
  background: #111;
  color: white;
  border: none;
  font-weight: 900;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.admin-scroll {
  padding: 32px;
  flex: 1;
  overflow-y: auto;
}

.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 32px;
}

.plan-card {
  background: white;
  border-radius: 32px;
  padding: 32px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.03);
  border: 2px solid transparent;
  transition: all 0.3s;
  position: relative;
}

.plan-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.08);
}

.plan-card.inactive {
  opacity: 0.6;
  filter: grayscale(1);
}

.plan-card.trial {
  border-color: #fcd34d;
  background: linear-gradient(to bottom, #fffbeb 0%, #fff 100%);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.plan-type-icon {
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

.plan-type-icon.trial {
  background: #fef3c7;
  color: #d97706;
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

.plan-main-info {
  margin-bottom: 24px;
}

.plan-name {
  font-size: 1.5rem;
  font-weight: 950;
  color: #111;
  margin: 0 0 12px 0;
  letter-spacing: -0.5px;
}

.plan-price {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.price-val {
  font-size: 1.75rem;
  font-weight: 950;
  color: #111;
}

.price-period {
  font-size: 0.85rem;
  font-weight: 700;
  color: #94a3b8;
}

.plan-slug {
  margin-top: 8px;
}

.plan-slug code {
  background: #f8fafc;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 800;
  color: #64748b;
}

.plan-description-s {
  font-size: 0.85rem;
  color: #64748b;
  font-weight: 600;
  line-height: 1.6;
  min-height: 3.2em;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 24px;
}

.plan-limits {
  display: grid;
  gap: 12px;
  background: #f8fafc;
  padding: 20px;
  border-radius: 20px;
  margin-bottom: 24px;
}

.limit-row {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.85rem;
  font-weight: 750;
  color: #475569;
}

.limit-row iconify-icon:not(.status-ico) {
  color: #94a3b8;
  font-size: 1.1rem;
}

.limit-row strong {
  margin-left: auto;
  color: #111;
  font-weight: 900;
}

.limit-row.ok {
  color: #111;
}

.status-ico {
  margin-left: auto;
  font-size: 1.1rem;
}

.limit-row.ok .status-ico {
  color: #10b981;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1.5px dashed #f1f5f9;
  padding-top: 24px;
}

.order-badge {
  font-size: 0.75rem;
  font-weight: 850;
  color: #94a3b8;
  text-transform: uppercase;
}

.status-toggle {
  padding: 6px 14px;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 900;
  border: 1.5px solid #e2e8f0;
  background: transparent;
  cursor: pointer;
  transition: all 0.2s;
}

.status-toggle.active {
  background: #dcfce7;
  color: #166534;
  border-color: #dcfce7;
}

.add-plan-card {
  background: transparent;
  border: 2px dashed #cbd5e1;
  border-radius: 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  cursor: pointer;
  transition: all 0.2s;
  min-height: 400px;
}

.add-plan-card:hover {
  border-color: #111;
  background: #f8fafc;
  color: #111;
}

.add-plan-card iconify-icon {
  font-size: 3rem;
  color: #94a3b8;
}

.add-plan-card span {
  font-weight: 900;
  font-size: 1rem;
  color: #64748b;
}


.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(8px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.modal-win {
  background: white;
  border-radius: 32px;
  width: 100%;
  max-width: 550px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 40px 100px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.modal-win.large {
  max-width: 800px;
}

.modal-header {
  padding: 24px 32px;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title-wrap {
  display: flex;
  align-items: center;
  gap: 24px;
}

.modal-title-wrap h3 {
  font-size: 1.25rem;
  font-weight: 950;
  margin: 0;
  letter-spacing: -0.5px;
}

.close-modal {
  width: 40px;
  height: 40px;
  border: none;
  background: #f1f5f9;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  cursor: pointer;
  transition: all 0.2s;
  color: #64748b;
}

.close-modal:hover {
  background: #ef4444;
  color: white;
}

.lang-pills {
  display: flex;
  background: #f1f5f9;
  padding: 4px;
  border-radius: 10px;
}

.lang-pills button {
  padding: 6px 14px;
  border: none;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 900;
  cursor: pointer;
  background: transparent;
  color: #64748b;
  transition: all 0.2s;
}

.lang-pills button.active {
  background: white;
  color: #111;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.plan-form {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.form-scroll {
  padding: 32px;
  overflow-y: auto;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.span-2 {
  grid-column: span 2;
}

.f-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.f-group label {
  font-size: 0.8rem;
  font-weight: 850;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.modern-input {
  width: 100%;
  padding: 12px 16px;
  border-radius: 12px;
  border: 1.5px solid #e2e8f0;
  background: #f8fafc;
  font-size: 0.95rem;
  font-weight: 700;
  transition: all 0.2s;
}

.modern-input:focus {
  outline: none;
  border-color: #111;
  background: white;
  box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.05);
}

textarea.modern-input {
  resize: vertical;
  min-height: 80px;
}

.f-switches {
  grid-column: span 2;
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  padding: 24px;
  background: #f8fafc;
  border-radius: 20px;
  border: 1.5px solid #f1f5f9;
}

.sw-row {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 850;
  font-size: 0.85rem;
  color: #1e293b;
  cursor: pointer;
}

.sw-row input {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: #111;
}

.modal-footer {
  padding: 24px 32px;
  background: #f8fafc;
  border-top: 1px solid #f1f5f9;
  display: flex;
  justify-content: flex-end;
  gap: 16px;
}

.btn-cancel {
  padding: 12px 24px;
  border-radius: 14px;
  border: 1.5px solid #e2e8f0;
  background: white;
  font-weight: 900;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
  color: #64748b;
}

.btn-cancel:hover {
  background: #f1f5f9;
  color: #111;
}

.btn-save {
  padding: 12px 32px;
  border-radius: 14px;
  border: none;
  background: #111;
  color: white;
  font-weight: 900;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-save:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* Animations */
.scale-enter-active,
.scale-leave-active {
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.loading-state {
  padding: 100px 0;
  text-align: center;
}

.loader {
  width: 44px;
  height: 44px;
  border: 4px solid #f1f5f9;
  border-top-color: #111;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto;
}

.loader-xs {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
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
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .span-2 {
    grid-column: span 1;
  }

  .modal-win {
    margin-top: auto;
    border-radius: 32px 32px 0 0;
    max-height: 95vh;
  }
}
</style>
