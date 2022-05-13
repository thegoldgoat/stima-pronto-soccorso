<template>
  <v-snackbar
    v-model="showSnackbarMessage"
    :timeout="5000"
    :color="snackbarColor"
    bottom
    @click="removeSnackBarMessage"
  >
    {{ snackbarMessage }}

    <template v-slot:action="{ attrs }">
      <v-btn text v-bind="attrs" @click.prevent="removeSnackBarMessage">
        OK
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
import { EventBus } from '@/functions/EventBus'

export default {
  data() {
    return {
      snackbarMessage: '',
      snackbarColor: '',
      showSnackbarMessage: false
    }
  },
  mounted() {
    EventBus.$on('error', message => {
      // Show the error
      this.snackbarMessage = message
      this.snackbarColor = 'error'
      this.showSnackbarMessage = true
    })
    EventBus.$on('confirm', message => {
      // Show the confirm message
      this.snackbarMessage = message
      this.snackbarColor = 'green'
      this.showSnackbarMessage = true
    })
  },
  methods: {
    removeSnackBarMessage() {
      this.snackbarMessage = ''
      this.showSnackbarMessage = false
    }
  }
}
</script>

<style></style>
