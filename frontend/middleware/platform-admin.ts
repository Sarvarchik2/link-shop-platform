export default defineNuxtRouteMiddleware(async (to, from) => {
    const { token, user, fetchUser } = useAuth()

    // If no token, redirect to login
    if (!token.value) {
        return navigateTo('/login')
    }

    // If user not loaded yet, try to fetch
    if (!user.value) {
        try {
            await fetchUser()
        } catch (e) {
            // Token invalid, clear and redirect
            token.value = null
            return navigateTo('/login')
        }
    }

    // Check if user is platform admin
    if (!user.value || user.value.role !== 'platform_admin') {
        return navigateTo('/login')
    }
})

