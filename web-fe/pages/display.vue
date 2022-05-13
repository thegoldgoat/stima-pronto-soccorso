<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
      <v-card>
        <v-card-title> Display </v-card-title>
        <v-card-text>
          <v-skeleton-loader :loading="isLoading" height="300" type="card">
            <v-expansion-panels>
              <v-expansion-panel
                v-for="patientEsteem in esteems"
                :key="patientEsteem.patient_id"
              >
                <v-expansion-panel-header>
                  {{ patientEsteem.patient_id }}
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <patient-data
                    :waiting_times="patientEsteem.waiting_times"
                    :emergency_code="patientEsteem.emergency_code"
                    :arrival_time="patientEsteem.arrival_time"
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
import PatientData from '@/components/visuals/PatientData.vue'

type EsteemFromMonitor = PatientEsteem & { patient_id: string }

@Component({
  components: {
    PatientData,
  },
})
export default class DisplayPage extends Vue {
  isLoading = true
  esteems: EsteemFromMonitor[] = []

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
