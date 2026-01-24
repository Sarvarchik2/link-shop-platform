export const useAuth = () => {
    const config = useRuntimeConfig()
    const token = useCookie('auth_token', {
        maxAge: 60 * 60 * 24 * 30, // 30 days
        sameSite: 'lax'
    })
    const user = useState<any>('user', () => null)

    // Lazy load localePath to avoid SSR issues
    const getLocalePath = () => {
        try {
            return useLocalePath()
        } catch (e) {
            return (path: string) => path
        }
    }

    const login = async (phone: string, password: string, redirect: boolean = true) => {
        const localePath = getLocalePath()
        try {
            const formData = new URLSearchParams()
            formData.append('username', phone)
            formData.append('password', password)

            const data: any = await $fetch(config.public.apiBase + '/token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: formData.toString()
            })
            token.value = data.access_token
            await fetchUser()
            useToast().success('Добро пожаловать!')

            if (redirect) {
                // Get return URL from query params or localStorage
                const route = useRoute()
                let queryReturnUrl: string | null = null

                if (Array.isArray(route.query.returnUrl)) {
                    queryReturnUrl = route.query.returnUrl[0] || null
                } else if (typeof route.query.returnUrl === 'string') {
                    queryReturnUrl = route.query.returnUrl
                }

                const returnUrl = queryReturnUrl || (process.client ? localStorage.getItem('returnUrl') : null)

                if (returnUrl) {
                    // Clear returnUrl from localStorage
                    if (process.client) {
                        localStorage.removeItem('returnUrl')
                    }
                    await navigateTo(returnUrl)
                } else {
                    await navigateTo(localePath('/'))
                }
            }
        } catch (error) {
            console.error('Login error:', error)
            throw error
        }
    }

    const register = async (phone: string, password: string, first_name: string, last_name: string) => {
        const localePath = getLocalePath()
        try {
            const data: any = await $fetch(config.public.apiBase + '/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ phone: phone, password, first_name, last_name })
            })
            token.value = data.access_token
            await fetchUser()
            useToast().success('Аккаунт успешно создан!')

            // Get return URL from query params or localStorage
            const route = useRoute()
            let queryReturnUrl: string | null = null

            if (Array.isArray(route.query.returnUrl)) {
                queryReturnUrl = route.query.returnUrl[0] || null
            } else if (typeof route.query.returnUrl === 'string') {
                queryReturnUrl = route.query.returnUrl
            }

            const returnUrl = queryReturnUrl || (process.client ? localStorage.getItem('returnUrl') : null)

            if (returnUrl) {
                // Clear returnUrl from localStorage
                if (process.client) {
                    localStorage.removeItem('returnUrl')
                }
                await navigateTo(returnUrl)
            } else {
                await navigateTo(localePath('/'))
            }
        } catch (error) {
            console.error('Register error:', error)
            throw error
        }
    }

    const fetchUser = async () => {
        if (!token.value) return

        // Use internal URL for SSR, public URL for client
        const baseUrl = process.server ? config.apiBaseInternal : config.public.apiBase

        try {
            user.value = await $fetch(baseUrl + '/users/me', {
                headers: { Authorization: `Bearer ${token.value}` }
            })
        } catch (e: any) {
            // Only clear token if it's a 401 Unauthorized
            // If it's a network error during SSR, don't clear the token!
            if (e?.status === 401) {
                token.value = null
                user.value = null
            } else if (!process.server) {
                // On client, we might want to be more aggressive, but still...
                if (e?.status) {
                    token.value = null
                    user.value = null
                }
            }
        }
    }

    const logout = () => {
        const localePath = getLocalePath()
        token.value = null
        user.value = null
        navigateTo(localePath('/login'))
    }

    return { token, user, login, register, logout, fetchUser }
}
