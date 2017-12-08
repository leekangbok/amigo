<template>
  <v-card flat>
    <v-dialog v-model="dialog"
      persistent
      max-width="500px">
      <v-card>
        <v-card-title>
          <span class="indigo--text">{{subject}} 글에 대한 댓글 작성 중입니다</span>
        </v-card-title>
        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12>
                <v-text-field color="purple darken-2"
                  label="이름"
                  required v-model="replyName"></v-text-field>
              </v-flex>
              <v-flex>
                <v-text-field color="teal"
                  label="내용"
                  multi-line
                  required v-model="replyBody"></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
          <small>*는 필수입력 항목입니다</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn flat small color="primary" outline
            @click.native="dialog = false">취소</v-btn>
          <v-btn flat small color="primary" outline
            @click.native="onReplySave">저장</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-form @submit.prevent="submit"
      ref="form">
      <v-container grid-list-xl
        fluid>
        <v-layout wrap>
          <v-flex xs12
            sm6>
            <v-text-field color="purple darken-2"
              label="이름"
              :value="author"
              disabled></v-text-field>
          </v-flex>
          <v-flex xs12
            sm6>
            <v-text-field color="purple darken-2"
              label="제목"
              :value="subject"
              :rules="rules.subject"
              disabled></v-text-field>
          </v-flex>
          <v-flex xs12>
            <v-text-field color="teal"
              multi-line
              :value="body"
              label="내용"
              disabled>
            </v-text-field>
          </v-flex>
        </v-layout>
      </v-container>
      <v-card-actions>
        <v-btn flat
          small
          color="primary"
          outline
          @click="dialog = true">댓글달기</v-btn>
        <v-btn flat
          small
          color="primary"
          outline
          @click="goBack()">돌아가기</v-btn>
        <!-- <v-spacer></v-spacer> -->
        <!-- <v-btn flat
          small
          outline
          color="primary"
          type="submit">저장</v-btn> -->
      </v-card-actions>
    </v-form>
    <v-text-field v-for="(r, index) in this.reply" v-model="r.body" :key="index" disabled></v-text-field>
  </v-card>
</template>

<script>
import { routeMixin } from '@/mixin'

export default {
  mixins: [routeMixin],
  props: ['author', 'subject', 'body', 'uid', 'reply'],
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
      dialog: false,
      errors: [],
      form: Object.assign({}, defaultForm),
      rules: {
        age: [val => val < 8 || `I don't believe you!`],
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
      defaultForm,
      replyName: '',
      replyBody: ''
    }
  },

  computed: {},

  methods: {
    onReplyCancel() {
      this.replyName = ''
      this.replyBody = ''
    },
    onReplySave() {
      this.$http
      .post('/api/doctor/consulting_reply', {
        consulting_uid: this.uid,
        author: this.replyName,
        body: this.replyBody
      })
      .then(({ data }) => {
        this.reply.push({body: this.replyBody})
        this.dialog = false
        this.replyName = ''
        this.replyBody = ''
      })
      .catch(e => {
          this.errors.push(e)
      })
    },
    resetForm() {
      this.form = Object.assign({}, this.defaultForm)
      this.$refs.form.reset()
    },
    submit() {
      // this.snackbar = true
      this.$http
        .post('/api/doctor/consulting', {
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
          this.$router.push({
            name: 'DentalConsulting',
            params: { snackbar: true, author: author, subject: subject }
          })
        })
        .catch(e => {
          this.errors.push(e)
        })
    }
  }
}
</script>