<template>
  <v-skeleton-loader :loading="isLoading" type="card">
    <patient-data
      :waiting_times="waiting_times"
      :arrival_time="arrival_time"
      :emergency_code="emergency_code"
    />
  </v-skeleton-loader>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'
import { manageError } from '~/functions/Errors'
import PatientData from '@/components/visuals/PatientData.vue'
import { WaitingTimesType } from '@/../restapi/src/models/esteem'

@Component({
  components: {
    PatientData,
  },
})
export default class IdForm extends Vue {
  @Prop({ type: String, required: true }) patientId!: string

  isLoading = true

  waiting_times: WaitingTimesType = new Map()
  emergency_code: Number = -1
  arrival_time: string = ''

  async updateValue() {
    this.isLoading = true
    try {
      const response = await this.$axios.get('/patient/' + this.patientId)

      this.waiting_times = response.data.waiting_times
      this.emergency_code = response.data.emergency_code
      this.arrival_time = response.data.arrival_time
    } catch (error) {
      manageError('Error while reading data about this patient', error)
    }

    this.isLoading = false
  }

  mounted() {
    this.updateValue()
  }
}
</script>
