<template>
  <v-app-bar style="-webkit-app-region: drag" app dense dark>
    <router-link to="/">
      <v-btn
        icon
        class="hidden-xs-only"
        v-on:click="$router.go(-1)"
        alt
        v-if="$route.name == 'settings'"
      >
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <!-- isso foi nojento -->
      <router-link to="/config">
        <v-btn
          icon
          class="hidden-xs-only"
          v-on:click="$router.go(-1)"
          alt
          v-if="$route.name == 'dashboard'"
        >
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
      </router-link>
      <img
        class="logo"
        src="../assets/img/parallax-logo-06.svg"
        alt
        v-if="$route.name != 'settings'"
        v-show="$route.name != 'dashboard'"
      />
    </router-link>
    <v-spacer>
      <h3 v-if="$route.name == 'settings'">Configurações</h3>
      <h3 v-if="$route.name == 'dashboard'">Dashboard</h3>
      <!-- <h3 v-if="online">Online </h3> -->
      <!-- <h3 v-if="!online">Offline </h3> -->
    </v-spacer>
    <!-- <v-icon v-show="showUpdateUI" dark color="light-green lighten-1" @click="accept()">mdi-reload</v-icon >   -->

    <v-spacer></v-spacer>
    <!-- <SnackBar /> -->

    <RestartButton
      v-if="$route.name == 'settings'"
      :online="isConnected"
    ></RestartButton>

    <v-icon dark color="light-green lighten-1" v-show="isConnected"
      >mdi-lan-check</v-icon
    >
    <v-icon dark color="red darken-1" v-show="!isConnected"
      >mdi-lan-disconnect</v-icon
    >

    <router-link to="/config">
      <v-btn icon v-if="$route.name != 'settings'">
        <v-icon dark id="tune">mdi-tune</v-icon>
      </v-btn>
    </router-link>
  </v-app-bar>
</template>

<script>
// import SnackBar from "../components/SnackBar";
// import { mapMutations } from "vuex"; Remove mapMutations -HB
import { mapState, mapMutations } from "vuex";
import { actions } from "../../src/store/index";
import RestartButton from "./navbar/RestarButton.vue";

export default {
  name: "NavBar",
  data: () => ({
    actions,
    restartDialog: false,
    online: false,
    showOnlineMsg: false,
    alert: true,
    url: "http://192.168.1.100:8080/exit",
  }),

  //checa se existe conexão tem a ver com o pwa
  mounted() {
    this.online = navigator.onLine;
    window.addEventListener("online", () => (this.online = true));
    window.addEventListener("offline", () => {
      this.online = false;
      this.showOnlineMsg = true;
    });
  },

  components: {
    RestartButton,
    // SnackBar,
  },
  methods: {
    ...mapMutations(["SEND_MESSAGE"]),
    close() {
      const remote = require("electron").remote;
      var window = remote.getCurrentWindow();
      window.close();
    },

    //pwa app
    async accept() {
      this.showUpdateUI = false;
      await this.$workbox.messageSW({ type: "SKIP_WAITING" });
    },
  },

  computed: {
    ...mapState(["isConnected", "configuration"]),
  },
};
</script>

<style scoped lang="scss">
.logo {
  height: 1.4em;
  margin-top: 0.5em;
}

.alert {
  // position: absolute;
  width: 100%;
  margin: 0 auto;
}
</style>