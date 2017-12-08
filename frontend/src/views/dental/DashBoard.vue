<template>
  <v-container grid-list-md
    fluid>
    <v-snackbar :timeout="6000"
      :top="true"
      color="cyan darken-2"
      v-model="dialog">
      {{ currentName }} 님 진료실에서 뵙겠습니다
    </v-snackbar>
    <!-- <v-dialog v-model="dialog"
      fullscreen
      transition="dialog-bottom-transition"
      :overlay=false>
      <v-card>
        <v-toolbar dark
          color="primary">
          <v-btn icon
            @click.native="dialog = false"
            dark>
            <v-icon>close</v-icon>
          </v-btn>
          <v-toolbar-title>{{currentName}}</v-toolbar-title>
        </v-toolbar>
      </v-card>
    </v-dialog> -->
    <v-layout row wrap>
      <v-flex d-flex xs12 sm6 md3>
        <v-card flat>
          <v-toolbar flat
            color="primary"
            dark>
            <v-toolbar-title center>
              <v-icon small>schedule</v-icon>
              뽀로로 <span class="yellow--text text--accent-2">{{nbun[total]}}</span> 보고계시네요
            </v-toolbar-title>
          </v-toolbar>
          <v-list two-line
            name="next-item"
            is="transition-group">
            <v-list-tile v-for="item in waitUsers"
              :key="item.uid"
              @click="">
              <v-list-tile-action color="primary--text">
                {{item.pri}}.
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>{{item.name}}</v-list-tile-title>
                <v-list-tile-sub-title>{{item.state === 'ing' ? '진료 중' : item.email}}</v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
        </v-card>
      </v-flex>
      <v-flex xs12 sm6 md9>
        <v-card flat
          height="450">
          <v-alert outline
            color="success"
            icon="check_circle"
            :value="true">
            Comming soon. 뽀로로.
          </v-alert>
          <div class="h_iframe">
            <iframe src="https://www.youtube.com/embed/XGSy3_Czz8k?autoplay=1">
            </iframe>
          </div>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex'
import types from '@/store/mutation-types'

export default {
  data() {
    return {
      // dialog: false
      nbun: ['아무도 안', '한 분', '두 분', '세 분', '네 분', '다섯 분', '여섯 분', '일곱 분', '여덟 분', '아홉 분', '열 분', '열한 분', '열두 분', '열세 분', '열네 분', '열다섯 분']
    }
  },
  methods: {},
  watch: {},
  computed: {
    ...mapGetters({
      waitUsers: types.WS_LIVESTREAM_GET,
      total: types.WS_LIVESTREAM_GET_TOTAL_COUNT,
      currentName: types.WS_WAITUSER_CURRENT_GET
    }),
    dialog: {
      get() {
        return this.$store.getters[types.WS_WAITUSER_WELCOME_GET]
      },
      set(n) {
        this.$store.commit({ type: types.WS_WAITUSER_WELCOME_SET, welcome: n })
      }
    }
  },
  created() {},
  components: {}
}
</script>

<style scoped>
.next-item {
  transition: all 2s;
}
.next-item-enter-active,
.next-item-leave-active {
  transition: all 3s;
}
.next-item-enter,
.next-item-leave-to {
  transform: translateY(-30px);
  /* transform: scaleY(0); */
  opacity: 0;
}
.next-item-move {
  transition: transform 2s;
}
.h_iframe iframe {
  width: 100%;
  height: 100%;
}
.h_iframe {
  height: 100%;
  width: 100%;
}
</style>