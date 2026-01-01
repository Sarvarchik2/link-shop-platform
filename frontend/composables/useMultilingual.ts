/**
 * Composable for handling multilingual content from API
 * Automatically selects the correct language field based on current locale
 */

export const useMultilingual = () => {
    const { locale } = useI18n()

    /**
     * Get field value in current language
     * @param obj - Object with multilingual fields (e.g., { name_uz, name_ru, name_en })
     * @param fieldName - Base field name (e.g., 'name', 'description')
     * @returns Value in current language or fallback
     */
    const getField = (obj: any, fieldName: string): string => {
        if (!obj) return ''

        const currentLang = locale.value || 'uz'
        const fieldKey = `${fieldName}_${currentLang}`

        // Try current language
        if (obj[fieldKey]) {
            return obj[fieldKey]
        }

        // Fallback to Uzbek
        const fallbackKey = `${fieldName}_uz`
        if (obj[fallbackKey]) {
            return obj[fallbackKey]
        }

        // Last resort: try the field without suffix (backwards compatibility)
        return obj[fieldName] || ''
    }

    /**
     * Get multiple fields as an object
     * @param obj - Object with multilingual fields
     * @param fieldNames - Array of field names
     * @returns Object with values in current language
     */
    const getFields = (obj: any, fieldNames: string[]) => {
        const result: Record<string, string> = {}
        fieldNames.forEach(fieldName => {
            result[fieldName] = getField(obj, fieldName)
        })
        return result
    }

    return {
        getField,
        getFields,
        currentLocale: locale
    }
}
