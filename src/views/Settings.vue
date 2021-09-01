<template>
  <section class="content d-flex justify-start align-start
">
      <v-expansion-panels multiple >
        <Assembly />
        <Controls />
        <Statistics />
        <Advanced-settings />
        <Infos />
        <router-link to="/dashboard">
        <v-btn
          class="ma-3 mt-10"
          outlined
          rounded
          color="warning"
          v-if="$route.name != 'dashboard'"
        >
          <v-icon class="ma-2" small dark>mdi-chart-line</v-icon>
          Dashboard
        </v-btn>
      </router-link>
      </v-expansion-panels>
       
  </section>
</template>


<script>
import Infos from "../components/settings/Infos";
import AdvancedSettings from "../components/settings/AdvancedSettings";
import Statistics from "../components/settings/Statistics.vue";
import Controls from "../components/settings/controls/Controls.vue";
import Assembly from "../components/settings/assembly/Assembly.vue";

export default {
  components: { AdvancedSettings, Infos, Statistics, Controls, Assembly },
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
#app{
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /* text-align: center; */
  color: #2c3e50;
  width: 100vw;
  height: 100%;
  /* padding: 1em 1em; */
}

.content{
  width: 100%;
  height: 100vh;
  }
  
.v-expansion-panels {
  padding: 1em;
  max-width: 800px;
  margin: 0 auto;
}

v-card {
  padding: 1em;
}
</style>
