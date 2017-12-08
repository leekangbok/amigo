<template>
  <v-container fluid>
    <AmiTab :id="id"
      @input="tabChanged"
      :tabs="tabs">
    </AmiTab>
    <router-view></router-view>
  </v-container>
</template>

<script>
import { routeMixin } from '@/mixin'
import AmiTab from '@/components/AmiTab'
import Implant from '@/views/dental/Implant'

export default {
  mixins: [routeMixin],
  data() {
    return {
      id: 'intro-tab',
      tabs: [
        {
          text: '치과소개',
          intro: `안녕하세요. 여러분의 가족 오치과 입니다`,
          subMenu: [
            { path: '/dental/Intro/Profile', text: '원장님소개' },
            { path: '/dental/Intro/Home', text: '치과둘러보기' }
          ]
        },
        {
          text: '임플란트',
          intro:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
          component: Implant
        },
        {
          text: '치아성형',
          intro:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
        },
        {
          text: '치아교정',
          intro:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
        },
        {
          text: '일반치료',
          intro:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
        },
        {
          text: '상담및예약',
          intro: `친절하고 정직하고 빠른 상담을 약속드립니다`,
          subMenu: [
            { path: '/dental/Intro/Consulting', text: '상담하기' },
            { path: '/dental/Intro/Reservation', text: '예약하기' }
          ]
        }
      ]
    }
  },
  components: {
    AmiTab
  },
  methods: {
    tabChanged(e) {
      this.go('/dental/Intro/default')
    }
  }
}
</script>