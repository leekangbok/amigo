<template>
  <v-btn outline
    small
    color="primary"
    :disabled="!valid"
    @click.stop="$emit(eventName, self)">
    <template v-if="icon">
      <v-icon light
        left
        class="ma-0 pa-0">{{icon}}</v-icon>
      {{text ? text : ''}}
    </template>
    <template v-else>
      {{text ? text : ''}}
    </template>
  </v-btn>
</template>
                                                                                                                                                                                                    
<script>
export default {
  props: {
    self: Object,
    valid: {
      type: Boolean,
      default: true
    },
    eventName: {
      type: String,
      default: 'evUpdate'
    },
    item: {
      type: Object,
      default() {
        return {}
      }
    }
  },
  data() {
    return {}
  },
  computed: {
    icon() {
      if (this.self.iconRender) {
        return this.self.iconRender(this.self, this.item)
      }
      return this.self.icon
    },
    text() {
      if (this.self.textRender) {
        return this.self.textRender(this.self, this.item)
      }
      return this.self.text
    }
  }
}
</script>