export const usePhoneFormatter = () => {
    const formatPhoneNumber = (value: string) => {
        if (!value) return '+998 '

        // Remove all non-digit characters
        const numbers = value.replace(/\D/g, '')

        // Handle backspace/deletion when only prefix remains
        if (numbers.length < 3) return '+998 '

        // Ensure it starts with 998
        let formatted = '+998'

        // Get the part after 998
        const rest = numbers.substring(3)

        if (rest.length > 0) {
            formatted += ' (' + rest.substring(0, 2)
        }

        if (rest.length >= 3) {
            formatted += ') ' + rest.substring(2, 5)
        }

        if (rest.length >= 6) {
            formatted += '-' + rest.substring(5, 7)
        }

        if (rest.length >= 8) {
            formatted += '-' + rest.substring(7, 9)
        }

        return formatted
    }

    // Helper to get raw number for API sending
    const unformatPhoneNumber = (value: string) => {
        const numbers = value.replace(/\D/g, '')
        return '+' + numbers
    }

    return {
        formatPhoneNumber,
        unformatPhoneNumber
    }
}
