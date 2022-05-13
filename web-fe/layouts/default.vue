<template>
  <v-app>
    <v-app-bar app>
      <v-app-bar-nav-icon
        @click.stop="showDrawer = !showDrawer"
      />
      <v-toolbar-title> Stima Pronto Soccorso </v-toolbar-title>
    </v-app-bar>
    <v-main>
      <router-view></router-view>
    </v-main>

    <v-navigation-drawer
      v-model="showDrawer"
      fixed
      app
      temporary
    >
      <v-list>
        <v-list-item
          v-for="(item, i) in linksDrawer"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <error-snackbar />
  </v-app>
</template>

<script>
import ErrorSnackbar from '@/components/visuals/ErrorSnackbar'

export default {
  components: {
    ErrorSnackbar
  },
  data() {
    return {
      showDrawer: false,
      linksDrawer: [
        {
          icon: 'mdi-home',
          title: 'Home',
          to: '/'
        },
        {
          icon: 'mdi-file-table-box-multiple',
          title: 'Display',
          to: '/display'
        },
        {
          icon: 'mdi-account',
          title: 'Patient data',
          to: '/patient'
        }
      ]
    }
  },
}
</script>

<style>
.row {
  margin-top: 0;
  margin-bottom: 0;
}
</style>
