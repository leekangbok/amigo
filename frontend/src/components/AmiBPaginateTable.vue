<template>
  <v-data-table :headers="headers"
    :items="items"
    :pagination="pagination"
    @update:pagination="n => $emit('update:pagination', n)"
    :total-items="totalItems"
    :loading="loading"
    class="elevation-0"
    :rows-per-page-items="[10, 20, 40, 80, { text: 'All', value: -1 }]"
    no-results-text="검색 결과를 찾을 수 없습니다.">
    <template slot="headerCell"
      slot-scope="props">
      <v-tooltip bottom>
        <span slot="activator">
          {{props.header.tooltip || props.header.text || ''}}
        </span>
        <span>
          {{props.header.text || ''}}
        </span>
      </v-tooltip>
    </template>
    <template slot="items"
      slot-scope="props">
      <tr @click="$emit('recordClick', props.item)">
        <template v-for="(header, index) of headers">
          <td :class="{ 'text-xs-right': !!index, 'text-xs-left': !!index }"
            v-if="header.components">
            <v-layout row-sm
              justify-end>
              <component v-for="item of header.components"
                :key="props.item[header.value]"
                :is="item.component"
                :item="props.item"
                @evUpdate="n => $emit(item.event || 'evUpdate', props.item)"
                :self="item">
              </component>
            </v-layout>
          </td>
          <td :class="{ 'text-xs-right': !!index, 'text-xs-left': !!index }"
            v-else-if="header.render">{{header.render(props.item, props.item[header.value])}}</td>
          <td :class="{ 'text-xs-right': !!index, 'text-xs-left': !!index }"
            v-else>{{props.item[header.value]}}</td>
        </template>
      </tr>
    </template>
    <template slot="no-data">
      <v-alert :value="true"
        color="success"
        icon="info">
        Sorry, nothing to display here :(
      </v-alert>
    </template>
  </v-data-table>
</template>

<script>
export default {
  props: {
    headers: Array,
    items: Array,
    totalItems: {
      type: Number,
      default: 0
    },
    loading: {
      type: Boolean,
      default: true
    },
    pagination: {
      type: Object,
      default() {
        return {}
      }
    }
  },
  data() {
    return {}
  },
  watch: {},
  methods: {},
  components: {},
  created() {}
}
</script>
