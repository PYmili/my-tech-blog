// store/modules/request.js
const ACCESS_KEY = 'my_tech_blog_access_token'
const REFRESH_KEY = 'my_tech_blog_refresh_token'

const storage = {
    get() {
        return {
            access: localStorage.getItem(ACCESS_KEY),
            refresh: localStorage.getItem(REFRESH_KEY)
        }
    },
    set(access, refresh) {
        localStorage.setItem(ACCESS_KEY, access)
        localStorage.setItem(REFRESH_KEY, refresh)
    },
    remove() {
        localStorage.removeItem(ACCESS_KEY)
        localStorage.removeItem(REFRESH_KEY)
    }
}

export default {
    namespaced: true,

    state: () => ({
        access: storage.get().access || null,
        refresh: storage.get().refresh || null
    }),

    getters: {
        isLogin: state => !!state.access && !!state.refresh,
        token: state => ({
            access: state.access,
            refresh: state.refresh
        })
    },

    mutations: {
        SET_TOKEN(state, { access, refresh }) {
            state.access = access
            state.refresh = refresh
            storage.set(access, refresh)
        },
        CLEAR_AUTH(state) {
            state.access = null
            state.refresh = null
            storage.remove()
        },
        REFRESH_STATE(state) {
            const res = storage.get();
            state.access = res.access || null
            state.refresh = res.refresh || null
        }
    },

    actions: {
        // 更新 token
        updateToken({ commit }, data) {
            commit('SET_TOKEN', data)
        },
        // 清理 token（登出）
        clearAuth({ commit }) {
            commit('CLEAR_AUTH')
        },
        // 刷新当前登录状态
        refreshAuthState({ commit }) {
            commit('REFRESH_STATE')
        }
    }
}
