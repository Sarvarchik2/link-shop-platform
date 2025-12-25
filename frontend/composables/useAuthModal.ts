import { ref } from 'vue'

const showAuthModal = ref(false)

export const useAuthModal = () => {
    const openModal = () => {
        showAuthModal.value = true
    }

    const closeModal = () => {
        showAuthModal.value = false
    }

    return {
        showAuthModal,
        openModal,
        closeModal
    }
}
