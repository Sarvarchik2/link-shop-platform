export default defineNuxtRouteMiddleware(async (to, from) => {
    const { token, user, fetchUser } = useAuth()

    if (!token.value) {
        return navigateTo('/login')
    }

    if (!user.value) {
        try {
            await fetchUser()
        } catch (e) {
            token.value = null
            return navigateTo('/login')
        }
    }

    if (!user.value) {
        return navigateTo('/login')
    }
})
