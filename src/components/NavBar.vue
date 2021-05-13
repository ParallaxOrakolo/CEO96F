<template>
  <section>
    <v-app-bar style="-webkit-app-region: drag" app dense dark>
      <router-link to="/">
      <img class="logo" src="../assets/img/parallax-logo-06.svg" alt />
      </router-link>  
      <v-spacer></v-spacer>
     <SnackBar />
      <router-link to="/config">
        <v-btn icon>
          <v-icon dark id="tune">tune</v-icon>
        </v-btn>
      </router-link>
    </v-app-bar>
  </section>
</template>

<script>

import SnackBar from "../components/SnackBar";

import { mapState } from "vuex";


export default {
  name: "NavBar",
  data: () => ({
         
  }),
  
  components: {
    SnackBar,
  },
  methods: {
    close() {
      const remote = require("electron").remote;
      var window = remote.getCurrentWindow();
      window.close();
    },
  },

   computed: {
    ...mapState(["isConnected"]),
  },

};
</script>

<style scoped lang="scss">
.logo {
  height: 1.4em;
}

</style>