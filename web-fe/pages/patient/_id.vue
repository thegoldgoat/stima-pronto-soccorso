<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
      <v-card>
        <v-card-title> Patient </v-card-title>
        <v-card-text>
          <patient-graph v-if="hasPatientId" :patientId="patientId" />
          <id-form v-else @newid="updateId($event)" />
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'

import IdForm from '@/components/PatientPage/IdForm.vue'
import PatientGraph from '@/components/PatientPage/PatientGraph.vue'

@Component({
  components: {
    IdForm,
    PatientGraph,
  },
})
export default class PatientPage extends Vue {
  get patientId(): string {
    return this.$route.params.id
  }

  get hasPatientId(): boolean {
    return this.patientId != undefined
  }

  updateId(newPatientId: string) {
    this.$router.replace('/patient/' + newPatientId)
  }
}
</script>
