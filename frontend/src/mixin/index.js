const routeMixin = {
  methods: {
    goBack() {
      window.history.length > 1 ? this.$router.go(-1) : this.$router.push('/')
    },
    go(path) {
      this.$router.push(path)
    }
  }
}

export {
  routeMixin
}
