<template>
  <v-text-field
    ref="patientId"
    @click:append="emitValue"
    @keydown.enter="emitValue"
    label="Patient ID"
    placeholder="Patient ID"
    append-icon="mdi-send"
  />
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator'

@Component
export default class IdForm extends Vue {
  emitValue() {
    const patientId = (this.$refs.patientId as any).lazyValue

    if (!patientId) return

    this.$emit('newid', patientId)
  }
}
</script>
