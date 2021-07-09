<template>
  <section class="content d-flex align-center flex-column">
    <!-- <ProgressStatus /> -->
    <VideoProgress v-show="state.started"/>
    <div v-show="state.started" v-text="numberParts" class="yellow--text text--darken-3 font-weight-light text-h2"></div>
    <div class="buttons">
      <v-btn
        v-if="!state.paused && !state.finished"
        rounded
        x-large
        v-on:click="SEND_MESSAGE({ command: actions.PAUSE_PROCESS })"
        color="warning"
        dark
        ><v-icon left> mdi-pause </v-icon> pausar</v-btn
      >
      <StartButton v-if="!state.playing"/>
      <!-- <v-btn
        rounded
        x-large
        v-on:click="
          () => {
            SEND_MESSAGE({
              command: actions.GENERATE_ERROR,
            });
            overlay = false;
          }
        "
        color="warning"
        dark
      >
        <v-icon>mdi-alert-box</v-icon></v-btn
      > -->
      <v-btn
        v-if="state.finished"
        rounded
        x-large
        v-on:click="SEND_MESSAGE({ command: actions.RESTART_PROCESS })"
        color="warning"
        dark
      >
        <v-icon left>mdi-reload</v-icon>reiniciar</v-btn
      >
      {{ state.configuration.statistics.des }}
      <v-btn
        v-if="state.started && state.playing"
        rounded
        x-large
        v-on:click="
          () => {
            SEND_MESSAGE({ command: actions.STOP_PROCESS });
            overlay = !overlay;
          }
        "
        color="error"
        dark
      >
        <v-icon left>mdi-stop</v-icon>Parar</v-btn
      >

      <!-- reasons -->
      <v-overlay :z-index="zIndex" :value="overlay" :opacity="opacity">
        <h1 color="white" class="mb-16">
          Por favor selecione o motivo da parada
        </h1>
        <v-btn
          v-for="(reason, index) in state.configuration.statistics.stopReasons"
          :key="index"
          :v-if="reason.listed"
          class="white--text buttons"
          color="warning"
          rounded
          x-large
          @click="
            () => {
              SEND_MESSAGE({
                command: actions.STOP_REASON_RESPONSE,
                parameter: stopReasonsMessage(reason.code),
              });
              overlay = false;
            }
          "
        >
          {{ reason.description }}
        </v-btn>
      </v-overlay>

      <!-- end reasons -->
      <!-- registrar valor no back -->
      <router-link to="/home">
        <!-- <v-btn
          v-if="!state.started || state.finished"
          rounded
          outlined
          x-large
          color="warning"
          >trocar conector ou bandeja</v-btn
        > -->
      </router-link>
    </div>
  </section>
</template>

<script>
//import ProgressStatus from "../components/ProgressStatus";
import { mapGetters, mapMutations } from "vuex";
import { actions } from "../store/index";
import VideoProgress from "../components/VideoProgress"
import StartButton from "../components/StartButton"

export default {
  // mixins: [mixins],
  name: "Progress",

  data: () => ({
    actions,
    buttomClicked: false,
    overlay: false,
    zIndex: 9,
    opacity: 1,
    }),

  components: {
    //ProgressStatus,
    VideoProgress,
    StartButton
  },

  computed: {
    ...mapGetters(["state"]),
    numberParts(){
      
      if(this.state.operation.total){
        return this.state.operation.placed + "/" + this.state.operation.total
      }else{
        return this.state.operation.placed + "/Ilimitado"
      }
      
    }
  },

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),

    stopReasonsMessage(code) {
      var message = {
        code: code,
        date: Math.floor(Date.now() / 1000),
      };
      return message;
    },
  },
};
</script>

<style lang="scss" >
section {

  .buttons {
    display: flex;
    flex-flow: column;
    justify-content: center;
    height: 100%;
    margin: 0 auto;

    button {
      margin-bottom: 2em;
    }

  }
}
</style>
