<template>
  <section class="content d-flex align-center flex-column">
    <ProgressStatus />
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
      <v-btn
        v-if="state.paused && !state.finished"
        rounded
        x-large
        v-on:click="
          () => {
            SEND_MESSAGE({ command: actions.START_PROCESS });
            //startStatusChage
            buttomClicked = true;
          }
        "
        color="warning"
        dark
      >
        <span
          v-show="
            () => {
              return !buttomClicked;
              buttomClicked = !buttomClicked;
            }
          "
          ><v-icon left>mdi-play</v-icon></span
        >
        <!-- <v-progress-circular
          v-show="buttomClicked"
          indeterminate
          color="white"
        ></v-progress-circular> -->
        Iniciar
      </v-btn>

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

      <v-btn
        v-if="state.started && !state.finished"
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
        <v-btn
          v-for="(reason, index) in state.stopReasons"
          :key="index"
          class="white--text buttons"
          color="warning"
          rounded
          x-large
          @click="
            () => {
              SEND_MESSAGE({
                command: actions.STOP_REASON_RESPONSE,
                parameter: stopReasonsMessage(reason)});
              overlay = false;
            }
          "
        >
          {{ reason }}
        </v-btn>
      </v-overlay>

      <!-- end reasons -->
      <!-- registrar valor no back -->
      <router-link to="/home">
        <v-btn
          v-if="!state.started || state.finished"
          rounded
          outlined
          x-large
          color="warning"
          >trocar conector ou bandeja</v-btn
        >
      </router-link>
    </div>
  </section>
</template>

<script>
import ProgressStatus from "../components/ProgressStatus";
import { mapGetters, mapMutations } from "vuex";
import { actions } from "../store/index";

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
    ProgressStatus,
  },

  computed: {
    ...mapGetters(["state"]),
  },

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),

    stopReasonsMessage(reason) {
      var message = {
        reason: reason,
        date: Math.floor(Date.now() / 1000),
      };
      return message;
    },
  }
};

</script>

<style lang="scss">
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
