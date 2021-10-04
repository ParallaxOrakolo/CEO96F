<template>
  <section class="content d-flex align-center flex-column">
    <!-- <ProgressStatus /> -->
    <VideoProgress v-show="running" />
    <v-img
      v-if="!started"
      class="mt-15"
      :src="require(`@/assets/img/estribo-quadrado-perspective.jpg`)"
      max-width="300"
    ></v-img>

    
    <div
      v-show="started"
      v-text="numberParts"
      class="yellow--text text--darken-3 font-weight-light text-h2"
    ></div>
    <div class="buttons">
      <!-- <v-btn
        class="mt-15"
        v-if="!paused && !finished"
        rounded
        x-large
        v-on:click="SEND_MESSAGE({ command: actions.PAUSE_PROCESS })"
        color="warning"
        dark
        ><v-icon left> mdi-pause </v-icon> pausar</v-btn
      > -->
      <StartButton v-if="!running" />
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
        v-if="finished"
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
        v-if="started && running"
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
        <span
          v-for="(reason, index) in state.configuration.statistics.stopReasons"
          :key="index"
        >
          <v-btn
            class="white--text buttons"
            color="warning"
            rounded
            v-if="reason.listed"
            x-large
            @click="
              () => {
                SEND_MESSAGE({
                  command: actions.STOP_REASON_RESPONSE,
                  parameter: stopReasonsMessage(reason.code),
                });
                overlay = false;
                finished = true;
              }
            "
          >
            {{ reason.description }}
          </v-btn>
        </span>
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
    <ProgressInfo
      averageTime="10"
      :right="operation.right"
      :wrong="operation.wrong"
      :total="operation.total"
      timePerCicle="60"
    ></ProgressInfo>
  </section>
</template>

<script>
//import ProgressStatus from "../components/ProgressStatus";
import { mapMutations, mapState } from "vuex";
import { actions } from "../store/index";
import VideoProgress from "../components/VideoProgress";
import StartButton from "../components/StartButton";
import ProgressInfo from "@/components/ProgressInfo";

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
    ProgressInfo,
    VideoProgress,
    StartButton,
  },

  computed: {
    ...mapState({
      operation: (state) => state.operation,
      state: (state) => state,
      started: (state) => state.operation.started,
      running: (state) => state.operation.running,
      finished: (state) => state.operation.finished,
    }),

    numberParts: function () {
      if (this.operation.finished) {
        this.$router.push({ path: "/success" }).catch(() => {});
      }
      if (this.operation.total) {
        return this.operation.placed + " de " + this.operation.total;
      } else {
        if (this.operation.onlyCorrectParts) {
          return this.operation.placed + " de infinitas";
        } else {
          this.operation.right + this.operation.wrong + " de infinitas";
        }
      }
    },
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
  .img {
    // max-height: 200px;
    max-width: 450px;
  }
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
