// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuetify from 'vuetify'
import App from './App'
import store from './store'
import router from './router'
import axios from 'axios'
import VueNativeSock from 'vue-native-websocket'
// import socketio from 'socket.io-client'
// import VueSocketIO from 'vue-socket.io'

import ('vuetify/dist/vuetify.min.css')

Vue.prototype.$http = axios

// export const SocketInstance = socketio('ws://localhost:9000', {
//   transports: ['websocket']
// })
// Vue.use(VueSocketIO, SocketInstance)

let HOST = location.origin.replace(/^http/, 'ws')
HOST = HOST.split(':')
Vue.use(VueNativeSock, `${HOST[0]}:${HOST[1]}:9000`, {
  reconnection: true, // (Boolean) whether to reconnect automatically (false)
  reconnectionAttempts: 5, // (Number) number of reconnection attempts before giving up (Infinity),
  reconnectionDelay: 3000, // (Number) how long to initially wait before attempting a new (1000)
  store: store,
  format: 'json'
})
Vue.use(Vuetify)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  sockets: {
    // connect() {
    //   console.log('socket connected')
    // },
    // customEmit(val) {
    //   console.log('this method fired by socket server. eg: io.emit("customEmit", data)')
    // },
    // onopen() {
    //   this.$socket.send('hello')
    //     // this.$socket.onmessage = data => {
    //     //   console.log(data)
    //     // }
    // }
  },
  template: `
    <App/>
  `,
  components: {
    App
  },
  data: {},
  computed: {},
  methods: {},
  created() {}
})
