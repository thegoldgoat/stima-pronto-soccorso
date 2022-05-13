<template>
  <div>
    <div class="subtitle-1">Emergency Code: {{ emergency_code }}</div>
    <div class="subtitle-2">Arrival: {{ arrival_time_formatted }}</div>
    <time-plot :value="amounts" :labels="labels" />
    <div>
      Average:
      <b> {{ statistics.average.toFixed(2) }} minutes </b>
    </div>
    <div>
      Mean Squared Error:
      <b> {{ statistics.meanSquaredError.toFixed(2) }} minutes </b>
    </div>
    <div>
      50% of probability to wait less than
      <b> {{ statistics.cumulateTo50 }} minutes </b>
    </div>
    <div>
      75% of probability to wait less than
      <b> {{ statistics.cumulateTo75 }} minutes </b>
    </div>
    <div>
      90% of probability to wait less than
      <b> {{ statistics.cumulateTo90 }} minutes </b>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import TimePlot from '@/components/visuals/TimePlot.vue'
import { WaitingTimesType } from '~/../restapi/src/models/esteem'

@Component({
  components: {
    TimePlot,
  },
})
export default class PatientData extends Vue {
  @Prop({ type: Object, required: true }) waiting_times!: WaitingTimesType
  @Prop({ type: Number, required: true }) emergency_code!: number
  @Prop({ type: String, required: true }) arrival_time!: string

  // 50, 75, 90

  get labels() {
    return Object.keys(this.waiting_times)
  }

  get amounts() {
    return Object.values(this.waiting_times)
  }

  get statistics() {
    let average = 0

    for (let i = 0; i < this.labels.length; i++) {
      const amount = this.amounts[i]
      const waited_time = parseInt(this.labels[i])

      average += amount * waited_time
    }

    let meanSquaredError = 0

    for (let i = 0; i < this.labels.length; i++) {
      const amount = this.amounts[i]
      const waited_time = parseInt(this.labels[i])

      meanSquaredError += Math.pow(waited_time - average, 2) * amount
    }

    meanSquaredError = Math.sqrt(meanSquaredError)

    let cumulateTo50 = -1
    let cumulateTo75 = -1
    let cumulateTo90 = -1

    let sum = 0

    for (let i = 0; i < this.labels.length; i++) {
      const amount = this.amounts[i]
      const waited_time = parseInt(this.labels[i])

      sum += amount

      if (sum >= 0.5 && cumulateTo50 === -1) {
        cumulateTo50 = waited_time
      }

      if (sum >= 0.75 && cumulateTo75 === -1) {
        cumulateTo75 = waited_time
      }

      if (sum >= 0.9 && cumulateTo90 === -1) {
        cumulateTo90 = waited_time
      }
    }

    return {
      average: average,
      meanSquaredError: meanSquaredError,
      cumulateTo50: cumulateTo50,
      cumulateTo75: cumulateTo75,
      cumulateTo90: cumulateTo90,
    }
  }

  get arrival_time_formatted() {
    console.debug(this.arrival_time)

    const dateValue = new Date(this.arrival_time)

    return dateValue.toLocaleString()
  }
}
</script>
