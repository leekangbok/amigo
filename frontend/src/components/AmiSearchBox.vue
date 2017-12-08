<template>
  <v-card-title>
    <v-spacer v-for="(i, index) of spacer"
      :key="index"></v-spacer>
    <v-text-field :max="max"
      autofocus
      append-icon="cancel"
      single-line
      hide-details
      :value="value"
      :label="label"
      @input="n => $emit('input', n)"
      :append-icon-cb="() => $emit(eventName, 'cancel')"
      @keyup.enter="() => $emit(eventName, 'enter')"
      loading
      light>
      <v-progress-linear slot="progress"
        :value="progress"
        height="7"
        :color="color"></v-progress-linear>
    </v-text-field>
  </v-card-title>
</template>

<script>
export default {
  props: {
    eventName: {
      type: String,
      default: 'evUpdate'
    },
    spacer: {
      type: Number,
      default: 1
    },
    value: {
      type: String,
      default: ''
    },
    max: {
      type: Number,
      default: 30
    },
    label: {
      type: String,
      default: ''
    }
  },
  data() {
    return {}
  },
  methods: {},
  computed: {
    progress() {
      return Math.min(100, this.value.length * 10)
    },
    color() {
      return ['error', 'warning', 'success'][Math.floor(this.progress / 40)]
    }
  }
}
</script>