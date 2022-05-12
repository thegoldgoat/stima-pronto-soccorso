<template>
  <div>patient graph for {{ patientId }}</div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'

@Component
export default class IdForm extends Vue {
  @Prop({ type: String, required: true }) patientId!: string
}
</script>
