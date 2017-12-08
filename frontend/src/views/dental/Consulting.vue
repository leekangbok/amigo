<template>
  <v-container fluid>
    <v-snackbar v-model="snackbar"
      absolute
      top
      color="success">
      <span>{{author}} 님, Thankyou!. '{{subject}}' 글이 저장되었습니다. 정확하고 빠른 상담을 약속드립니다.</span>
      <v-icon dark>check_circle</v-icon>
    </v-snackbar>
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
      <AmiButton @evUpdate="go('/dental/Intro/ConsultingAdd')"
        :self="{text: '글쓰기', icon: 'add'}">
      </AmiButton>
    </AmiToolBar>
    <AmiBPaginateTable :headers="headers"
      :items="consults.items"
      :loading="loading"
      :totalItems="consults.total"
      :pagination="pagination"
      @recordClick="onEdit"
      @update:pagination="onUpdatePagination">
    </AmiBPaginateTable>
  </v-container>
</template>

<script>
import { routeMixin } from '@/mixin'
import AmiBPaginateTable from '@/components/AmiBPaginateTable'
import AmiSearchBox from '@/components/AmiSearchBox'
import AmiButton from '@/components/AmiButton'
import AmiToolBar from '@/components/AmiToolBar'
import moment from 'moment'

export default {
  mixins: [routeMixin],
  props: {
    snackbar: {
      type: Boolean,
      default: false
    },
    author: {
      type: String,
      default: ''
    },
    subject: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      isViewSearchBox: false,
      search: '',
      consults: {
        items: [],
        total: 0
      },
      loading: true,
      pagination: {},
      headers: [
        {
          text: '번호',
          align: 'left',
          value: 'sequence',
          sortable: false
        },
        {
          sortable: false,
          text: '제목',
          value: 'subject'
        },
        {
          sortable: false,
          text: '글쓴이',
          value: 'author'
        },
        {
          sortable: false,
          text: '등록일',
          value: 'reg_date',
          render(item, value) {
            let timestamp = moment.unix(value)
            return timestamp.format('YYYY-MM-DD HH:mm:ss')
          }
        },
        {
          sortable: false,
          text: '조회수',
          value: 'clicked'
        },
        {
          sortable: false,
          text: '댓글',
          value: 'reply',
          render(item, value) {
            return value.length
          }
        }
      ],
      errors: []
    }
  },
  watch: {
    $route: 'fetchData'
  },
  methods: {
    searchBoxClose() {
      this.isViewSearchBox = false
      this.search = ''
      this.loading = true
      this.pagination.page = 1
      this.fetchData(this.pagination, this.search)
    },
    doSearch(action) {
      if (action === 'enter') {
        this.loading = true
        this.pagination.page = 1
        this.fetchData(this.pagination, this.search)
      } else {
        this.searchBoxClose()
      }
    },
    onEdit({ uid }) {
      this.$http
        .get(`/api/doctor/consulting/${uid}`)
        .then(({ data }) => {
          console.log(data)
          this.$router.push({
            name: 'DentalConsultingEdit',
            params: {
              author: data.items[0].author,
              subject: data.items[0].subject,
              body: data.items[0].body,
              uid: data.items[0].uid,
              reply: data.items[0].reply
            }
          })
        })
        .catch(e => {
          this.errors.push(e)
        })
    },
    fetchData(
      { sortBy = '', descending = false, page = 1, rowsPerPage = 10 } = {},
      question = ''
    ) {
      this.$http
        .get('/api/doctor/consulting', {
          params: {
            sortBy,
            descending,
            page: (page - 1) * rowsPerPage,
            rowsPerPage,
            subject: question,
            author: question,
            body: question
          }
        })
        .then(({ data }) => {
          this.consults.items = data.items
          this.consults.total = data.result.total
          for (let [index, item] of this.consults.items.entries()) {
            item.sequence =
              this.consults.total - (page - 1) * rowsPerPage - index
          }
          this.loading = false
        })
        .catch(e => {
          this.errors.push(e)
        })
    },
    onUpdatePagination({ sortBy, descending, page, rowsPerPage }) {
      this.loading = true
      this.pagination = { sortBy, descending, page, rowsPerPage }
      this.fetchData(this.pagination, this.search)
    }
  },
  created() {
    this.fetchData(this.pagination)
  },
  computed: {},
  components: {
    AmiBPaginateTable,
    AmiSearchBox,
    AmiButton,
    AmiToolBar
  }
}
</script>