<template>
  <v-container fluid>
    <AmiToolBar>
      <AmiButton @evUpdate="go('/customer/add')"
        :self="{text: '등록', icon: 'add'}"></AmiButton>
      <AmiButton @evUpdate="onUserDelete"
        :valid="!!xtableData.selectedItems.length"
        :self="{text: '삭제', icon: 'delete'}"></AmiButton>
    </AmiToolBar>
    <AmiSTable @onDelete="onDelete"
      @recordClick="onRowClick"
      :headers="headers"
      :items="items"
      v-model="xtableData.selectedItems"
      itemKey="name">
    </AmiSTable>
    <AmiBTable :headers="xtableData.headers"
      :items="xtableData.items">
    </AmiBTable>
  </v-container>
</template>

<script>
import { routeMixin } from '@/mixin'
import AmiToolBar from '@/components/AmiToolBar'
import AmiButton from '@/components/AmiButton'
import AmiSTable from '@/components/AmiSTable'
import AmiBTable from '@/components/AmiBTable'

export default {
  mixins: [routeMixin],
  computed: {
    headers() {
      let headers = Array.from(this.xtableData.headers)
      headers.push({
        sortable: false,
        components: [
          {
            event: 'onDelete',
            icon: 'delete',
            text: '삭제',
            component: AmiButton
          },
          {
            event: 'onDelete',
            icon: 'update',
            text: '수정',
            component: AmiButton
          }
        ]
      })
      return headers
    },
    items() {
      return this.xtableData.items
      // return this.xtableData.items.map(n => {
      //   const item = Object.assign(n, { edit: `${n['name']}-edit` })
      //   return item
      // })
    }
  },
  data() {
    return {
      randomNumber: 0,
      xtableData: {
        selectedItems: [],
        headers: [
          {
            text: 'Dessert (100g serving)',
            align: 'left',
            sortable: false,
            value: 'name'
          },
          { text: 'Calories', value: 'calories' },
          { text: 'Fat (g)', value: 'fat' },
          { text: 'Carbs (g)', value: 'carbs' },
          { text: 'Protein (g)', value: 'protein' },
          { text: 'Sodium (mg)', value: 'sodium' },
          { text: 'Calcium (%)', value: 'calcium' },
          { text: 'Iron (%)', value: 'iron' }
        ],
        items: [
          {
            value: false,
            name: 'Frozen Yogurt',
            calories: 159,
            fat: 6.0,
            carbs: 24,
            protein: 4.0,
            sodium: 87,
            calcium: '14%',
            iron: '1%'
          },
          {
            value: false,
            name: 'Ice cream sandwich',
            calories: 237,
            fat: 9.0,
            carbs: 37,
            protein: 4.3,
            sodium: 129,
            calcium: '8%',
            iron: '1%'
          },
          {
            value: false,
            name: 'Eclair',
            calories: 262,
            fat: 16.0,
            carbs: 23,
            protein: 6.0,
            sodium: 337,
            calcium: '6%',
            iron: '7%'
          },
          {
            value: false,
            name: 'Cupcake',
            calories: 305,
            fat: 3.7,
            carbs: 67,
            protein: 4.3,
            sodium: 413,
            calcium: '3%',
            iron: '8%'
          },
          {
            value: false,
            name: 'Gingerbread',
            calories: 356,
            fat: 16.0,
            carbs: 49,
            protein: 3.9,
            sodium: 327,
            calcium: '7%',
            iron: '16%'
          },
          {
            value: false,
            name: 'Jelly bean',
            calories: 375,
            fat: 0.0,
            carbs: 94,
            protein: 0.0,
            sodium: 50,
            calcium: '0%',
            iron: '0%'
          },
          {
            value: false,
            name: 'Lollipop',
            calories: 392,
            fat: 0.2,
            carbs: 98,
            protein: 0,
            sodium: 38,
            calcium: '0%',
            iron: '2%'
          },
          {
            value: false,
            name: 'Honeycomb',
            calories: 408,
            fat: 3.2,
            carbs: 87,
            protein: 6.5,
            sodium: 562,
            calcium: '0%',
            iron: '45%'
          },
          {
            value: false,
            name: 'Donut',
            calories: 452,
            fat: 25.0,
            carbs: 51,
            protein: 4.9,
            sodium: 326,
            calcium: '2%',
            iron: '22%'
          },
          {
            value: false,
            name: 'KitKat',
            calories: 518,
            fat: 26.0,
            carbs: 65,
            protein: 7,
            sodium: 54,
            calcium: '12%',
            iron: '6%'
          }
        ]
      }
    }
  },
  methods: {
    onRowClick(n) {
      console.log(n)
    },
    onClick(item) {
      const path = '/api/random'
      this.$http
        .get(path, {
          params: {
            id: 1234
          }
        })
        .then(response => {
          this.randomNumber = response.data.randomNumber
        })
        .catch(error => {
          console.log(error)
        })
    },
    onDelete(item) {
      this.xtableData.items = this.xtableData.items.filter(n => {
        if (n.name === item.name) {
          return false
        }
        return true
      })
    },
    onUserDelete() {
      for (const item of this.xtableData.selectedItems) {
        this.$http.delete(`/api/users/${item.name}`)
      }
    }
  },
  watch: {
    'xtableData.selectedItems'(n, o) {
      console.log(this.xtableData.selectedItems)
    }
  },
  created() {},
  components: {
    AmiButton,
    AmiSTable,
    AmiBTable,
    AmiToolBar
  }
}
</script>
