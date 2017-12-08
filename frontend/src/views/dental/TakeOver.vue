<template>
  <v-container fluid>
    <AmiToolBar :spacer="1">
      <AmiSearchBox :spacer="0"
        v-model="search"
        @evUpdate="doSearch"
        v-if="isViewSearchBox">
      </AmiSearchBox>
      <AmiButton @evUpdate="isViewSearchBox = true"
        :self="{icon: 'search'}"
        v-if="!isViewSearchBox">
      </AmiButton>
      <AmiButton @evUpdate="go('/dental/UserAdd')"
        :self="{text: '등록', icon: 'add'}">
      </AmiButton>
    </AmiToolBar>
    <AmiBTable :headers="headers"
      @onDone="onDone"
      :items="wsWaitAllUsers"
      :search="search">
    </AmiBTable>
  </v-container>
</template>

<script>
import { routeMixin } from '@/mixin'
import { mapGetters } from 'vuex'
import types from '@/store/mutation-types'
import AmiButton from '@/components/AmiButton'
import AmiBTable from '@/components/AmiBTable'
import AmiToolBar from '@/components/AmiToolBar'
import AmiSearchBox from '@/components/AmiSearchBox'

export default {
  mixins: [routeMixin],
  data() {
    return {
      isViewSearchBox: false,
      search: '',
      dialog: false,
      headers: [
        { text: '순서', align: 'left', value: 'pri', sortable: false },
        { text: '이름', sortable: false, value: 'name' },
        { text: '상태', sortable: false, value: 'state' },
        {
          components: [
            {
              event: 'onDone',
              icon: 'done',
              // text: '검진완료',
              textRender(self, item) {
                if (item.state === 'wait') {
                  return '검진'
                }
                if (item.state === 'ing') {
                  return '검진완료'
                }
                return '뭐야'
              },
              component: AmiButton
            }
          ],
          sortable: false
        }
      ],
      waitAllUsers: []
    }
  },
  methods: {
    // fetchData() {
    //   this.$http
    //     .get('/api/user_wait')
    //     .then(({ data }) => {
    //       this.waitAllUsers = data
    //     })
    //     .catch(e => {
    //       console.error(e)
    //     })
    // },
    onDone(item) {
      if (item.state === 'wait') {
        this.$http
          .put(`/api/user_wait/${item.uid}`, {
            ...item,
            state: 'ing'
          })
          .then(({ data }) => {})
          .catch(e => {
            console.error(e)
          })
      } else {
        this.$http
          .delete(`/api/user_wait/${item.uid}`)
          .then(({ data }) => {
            // this.fetchData()
          })
          .catch(e => {
            console.error(e)
          })
      }
    },
    searchBoxClose() {
      this.isViewSearchBox = false
      this.search = ''
    },
    doSearch(action) {
      if (action === 'enter') {
      } else {
        this.searchBoxClose()
      }
    }
  },
  watch: {
    $route: 'fetchData'
  },
  computed: {
    ...mapGetters({
      waitUsers: types.WS_LIVESTREAM_GET,
      total: types.WS_LIVESTREAM_GET_TOTAL_COUNT,
      wsWaitAllUsers: types.WS_WAITALLUSERS_GET
    })
  },
  created() {
    // this.fetchData()
  },
  components: {
    AmiBTable,
    AmiToolBar,
    AmiButton,
    AmiSearchBox
  }
}
</script>