<template>
  <v-sparkline
    v-bind="$attrs"
    gradient-direction="top"
    smooth="10"
    line-width="2"
    :gradient="['#f72047', '#ffd200', '#1feaea']"
  >
    <template v-slot:label="item">
      {{ item.index % labelToPlotCount == 0 ? labels[item.index] : '' }}
    </template>
  </v-sparkline>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'

@Component
export default class TimePlot extends Vue {
  @Prop({ type: Array, required: true }) labels!: []

  get totalLabels() {
    return this.labels.length
  }

  get labelToPlotCount() {
    return Math.ceil(this.totalLabels / 10)
  }
}
</script>
