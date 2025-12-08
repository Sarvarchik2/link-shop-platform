<template>
  <div class="cart-page">
    <!-- Desktop Header -->
    <AppHeader class="desktop-header" />
    
    <!-- Mobile Header -->
    <header class="cart-header mobile-header">
        <button @click="$router.back()" class="back-btn">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
        </button>
      <h1 class="cart-title">Savatcha</h1>
      <div class="header-spacer"></div>
    </header>

    <main class="cart-content">
      <div v-if="items.length === 0" class="empty-cart">
        <div class="empty-icon">
          <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
          </svg>
        </div>
        <h2 class="empty-title">Savatchangiz bo'sh</h2>
        <p class="empty-text">Boshlash uchun mahsulotlar qo'shing</p>
        <NuxtLink to="/products" class="btn-shop">Xaridni davom ettirish</NuxtLink>
      </div>

      <div v-else class="cart-items">
        <div 
          v-for="item in items" 
          :key="item.cartKey" 
          class="cart-item"
          :class="{ swiped: swipedItem === item.cartKey }"
        >
          <div 
            class="item-content" 
            @touchstart="handleTouchStart($event, item.cartKey)"
            @touchmove="handleTouchMove($event, item.cartKey)"
            @touchend="handleTouchEnd"
            :style="getSwipeStyle(item.cartKey)"
          >
            <div class="item-image">
              <img :src="item.image_url" :alt="item.name" />
            </div>
            <div class="item-info">
              <h3 class="item-name">{{ item.name }}</h3>
              <p class="item-meta">
                {{ item.brand }}
                <span v-if="item.selectedColor"> · {{ item.selectedColor.name }}</span>
                <span v-if="item.selectedSize"> · {{ item.selectedSize }}</span>
              </p>
              <p class="item-price">${{ item.price?.toFixed(2) }}</p>
            </div>
            <div class="item-controls">
              <div class="item-quantity">
                <button class="qty-btn" @click="updateQuantity(item.cartKey, -1)">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="8" y1="12" x2="16" y2="12"/>
                  </svg>
                </button>
                <span class="qty-value">{{ item.quantity }}</span>
                <button class="qty-btn" @click="updateQuantity(item.cartKey, 1)">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="8" x2="12" y2="16"/>
                    <line x1="8" y1="12" x2="16" y2="12"/>
                  </svg>
                </button>
              </div>
              <!-- Desktop delete button -->
              <button class="delete-btn-desktop" @click="removeItem(item.cartKey)" title="O'chirish">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
              </button>
            </div>
          </div>
          <!-- Mobile swipe delete button -->
          <button class="delete-btn-mobile" @click="removeItem(item.cartKey)">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
          </button>
        </div>
      </div>
    </main>

    <footer v-if="items.length > 0" class="cart-footer">
      <div class="total-section">
        <span class="total-label">Jami</span>
        <span class="total-price">${{ totalPrice.toFixed(2) }}</span>
      </div>
      <button @click="handleCheckout" class="btn-checkout">BUYURTMA BERISH</button>
    </footer>
  </div>
</template>

<script setup>
const { items, removeItem, updateQuantity, totalPrice, clearCart } = useCart()
const { token } = useAuth()

const swipedItem = ref(null)
const swipeOffset = ref({})
let touchStartX = 0
let currentTouchX = 0
let isSwiping = false

const handleTouchStart = (e, cartKey) => {
  touchStartX = e.touches[0].clientX
  currentTouchX = touchStartX
  isSwiping = true
  
  // If another item is swiped, close it
  if (swipedItem.value && swipedItem.value !== cartKey) {
    swipedItem.value = null
    swipeOffset.value = {}
  }
}

const handleTouchMove = (e, cartKey) => {
  if (!isSwiping) return
  
  currentTouchX = e.touches[0].clientX
  const diff = touchStartX - currentTouchX
  
  // Only allow left swipe (positive diff)
  if (diff > 0) {
    // Limit the swipe distance
    const offset = Math.min(diff, 80)
    swipeOffset.value = { [cartKey]: offset }
  } else if (diff < -20 && swipedItem.value === cartKey) {
    // Closing swipe
    swipeOffset.value = { [cartKey]: Math.max(80 + diff, 0) }
  }
}

const handleTouchEnd = () => {
  if (!isSwiping) return
  isSwiping = false
  
  const diff = touchStartX - currentTouchX
  const currentKey = Object.keys(swipeOffset.value)[0]
  
  if (diff > 40) {
    // Snap to open
    swipedItem.value = currentKey
    swipeOffset.value = { [currentKey]: 80 }
  } else if (diff < -20) {
    // Snap to close
    swipedItem.value = null
    swipeOffset.value = {}
  } else {
    // Return to previous state
    if (swipedItem.value === currentKey) {
      swipeOffset.value = { [currentKey]: 80 }
    } else {
      swipeOffset.value = {}
    }
  }
}

const getSwipeStyle = (cartKey) => {
  const offset = swipeOffset.value[cartKey] || 0
  return {
    transform: `translateX(-${offset}px)`,
    transition: isSwiping ? 'none' : 'transform 0.3s ease'
  }
}

const toast = useToast()

const handleCheckout = () => {
  if (!token.value) {
    toast.warning('Buyurtma berish uchun tizimga kiring')
    navigateTo('/login')
    return
  }

  if (items.value.length === 0) {
    toast.warning('Savatchangiz bo\'sh')
    return
  }
  
  navigateTo('/checkout')
}
</script>

<style scoped>
.cart-page {
  min-height: 100vh;
  background: #F5F5F5;
  display: flex;
  flex-direction: column;
}

/* Desktop header hidden on mobile */
.desktop-header {
  display: none;
}

/* Mobile header */
.mobile-header {
  display: flex;
}

.cart-header {
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
  transition: background 0.2s;
}

.back-btn:hover {
  background: #f5f5f5;
}

.cart-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111;
}

.header-spacer {
  width: 44px;
}

.cart-content {
  flex: 1;
  padding: 16px;
  padding-bottom: 140px;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

.empty-cart {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 20px;
  margin-top: 20px;
}

.empty-icon {
  color: #D1D5DB;
  margin-bottom: 24px;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 8px;
}

.empty-text {
  color: #9CA3AF;
  margin-bottom: 24px;
}

.btn-shop {
  display: inline-block;
  padding: 14px 32px;
  background: #111;
  color: white;
  border-radius: 30px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-shop:hover {
  background: #000;
  transform: translateY(-2px);
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.cart-item {
  position: relative;
  overflow: hidden;
  border-radius: 16px;
  background: #F87171;
}

.item-content {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: white;
  border-radius: 16px;
  position: relative;
  z-index: 1;
}

.delete-btn-mobile {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 80px;
  background: #F87171;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  z-index: 0;
}

/* Hide mobile delete on desktop, show on mobile */
@media (min-width: 769px) {
  .delete-btn-mobile {
    display: none;
  }
  
  .item-content {
    transform: none !important;
  }
}

.delete-btn-desktop {
  display: none;
  width: 40px;
  height: 40px;
  background: #FEE2E2;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  align-items: center;
  justify-content: center;
  color: #EF4444;
  transition: all 0.2s;
  flex-shrink: 0;
}

.delete-btn-desktop:hover {
  background: #FECACA;
  color: #DC2626;
}

@media (min-width: 769px) {
  .delete-btn-desktop {
    display: flex;
  }
}

.item-image {
  width: 80px;
  height: 80px;
  background: #F9FAFB;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  padding: 8px;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  mix-blend-mode: multiply;
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-name {
  font-size: 1rem;
  font-weight: 600;
  color: #111;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.item-meta {
  font-size: 0.8rem;
  color: #9CA3AF;
  margin-bottom: 6px;
}

.item-price {
  font-size: 1rem;
  font-weight: 700;
  color: #111;
}

.item-controls {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-shrink: 0;
}

.item-quantity {
  display: flex;
  align-items: center;
  gap: 12px;
}

.qty-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  cursor: pointer;
  color: #9CA3AF;
  transition: color 0.2s;
}

.qty-btn:hover {
  color: #111;
}

.qty-value {
  min-width: 24px;
  text-align: center;
  font-weight: 600;
  font-size: 1rem;
}

.cart-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  padding: 20px;
  border-top: 1px solid #E5E7EB;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  z-index: 100;
}

.total-section {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.total-label {
  font-size: 0.875rem;
  color: #9CA3AF;
}

.total-price {
  font-size: 1.5rem;
  font-weight: 800;
  color: #111;
}

.btn-checkout {
  padding: 16px 40px;
  background: #111;
  color: white;
  border: none;
  border-radius: 30px;
  font-weight: 700;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  letter-spacing: 0.5px;
}

.btn-checkout:hover {
  background: #000;
  transform: translateY(-2px);
}

/* Desktop improvements */
@media (min-width: 769px) {
  .desktop-header {
    display: block;
  }
  
  .mobile-header {
    display: none;
  }
  
  .cart-page {
    padding-bottom: 0;
  }
  
  .cart-content {
    padding: 40px;
    padding-bottom: 140px;
    max-width: 900px;
  }
  
  .cart-footer {
    padding: 24px 40px;
    max-width: 940px;
    left: 50%;
    transform: translateX(-50%);
    border-radius: 20px 20px 0 0;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.08);
  }
  
  .item-content {
    padding: 20px;
    gap: 24px;
  }
  
  .item-image {
    width: 100px;
    height: 100px;
  }
  
  .item-name {
    font-size: 1.125rem;
  }
  
  .cart-item {
    transition: box-shadow 0.2s;
  }
  
  .cart-item:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  }
  
  .empty-cart {
    margin-top: 40px;
    padding: 80px 40px;
  }
}

/* Mobile swipe hint */
@media (max-width: 768px) {
  .cart-item:first-child::after {
    content: '';
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    width: 4px;
    height: 40px;
    background: #E5E7EB;
    border-radius: 2px;
    opacity: 0;
    animation: swipeHint 2s ease-in-out 1s;
  }
  
  @keyframes swipeHint {
    0%, 100% { opacity: 0; transform: translateY(-50%) translateX(0); }
    50% { opacity: 1; transform: translateY(-50%) translateX(-10px); }
  }
}
</style>
