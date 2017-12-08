import _ from 'lodash'
import types from '../mutation-types'

const state = {
  totalCount: 0,
  waitUsers: [],
  waitAllUsers: [],
  welcome: false,
  currentName: ''
}

const mutations = {
  [types.WS_WAITUSER_WELCOME_SET](state, { welcome, currentName = '' }) {
    state.welcome = welcome
    state.currentName = currentName
  },
  [types.WS_TEST](state, message) {},
  [types.WS_LIVESTREAM_APPEND](state, message) {
    state.totalCount = message.total

    for (let data of message.data) {
      let idx

      idx = _.findIndex(state.waitUsers, o => o.uid === data.uid)
      if (idx !== -1) {
        state.waitUsers.splice(idx, 1, data)
      } else {
        state.waitUsers.push(data)
      }

      idx = _.findIndex(state.waitAllUsers, o => o.uid === data.uid)
      if (idx !== -1) {
        state.waitAllUsers.splice(idx, 1, data)
      } else {
        state.waitAllUsers.push(data)
      }
    }

    if (state.waitUsers.length > 8) {
      state.waitUsers.splice(0, 1)
    } else {
      state.waitUsers = state.waitUsers.sort((a, b) => a.pri - b.pri)
    }
  },
  [types.WS_LIVESTREAM_DELETE](state, message) {
    state.waitUsers = state.waitUsers.filter(o => o.uid !== message.uid)
    state.totalCount = state.waitUsers.length

    state.waitAllUsers = state.waitAllUsers.filter(o => o.uid !== message.uid)
  },
  [types.WS_WAITALLUSERS_APPEND](state, message) {
    if (message.data.length === 0) {
      state.waitAllUsers.splice(0, state.waitAllUsers.length)
      return
    }
    for (let data of message.data) {
      let idx = _.findIndex(state.waitAllUsers, o => o.uid === data.uid)
      if (idx !== -1) {
        state.waitAllUsers.splice(idx, 1, data)
      } else {
        state.waitAllUsers.push(data)
      }
    }
  }
}

const getters = {
  [types.WS_LIVESTREAM_GET](state) {
    return state.waitUsers
  },
  [types.WS_LIVESTREAM_GET_TOTAL_COUNT](state) {
    return state.totalCount
  },
  [types.WS_WAITALLUSERS_GET](state) {
    return state.waitAllUsers
  },
  [types.WS_WAITUSER_WELCOME_GET](state) {
    return state.welcome
  },
  [types.WS_WAITUSER_CURRENT_GET](state) {
    return state.currentName
  }
}

export default {
  state,
  mutations,
  getters
}
