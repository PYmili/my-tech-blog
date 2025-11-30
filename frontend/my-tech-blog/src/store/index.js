import { createStore } from 'vuex'
import auth from './modules/auth.js'

export default createStore({
    modules: { auth }
})