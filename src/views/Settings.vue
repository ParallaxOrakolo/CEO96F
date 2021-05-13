<template>
  <section class="content d-flex align-center flex-column">
    <div class="align-self-center d-flex align-center flex-column">
      <img class="logo" src="../assets/img/parallax-logo-06.svg" alt />
      <br />
      <!-- <v-btn x-large v-on:click="sendInfo('helo')" class="align-self-center" color="warning">iniciar</v-btn> -->
    </div>
  <div id="app">
    <h2>Vue.js WebSocket Tutorial</h2> 
    <v-btn v-on:click="sendMessage(operation.type)">Send Message: {{operation.type}}</v-btn>
  </div>
  </section>
</template>

<script>
export default {
  name: 'App',
  data: function() {
    return {
      connection: null,

      operation: {
      name: "sc",
      type: "simplex",
      panel: "Oficce",
      timeSeconds: 10,
      total: 40,
      placed: 0,
    },
      
    }
  },
  methods: {
    sendMessage: function(message) {
      // console.log(message)
      console.log(this.connection);
      this.connection.send(message);
    }
  },
  created: function() {
    console.log("Starting connection to WebSocket Server")
    this.connection = new WebSocket("ws://localhost:8765")

    this.connection.onmessage = function(event) {
      console.log("mensagem: "+ event.data);
    }

    this.connection.onopen = function() {
      console.log("conecxão aberta")
      console.log("Successfully connected to the echo websocket server...")
    }

  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
