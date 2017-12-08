<template>
  <v-container grid-list-md
    fluid>
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
          <v-toolbar-title>{{ currentName }}</v-toolbar-title>
        </v-toolbar>
      </v-card>
    </v-dialog> -->
    <v-layout>
      <v-flex xs4>
        <v-card flat>
          <v-toolbar flat
            dark
            light
            color="teal darken-3">
            <v-toolbar-title>
              <v-icon small>sentiment_very_satisfied</v-icon>
              잠시만 기다려주세요.<br> (대기 중: {{total}} 명)
            </v-toolbar-title>
          </v-toolbar>
          <v-list two-line
            name="next-item"
            is="transition-group">
            <v-list-tile v-for="item in items"
              :key="item.uid"
              @click="dialog = !dialog">
              <v-list-tile-action>
                <v-icon color="indigo">phone</v-icon>
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>{{item.name}}</v-list-tile-title>
                <v-list-tile-sub-title>{{item.email}}</v-list-tile-sub-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
        </v-card>
      </v-flex>
      <v-flex xs8>
        <v-alert outline
          color="success"
          icon="check_circle"
          :value="true">
          Comming soon. 뽀로로.
        </v-alert>
        <AmiToolBar>
          <AmiButton @evUpdate="go('/customer/add')"
            :self="{text: '등록', icon: 'add'}">
          </AmiButton>
        </AmiToolBar>
        <AmiBTable :headers="headers"
          @onDone="onDone"
          :items="waitUsers">
        </AmiBTable>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { routeMixin } from '@/mixin'
import { mapGetters } from 'vuex'
import types from '@/store/mutation-types'
import AmiButton from '@/components/AmiButton'
import AmiBTable from '@/components/AmiBTable'
import AmiToolBar from '@/components/AmiToolBar'

export default {
  mixins: [routeMixin],
  data() {
    return {
      dialog: false,
      headers: [
        { text: '이름', align: 'left', sortable: false, value: 'name' },
        { text: '이메일', value: 'email', sortable: false },
        {
          components: [
            {
              event: 'onDone',
              icon: 'done',
              component: AmiButton
            }
          ],
          sortable: false
        }
      ],
      waitUsers: [{ name: 'a', email: 'a@email.com' }]
    }
  },
  methods: {
    fetchData() {
      this.$http
        .get('/api/user_wait')
        .then(({ data }) => {
          this.waitUsers = data
        })
        .catch(e => {
          console.error(e)
        })
    },
    onDone(item) {
      this.$http
        .delete(`/api/user_wait/${item.uid}`)
        .then(({ data }) => {
          this.fetchData()
        })
        .catch(e => {
          console.error(e)
        })
    }
  },
  watch: {
    $route: 'fetchData'
  },
  computed: {
    ...mapGetters({
      items: types.WS_LIVESTREAM_GET,
      total: types.WS_LIVESTREAM_GET_TOTAL_COUNT
    })
  },
  created() {
    this.fetchData()
  },
  components: {
    AmiBTable,
    AmiToolBar,
    AmiButton
  }
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
</style>