<template>
  <v-navigation-drawer fixed
    clipped
    app
    :value="drawer"
    @input="value => $emit('update:drawer', value)"
    width=250
    class="blue-grey darken-4"
    dark>
    <v-list dense>
      <template v-for="(item, i) in items">
        <v-list-group v-if="item.children"
          v-model="item.model"
          no-action>
          <v-list-tile slot="item"
            @click="">
            <v-list-tile-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>
                {{ item.text }}
              </v-list-tile-title>
            </v-list-tile-content>
            <v-list-tile-action>
              <v-icon>keyboard_arrow_down</v-icon>
            </v-list-tile-action>
          </v-list-tile>
          <v-list-tile v-for="(child, i) in item.children"
            :key="i"
            @click="$router.push(child.path)">
            <v-list-tile-action>
              <v-icon></v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>
                {{ child.text }}
              </v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </v-list-group>
        <v-list-tile v-else
          @click="$router.push(item.path)">
          <v-list-tile-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title>
              {{ item.text }}
            </v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </template>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  props: ['items', 'drawer'],
  computed: {},
  data() {
    return {}
  }
}
</script>

<style>
#keep main .container {
  height: 660px;
}
/* .navigation-drawer__border {
  display: none;
} */
/* .text {
  font-weight: 400;
}
*/
.list__tile__title {
  font-weight: 600;
}
</style>