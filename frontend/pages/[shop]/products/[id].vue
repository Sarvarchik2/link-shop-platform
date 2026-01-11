<template>
  <div class="product-page">
    <AppHeader />

    <main class="container py-8">
      <div v-if="pending" class="text-center py-12">
        <div class="loading-spinner"></div>
        <p class="mt-4 text-gray-400">{{ $t('product.loading') }}</p>
      </div>

      <div v-else-if="product" class="product-content">
        <div class="product-gallery">
          <div class="main-image">
            <img :src="selectedImage || product.image_url" :alt="getField(product, 'name')" />
          </div>
          <div v-if="productImages.length > 1" class="thumbnail-images">
            <div v-for="(img, index) in productImages" :key="index" class="thumbnail"
              :class="{ active: selectedImage === img }" @click="selectedImage = img">
              <img :src="img" :alt="`${getField(product, 'name')} ${index + 1}`" />
            </div>
          </div>
        </div>

        <div class="product-details">
          <div class="product-category">{{ getField(product, 'category') }}</div>
          <h1 class="product-title">{{ getField(product, 'name') }}</h1>

          <div class="product-price-section">
            <div class="price-container">
              <div v-if="product.discount > 0" class="price-with-discount">
                <div class="product-price-discounted">{{ formatPrice(finalPrice) }}</div>
                <div class="product-price-original">{{ formatPrice(product.price) }}</div>
                <div class="discount-badge">-{{ product.discount }}%</div>
              </div>
              <div v-else class="product-price">{{ formatPrice(product.price) }}</div>
            </div>
            <!-- Stock badge based on selected variant -->
            <template v-if="productVariants.length > 0">
              <div v-if="totalColorStock === 0" class="stock-badge out-of-stock">{{ $t('product.outOfStock') }}</div>
              <div v-else-if="selectedColor && selectedSize && selectedVariant">
                <div v-if="selectedVariant.stock === 0" class="stock-badge out-of-stock">{{ selectedSize }} / {{
                  selectedColor.name }} - {{ $t('product.outOfStock') }}</div>
                <div v-else-if="selectedVariant.stock <= 5" class="stock-badge low-stock">{{ selectedSize }} / {{
                  selectedColor.name }}: {{ $t('product.lowStock', { count: selectedVariant.stock }) }}</div>
                <div v-else class="stock-badge in-stock">{{ selectedSize }} / {{ selectedColor.name }}: {{
                  $t('product.inStock', { count: selectedVariant.stock }) }}</div>
              </div>
              <div v-else-if="selectedColor && !selectedSize" class="stock-badge select-color">{{
                $t('product.selectVariant') }}</div>
              <div v-else-if="!selectedColor && selectedSize" class="stock-badge select-color">{{
                $t('product.selectVariant') }}</div>
              <div v-else class="stock-badge select-color">{{ $t('product.selectVariant') }}</div>
            </template>
            <!-- Stock badge for products without variants -->
            <template v-else>
              <div v-if="product.stock === 0" class="stock-badge out-of-stock">{{ $t('product.outOfStock') }}</div>
              <div v-else-if="product.stock <= 5" class="stock-badge low-stock">{{ $t('product.lowStock', {
                count:
                  product.stock
              }) }}</div>
              <div v-else class="stock-badge in-stock">{{ $t('product.inStock', { count: product.stock }) }}</div>
            </template>
          </div>

          <div v-if="productColors.length > 0" class="color-selector">
            <h3 class="section-title">
              {{ $t('product.selectColor') }}
              <span v-if="productSizes.length > 0" class="required-badge">*</span>
            </h3>
            <div class="colors">
              <button v-for="color in productColors" :key="color.name" class="color-btn"
                :class="{ active: selectedColor?.name === color.name, 'out-of-stock': color.stock === 0 }"
                :style="{ '--color': color.hex }" @click="selectColor(color)" :disabled="color.stock === 0"
                :title="color.stock === 0 ? $t('product.outOfStock') : `${color.name} (${$t('product.inStock', { count: color.stock })})`">
                <span class="color-swatch"></span>
                <span class="color-name">{{ color.name }}</span>
                <span v-if="color.stock === 0" class="color-oos">✕</span>
              </button>
            </div>
          </div>

          <div v-if="productSizes.length > 0" class="size-selector">
            <h3 class="section-title">
              {{ $t('product.selectSize') }}
              <span v-if="productColors.length > 0" class="required-badge">*</span>
            </h3>
            <div class="sizes">
              <button v-for="size in productSizes" :key="size.name || size" class="size-btn"
                :class="{ active: selectedSize === (size.name || size), 'out-of-stock': size.stock === 0 }"
                @click="selectSize(size)" :disabled="size.stock === 0"
                :title="size.stock === 0 ? $t('product.outOfStock') : `${size.name || size} (${size.stock || $t('status.active')})`">
                {{ size.name || size }}
                <span v-if="size.stock === 0" class="size-oos">✕</span>
              </button>
            </div>
          </div>

          <div class="product-description">
            <h3 class="section-title">{{ $t('product.description') }}</h3>
            <p>{{ getField(product, 'description') }}</p>
          </div>

          <div class="product-meta">
            <div class="meta-item">
              <span class="meta-label">{{ $t('product.brand') }}:</span>
              <span class="meta-value">{{ getField(product, 'brand') }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">{{ $t('product.category') }}:</span>
              <span class="meta-value">{{ getField(product, 'category') }}</span>
            </div>
          </div>

          <div class="product-actions">
            <button v-if="canAddToCart || !user" @click="addToCart" class="btn-add-cart"
              :disabled="user && !canAddToCart">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
              </svg>
              {{ buttonText }}
            </button>
            <button v-else-if="showPreorderButton || (!user && product?.is_preorder_enabled && totalColorStock === 0)"
              @click="openPreorderModal" class="btn-preorder">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
                <path d="M2 17l10 5 10-5"></path>
                <path d="M2 12l10 5 10-5"></path>
              </svg>
              {{ $t('product.preorder') }}
            </button>
            <button @click="toggleFavorite" class="btn-favorite" :class="{ active: product.is_favorite }">
              <svg width="20" height="20" viewBox="0 0 24 24" :fill="product.is_favorite ? 'currentColor' : 'none'"
                stroke="currentColor" stroke-width="2">
                <path
                  d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z">
                </path>
              </svg>
            </button>
          </div>

          <!-- Pre-order Modal -->
          <div v-if="showPreorderModal" class="modal-overlay" @click="closePreorderModal">
            <div class="modal-content" @click.stop>
              <div class="modal-header">
                <h2>{{ $t('product.preorder') }}</h2>
                <button @click="closePreorderModal" class="modal-close">×</button>
              </div>
              <div class="modal-body">
                <p class="preorder-description">
                  {{ $t('product.preorderDesc') }}
                </p>
                <div class="form-group">
                  <label>{{ $t('product.form.name') }}</label>
                  <input v-model="preorderForm.name" type="text" :placeholder="$t('product.form.name')" />
                </div>
                <div class="form-group">
                  <label>{{ $t('product.form.phone') }} *</label>
                  <input v-model="preorderForm.phone" type="tel" placeholder="+998901234567" required />
                </div>
                <div v-if="productVariants.length > 0" class="form-group">
                  <p class="form-info">
                    <strong>{{ $t('product.preorderConfig') }}</strong><br>
                    <span v-if="selectedColor">{{ $t('admin.color') }}: {{ selectedColor.name }}</span>
                    <span v-if="selectedColor && selectedSize">, </span>
                    <span v-if="selectedSize">{{ $t('admin.size') }}: {{ selectedSize }}</span>
                  </p>
                </div>
              </div>
              <div class="modal-footer">
                <button @click="closePreorderModal" class="btn-cancel">{{ $t('common.cancel') }}</button>
                <button @click="submitPreorder" class="btn-submit"
                  :disabled="!preorderForm.phone || isSubmittingPreorder">
                  {{ isSubmittingPreorder ? $t('common.sending') : $t('product.submitPreorder') }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="relatedProducts.length > 0" class="related-products">
        <h2 class="section-title">{{ $t('product.relatedProducts') || 'You might also like' }}</h2>
        <div class="products-grid">
          <ProductCard v-for="related in relatedProducts" :key="related.id" :product="related" :shop-slug="shopSlug" />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
const route = useRoute()
const shopSlug = route.params.shop
const { addItem } = useCart()
const { user } = useAuth()
const { getField } = useMultilingual()
const { t } = useI18n()
const { formatPrice } = useCurrency()
const { openModal } = useAuthModal()
const config = useRuntimeConfig()
const localePath = useLocalePath()

const { data: product, pending, refresh } = await useFetch(() => `${config.public.apiBase}/products/${route.params.id}`, {
  server: false
})

// Fetch related products (same shop)
// Prioritize category for related items
const { data: relatedProductsData } = await useFetch(() => `${config.public.apiBase}/products`, {
  params: {
    shop_slug: shopSlug,
    category: product.value?.category,
    limit: 10 // Fetch enough to filter out current
  },
  server: false,
  watch: [product] // Re-fetch when product changes
})

const relatedProducts = computed(() => {
  if (!relatedProductsData.value) return []
  // Filter out current product and limit to 3
  return relatedProductsData.value
    .filter(p => p.id !== parseInt(route.params.id))
    .slice(0, 3)
})

const selectedImage = ref(null)
const selectedSize = ref(null)
const selectedColor = ref(null)

// ... (rest of the script)

// Add mobile carousel styles
const mobileCarouselStyles = `
@media (max-width: 768px) {
  .products-grid {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    gap: 16px;
    padding-bottom: 16px; 
    margin-right: -20px; /* Bleed out right edge */
    padding-right: 20px;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none; /* Firefox */
  }

  .products-grid::-webkit-scrollbar {
    display: none; /* Chrome/Safari */
  }
  
  .products-grid > * {
    flex: 0 0 280px; /* Fixed width cards */
    scroll-snap-align: center;
  }
}
`
// Wait, I can't inject const styles like that in <script setup> easily without a <style> block update.
// I will split this into two edits: one for script, one for style.


// Calculate final price with discount
const finalPrice = computed(() => {
  if (!product.value) return 0
  if (product.value.discount > 0) {
    return product.value.price * (1 - product.value.discount / 100)
  }
  return product.value.price
})

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
    const hasSizes = product.value.sizes && product.value.sizes.trim()
    const hasColors = product.value.colors && product.value.colors.trim()

    if (hasSizes && hasColors) {
      // Both sizes and colors
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
    } else if (hasColors && !hasSizes) {
      // Only colors, no sizes
      const colors = JSON.parse(product.value.colors)
      return colors.map(color => {
        const colorObj = typeof color === 'string' ? { name: color, hex: '#000000', stock: 0 } : color
        return {
          size: null,
          color: colorObj.name || color,
          colorHex: colorObj.hex || '#000000',
          stock: colorObj.stock || 0
        }
      })
    } else if (hasSizes && !hasColors) {
      // Only sizes, no colors
      const sizes = JSON.parse(product.value.sizes)
      return sizes.map(size => {
        const sizeName = typeof size === 'string' ? size : (size.name || size)
        const sizeStock = typeof size === 'object' ? (size.stock || 0) : 0
        return {
          size: sizeName,
          color: null,
          colorHex: null,
          stock: sizeStock
        }
      })
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

// Get selected variant (based on selected size and color)
const selectedVariant = computed(() => {
  if (productVariants.value.length === 0) return null

  // If product has both sizes and colors, both must be selected
  if (productSizes.value.length > 0 && productColors.value.length > 0) {
    if (!selectedColor.value || !selectedSize.value) return null
    return productVariants.value.find(v =>
      v.color === selectedColor.value.name && v.size === selectedSize.value
    )
  }
  // If product has only colors (no sizes)
  else if (productColors.value.length > 0 && productSizes.value.length === 0) {
    if (!selectedColor.value) return null
    // Find variant with this color (size can be null or any)
    return productVariants.value.find(v => v.color === selectedColor.value.name)
  }
  // If product has only sizes (no colors)
  else if (productSizes.value.length > 0 && productColors.value.length === 0) {
    if (!selectedSize.value) return null
    // Find variant with this size (color can be null or any)
    return productVariants.value.find(v => v.size === selectedSize.value)
  }

  return null
})

// Total available stock (sum of all variant stocks)
const totalColorStock = computed(() => {
  if (productVariants.value.length === 0) return product.value?.stock || 0
  return productVariants.value.reduce((sum, v) => sum + (v.stock || 0), 0)
})

// Auto-select first available color and size on load
watch(product, (newProduct) => {
  if (newProduct) {
    // If product has both sizes and colors
    if (productSizes.value.length > 0 && productColors.value.length > 0) {
      const firstAvailable = productColors.value.find(c => c.stock > 0)
      if (firstAvailable) {
        selectedColor.value = firstAvailable
      }
      // Auto-select first size
      const firstSize = productSizes.value[0]
      selectedSize.value = typeof firstSize === 'object' ? firstSize.name : firstSize
    }
    // If product has only colors (no sizes), auto-select color
    else if (productColors.value.length > 0 && productSizes.value.length === 0) {
      const firstAvailable = productColors.value.find(c => c.stock > 0)
      if (firstAvailable) {
        selectedColor.value = firstAvailable
      }
      // Clear size selection
      selectedSize.value = null
    }
    // If product has only sizes (no colors), auto-select size
    else if (productSizes.value.length > 0 && productColors.value.length === 0) {
      const firstSize = productSizes.value[0]
      selectedSize.value = typeof firstSize === 'object' ? firstSize.name : firstSize
      // Clear color selection
      selectedColor.value = null
    }
    // If product has no variants, clear selections
    else {
      selectedColor.value = null
      selectedSize.value = null
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
  // Removed mandatory login check for button visibility

  if (!product.value) return false

  // If product has variants
  if (productVariants.value.length > 0) {
    // If product has both sizes and colors, both must be selected
    if (productSizes.value.length > 0 && productColors.value.length > 0) {
      if (!selectedColor.value || !selectedSize.value) return false
    }
    // If product has only colors (no sizes), only color must be selected
    else if (productColors.value.length > 0 && productSizes.value.length === 0) {
      if (!selectedColor.value) return false
    }
    // If product has only sizes (no colors), only size must be selected
    else if (productSizes.value.length > 0 && productColors.value.length === 0) {
      if (!selectedSize.value) return false
    }
    // If product has variants but no sizes and no colors, check variant stock
    // This case is rare but handle it

    // Check if selected variant has stock
    const variant = selectedVariant.value
    if (variant && (variant.stock || 0) === 0) return false

    // If we have colors/sizes but no variant found, can't add
    if ((productSizes.value.length > 0 || productColors.value.length > 0) && !variant) return false
  }
  // No variants - check general stock
  else {
    if (product.value.stock === 0) return false
  }

  return true
})

const buttonText = computed(() => {
  if (!product.value) return t('product.loading')

  // Check if user is logged in
  if (!user.value) {
    return t('product.addToCart') // Show the normal text even if not logged in
  }

  // If product has variants
  if (productVariants.value.length > 0) {
    // If product has both sizes and colors
    if (productSizes.value.length > 0 && productColors.value.length > 0) {
      if (!selectedColor.value) return t('product.selectColor')
      if (!selectedSize.value) return t('product.selectSize')
    }
    // If product has only colors (no sizes)
    else if (productColors.value.length > 0 && productSizes.value.length === 0) {
      if (!selectedColor.value) return t('product.selectColor')
    }
    // If product has only sizes (no colors)
    else if (productSizes.value.length > 0 && productColors.value.length === 0) {
      if (!selectedSize.value) return t('product.selectSize')
    }

    const variant = selectedVariant.value
    if (variant && (variant.stock || 0) === 0) return t('product.outOfStock')
  }
  // No variants - check general stock
  else if (product.value.stock === 0) {
    return t('product.outOfStock')
  }

  return t('product.addToCart')
})

const toast = useToast()

// Pre-order state
const showPreorderModal = ref(false)
const isSubmittingPreorder = ref(false)
const preorderForm = ref({
  name: '',
  phone: ''
})

// Check if pre-order button should be shown
const showPreorderButton = computed(() => {
  if (!product.value) return false
  if (!product.value.is_preorder_enabled) return false

  // Check if product is out of stock
  if (productVariants.value.length > 0) {
    // Check if we need to select variants
    const needsColor = productColors.value.length > 0
    const needsSize = productSizes.value.length > 0

    // If we need both but haven't selected them, don't show pre-order button yet
    if (needsColor && needsSize && (!selectedColor.value || !selectedSize.value)) {
      return false
    }
    // If we need only color but haven't selected it
    if (needsColor && !needsSize && !selectedColor.value) {
      return false
    }
    // If we need only size but haven't selected it
    if (!needsColor && needsSize && !selectedSize.value) {
      return false
    }

    const variant = selectedVariant.value
    if (variant && (variant.stock || 0) > 0) return false
    // If variant selected but out of stock, or no variant selected but all out of stock
    return totalColorStock.value === 0 || (!variant || (variant.stock || 0) === 0)
  } else {
    return product.value.stock === 0
  }
})

const openPreorderModal = () => {
  if (!user.value) {
    openModal()
    return
  }

  // Pre-fill user data if available
  if (user.value) {
    preorderForm.value.name = `${user.value.first_name || ''} ${user.value.last_name || ''}`.trim()
    preorderForm.value.phone = user.value.phone || ''
  }

  showPreorderModal.value = true
}

const closePreorderModal = () => {
  showPreorderModal.value = false
  preorderForm.value = { name: '', phone: '' }
}

const submitPreorder = async () => {
  if (!preorderForm.value.phone) {
    toast.error(t('validation.phoneRequired'))
    return
  }

  if (!user.value) {
    toast.warning(t('validation.loginRequired'))
    return
  }

  isSubmittingPreorder.value = true

  try {
    const { token } = useAuth()
    await $fetch(`${config.public.apiBase}/products/${route.params.id}/preorder`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token.value}`
      },
      body: {
        product_id: parseInt(route.params.id),
        selected_color: selectedColor.value?.name || null,
        selected_size: selectedSize.value || null,
        phone: preorderForm.value.phone,
        name: preorderForm.value.name || null
      }
    })

    toast.success(t('product.preorderSuccess'))
    closePreorderModal()
  } catch (e) {
    console.error('Preorder error:', e)
    if (e?.data?.detail) {
      toast.error(e.data.detail)
    } else {
      toast.error(t('product.preorderError'))
    }
  } finally {
    isSubmittingPreorder.value = false
  }
}

const addToCart = () => {
  // Check if user is logged in
  if (!user.value) {
    openModal()
    return
  }

  if (!canAddToCart.value) {
    // If product has both sizes and colors
    if (productSizes.value.length > 0 && productColors.value.length > 0) {
      if (!selectedColor.value) {
        toast.warning(t('product.selectColor'))
        return
      }
      if (selectedColor.value.stock === 0) {
        toast.error(t('product.outOfStock'))
        return
      }
      if (!selectedSize.value) {
        toast.warning(t('product.selectSize'))
        return
      }
    }
    // If product has only sizes (no colors)
    else if (productSizes.value.length > 0 && productColors.value.length === 0) {
      if (!selectedSize.value) {
        toast.warning(t('product.selectSize'))
        return
      }
    }
    // If product has only colors (no sizes)
    else if (productColors.value.length > 0 && productSizes.value.length === 0) {
      if (!selectedColor.value) {
        toast.warning(t('product.selectColor'))
        return
      }
      if (selectedColor.value.stock === 0) {
        toast.error(t('product.outOfStock'))
        return
      }
    }
    return
  }

  addItem({
    ...product.value,
    price: finalPrice.value,  // Add discounted price
    originalPrice: product.value.price,  // Keep original price
    discount: product.value.discount,
    selectedColor: selectedColor.value || null,
    selectedSize: selectedSize.value || null,
    shopSlug: shopSlug
  })
  toast.success(t('product.addedToCart'))
}

const toggleFavorite = async () => {
  if (!user.value) {
    openModal()
    return
  }

  try {
    await $fetch(`${config.public.apiBase}/products/${route.params.id}/favorite`, { method: 'POST' })
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  height: 500px;
  /* Fixed height */
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  mix-blend-mode: multiply;
  border-radius: 20px;
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

.price-container {
  display: flex;
  align-items: center;
  gap: 12px;
}

.product-price {
  font-size: 2.5rem;
  font-weight: 800;
  color: #111;
}

.price-with-discount {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.product-price-discounted {
  font-size: 2.5rem;
  font-weight: 800;
  color: #EF4444;
}

.product-price-original {
  font-size: 1.5rem;
  font-weight: 600;
  color: #9CA3AF;
  text-decoration: line-through;
}

.discount-badge {
  padding: 6px 12px;
  background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
  color: white;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.875rem;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
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
  border: 2px solid rgba(0, 0, 0, 0.1);
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
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

@media (min-width: 768px) {
  .product-content {
    grid-template-columns: 1fr 1fr;
  }

  .product-title {
    font-size: 3rem;
  }
}

.btn-preorder {
  flex: 1;
  padding: 16px 32px;
  background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
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

.btn-preorder:hover {
  background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 24px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #E5E7EB;
}

.modal-header h2 {
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
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #F3F4F6;
  color: #111;
}

.modal-body {
  padding: 24px;
}

.preorder-description {
  color: #6B7280;
  line-height: 1.6;
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-weight: 600;
  color: #111;
  margin-bottom: 8px;
  font-size: 0.875rem;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #6366F1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.form-info {
  padding: 12px;
  background: #F9FAFB;
  border-radius: 12px;
  color: #6B7280;
  font-size: 0.875rem;
  line-height: 1.6;
  margin: 0;
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 24px;
  border-top: 1px solid #E5E7EB;
}

.btn-cancel {
  flex: 1;
  padding: 12px 24px;
  background: white;
  border: 2px solid #E5E7EB;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  color: #6B7280;
}

.btn-cancel:hover {
  border-color: #D1D5DB;
  background: #F9FAFB;
}

.btn-submit {
  flex: 1;
  padding: 12px 24px;
  background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-submit:hover:not(:disabled) {
  background: linear-gradient(135deg, #4F46E5 0%, #4338CA 100%);
  transform: translateY(-1px);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

  .btn-add-cart,
  .btn-preorder {
    padding: 14px 24px;
  }

  .modal-content {
    margin: 20px;
  }
}

.related-products {
  margin-top: 80px;
  border-top: 1px solid #E5E7EB;
  padding-top: 40px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin-top: 24px;
}

@media (max-width: 768px) {
  .products-grid {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    gap: 16px;
    padding-bottom: 24px;
    margin-right: -20px;
    /* Bleed to edge */
    padding-right: 20px;
    -webkit-overflow-scrolling: touch;
  }

  .products-grid::-webkit-scrollbar {
    display: none;
  }

  .products-grid>* {
    flex: 0 0 85%;
    /* Shows part of next card */
    min-width: 260px;
    scroll-snap-align: start;
  }
}
</style>
