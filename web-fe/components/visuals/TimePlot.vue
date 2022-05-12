<template>
  <v-sparkline
    :value="computedProps.value"
    :labels="computedProps.labels"
    gradient-direction="top"
    smooth="10"
    line-width="2"
    fill
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
  @Prop({ type: Array, required: true }) value!: []

  get totalLabels() {
    return this.labels.length
  }

  get labelToPlotCount() {
    return Math.ceil(this.totalLabels / 10)
  }

  /*
   * Since the esteems from the rest API come with "holes" in the horizontal axis,
   * e.g. {0: 0.5, 2: 0.5} we do a linear interpolation to fill these holes, so that
   * the Vuetify Plotting component can plot that correctly
   */
  get computedProps() {
    const new_wait_times: number[] = []
    const new_amount_times: number[] = []
    for (let j = 0; j < this.labels.length; j++) {
      const wait_time = this.labels[j]
      const amount = this.value[j]

      const wait_time_int = parseInt(wait_time)
      if (new_wait_times.length == 0) {
        new_wait_times.push(wait_time_int)
        new_amount_times.push(amount)
        continue
      }

      let diff
      if (
        (diff =
          wait_time_int - new_wait_times[new_wait_times.length - 1] - 1) != 0
      ) {
        const last_amount = new_amount_times[new_amount_times.length - 1]
        // m as in y = mx + q aka dy/dx
        const m = (last_amount - amount) / (diff + 1)

        for (let i = 1; i <= diff; i++) {
          new_wait_times.push(wait_time_int - i)
          new_amount_times.push(amount + m * i)
        }
      }

      new_wait_times.push(wait_time_int)
      new_amount_times.push(amount)
    }

    return {
      value: new_amount_times,
      labels: new_wait_times,
    }
  }
}
</script>
