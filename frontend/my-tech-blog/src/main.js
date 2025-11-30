import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'element-plus/dist/index.css'
// 深色主题css
import 'element-plus/theme-chalk/dark/css-vars.css'
import ElementPlus from 'element-plus'
// 中文包
import {zhCn} from "element-plus/es/locale/index";
import store from './store'

const app = createApp(App)

// 路由
app.use(router)
// Element-plus
app.use(ElementPlus, {
    locale: zhCn,
})

// vuex
app.use(store)

app.mount('#app')
