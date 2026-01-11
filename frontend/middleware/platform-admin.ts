export default defineNuxtRouteMiddleware(async (to, from) => {
    const { token, user, fetchUser } = useAuth()
    const localePath = useLocalePath()

    // If no token, redirect to login
    if (!token.value) {
        return navigateTo(localePath('/login'))
    }

    // If user not loaded yet, try to fetch
    if (!user.value) {
        try {
            await fetchUser()
        } catch (e) {
            // Token invalid, clear and redirect
            token.value = null
            return navigateTo(localePath('/login'))
        }
    }

    // Check if user is platform admin
    const userData = user.value as any
    if (!userData || userData.role !== 'platform_admin') {
        return navigateTo(localePath('/login'))
    }
})

