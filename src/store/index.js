import { constants } from "fs";
import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

var wsConnection = constants;

export const actions = {
  START_AUTOCHECK: "startAutoCheck",
  SCAN_CONNECTORS: "scanConnectors",
  START_PROCESS: "startProcess",
  PAUSE_PROCESS: "pauseProcess",
  STOP_PROCESS: "stopProcess",
  RESTART_PROCESS: "restartProcess",

  STOP_REASON_RESPONSE: "stopReasonsResponse",
};

const store = new Vuex.Store({
  //estado do dado

  state: {
    operation: {
      name: "",
      type: "",
      panel: "",
      timeSeconds: 0,
      total: 0,
      placed: 0,
    },

    localTimer: {
      currentSeconds: null, 
      minutes: null,
      seconds: null,
    },

    progress: 5.1,
    started: false,
    paused: true,
    finished: false,

    idVar: null,

    connectionStatus: null,

    ws_message: {
      command: "",
      parameter: "",
    },

    stopReasons: [],

    statistics: {
      version: {
        back: "",
        front: "0.1.0", //fazer sistema para pegar automaticamente
      },
    },

    isConnected: true,
    autoCheckComplete: false,
    scanConnectorsComplete: false,
  },

  //função em cima desses dados
  mutations: {
    START_CONNECTION: (state) => {
      console.log("Starting connection to WebSocket Server");

      // wsConnection = new WebSocket("ws://192.168.100.99:443");
      wsConnection = new WebSocket("ws://192.168.1.38:5021");
      // ws://localhost:8765

      wsConnection.onmessage = function(event) {
        console.log(event.data);
        // state.message = JSON.parse(event.data);
        // state.message = JSON.parse(event.data);
        store.commit("RUN_COMMAND", JSON.parse(event.data));

        // state = Object.assign(state, JSON.parse(event.data)); //unifica os objetos
      };

      wsConnection.onopen = function() {
        console.log("Successfully connected to websocket server...");
        state.connectionStatus = "Conectando com sucesso!";
        state.isConnected = true
        // wsConnection.send(actions.START_AUTOCHECK);
        store.commit("SEND_MESSAGE", {command: actions.START_AUTOCHECK})
        
      };

      wsConnection.onclose = function() {
        console.log("Closed websocket server connection...");
        state.connectionStatus = "A conexão foi interrompida";
        state.isConnected = false
      };

      wsConnection.onerror = function() {
        console.log("Erro in connection");
        state.isConnected = "";
      };

      // state.connection.send("connected")
    },

    RUN_COMMAND: (state, message) => {
      switch (message.command) {
        case actions.START_AUTOCHECK + "_success":
          console.log("autocheck");
          state.autoCheckComplete = true;
          break;

        case actions.SCAN_CONNECTORS + "_success":
          state.scanConnectorsComplete = true;
          console.log("scan conector");
          // code block
          break;

        case actions.START_PROCESS + "_success":
          store.commit("START");
          console.log("START process");
          // code block
          break;

        case actions.PAUSE_PROCESS + "_success":
          store.commit("START");
          console.log("PAUSE process");
          // code block
          break;

        case actions.RESTART_PROCESS + "_success":
          store.commit("RESTART");
          console.log("RESTART process");
          // code block
          break;

        case actions.STOP_PROCESS + "_success":
          store.commit("STOP");
          console.log("STOP Process");
          // code block
          break;

        case "update":
          state = Object.assign(state, message.parameter);
          console.log("update");
          // code block
          break;

        default:
          console.log("default");
        // code block
      }
    },

    SCAN_COMPLETE_CHANGE: (state) => (state.scanConnectorsComplete = false),

    SEND_MESSAGE2(state, payload) {
      state.message = payload;
      wsConnection.send(payload);
      // console.log("Enviado:" + payload)
    },

    SEND_MESSAGE: (state, payload) => {
      // console.log("Enviado: " + payload);
      state.ws_message.command = payload.command;
      state.ws_message.parameter = payload.parameter ;
      wsConnection.send(JSON.stringify(state.ws_message));
      console.log("Enviado: " + JSON.stringify(state.ws_message));
    },

    START: (state) => {
      state.started = true;
      state.paused = !state.paused;

      if (state.localTimer.currentSeconds == null) {
        state.localTimer.currentSeconds = state.operation.timeSeconds;

        state.localTimer.minutes = Math.floor(state.operation.timeSeconds / 60);
        state.localTimer.seconds = state.operation.timeSeconds % 60;
      }

      console.log(state.localTimer.currentSeconds);

      if (state.paused == false && state.localTimer.currentSeconds > 0) {
        state.idVar = setInterval(() => {
          console.log("current time: " + state.localTimer.currentSeconds);

          //diminui em 1 seg
          if (state.localTimer.currentSeconds > 0) {
            state.localTimer.currentSeconds--;
          }

          //caucula a porcentagem
          if (state.localTimer.currentSeconds == null) {
            state.localTimer.currentSeconds = state.operation.timeSeconds;
          }

          state.progress = Math.floor(
            (state.localTimer.currentSeconds * 100) /
              state.operation.timeSeconds
          );

          //se o tempo for zero, interronpe o loop
          if (state.localTimer.currentSeconds == 0) {
            state.finished = true;
            clearInterval(state.idVar);
          }
        }, 1000);
      } else {
        state.paused = true;
        clearInterval(state.idVar);
      }
    },

    RESTART(state) {
      state.localTimer.currentSeconds = null;
      state.progress = 5.1;
      state.paused = true;
      state.finished = false;
      state.started = false;
    },

    STOP(state) {
      state.localTimer.currentSeconds = 0;
      state.progress = 5.1;
      state.paused = true;
      state.finished = false;
      state.started = false;
    },
  },

  //trata os dados
  getters: {
    operation: (state) => state.operation,
    minutes: (state) =>
      (state.localTimer.minutes = Math.floor(
        state.localTimer.currentSeconds / 60
      )),
    seconds: (state) =>
      (state.localTimer.seconds = state.localTimer.currentSeconds % 60),
    progress: (state) => 100 - state.progress,
    state: (state) => state,
  },

  //conecta com o banco e o commit chama o mutation
  actions: {
    startConnection: (context) => context.commit("START_CONNECTION"),
    // sendMessage: (context) => context.commit('sendMessage', payload),
    startStatusChage: (context) => context.commit("START"),
    restart: (context) => context.commit("RESTART"),
    stop: (context) => context.commit("STOP"),

    // sendMessage: ({ commit }, { command, parameter }) => commit("SEND_MESSAGE", { command, parameter }),
   
  },
})

export { store };
