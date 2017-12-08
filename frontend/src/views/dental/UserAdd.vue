<template>
  <v-container fluid>
    <v-form v-model="valid">
      <v-text-field label="Name"
        v-model="name"
        :rules="nameRules"
        :counter="10"
        required></v-text-field>
      <v-text-field label="E-mail"
        v-model="email"
        :rules="emailRules"
        required></v-text-field>
    </v-form>
    <AmiToolBar>
      <AmiButton @evUpdate="register"
        :self="{text: '등록', icon: 'done'}"></AmiButton>
      <AmiButton @evUpdate="goBack()"
        :self="{text: '취소', icon: 'cancel'}"></AmiButton>
    </AmiToolBar>
  </v-container>
</template>

<script>
import { routeMixin } from '@/mixin'
import AmiToolBar from '@/components/AmiToolBar'
import AmiButton from '@/components/AmiButton'

export default {
  mixins: [routeMixin],
  data() {
    return {
      valid: false,
      name: '',
      nameRules: [
        v => !!v || 'Name is required',
        v => v.length <= 10 || 'Name must be less than 10 characters'
      ],
      email: '',
      emailRules: [
        v => !!v || 'E-mail is required',
        v =>
          /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(v) ||
          'E-mail must be valid'
      ]
    }
  },
  methods: {
    register() {
      this.$http
        .post('/api/user_wait', {
          name: this.name,
          email: this.email,
          state: 'wait'
        })
        .then(() => {
          this.goBack()
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  components: {
    AmiToolBar,
    AmiButton
  }
}
</script>