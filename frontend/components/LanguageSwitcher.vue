<template>
    <div class="language-switcher" v-click-outside="closeDropdown">
        <button @click="toggleDropdown" class="lang-btn">
            <span class="flag">{{ currentLocale.flag }}</span>
            <span class="code">{{ currentLocale.code.toUpperCase() }}</span>
            <svg class="chevron" :class="{ rotated: isOpen }" width="16" height="16" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
        </button>

        <div v-show="isOpen" class="lang-dropdown">
            <button v-for="locale in availableLocales" :key="locale.code" @click="switchLanguage(locale.code)"
                class="lang-option" :class="{ active: currentLocale.code === locale.code }">
                <span class="flag">{{ locale.flag }}</span>
                <span class="name">{{ locale.name }}</span>
            </button>
        </div>
    </div>
</template>

<script setup>
const { locale, setLocale } = useI18n()
const isOpen = ref(false)

const locales = [
    { code: 'uz', name: "O'zbek", flag: '🇺🇿' },
    { code: 'ru', name: 'Русский', flag: '🇷🇺' },
    { code: 'en', name: 'English', flag: '🇬🇧' }
]

const currentLocale = computed(() => {
    return locales.find(l => l.code === locale.value) || locales[0]
})

const availableLocales = computed(() => {
    return locales
})

const toggleDropdown = () => {
    isOpen.value = !isOpen.value
}

const closeDropdown = () => {
    isOpen.value = false
}

const switchLanguage = (code) => {
    setLocale(code)
    isOpen.value = false
    // Optional: Refresh page if needed mostly for heavy static content, 
    // but vue-i18n usually handles reactivity well.
    // location.reload() 
}

// Directive to close dropdown when clicking outside
const vClickOutside = {
    mounted(el, binding) {
        el.clickOutsideEvent = (event) => {
            if (!(el === event.target || el.contains(event.target))) {
                binding.value(event)
            }
        }
        document.body.addEventListener('click', el.clickOutsideEvent)
    },
    unmounted(el) {
        document.body.removeEventListener('click', el.clickOutsideEvent)
    }
}
</script>

<style scoped>
.language-switcher {
    position: relative;
    z-index: 50;
}

.lang-btn {
    display: flex;
    align-items: center;
    gap: 6px;
    background: transparent;
    border: 1px solid #E5E7EB;
    padding: 6px 12px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
    color: #374151;
    font-weight: 500;
    font-size: 0.875rem;
}

.lang-btn:hover {
    background: #F3F4F6;
    border-color: #D1D5DB;
}

.flag {
    font-size: 1.1em;
    line-height: 1;
}

.chevron {
    transition: transform 0.2s;
    opacity: 0.5;
}

.chevron.rotated {
    transform: rotate(180deg);
}

.lang-dropdown {
    position: absolute;
    top: 100%;
    right: 0;
    margin-top: 4px;
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 4px;
    min-width: 140px;
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.lang-option {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    border: none;
    background: transparent;
    cursor: pointer;
    border-radius: 8px;
    text-align: left;
    font-size: 0.875rem;
    color: #374151;
    transition: all 0.2s;
}

.lang-option:hover {
    background: #F3F4F6;
}

.lang-option.active {
    background: #F0F9FF;
    color: #0284C7;
    font-weight: 600;
}
</style>
