<template>
  <section class="content d-flex align-center flex-column">
    <div class="align-self-center d-flex align-center flex-column">
      <!-- <img class="logo" src="../assets/img/parallax-logo-06.svg" alt /> -->
      <!-- <br /> -->
      <!-- <v-btn x-large v-on:click="sendInfo('helo')" class="align-self-center" color="warning">iniciar</v-btn> -->
    </div>
    <div id="app">
      <v-expansion-panels multiple>
        <Infos />
        <!-- <CameraConfig/> -->
        <Controls />
        <Advanced-settings />
        <Statistics />
      </v-expansion-panels>
    </div>
  </section>
</template>


<script>
import Infos from "../components/settings/Infos";
import AdvancedSettings from "../components/settings/AdvancedSettings";
import Statistics from "../components/settings/Statistics.vue";
import Controls from "../components/settings/controls/Controls.vue";
import CameraConfig from "../components/settings/CameraConfig.vue"

export default {
  components: { AdvancedSettings, Infos, Statistics, Controls, CameraConfig },
  name: "settings",
  methods: {
    sendMessage: function (message) {
      // console.log(message)
      console.log(this.connection);
      this.connection.send(message);
    },
  },
  created: function () {
    // console.log("Starting connection to WebSocket Server");
    // this.connection = new WebSocket("ws://localhost:8765");
    // this.connection.onmessage = function (event) {
    //   console.log("mensagem: " + event.data);
    // };
    // this.connection.onopen = function () {
    //   console.log("conecxão aberta");
    //   console.log("Successfully connected to the echo websocket server...");
    // };
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
  width: 100vw;
  /* padding: 1em 1em; */
}

.v-expansion-panels {
  padding: 1em;
  
}

v-card {
  padding: 1em;
}
</style>
