import Vue from 'vue'
import VueRouter from 'vue-router'
import Welcome from '@/components/Welcome'
import store from '@/store'
import types from '@/store/mutation-types'

Vue.use(VueRouter)

const routes = [{
    path: '/',
    component: Welcome
  },
  ...store.getters[types.GET_ROUTES]
]

export default new VueRouter({
  routes
})
