<template>
  <v-container fluid>
    <v-dialog v-model="dialog"
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
    </v-dialog>
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
    </AmiToolBar>
    <AmiBPaginateTable :headers="headers"
      :items="stock.items"
      :loading="loading"
      :totalItems="stock.totalLength"
      :pagination="pagination"
      @recordClick="onClickStock"
      @update:pagination="onUpdatePagination">
    </AmiBPaginateTable>
    <v-navigation-drawer right
      temporary
      v-model="right"
      fixed
      width=500>
      <AmiBTable :headers="stockHeaders"
        :items="stockData">
      </AmiBTable>
    </v-navigation-drawer>
  </v-container>
</template>

<script>
// import _ from 'lodash'
import { routeMixin } from '@/mixin'
import AmiBTable from '@/components/AmiBTable'
import AmiBPaginateTable from '@/components/AmiBPaginateTable'
import AmiSearchBox from '@/components/AmiSearchBox'
import AmiToolBar from '@/components/AmiToolBar'
import AmiButton from '@/components/AmiButton'

export default {
  mixins: [routeMixin],
  data() {
    return {
      loading: true,
      pagination: {},
      headers: [
        {
          text: '종목',
          align: 'left',
          value: 'stockName'
        },
        {
          sortable: false,
          text: '투자의견',
          value: 'stockCode',
          render(item) {
            if (item.per && item.eps1 && item.eps2) {
              let price = parseFloat(item.curPrice.replace(/,/gi, ''))
              let e1 = parseFloat(item.per) * parseFloat(item.eps1)
              let e2 = parseFloat(item.per) * parseFloat(item.eps2)

              if (price < e1 && price < e2) {
                return `추천(${e1.toFixed(2)} ~ ${e2.toFixed(2)})`
              }
              if (price < e1 || price < e2) {
                return `-(${e1.toFixed(2)} ~ ${e2.toFixed(2)})`
              }
              return `나쁨(${e1.toFixed(2)} ~ ${e2.toFixed(2)})`
            }
            return '??'
          }
        },
        {
          sortable: false,
          text: '현재가',
          value: 'curPrice'
        },
        {
          sortable: false,
          text: '전일비',
          value: 'sise',
          components: [
            {
              component: {
                props: ['self', 'item'],
                template: `
                  <div>
                    <span>{{item.sise}}</span>
                    <v-icon v-if='item.down' light>arrow_downward</v-icon>
                    <v-icon v-else light>arrow_upward</v-icon>
                  </div>
                `
              }
            }
          ]
        },
        {
          sortable: false,
          text: '전일비(%)',
          value: 'rate'
        }
      ],
      stockHeaders: [
        { text: '날짜', value: 'date', align: 'left' },
        { text: '종가', value: 'curPrice' },
        {
          text: '전일비',
          value: 'sise',
          components: [
            {
              component: {
                props: ['self', 'item'],
                template: `
                  <div>
                    <span>{{item.sise}}</span>
                    <v-icon v-if='item.down' light>arrow_downward</v-icon>
                    <v-icon v-else light>arrow_upward</v-icon>
                  </div>
                `
              }
            }
          ]
        },
        { text: '거래량', value: 'volume' }
      ],
      stock: {
        items: [],
        totalLength: 0
      },
      stockData: [],
      errors: [],
      isViewSearchBox: false,
      search: '',
      currentName: '',
      currentCode: '',
      dialog: false,
      right: false
    }
  },
  watch: {
    $route: 'fetchData'
    // search() {
    //   this.getAnswer()
    // }
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
    // getAnswer: _.debounce(function() {
    //   this.fetchData(this.pagination, this.search)
    // }, 500),
    onClickStock({ stockName, stockCode }) {
      this.$http
        .get(`/api/stocks/${stockCode}`)
        .then(({ data }) => {
          this.currentName = stockName
          this.currentCode = stockCode
          this.right = true
          this.stockData = data
        })
        .catch(e => {
          this.errors.push(e)
        })
    },
    fetchData(
      {
        sortBy = 'stockName',
        descending = false,
        page = 1,
        rowsPerPage = 10
      } = {},
      question = ''
    ) {
      this.$http
        .get('/api/stocks', {
          params: { sortBy, descending, page, rowsPerPage, question }
        })
        .then(({ data }) => {
          this.stock.items = Array.from(data.stocks, i => {
            i.value = false
            return i
          })
          // this.stock.items = data.stocks.map(i => {
          //   i.vaue = false
          //   return i
          // })
          this.stock.totalLength = data.totalLength
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
    AmiBTable,
    AmiBPaginateTable,
    AmiSearchBox,
    AmiToolBar,
    AmiButton
  }
}
</script>