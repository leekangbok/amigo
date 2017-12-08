import Vue from 'vue'
import vuex from 'vuex'
import menu from './menu'
import ws from './ws'

Vue.use(vuex)

const state = {
  socket: {
    isConnected: false,
    message: '',
    reconnectError: false
  }
}

export default new vuex.Store({
  state,
  mutations: {
    SOCKET_ONOPEN(state, event) {
      state.socket.isConnected = true
      console.log('connected')
    },
    SOCKET_ONCLOSE(state, event) {
      state.socket.isConnected = false
      console.log('closed')
    },
    SOCKET_ONERROR(state, event) {
      console.error(state, event)
    },
    // default handler called for all methods
    SOCKET_ONMESSAGE(state, message) {
      state.message = message
      console.log(message)
    },
    // mutations for reconnect methods
    SOCKET_RECONNECT(state, count) {
      console.info(state, count)
    },
    SOCKET_RECONNECT_ERROR(state) {
      state.socket.reconnectError = true
    },
    SOCKET_TEST(state, message) {
      console.log('test', message)
    }
  },
  modules: {
    menu,
    ws
  }
})
