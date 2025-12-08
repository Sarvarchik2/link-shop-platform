<template>
  <div class="product-page">
    <AppHeader />
    
    <main class="container py-8">
      <div v-if="pending" class="text-center py-12">
        <div class="loading-spinner"></div>
        <p class="mt-4 text-gray-400">Yuklanmoqda...</p>
      </div>

      <div v-else-if="product" class="product-content">
        <div class="product-gallery">
          <div class="main-image">
            <img :src="selectedImage || product.image_url" :alt="product.name" />
          </div>
          <div v-if="productImages.length > 1" class="thumbnail-images">
            <div 
              v-for="(img, index) in productImages" 
              :key="index" 
              class="thumbnail"
              :class="{ active: selectedImage === img }"
              @click="selectedImage = img"
            >
              <img :src="img" :alt="`${product.name} ${index + 1}`" />
            </div>
          </div>
        </div>

        <div class="product-details">
          <div class="product-category">{{ product.category }}</div>
          <h1 class="product-title">{{ product.name }}</h1>

          <div class="product-price-section">
            <div class="product-price">${{ product.price.toFixed(2) }}</div>
            <!-- Stock badge based on selected variant -->
            <template v-if="productVariants.length > 0">
              <div v-if="totalColorStock === 0" class="stock-badge out-of-stock">TUGADI</div>
              <div v-else-if="selectedColor && selectedSize && selectedVariant">
                <div v-if="selectedVariant.stock === 0" class="stock-badge out-of-stock">{{ selectedSize }} / {{ selectedColor.name }} - TUGADI</div>
                <div v-else-if="selectedVariant.stock <= 5" class="stock-badge low-stock">{{ selectedSize }} / {{ selectedColor.name }}: Faqat {{ selectedVariant.stock }} ta qoldi!</div>
                <div v-else class="stock-badge in-stock">{{ selectedSize }} / {{ selectedColor.name }}: Mavjud ({{ selectedVariant.stock }})</div>
              </div>
              <div v-else-if="selectedColor && !selectedSize" class="stock-badge select-color">Mavjudligini ko'rish uchun o'lchamni tanlang</div>
              <div v-else-if="!selectedColor && selectedSize" class="stock-badge select-color">Mavjudligini ko'rish uchun rangni tanlang</div>
              <div v-else class="stock-badge select-color">Mavjudligini ko'rish uchun o'lcham va rangni tanlang</div>
            </template>
            <!-- Stock badge for products without variants -->
            <template v-else>
            <div v-if="product.stock === 0" class="stock-badge out-of-stock">TUGADI</div>
            <div v-else-if="product.stock <= 5" class="stock-badge low-stock">Faqat {{ product.stock }} ta qoldi!</div>
            <div v-else class="stock-badge in-stock">Mavjud ({{ product.stock }})</div>
            </template>
          </div>

          <div v-if="productColors.length > 0" class="color-selector">
            <h3 class="section-title">
              Rangni tanlang
              <span v-if="productSizes.length > 0" class="required-badge">*</span>
            </h3>
            <div class="colors">
              <button 
                v-for="color in productColors" 
                :key="color.name" 
                class="color-btn"
                :class="{ active: selectedColor?.name === color.name, 'out-of-stock': color.stock === 0 }"
                :style="{ '--color': color.hex }"
                @click="selectColor(color)"
                :disabled="color.stock === 0"
                :title="color.stock === 0 ? 'Tugagan' : `${color.name} (${color.stock} ta mavjud)`"
              >
                <span class="color-swatch"></span>
                <span class="color-name">{{ color.name }}</span>
                <span v-if="color.stock === 0" class="color-oos">✕</span>
              </button>
            </div>
          </div>

          <div v-if="productSizes.length > 0" class="size-selector">
            <h3 class="section-title">
              O'lchamni tanlang
              <span v-if="productColors.length > 0" class="required-badge">*</span>
            </h3>
            <div class="sizes">
              <button 
                v-for="size in productSizes" 
                :key="size.name || size" 
                class="size-btn"
                :class="{ active: selectedSize === (size.name || size), 'out-of-stock': size.stock === 0 }"
                @click="selectSize(size)"
                :disabled="size.stock === 0"
                :title="size.stock === 0 ? 'Tugagan' : `${size.name || size} (${size.stock || 'mavjud'})`"
              >
                {{ size.name || size }}
                <span v-if="size.stock === 0" class="size-oos">✕</span>
              </button>
            </div>
          </div>

          <div class="product-description">
            <h3 class="section-title">Tavsif</h3>
            <p>{{ product.description }}</p>
          </div>

          <div class="product-meta">
            <div class="meta-item">
              <span class="meta-label">Brend:</span>
              <span class="meta-value">{{ product.brand }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Kategoriya:</span>
              <span class="meta-value">{{ product.category }}</span>
            </div>
          </div>

          <div class="product-actions">
            <button 
              @click="addToCart" 
              class="btn-add-cart"
              :disabled="!canAddToCart"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
              </svg>
              {{ buttonText }}
            </button>
            <button @click="toggleFavorite" class="btn-favorite" :class="{ active: product.is_favorite }">
              <svg width="20" height="20" viewBox="0 0 24 24" :fill="product.is_favorite ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="2">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
const route = useRoute()
const { addItem } = useCart()
const { user } = useAuth()

const { data: product, pending, refresh } = await useFetch(`http://localhost:8000/products/${route.params.id}`, {
  server: false
})

const selectedImage = ref(null)
const selectedSize = ref(null)
const selectedColor = ref(null)

const productImages = computed(() => {
  if (!product.value) return []
  try {
    const images = product.value.images ? JSON.parse(product.value.images) : []
    return images.length > 0 ? images : [product.value.image_url]
  } catch {
    return [product.value.image_url]
  }
})

// Parse variants (new format) or fallback to sizes/colors (legacy)
const productVariants = computed(() => {
  if (!product.value) return []
  try {
    // New format: variants
    if (product.value.variants) {
      return JSON.parse(product.value.variants)
    }
    // Legacy format: sizes + colors
    if (product.value.sizes && product.value.colors) {
      const sizes = JSON.parse(product.value.sizes)
      const colors = JSON.parse(product.value.colors)
      const variants = []
      sizes.forEach(size => {
        const sizeName = typeof size === 'string' ? size : (size.name || size)
        colors.forEach(color => {
          const colorObj = typeof color === 'string' ? { name: color, hex: '#000000', stock: 0 } : color
          variants.push({
            size: sizeName,
            color: colorObj.name || color,
            colorHex: colorObj.hex || '#000000',
            stock: colorObj.stock || 0
          })
        })
      })
      return variants
    }
    return []
  } catch {
    return []
  }
})

// Get unique sizes from variants
const productSizes = computed(() => {
  const sizes = [...new Set(productVariants.value.map(v => v.size).filter(Boolean))]
  return sizes
})

// Get unique colors from variants
const productColors = computed(() => {
  const colorMap = new Map()
  productVariants.value.forEach(v => {
    if (v.color) {
      if (!colorMap.has(v.color)) {
        // Get colorHex from first variant with this color, with fallback
        const firstVariant = productVariants.value.find(v2 => v2.color === v.color)
        const hex = firstVariant?.colorHex || v.colorHex || getDefaultColorHex(v.color)
        colorMap.set(v.color, {
          name: v.color,
          hex: hex,
          stock: 0 // Will calculate from variants
        })
      }
    }
  })
  // Calculate stock for each color
  colorMap.forEach((color, colorName) => {
    color.stock = productVariants.value
      .filter(v => v.color === colorName)
      .reduce((sum, v) => sum + (v.stock || 0), 0)
  })
  return Array.from(colorMap.values())
})

// Helper function to get default hex for common color names
const getDefaultColorHex = (colorName) => {
  const colorMap = {
    'black': '#000000',
    'white': '#FFFFFF',
    'red': '#FF0000',
    'blue': '#0000FF',
    'green': '#008000',
    'yellow': '#FFFF00',
    'gold': '#FFD700',
    'silver': '#C0C0C0',
    'brown': '#A52A2A',
    'tortoise': '#8B4513',
    'matte black': '#1a1a1a',
    'polished black': '#000000',
    'shiny black': '#000000'
  }
  return colorMap[colorName.toLowerCase()] || '#000000'
}

// Get available colors (with stock > 0)
const availableColors = computed(() => {
  return productColors.value.filter(c => c.stock > 0)
})

// Get available sizes based on selected color
const availableSizes = computed(() => {
  if (!selectedColor.value) return productSizes.value
  // Get sizes that have stock for selected color
  return productSizes.value.filter(size => {
    const variant = productVariants.value.find(v => 
      v.size === size && v.color === selectedColor.value.name && (v.stock || 0) > 0
    )
    return !!variant
  })
})

// Get selected variant (based on selected size and color)
const selectedVariant = computed(() => {
  if (!selectedColor.value || !selectedSize.value) return null
  return productVariants.value.find(v => 
    v.color === selectedColor.value.name && v.size === selectedSize.value
  )
})

// Total available stock (sum of all variant stocks)
const totalColorStock = computed(() => {
  if (productVariants.value.length === 0) return product.value?.stock || 0
  return productVariants.value.reduce((sum, v) => sum + (v.stock || 0), 0)
})

// Auto-select first available color and size on load
watch(product, (newProduct) => {
  if (newProduct) {
    // If product has sizes, color is required
    if (productSizes.value.length > 0 && productColors.value.length > 0) {
      const firstAvailable = productColors.value.find(c => c.stock > 0)
      if (firstAvailable) {
        selectedColor.value = firstAvailable
      }
      // Auto-select first size
      const firstSize = productSizes.value[0]
      selectedSize.value = typeof firstSize === 'object' ? firstSize.name : firstSize
    }
    // If product has colors but no sizes, auto-select color
    else if (productColors.value.length > 0 && productSizes.value.length === 0) {
      const firstAvailable = productColors.value.find(c => c.stock > 0)
      if (firstAvailable) {
        selectedColor.value = firstAvailable
      }
    }
    // If product has sizes but no colors, auto-select size
    else if (productSizes.value.length > 0 && productColors.value.length === 0) {
      const firstSize = productSizes.value[0]
      selectedSize.value = typeof firstSize === 'object' ? firstSize.name : firstSize
    }
  }
}, { immediate: true })

const selectColor = (color) => {
  if (color.stock > 0) {
    selectedColor.value = color
  }
}

const selectSize = (size) => {
  // Handle both object format { name, stock } and string format
  if (typeof size === 'object') {
    selectedSize.value = size.name
  } else {
    selectedSize.value = size
  }
}

const canAddToCart = computed(() => {
  if (!product.value) return false
  
  // If product has variants (sizes + colors)
  if (productVariants.value.length > 0) {
    // Both size and color must be selected
    if (!selectedColor.value || !selectedSize.value) return false
    // Check if selected variant has stock
    const variant = selectedVariant.value
    if (!variant || (variant.stock || 0) === 0) return false
  }
  // No variants - check general stock
  else {
    if (product.value.stock === 0) return false
  }
  
  return true
})

const buttonText = computed(() => {
  if (!product.value) return 'Yuklanmoqda...'
  
  // If product has variants
  if (productVariants.value.length > 0) {
    if (!selectedColor.value) return 'Rangni tanlang'
    if (!selectedSize.value) return 'O\'lchamni tanlang'
    const variant = selectedVariant.value
    if (!variant || (variant.stock || 0) === 0) return 'Tugagan'
  }
  // No variants - check general stock
  else if (product.value.stock === 0) {
    return 'Tugagan'
  }
  
  return 'SAVATGA QO\'SHISH'
})

const toast = useToast()

const addToCart = () => {
  if (!canAddToCart.value) {
    // If product has sizes, color is required
    if (productSizes.value.length > 0) {
      if (productColors.value.length > 0) {
        // Has both sizes and colors
        if (!selectedColor.value) {
          toast.warning('Iltimos, rangni tanlang')
          return
        }
        if (selectedColor.value.stock === 0) {
          toast.error('Bu rang tugagan')
          return
        }
        if (!selectedSize.value) {
          toast.warning('Iltimos, o\'lchamni tanlang')
          return
        }
      } else {
        // Has sizes but no colors
        if (!selectedSize.value) {
          toast.warning('Iltimos, o\'lchamni tanlang')
          return
        }
      }
    }
    // If product has colors but no sizes, color is required
    else if (productColors.value.length > 0) {
      if (!selectedColor.value) {
        toast.warning('Iltimos, rangni tanlang')
        return
      }
      if (selectedColor.value.stock === 0) {
        toast.error('Bu rang tugagan')
        return
      }
    }
    return
  }
  
  addItem({
    ...product.value,
    selectedColor: selectedColor.value || null,
    selectedSize: selectedSize.value || null
  })
  toast.success('Savatga qo\'shildi!')
}

const toggleFavorite = async () => {
  if (!user.value) {
    toast.warning('Sevimlilar ro\'yxatiga qo\'shish uchun tizimga kiring')
    navigateTo('/login')
    return
  }
  
  try {
    await $fetch(`http://localhost:8000/products/${route.params.id}/favorite`, { method: 'POST' })
    refresh()
  } catch (e) {
    console.error(e)
  }
}
</script>

<style scoped>
.product-page {
  min-height: 100vh;
  background: #FAFAFA;
  padding-bottom: 100px;
}

.product-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.product-gallery {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.main-image {
  background: white;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  mix-blend-mode: multiply;
}

.thumbnail-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  gap: 12px;
}

.thumbnail {
  background: white;
  border-radius: 12px;
  padding: 12px;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s;
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.thumbnail:hover,
.thumbnail.active {
  border-color: #111;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  mix-blend-mode: multiply;
}

.product-details {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.product-category {
  font-size: 0.875rem;
  color: #9CA3AF;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.product-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #111;
  line-height: 1.2;
}

.product-price-section {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.product-price {
  font-size: 2.5rem;
  font-weight: 800;
  color: #111;
}

.stock-badge {
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.875rem;
}

.in-stock {
  background: #D1FAE5;
  color: #065F46;
}

.low-stock {
  background: #FEF3C7;
  color: #92400E;
}

.out-of-stock {
  background: #FEE2E2;
  color: #991B1B;
}

.select-color {
  background: #E5E7EB;
  color: #6B7280;
}

.color-selector {
  padding: 24px 0;
  border-top: 1px solid #E5E7EB;
}

.colors {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.color-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 50px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.color-btn:hover:not(:disabled) {
  border-color: #111;
}

.color-btn.active {
  border-color: #111;
  background: #F9FAFB;
}

.color-btn.out-of-stock {
  opacity: 0.5;
  cursor: not-allowed;
}

.color-swatch {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--color);
  border: 2px solid rgba(0,0,0,0.1);
}

.color-name {
  font-weight: 600;
  font-size: 0.875rem;
}

.color-oos {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 1.5rem;
  color: #EF4444;
}

.size-selector {
  padding: 24px 0;
  border-top: 1px solid #E5E7EB;
  border-bottom: 1px solid #E5E7EB;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #111;
  display: flex;
  align-items: center;
  gap: 4px;
}

.required-badge {
  color: #EF4444;
  font-size: 1.25rem;
  line-height: 1;
}

.sizes {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.size-btn {
  min-width: 60px;
  padding: 12px 20px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  background: white;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.size-btn:hover:not(:disabled) {
  border-color: #111;
}

.size-btn.active {
  background: #111;
  color: white;
  border-color: #111;
}

.size-btn.out-of-stock {
  opacity: 0.5;
  cursor: not-allowed;
  background: #F3F4F6;
  text-decoration: line-through;
}

.size-oos {
  color: #EF4444;
  font-size: 0.75rem;
}

.product-description {
  padding: 24px 0;
}

.product-description p {
  color: #6B7280;
  line-height: 1.6;
}

.product-meta {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.meta-item {
  display: flex;
  gap: 8px;
}

.meta-label {
  font-weight: 600;
  color: #6B7280;
}

.meta-value {
  color: #111;
  font-weight: 500;
}

.product-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.btn-add-cart {
  flex: 1;
  padding: 16px 32px;
  background: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  transition: all 0.2s;
}

.btn-add-cart:hover:not(:disabled) {
  background: #000;
  transform: translateY(-2px);
}

.btn-add-cart:disabled {
  background: #9CA3AF;
  cursor: not-allowed;
}

.btn-favorite {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: white;
  border: 2px solid #E5E7EB;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  color: #9CA3AF;
}

.btn-favorite:hover,
.btn-favorite.active {
  border-color: #EF4444;
  color: #EF4444;
  background: #FEF2F2;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #111;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (min-width: 768px) {
  .product-content {
    grid-template-columns: 1fr 1fr;
  }
  
  .product-title {
    font-size: 3rem;
  }
}

@media (max-width: 767px) {
  .main-image {
    padding: 24px;
  }
  
  .product-title {
    font-size: 1.75rem;
  }
  
  .product-price {
    font-size: 2rem;
  }
  
  .btn-add-cart {
    padding: 14px 24px;
  }
}
</style>
