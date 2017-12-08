<template>
  <v-card flat>
    <!-- <v-snackbar
      v-model="snackbar"
      absolute
      bottom
      color="success"
    >
      <span>ThankYou!. 정확하고 빠른 상담을 약속드립니다.</span>
      <v-icon dark>check_circle</v-icon>
    </v-snackbar> -->
    <v-form @submit.prevent="submit" ref="form">
      <v-container grid-list-xl fluid>
        <v-layout wrap>
          <v-flex xs12 sm6>
            <v-text-field
              color="purple darken-2"
              label="이름"
              required
              v-model="form.name"
              :rules="rules.name"
            ></v-text-field>
          </v-flex>
          <v-flex xs12 sm6>
            <v-text-field
              color="purple darken-2"
              label="제목"
              required
              v-model="form.subject"
              :rules="rules.subject"
            ></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field
              color="teal"
              multi-line
              required
              v-model="form.body"
              label="내용"
              :rules="rules.body"
            >
            </v-text-field>
          </v-flex>
          <v-flex xs12 sm6>
            <v-select
              color="pink"
              label="성별"
              v-model="form.sex"
              required
              :items="sex"
              :rules="rules.sex"
            ></v-select>
          </v-flex>
          <v-flex xs12 sm6>
            <v-slider
              color="orange"
              label="나이"
              hint="나이는 숫자에 불과합니다"
              min="1"
              max="100"
              thumb-label
              v-model="form.age"
              :rules="rules.age"
            ></v-slider>
          </v-flex>
          <v-flex xs12>
            <v-checkbox
              color="green"
              v-model="form.terms"
            >
              <div slot="label" @click.stop="">
                <a href="javascript:;" @click.stop="terms = true">개인정보제공</a>
                그리고
                <a href="javascript:;" @click.stop="conditions = true">약관</a>
                에 동의하시나요?
              </div>
            </v-checkbox>
          </v-flex>
        </v-layout>
      </v-container>
      <v-card-actions>
        <v-btn flat small color="primary" outline @click="resetForm">다시쓰기</v-btn>
        <v-btn flat small color="primary" outline @click="goBack()">돌아가기</v-btn>
        <v-spacer></v-spacer>
        <v-btn
          flat
          small
          outline
          color="primary"
          type="submit"
          :disabled="!formIsValid"
        >저장</v-btn>
      </v-card-actions>
    </v-form>
    <v-dialog v-model="terms" width="70%">
      <v-card>
        <v-card-title class="title">Terms</v-card-title>
        <v-card-text v-for="n in 5" :key="n">
          {{ content }}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            flat
            color="purple"
            @click="terms = false"
          >Ok</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="conditions" width="70%">
      <v-card>
        <v-card-title class="title">Conditions</v-card-title>
        <v-card-text v-for="n in 5" :key="n">
          {{ content }}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            flat
            color="purple"
            @click="conditions = false"
          >Ok</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import {routeMixin} from '@/mixin'

export default {
  mixins: [routeMixin],
  data() {
    const defaultForm = Object.freeze({
      name: '',
      subject: '',
      body: '',
      sex: '',
      age: null,
      terms: false
    })

    return {
      errors: [],
      form: Object.assign({}, defaultForm),
      rules: {
        age: [
          val => val < 8 || `I don't believe you!`
        ],
        sex: [val => (val || '').length > 0 || 'This field is required'],
        subject: [val => (val || '').length > 0 || 'This field is required'],
        body: [val => (val || '').length > 0 || 'This field is required'],
        name: [val => (val || '').length > 0 || 'This field is required']
      },
      sex: ['남', '여'],
      conditions: false,
      content: `개인정보를 제공하는것에 동의 합니다.`,
      // snackbar: false,
      terms: false,
      defaultForm
    }
  },

  computed: {
    formIsValid() {
      return (
        this.form.name &&
        this.form.subject &&
        this.form.body &&
        this.form.sex &&
        this.form.terms
      )
    }
  },

  methods: {
    resetForm() {
      this.form = Object.assign({}, this.defaultForm)
      this.$refs.form.reset()
    },
    submit() {
      // this.snackbar = true
      this.$http.post('/api/doctor/consulting', {
        author: this.form.name,
        subject: this.form.subject,
        body: this.form.body,
        sex: this.form.sex,
        age: this.form.age
      })
      .then(({ data }) => {
        let author = this.form.name
        let subject = this.form.subject
        this.resetForm()
        this.$router.push({name: 'DentalConsulting', params: {snackbar: true, author: author, subject: subject}})
      })
      .catch(e => {
          this.errors.push(e)
      })
    }
  }
}
</script>