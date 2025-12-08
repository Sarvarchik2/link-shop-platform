export const useCart = () => {
    const items = useState<any[]>('cart_items', () => [])

    // Create unique key for cart item based on product, color, and size
    const getItemKey = (product: any) => {
        const colorKey = product.selectedColor?.name || 'no-color'
        const sizeKey = product.selectedSize || 'no-size'
        return `${product.id}-${colorKey}-${sizeKey}`
    }

    const addItem = (product: any) => {
        const itemKey = getItemKey(product)
        const existing = items.value.find(i => getItemKey(i) === itemKey)
        
        if (existing) {
            existing.quantity++
        } else {
            items.value.push({ 
                ...product, 
                quantity: 1,
                cartKey: itemKey
            })
        }
    }

    const removeItem = (cartKey: string) => {
        items.value = items.value.filter(i => i.cartKey !== cartKey)
    }

    const updateQuantity = (cartKey: string, delta: number) => {
        const item = items.value.find(i => i.cartKey === cartKey)
        if (item) {
            item.quantity += delta
            if (item.quantity <= 0) {
                removeItem(cartKey)
            }
        }
    }

    const totalItems = computed(() => items.value.reduce((acc, item) => acc + item.quantity, 0))
    const totalPrice = computed(() => items.value.reduce((acc, item) => acc + (item.price * item.quantity), 0))

    const clearCart = () => {
        items.value = []
    }

    return {
        items,
        addItem,
        removeItem,
        updateQuantity,
        totalItems,
        totalPrice,
        clearCart
    }
}
