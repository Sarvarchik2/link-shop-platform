<template>
  <div class="product-card" @click="navigateTo(productUrl)">
    <div class="product-image">
      <button class="fav-btn" :class="{ 'is-fav': isFavoriteDisplay }" @click.stop="toggleFav">
        <svg width="20" height="20" viewBox="0 0 24 24" :fill="isFavoriteDisplay ? '#EF4444' : 'none'" :stroke="isFavoriteDisplay ? '#EF4444' : '#9CA3AF'" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
        </svg>
      </button>
      <div v-if="totalStock === 0" class="sold-out-badge">SOLD OUT</div>
      <img :src="product.image_url" :alt="product.name" :class="{ 'out-of-stock': totalStock === 0 }" />
    </div>
    <div class="product-info">
      <div class="product-category">{{ product.category }}</div>
      <h3 class="product-name">{{ product.name }}</h3>
      <div class="product-footer">
        <div class="price-container">
          <div v-if="product.discount > 0" class="price-with-discount">
            <div class="product-price-discounted">${{ finalPrice.toFixed(2) }}</div>
            <div class="product-price-original">${{ product.price.toFixed(2) }}</div>
            <div class="discount-badge-small">-{{ product.discount }}%</div>
          </div>
          <div v-else class="product-price">${{ product.price.toFixed(2) }}</div>
        </div>
      </div>
      <div v-if="totalStock > 0 && totalStock <= 5" class="stock-warning">
        Only {{ totalStock }} left!
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  product: Object,
  shopSlug: String
})

const productUrl = computed(() => {
  if (props.shopSlug) {
    return `/${props.shopSlug}/products/${props.product.id}`
  }
  return `/products/${props.product.id}`
})

const { user } = useAuth()

// Calculate final price with discount
const finalPrice = computed(() => {
  if (props.product.discount > 0) {
    return props.product.price * (1 - props.product.discount / 100)
  }
  return props.product.price
})

// Calculate total stock from colors if available, otherwise use product stock
const totalStock = computed(() => {
  if (props.product.colors) {
    try {
      const colors = JSON.parse(props.product.colors)
      return colors.reduce((sum, c) => sum + (c.stock || 0), 0)
    } catch {
      return props.product.stock || 0
    }
  }
  return props.product.stock || 0
})

// Local reactive state for instant UI feedback
const isFavorite = ref(props.product.is_favorite || false)

// Only show as favorite if user is logged in AND product is favorite
const isFavoriteDisplay = computed(() => {
  if (!user.value) return false // Not logged in = always false
  return isFavorite.value
})

// Sync with prop changes (only if user is logged in)
watch(() => props.product.is_favorite, (newVal) => {
  if (user.value) {
    isFavorite.value = newVal || false
  } else {
    isFavorite.value = false
  }
})

// Watch user changes - reset favorite state when user logs out
watch(() => user.value, (newUser) => {
  if (!newUser) {
    isFavorite.value = false
  } else {
    // User logged in - sync with product state
    isFavorite.value = props.product.is_favorite || false
  }
})

const toggleFav = async () => {
  // Check if user is logged in
  if (!user.value) {
    useToast().warning('Please login to add items to favorites')
    // Save returnUrl - preserve current product page
    const returnUrl = productUrl.value
    navigateTo(`/login?returnUrl=${encodeURIComponent(returnUrl)}`)
    return
  }
  
  // Toggle immediately for instant feedback
  const previousState = isFavorite.value
  isFavorite.value = !isFavorite.value
  
  try {
    const result = await $fetch(`http://localhost:8000/products/${props.product.id}/favorite`, { method: 'POST' })
    // Sync the actual state from server
    isFavorite.value = result.is_favorite
    
    if (isFavorite.value) {
      useToast().success('Added to favorites!')
    } else {
      useToast().info('Removed from favorites')
    }
  } catch (e) {
    // Revert on error
    isFavorite.value = previousState
    useToast().error('Failed to update favorites')
    console.error(e)
  }
}
</script>

<style scoped>
.product-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0,0,0,0.08);
}

.product-image {
  position: relative;
  background: #F9FAFB;
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  mix-blend-mode: multiply;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

.fav-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  z-index: 2;
  transition: all 0.2s;
}

.fav-btn:hover {
  transform: scale(1.1);
}

.fav-btn.is-fav {
  background: #FEE2E2;
}

.fav-btn.is-fav:hover {
  background: #FECACA;
}

.sold-out-badge {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(239, 68, 68, 0.95);
  color: white;
  padding: 12px 17px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 18px;
  letter-spacing: 1px;
  z-index: 3;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

.out-of-stock {
  opacity: 0.4;
  filter: grayscale(100%);
}

.product-info {
  padding: 16px;
}

.product-category {
  font-size: 0.75rem;
  color: #9CA3AF;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.product-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: #111;
  margin-bottom: 12px;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price-container {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.product-price {
  font-size: 1.125rem;
  font-weight: 800;
  color: #111;
}

.price-with-discount {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.product-price-discounted {
  font-size: 1.125rem;
  font-weight: 800;
  color: #EF4444;
}

.product-price-original {
  font-size: 0.875rem;
  font-weight: 600;
  color: #9CA3AF;
  text-decoration: line-through;
}

.discount-badge-small {
  padding: 4px 8px;
  background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
  color: white;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.75rem;
  box-shadow: 0 2px 6px rgba(239, 68, 68, 0.3);
}

.stock-warning {
  margin-top: 8px;
  padding: 6px 12px;
  background: #FEF3C7;
  color: #92400E;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
  text-align: center;
}
</style>
