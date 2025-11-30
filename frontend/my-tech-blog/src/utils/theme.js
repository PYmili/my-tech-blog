import {ref} from "vue";

export const isDark = ref(false)

/**
 * 应用主题
 * @param {boolean} dark - 是否为暗黑模式
 */
export const applyTheme = (dark) => {
    const htmlElement = document.documentElement
    if (dark) {
        htmlElement.classList.add('dark')
    } else {
        htmlElement.classList.remove('dark')
    }
}

/**
 * 初始化主题
 */
export const initTheme = () => {
    // 从 localStorage 读取主题设置
    const savedTheme = localStorage.getItem('my_tech_blog_theme')
    if (savedTheme === 'dark') {
        isDark.value = true
        applyTheme(true)
    } else if (savedTheme === 'light') {
        isDark.value = false
        applyTheme(false)
    } else {
        // 如果没有保存的主题，使用系统偏好
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
        isDark.value = prefersDark
        applyTheme(prefersDark)
        localStorage.setItem('my_tech_blog_theme', prefersDark ? 'dark' : 'light')
    }
}
