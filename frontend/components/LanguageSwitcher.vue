<template>
    <div class="language-switcher" :class="props.direction" v-click-outside="closeDropdown">
        <button @click="toggleDropdown" class="lang-btn">
            <span class="code">{{ currentLocale.code.toUpperCase() }}</span>
            <svg class="chevron" :class="{ rotated: isOpen }" width="14" height="14" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
        </button>

        <Transition name="fade">
            <div v-show="isOpen" class="lang-dropdown">
                <button v-for="locale in availableLocales" :key="locale.code" @click="switchLanguage(locale.code)"
                    class="lang-option" :class="{ active: currentLocale.code === locale.code }">
                    <span class="code-sm">{{ locale.code.toUpperCase() }}</span>
                    <span class="name">{{ locale.name }}</span>
                </button>
            </div>
        </Transition>
    </div>
</template>

<script setup>
const { locale, setLocale } = useI18n()
const isOpen = ref(false)

const locales = [
    { code: 'uz', name: "O'zbek" },
    { code: 'ru', name: 'Русский' },
    { code: 'en', name: 'English' }
]

const props = defineProps({
    direction: {
        type: String,
        default: 'down',
        validator: (value) => ['up', 'down'].includes(value)
    }
})

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
    height: 44px;
    padding: 0 12px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
    background: #f9f9f9;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    color: #111;
    font-weight: 700;
    font-size: 0.9rem;
}

.lang-btn:hover {
    background: #111;
    color: white;
    transform: translateY(-2px);
}

@media (max-width: 767px) {
    .lang-btn {
        height: 40px;
        border-radius: 10px;
    }
}

.chevron {
    transition: transform 0.2s;
    opacity: 0.6;
}

.lang-btn:hover .chevron {
    opacity: 1;
}

.chevron.rotated {
    transform: rotate(180deg);
}

.lang-dropdown {
    position: absolute;
    right: 0;
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 16px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
    padding: 6px;
    min-width: 160px;
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.language-switcher.down .lang-dropdown {
    top: calc(100% + 8px);
}

.language-switcher.up .lang-dropdown {
    bottom: calc(100% + 8px);
    top: auto;
}

.lang-option {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border: none;
    background: transparent;
    cursor: pointer;
    border-radius: 10px;
    text-align: left;
    font-size: 0.875rem;
    color: #374151;
    transition: all 0.2s;
}

.lang-option:hover {
    background: #F3F4F6;
    color: #111;
}

.lang-option.active {
    background: #000000;
    color: #ffffff;
    font-weight: 600;
}

.code-sm {
    font-weight: 700;
    font-size: 0.75rem;
    color: #9CA3AF;
    width: 24px;
    text-align: center;
}

.lang-option.active .code-sm {
    color: #ffffff;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
    transition: 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}
</style>
