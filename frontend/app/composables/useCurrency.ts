export const useCurrency = () => {
    const formatPrice = (value: number | string | null | undefined): string => {
        if (value === null || value === undefined || value === '') return 'UZS 0'

        // Convert string to number if needed
        const numValue = typeof value === 'string' ? parseFloat(value) : value

        // Check if valid number
        if (isNaN(numValue)) return 'UZS 0'

        // Format number with thousand separators
        const formatted = Math.round(numValue).toLocaleString('en-US')

        return `UZS ${formatted}`
    }

    return {
        formatPrice
    }
}
