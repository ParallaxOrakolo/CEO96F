<template>
  <v-app>
    <snack-bar v-if="!isConnected"></snack-bar>
    <DialogAlert />
    <NavBar />
    <v-main>
      <router-view />
      <!-- <Home/> -->
    </v-main>
  </v-app>
</template>

<script>
//import Home from "./views/Home";
import NavBar from "./components/NavBar";
import { mapState } from "vuex";
import SnackBar from "./components/SnackBar.vue";
import DialogAlert from "./components/DialogAlert.vue";

export default {
  name: "App",

  components: {
    //Home,
    NavBar,
    DialogAlert,
    SnackBar,
  },


  created() {
    if (this.$workbox) {
      this.$workbox.addEventListener("waiting", () => {
        this.showUpdateUI = true;
      });
    }
  },

  computed: {
    ...mapState(["isConnected"]),
  },

};
</script>

<style lang="scss">
::-webkit-scrollbar {
  display: none;
}

html,
body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}
</style>