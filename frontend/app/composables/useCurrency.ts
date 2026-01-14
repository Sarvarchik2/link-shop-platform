export const useCurrency = () => {
    const formatPrice = (value: number | string | null | undefined): string => {
        if (value === null || value === undefined || value === '') return '0 UZS'

        // Convert string to number if needed
        const numValue = typeof value === 'string' ? parseFloat(value) : value

        // Check if valid number
        if (isNaN(numValue)) return '0 UZS'

        return new Intl.NumberFormat('uz-UZ', {
            style: 'currency',
            currency: 'UZS',
            maximumFractionDigits: 0
        }).format(numValue)
    }

    return {
        formatPrice
    }
}
