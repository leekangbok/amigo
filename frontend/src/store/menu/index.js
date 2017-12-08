import _ from 'lodash'
import types from '../mutation-types'
import items from './items'

const state = {
  items: [...items]
}

const mutations = {}

const getters = {
  [types.GET_SIDEBAR_MENU](state, getters) {
    return _.sortBy(_.filter(state.items, n => n.pri), [function (o) {
      return o.pri
    }])
  },
  [types.GET_ROUTES](state, getters) {
    return generateRoutes(state.items)
  }
}

function generateRoutes(menu = [], routes = []) {
  for (let i = 0, l = menu.length; i < l; i++) {
    let item = menu[i]

    if (item.path) {
      routes.push(item)
    }
    if (!item.component) {
      generateRoutes(item.children, routes)
    }
  }
  return routes
}

export default {
  state,
  mutations,
  getters
}
