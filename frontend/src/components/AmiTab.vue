<template>
  <v-tabs :id="id"
    @input="tabsInput"
    grow>
    <v-tabs-bar>
      <v-tabs-slider color="primary"></v-tabs-slider>
      <v-tabs-item v-for="(tab, index) in tabs"
        :href="'#' + id + '-' + index"
        class="primary--text"
        :key="index">
        {{tab.text}}
      </v-tabs-item>
    </v-tabs-bar>
    <v-tabs-items>
      <v-tabs-content v-for="(tab, index) in tabs"
        :key="index"
        :id="id + '-' + index">
        <v-card flat
          v-if="tab.intro">
          <v-card-text>{{ tab.intro }}</v-card-text>
        </v-card>
        <v-card flat
          v-if="tab.subMenu">
          <AmiButton v-for="(sub, subIndex) in tab.subMenu"
            @evUpdate="go(sub.path)"
            :self="{text: sub.text, icon: sub.icon}"
            :key="subIndex">
          </AmiButton>
        </v-card>
        <v-card flat
          v-if="tab.component">
          <component :is="tab.component">
          </component>
        </v-card>
      </v-tabs-content>
    </v-tabs-items>
  </v-tabs>
</template>

<script>
import { routeMixin } from '@/mixin'
import AmiButton from '@/components/AmiButton'

export default {
  mixins: [routeMixin],
  props: ['id', 'tabs'],
  data() {
    return {}
  },
  components: {
    AmiButton
  },
  methods: {
    tabsInput(e) {
      this.$emit('input', e)
    }
  }
}
</script>
