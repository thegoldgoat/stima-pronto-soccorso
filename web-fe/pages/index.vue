<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
      <v-card>
        <v-card-title class="headline">
          Welcome to Stima Pronto Soccorso
        </v-card-title>
        <v-card-text>
          <p>
            Stima Pronto Soccorso goal is to predict the waiting times in an emergency room
          </p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="primary" nuxt to="/display"> Display </v-btn>
          <v-btn color="primary" nuxt to="/patient"> Patient </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'IndexPage',
}
</script>
