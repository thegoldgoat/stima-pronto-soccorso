<template>
  <div>
    <div class="subtitle-1">Emergency Code: {{ emergency_code }}</div>
    <div class="subtitle-2">Arrival: {{ arrival_time_formatted }}</div>
    <time-plot
      :value="Object.values(waiting_times)"
      :labels="Object.keys(waiting_times)"
    />
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

  get arrival_time_formatted() {
    console.debug(this.arrival_time)

    const dateValue = new Date(this.arrival_time)

    return dateValue.toLocaleString()
  }
}
</script>
