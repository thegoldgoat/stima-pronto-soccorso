<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
      <v-card>
        <v-card-title> Display </v-card-title>
        <v-card-text>
          <v-skeleton-loader :loading="isLoading" height="300" type="card">
            <v-expansion-panels>
              <v-expansion-panel
                v-for="patientEsteem in esteemsForGraphs"
                :key="patientEsteem.patient_id"
              >
                <v-expansion-panel-header>
                  {{ patientEsteem.patient_id }}
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <time-plot
                    :value="Object.values(patientEsteem.waiting_times)"
                    :labels="Object.keys(patientEsteem.waiting_times)"
                  />
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-skeleton-loader>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'
import { manageError } from '@/functions/Errors'
import { PatientEsteem } from '@/../restapi/src/types/PatientEsteem'
import TimePlot from '@/components/visuals/TimePlot.vue'

type EsteemFromMonitor = PatientEsteem & { patient_id: string }

@Component({
  components: {
    TimePlot,
  },
})
export default class DisplayPage extends Vue {
  isLoading = true
  esteems: EsteemFromMonitor[] = []

  /*
   * Since the esteems from the rest API come with "holes" in the horizontal axis,
   * e.g. {0: 0.5, 2: 0.5} we do a linear interpolation to fill these holes, so that
   * the Vuetify Plotting component can plot that correctly
   */
  get esteemsForGraphs(): EsteemFromMonitor[] {
    return this.esteems.map((esteem): EsteemFromMonitor => {
      const new_wait_times: number[] = []
      const new_amount_times: number[] = []

      const wait_times = Object.keys(esteem.waiting_times)
      const amount_times = Object.values(esteem.waiting_times)
      for (let j = 0; j < wait_times.length; j++) {
        const wait_time = wait_times[j]
        const amount = amount_times[j]

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

      const new_waiting_times: Map<string, number> = new Map()
      for (let i = 0; i < new_wait_times.length; i++) {
        new_waiting_times.set(new_wait_times[i].toString(), new_amount_times[i])
      }

      return {
        waiting_times: Object.fromEntries(new_waiting_times),
        patient_id: esteem.patient_id,
        emergency_code: esteem.emergency_code,
        arrival_time: esteem.arrival_time,
      } as any
    })
  }

  async updateDisplay() {
    this.isLoading = true
    try {
      this.esteems = (await this.$axios('monitor/all')).data
    } catch (error) {
      manageError('Error while getting data for display', error)
    }
    this.isLoading = false
  }

  async mounted() {
    this.updateDisplay()
  }
}
</script>
