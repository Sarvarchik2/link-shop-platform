export const useCurrency = () => {
    const { t } = useI18n()

    const formatPrice = (value: number | string | null | undefined): string => {
        const currency = t('currency')
        if (value === null || value === undefined || value === '') return `0 ${currency}`

        // Convert string to number if needed
        const numValue = typeof value === 'string' ? parseFloat(value) : value

        // Check if valid number
        if (isNaN(numValue)) return `0 ${currency}`

        // Format number with thousand separators (space)
        const formatted = Math.round(numValue).toLocaleString('ru-RU').replace(/,/g, ' ')

        return `${formatted} ${currency}`
    }

    return {
        formatPrice
    }
}
