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

          <!-- Order Notes -->
          <section class="checkout-section">
            <h2 class="section-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
              </svg>
              {{ $t('checkout.sections.notes') }}
            </h2>
            <textarea v-model="form.notes" class="form-input" rows="2"
              :placeholder="$t('checkout.form.notesPlaceholder')"></textarea>
          </section>
        </div>

        <!-- Right Column - Summary (Desktop) -->
        <div class="checkout-summary">
          <div class="summary-card">
            <h2 class="summary-title">{{ $t('checkout.sections.summary') }}</h2>

            <div class="summary-items">
              <div v-for="item in items" :key="item.cartKey" class="summary-item">
                <img :src="item.image_url" :alt="item.name" class="summary-img" />
                <div class="summary-info">
                  <span class="summary-name">{{ item.name }}</span>
                  <span class="summary-meta">
                    {{ item.selectedColor?.name || '' }} {{ item.selectedSize || '' }} × {{ item.quantity }}
                  </span>
                </div>
                <span class="summary-price">${{ (item.price * item.quantity).toFixed(2) }}</span>
              </div>
            </div>

            <div class="summary-totals">
              <div class="summary-row">
                <span>{{ $t('checkout.summary.subtotal') }}</span>
                <span>${{ totalPrice.toFixed(2) }}</span>
              </div>
              <div class="summary-row">
                <span>{{ $t('checkout.summary.shipping') }}</span>
                <span class="free">{{ $t('checkout.summary.free') }}</span>
              </div>
              <div class="summary-row total">
                <span>{{ $t('checkout.summary.total') }}</span>
                <span>${{ totalPrice.toFixed(2) }}</span>
              </div>
            </div>

            <!-- Desktop Place Order Button -->
            <button @click="placeOrder" class="btn-place-order desktop-btn" :disabled="loading || !isFormValid">
              {{ loading ? $t('checkout.summary.processing') : $t('checkout.summary.placeOrder') }}
            </button>
          </div>
        </div>
      </div>

      <!-- Mobile Order Summary -->
      <section class="checkout-section order-summary-mobile">
        <h2 class="section-title">{{ $t('checkout.sections.summary') }}</h2>

        <div class="summary-items">
          <div v-for="item in items" :key="item.cartKey" class="summary-item">
            <img :src="item.image_url" :alt="item.name" class="summary-img" />
            <div class="summary-info">
              <span class="summary-name">{{ item.name }}</span>
              <span class="summary-meta">
                {{ item.selectedColor?.name || '' }} {{ item.selectedSize || '' }} × {{ item.quantity }}
              </span>
            </div>
            <span class="summary-price">${{ (item.price * item.quantity).toFixed(2) }}</span>
          </div>
        </div>

        <div class="summary-totals">
          <div class="summary-row">
            <span>{{ $t('checkout.summary.subtotal') }}</span>
            <span>${{ totalPrice.toFixed(2) }}</span>
          </div>
          <div class="summary-row">
            <span>{{ $t('checkout.summary.shipping') }}</span>
            <span class="free">{{ $t('checkout.summary.free') }}</span>
          </div>
          <div class="summary-row total">
            <span>{{ $t('checkout.summary.total') }}</span>
            <span>${{ totalPrice.toFixed(2) }}</span>
          </div>
        </div>
      </section>
    </main>

    <!-- Mobile Footer -->
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

const { t } = useI18n()
const { items, totalPrice, clearCart } = useCart()
const { token, user } = useAuth()

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

    // Get shop_slug from first item if available
    const shopSlug = items.value[0]?.shopSlug || null
    const url = shopSlug
      ? `http://localhost:8000/orders?shop_slug=${shopSlug}`
      : 'http://localhost:8000/orders'

    await $fetch(url, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: {
        items: orderItems,
        ...form
      }
    })

    clearCart()
    toast.success(t('checkout.success'))
    navigateTo('/orders')
  } catch (e) {
    console.error(e)
    toast.error(t('checkout.error'))
  } finally {
    loading.value = false
  }
}

// Redirect if cart is empty
// if (items.value.length === 0) {
//   navigateTo('/cart')
// }
</script>

<style scoped>
.checkout-page {
  min-height: 100vh;
  background: #F5F5F5;
}

/* Desktop header hidden on mobile */
.desktop-header {
  display: none;
}

/* Mobile header */
.mobile-header {
  display: flex;
}

.checkout-header {
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: white;
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid #f0f0f0;
}

.back-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  cursor: pointer;
  color: #111;
  border-radius: 12px;
}

.page-title {
  font-size: 1.25rem;
  font-weight: 700;
}

.spacer {
  width: 44px;
}

.checkout-content {
  padding: 16px;
  padding-bottom: 120px;
  max-width: 1200px;
  margin: 0 auto;
}

.checkout-layout {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.checkout-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Desktop Summary - hidden on mobile */
.checkout-summary {
  display: none;
}

.checkout-section {
  background: white;
  border-radius: 16px;
  padding: 20px;
}

.section-title {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #111;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #6B7280;
  margin-bottom: 6px;
}

.form-input {
  width: 100%;
  padding: 14px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.2s;
  background: #F9FAFB;
}

.form-input:focus {
  outline: none;
  border-color: #111;
  background: white;
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

.payment-option input {
  display: none;
}

.payment-option.active {
  border-color: #111;
  background: #F9FAFB;
}

.payment-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.payment-icon svg {
  width: 24px;
  height: 24px;
}

.payment-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.payment-name {
  font-weight: 600;
  color: #111;
}

.payment-desc {
  font-size: 0.75rem;
  color: #9CA3AF;
}

.payment-check {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #111;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Mobile Order Summary */
.order-summary-mobile {
  display: block;
  background: #FAFAFA;
  border: 2px solid #E5E7EB;
  margin-top: 16px;
}

.summary-title {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: 20px;
  color: #111;
}

.summary-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #E5E7EB;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.summary-img {
  width: 50px;
  height: 50px;
  object-fit: contain;
  background: white;
  border-radius: 8px;
  padding: 4px;
}

.summary-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.summary-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #111;
}

.summary-meta {
  font-size: 0.75rem;
  color: #9CA3AF;
}

.summary-price {
  font-weight: 600;
}

.summary-totals {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  color: #6B7280;
}

.summary-row.total {
  font-size: 1.125rem;
  font-weight: 700;
  color: #111;
  padding-top: 12px;
  border-top: 1px solid #E5E7EB;
}

.summary-row .free {
  color: #10B981;
  font-weight: 600;
}

/* Mobile Footer */
.checkout-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px 20px;
  padding-bottom: calc(16px + env(safe-area-inset-bottom));
  background: white;
  border-top: 1px solid #E5E7EB;
  z-index: 100;
}

.btn-place-order {
  width: 100%;
  padding: 18px;
  background: #111;
  color: white;
  border: none;
  border-radius: 30px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  letter-spacing: 0.5px;
}

.btn-place-order:hover:not(:disabled) {
  background: #000;
  transform: translateY(-2px);
}

.btn-place-order:disabled {
  background: #9CA3AF;
  cursor: not-allowed;
}

.desktop-btn {
  display: none;
}

/* Desktop Styles */
@media (min-width: 768px) {
  .desktop-header {
    display: block;
  }

  .mobile-header {
    display: none;
  }

  .mobile-footer {
    display: none;
  }

  .order-summary-mobile {
    display: none;
  }

  .checkout-content {
    padding: 40px;
    padding-bottom: 40px;
  }

  .checkout-layout {
    flex-direction: row;
    gap: 40px;
    align-items: flex-start;
  }

  .checkout-form {
    flex: 1;
    min-width: 0;
  }

  .checkout-summary {
    display: block;
    width: 400px;
    flex-shrink: 0;
    position: sticky;
    top: 100px;
  }

  .summary-card {
    background: white;
    border-radius: 24px;
    padding: 28px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  }

  .checkout-section {
    border-radius: 20px;
    padding: 28px;
  }

  .form-row {
    grid-template-columns: repeat(2, 1fr);
  }

  .desktop-btn {
    display: block;
    margin-top: 24px;
  }
}

@media (min-width: 1024px) {
  .checkout-summary {
    width: 420px;
  }
}
</style>
