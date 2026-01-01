<template>
  <div class="checkout-page">
    <!-- Desktop Header -->
    <AppHeader class="desktop-header" />

    <!-- Mobile Header -->
    <header class="checkout-header mobile-header">
      <button @click="$router.back()" class="back-btn">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5M12 19l-7-7 7-7" />
        </svg>
      </button>
      <h1 class="page-title">{{ $t('checkout.title') }}</h1>
      <div class="spacer"></div>
    </header>

    <main class="checkout-content">
      <div class="checkout-layout">
        <!-- Left Column - Form -->
        <div class="checkout-form">
          <!-- Delivery Info -->
          <section class="checkout-section">
            <h2 class="section-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                <circle cx="12" cy="10" r="3"></circle>
              </svg>
              {{ $t('checkout.sections.delivery') }}
            </h2>

            <div class="form-row">
              <div class="form-group">
                <label class="form-label">{{ $t('checkout.form.name') }}</label>
                <input v-model="form.recipient_name" type="text" class="form-input"
                  :placeholder="$t('checkout.form.namePlaceholder')" required />
              </div>

              <div class="form-group">
                <label class="form-label">{{ $t('checkout.form.phone') }}</label>
                <input v-model="form.delivery_phone" type="tel" class="form-input"
                  :placeholder="$t('checkout.form.phonePlaceholder')" required />
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">{{ $t('checkout.form.city') }}</label>
              <select v-model="form.delivery_city" class="form-input" required>
                <option value="">{{ $t('checkout.form.selectCity') }}</option>
                <option value="Toshkent">Toshkent</option>
                <option value="Samarqand">Samarqand</option>
                <option value="Buxoro">Buxoro</option>
                <option value="Namangan">Namangan</option>
                <option value="Andijon">Andijon</option>
                <option value="Farg'ona">Farg'ona</option>
                <option value="Boshqa">Boshqa</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">{{ $t('checkout.form.address') }}</label>
              <textarea v-model="form.delivery_address" class="form-input" rows="3"
                :placeholder="$t('checkout.form.addressPlaceholder')" required></textarea>
            </div>
          </section>

          <!-- Payment Method -->
          <section class="checkout-section">
            <h2 class="section-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
                <line x1="1" y1="10" x2="23" y2="10"></line>
              </svg>
              {{ $t('checkout.sections.payment') }}
            </h2>

            <div class="payment-options">
              <label class="payment-option" :class="{ active: form.payment_method === 'cash' }">
                <input type="radio" v-model="form.payment_method" value="cash" />
                <div class="payment-icon">💵</div>
                <div class="payment-info">
                  <span class="payment-name">{{ $t('checkout.payment.cash.title') }}</span>
                  <span class="payment-desc">{{ $t('checkout.payment.cash.desc') }}</span>
                </div>
                <div class="payment-check">
                  <svg v-if="form.payment_method === 'cash'" width="20" height="20" viewBox="0 0 24 24"
                    fill="currentColor">
                    <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
                  </svg>
                </div>
              </label>

              <label class="payment-option" :class="{ active: form.payment_method === 'card' }">
                <input type="radio" v-model="form.payment_method" value="card" />
                <div class="payment-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
                    <line x1="1" y1="10" x2="23" y2="10"></line>
                  </svg>
                </div>
                <div class="payment-info">
                  <span class="payment-name">{{ $t('checkout.payment.card.title') }}</span>
                  <span class="payment-desc">{{ $t('checkout.payment.card.desc') }}</span>
                </div>
                <div class="payment-check">
                  <svg v-if="form.payment_method === 'card'" width="20" height="20" viewBox="0 0 24 24"
                    fill="currentColor">
                    <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
                  </svg>
                </div>
              </label>
            </div>
          </section>

          <!-- Notes -->
          <section class="checkout-section">
            <h2 class="section-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <polyline points="10 9 9 9 8 9"></polyline>
              </svg>
              {{ $t('checkout.sections.notes') }}
            </h2>
            <textarea v-model="form.notes" class="form-input" rows="3"
              :placeholder="$t('checkout.form.notesPlaceholder')"></textarea>
          </section>
        </div>

        <!-- Right Column - Order Summary -->
        <div class="checkout-summary">
          <div class="summary-card">
            <h2 class="summary-title">{{ $t('checkout.sections.summary') }}</h2>

            <div class="summary-items">
              <div v-for="item in items" :key="item.cartKey" class="summary-item">
                <div class="item-image">
                  <img :src="item.image_url" :alt="item.name" />
                </div>
                <div class="item-details">
                  <div class="item-name">{{ item.name }}</div>
                  <div class="item-meta">
                    <span v-if="item.selectedColor">{{ $t('admin.color') }}: {{ item.selectedColor.name }}</span>
                    <span v-if="item.selectedSize">{{ $t('admin.size') }}: {{ item.selectedSize }}</span>
                  </div>
                  <div class="item-price">${{ (item.price * item.quantity).toFixed(2) }}</div>
                </div>
                <div class="item-quantity">x{{ item.quantity }}</div>
              </div>
            </div>

            <div class="summary-totals">
              <div class="total-row">
                <span class="total-label">{{ $t('checkout.summary.total') }}:</span>
                <span class="total-value">${{ totalPrice.toFixed(2) }}</span>
              </div>
            </div>

            <button @click="placeOrder" class="btn-place-order" :disabled="loading || !isFormValid">
              {{ loading ? $t('checkout.summary.processing') : $t('checkout.summary.placeOrder') }}
            </button>
          </div>
        </div>
      </div>
    </main>

    <footer class="checkout-footer mobile-footer">
      <button @click="placeOrder" class="btn-place-order" :disabled="loading || !isFormValid">
        {{ loading ? $t('checkout.summary.processing') : $t('checkout.summary.placeOrder') }}
      </button>
    </footer>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'auth'
})

const route = useRoute()
const shopSlug = route.params.shop
const { t } = useI18n()

const { items, totalPrice, clearCart } = useCart()
const { token, user } = useAuth()
const config = useRuntimeConfig()

const loading = ref(false)

const form = reactive({
  recipient_name: '',
  delivery_phone: '',
  delivery_city: '',
  delivery_address: '',
  payment_method: 'cash',
  notes: ''
})

// Pre-fill with user data if available
onMounted(() => {
  if (user.value) {
    form.recipient_name = `${user.value.first_name} ${user.value.last_name}`.trim()
    form.delivery_phone = user.value.phone
  }
})

const isFormValid = computed(() => {
  return form.recipient_name && form.delivery_phone && form.delivery_city && form.delivery_address && items.value.length > 0
})

const toast = useToast()

const placeOrder = async () => {
  if (!isFormValid.value) {
    toast.warning(t('checkout.validation.required'))
    return
  }

  loading.value = true

  try {
    const orderItems = items.value.map(item => ({
      product_id: item.id,
      quantity: item.quantity,
      selected_color: item.selectedColor?.name || null,
      selected_size: item.selectedSize || null
    }))

    await $fetch(`${config.public.apiBase}/orders?shop_slug=${shopSlug}`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: {
        items: orderItems,
        ...form
      }
    })

    clearCart()
    toast.success(t('checkout.success'))
    navigateTo(`/${shopSlug}/orders`)
  } catch (e) {
    console.error(e)
    toast.error(t('checkout.error'))
  } finally {
    loading.value = false
  }
}

// Redirect if cart is empty
if (items.value.length === 0) {
  navigateTo(`/${shopSlug}/cart`)
}
</script>

<style scoped>
/* Copy styles from checkout.vue - they are the same */
.checkout-page {
  min-height: 100vh;
  background: #F5F5F5;
}

.desktop-header {
  display: none;
}

.mobile-header {
  display: flex;
}

.checkout-header {
  background: white;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  border-bottom: 1px solid #E5E7EB;
}

.back-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-title {
  font-size: 1.25rem;
  font-weight: 700;
  flex: 1;
}

.spacer {
  width: 40px;
}

.checkout-content {
  padding: 24px 16px;
  max-width: 1200px;
  margin: 0 auto;
}

.checkout-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}

.checkout-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.checkout-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.section-title {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #111;
}

.form-input {
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 1rem;
  font-family: inherit;
  transition: all 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #111;
}

.payment-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.payment-option {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.payment-option:hover {
  border-color: #111;
}

.payment-option.active {
  border-color: #111;
  background: #F9FAFB;
}

.payment-option input {
  display: none;
}

.payment-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F3F4F6;
  border-radius: 12px;
}

.payment-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.payment-name {
  font-weight: 600;
  color: #111;
}

.payment-desc {
  font-size: 0.875rem;
  color: #6B7280;
}

.payment-check {
  color: #10B981;
}

.checkout-summary {
  position: sticky;
  top: 24px;
  height: fit-content;
}

.summary-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.summary-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 20px;
}

.summary-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
  max-height: 400px;
  overflow-y: auto;
}

.summary-item {
  display: flex;
  gap: 12px;
}

.item-image {
  width: 80px;
  height: 80px;
  border-radius: 12px;
  overflow: hidden;
  background: #F9FAFB;
  flex-shrink: 0;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.item-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.item-name {
  font-weight: 600;
  font-size: 0.875rem;
}

.item-meta {
  font-size: 0.75rem;
  color: #6B7280;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.item-price {
  font-weight: 700;
  color: #111;
  font-size: 0.875rem;
}

.item-quantity {
  font-weight: 600;
  color: #6B7280;
  font-size: 0.875rem;
}

.summary-totals {
  padding-top: 20px;
  border-top: 2px solid #E5E7EB;
  margin-bottom: 20px;
}

.total-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.total-label {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111;
}

.total-value {
  font-size: 1.5rem;
  font-weight: 900;
  color: #111;
}

.btn-place-order {
  width: 100%;
  padding: 16px;
  background: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-place-order:hover:not(:disabled) {
  background: #000;
  transform: translateY(-2px);
}

.btn-place-order:disabled {
  background: #9CA3AF;
  cursor: not-allowed;
}

.checkout-footer {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  padding: 16px;
  border-top: 1px solid #E5E7EB;
  box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.1);
}

.mobile-footer {
  display: block;
}

@media (min-width: 1024px) {
  .desktop-header {
    display: block;
  }

  .mobile-header,
  .mobile-footer {
    display: none;
  }

  .checkout-layout {
    grid-template-columns: 2fr 1fr;
  }

  .form-row {
    grid-template-columns: 1fr 1fr;
  }
}
</style>
