/**
 * Composable for managing shop context across navigation
 * Saves the current shop slug so users can return to the shop they were viewing
 */

export const useShopContext = () => {
  const SHOP_CONTEXT_KEY = 'current_shop_slug'
  const shopCookie = useCookie(SHOP_CONTEXT_KEY, {
    maxAge: 60 * 60 * 24 * 7, // 1 week
    path: '/'
  })

  // Get shop slug from cookie
  const getShopSlug = (): string | null => {
    return shopCookie.value || null
  }

  // Save shop slug to cookie
  const setShopSlug = (slug: string | null) => {
    shopCookie.value = slug
  }

  // Get shop slug from current route or from cookie
  const getCurrentShopSlug = (route: any): string | null => {
    // First, try to get from route params
    const routeSlug = route.params?.shop || route.params?.slug
    if (routeSlug) {
      // Save it for future use
      setShopSlug(routeSlug)
      return routeSlug as string
    }

    // If not in route, try to get from cookie
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
