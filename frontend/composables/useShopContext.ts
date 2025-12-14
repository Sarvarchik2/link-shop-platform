/**
 * Composable for managing shop context across navigation
 * Saves the current shop slug so users can return to the shop they were viewing
 */

export const useShopContext = () => {
  const SHOP_CONTEXT_KEY = 'current_shop_slug'

  // Get shop slug from localStorage
  const getShopSlug = (): string | null => {
    if (process.client) {
      return localStorage.getItem(SHOP_CONTEXT_KEY)
    }
    return null
  }

  // Save shop slug to localStorage
  const setShopSlug = (slug: string | null) => {
    if (process.client) {
      if (slug) {
        localStorage.setItem(SHOP_CONTEXT_KEY, slug)
      } else {
        localStorage.removeItem(SHOP_CONTEXT_KEY)
      }
    }
  }

  // Get shop slug from current route or from localStorage
  const getCurrentShopSlug = (route: any): string | null => {
    // First, try to get from route params
    const routeSlug = route.params?.shop || route.params?.slug
    if (routeSlug) {
      // Save it for future use
      setShopSlug(routeSlug)
      return routeSlug
    }
    
    // If not in route, try to get from localStorage
    return getShopSlug()
  }

  // Clear shop context (when user explicitly navigates away from shops)
  const clearShopContext = () => {
    setShopSlug(null)
  }

  return {
    getShopSlug,
    setShopSlug,
    getCurrentShopSlug,
    clearShopContext
  }
}
