<template>
  <v-app id="inspire">
    <SideNav :items="menus"
      :drawer.sync="drawer"></SideNav>
    <v-toolbar color="light-blue darken-4"
      dark
      app
      clipped-left
      fixed>
      <v-toolbar-title :style="$vuetify.breakpoint.smAndUp ? 'width: 300px; min-width: 250px' : 'min-width: 72px'"
        class="ml-0 pl-3">
        <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
        <span class="hidden-xs-only">Ami
          <span class="teal--text text--lighten-1">Go</span>
        </span>
      </v-toolbar-title>
    </v-toolbar>
    <v-content>
      <v-container fluid>
        <transition name="route-fade"
          mode="out-in"
          appear>
          <router-view></router-view>
        </transition>
      </v-container>
    </v-content>
    <v-footer color="light-blue darken-4"
      dark
      class="white--text"
      app>
      <span>Sonrie, es un mal dia no una mala vida, Smile, it's been just a bad day, not a bad life</span>
      <v-spacer></v-spacer>
      <span>&copy; 2017</span>
    </v-footer>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex'
import types from './store/mutation-types'
import SideNav from './components/SideNav'

export default {
  components: {
    SideNav
  },
  computed: {
    ...mapGetters({
      menus: types.GET_SIDEBAR_MENU
    })
  },
  data() {
    return {
      drawer: true
    }
  },
  created() {}
}
</script>

<style>
.content {
  background-color: white;
}
.route-fade-enter-active,
.route-fade-leave-active {
  transition: opacity 0.5s;
}

.route-fade-enter,
.route-fade-leave-active {
  opacity: 0;
}
</style>