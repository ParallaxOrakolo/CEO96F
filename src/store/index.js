import { constants } from "fs";
import Vue from "vue";
import Vuex from "vuex";
import machineJson from "../../engine_H/Json/machineParamters.json";
Vue.use(Vuex);

var wsConnection = constants;

//lista de coisas q eu posso pedir pro back
export const actions = {
  STOP_REASON_RESPONSE: "stopReasonsResponse",
  START_CAMERA_STREAM: "startCameraStream",
  START_AUTOCHECK: "startAutoCheck",
  RESTART_PROCESS: "restartProcess",
  SERIAL_MONITOR: "serialMonitor",
  UPDATE_FILTER: "updateFilter",
  START_PROCESS: "startProcess",
  PAUSE_PROCESS: "pauseProcess",
  PARAFUSA: "sendParafusa",
  UPDATE_SLIDER: "updateSlider",
  STOP_PROCESS: "stopProcess",
  LOG_REQUEST: "logRequest",
  STOP_REASONS_LIST_REQUEST: "stopReasonsListRequest",
  UPDATE_USER: "updateUser",
  UPDATE_CAMERA: "updateCamera",
  SEND_GCODE: "sendGcode",
  START_SCAN: "startScan",
  SAVE_CAMERA: "saveCamera",
  SHOW_POPUP: "showPopup",
  GENERATE_ERROR: "generateError",
  SHUTDOWN_RASPBERRY: "shutdown_raspberry",
  RESTORE_JSON: "restoreJson",
  RESTORE_CAMERA: "restoreCamera",
  MODIFY_JSON: "modifyJson",
  REQUEST_JSON: "requestJson",
  POPUP_TRIGGER: "popupTigger"
};

const store = new Vuex.Store({
  //estado do dado

  state: {
    operation: {
      name: "",
      type: "",
      panel: "",
      timeSeconds: 0,
      total: 10,
      placed: 5,
    },

    localTimer: {
      currentSeconds: null,
      minutes: null,
      seconds: null,
    },

    allJsons: {
      "AVI": {
        "code": 113,
        "description": "Auto verificiação iniciou",
        "listed": false,
        "type": "info"
      },
    },

    progress: 5.1,
    started: false,
    playing: false,
    paused: true,
    finished: false,
    stoped: true,

    idVar: null,

    connectionStatus: null,
    connectionStatusList: {
      connecting: "Tentando se conectar ao servidor...",
      connected: "Conectando com sucesso!",
      closed: "A conexão foi encerrada!",
      error: "Não conseguimos conectar ao servidor!, certifique-se que ele está ligado",
    },

    ws_message: {
      command: "",
      parameter: "",
    },

    dialogAlert: {
      show: false,
      code: 0,
      description: "",
      type: "error",
      button_text: "None",
      button_action: "None"
    },

    isConnecting: false,
    isConnected: true,
    autoCheckComplete: false,
    scanConnectorsComplete: false,

    log: [
      {
        code: Number,
        description: String,
        type: String,
        date: Number,
      }
    ],

    serialMonitor: [
      // {hour: 1611539081 ,sent: true, message:["ok","eaee","M117"]},
    ],

    selectedFilter: "hole",

    configuration: {
      logged : false,
      allJsons: {
        // name: 'mike',
        // age: 23,
        // phone: '419988756100',
        // address: ['AAA C1', 'BBB C2']
      },

      cameraList: [
        {
          name: "Camera Furação",
          cameraId: 0,
          filter: "Hole",
        },
        {
          name: "Camera de Validação",
          cameraId: 1,
          filter: "Screw",
        },
      ],

      informations: {
        ip: machineJson.configuration.informations.ip,
        connectionId: 123456,
        port: machineJson.configuration.informations.port,
        portStream: machineJson.configuration.informations.portStream,
        userList: [null],
        version: {
          backend: "0",
          frontend: "0", //fazer sistema para pegar automaticamente
          marlin: "0",
        },
        machine: {
          limits: {
            xMin: null,
            yMin: null,
            zMin: null,
            aMin: null,
            bMin: null,
            xMax: null,
            yMax: null,
            zMax: null,
            aMax: null,
            bMax: null,
          },
          maxFeedrate: {
            xMax: null,
            yMax: null,
            zMax: null,
            aMax: null,
            bMax: null,
          },
          defaultPosition: {
            pegaTombador: {
              X: 2,
              Y: 49,
              Z: null,
              E: 0
            },

            analisaFoto: {
              X: 80,
              Y: 9,
              Z: null,
              E: null
            },

            descarteErrado: {
              X: 230,
              Y: 0,
              Z: null,
              E: null
            },

            descarteCerto: {
              X: 0,
              Y: 0,
              Z: null,
              E: 0
            },

            camera0Centro: {
              X: 74.5,
              Y: 7.5,
              Z: null,
              E: null
            },

            camera1Centro: {
              X: 230,
              Y: 0,
              Z: null,
              E: null
            },

            parafusadeiraCentro: {
              X: 240,
              Y: 16,
              Z: null,
              E: null
            },
          },
        },
      },
      statistics: {
        stopReasons: [],
        stopReasonsList: [
          { "000": "Maquin ok" },
        ],
      },
      camera: {
        process: null,
        filters: {
          hole: {
            name: "hole",
            area: [10, 20],
            gradient: {
              color: "#a02727",
              color2: "#e261ae",
            },
            hue: [2, 50],
            sat: [0, 250],
            val: [30, 50],
          }

        },
      },
    },
  },

  //função em cima desses dados
  mutations: {
    START_CONNECTION: (state) => {
      console.log("Starting connection to WebSocket Server");
      state.isConnecting = true;
      state.connectionStatus = state.connectionStatusList.connecting;
      wsConnection = new WebSocket(
        "ws://" +
        state.configuration.informations.ip +
        ":" +
        state.configuration.informations.port// +
        //"?id=" +
        //state.configuration.informations.connectionId 

      );

      wsConnection.onmessage = function (event) {
        console.log("Recebido:");
        console.log(event.data);
        // state.message = JSON.parse(event.data);
        // state.message = JSON.parse(event.data);
        store.commit("RUN_COMMAND", JSON.parse(event.data));

        // state = Object.assign(state, JSON.parse(event.data)); //unifica os objetos
      };

      wsConnection.onopen = function () {
        console.log("Successfully connected to websocket server...");
        state.connectionStatus = state.connectionStatusList.connected;
        state.isConnected = true;
        // wsConnection.send(actions.START_AUTOCHECK);
        store.commit("SEND_MESSAGE", { command: actions.START_AUTOCHECK });
        state.isConnecting = false;
      };

      wsConnection.onclose = function () {
        console.log("Closed websocket server connection...");
        state.connectionStatus = state.connectionStatusList.closed;
        state.isConnected = false;
        state.isConnecting = false;
      };

      wsConnection.onerror = function () {
        console.log("Não foi possivel se conecar com o servidor");
        state.connectionStatus = state.connectionStatusList.error;
        state.isConnected = "";
        state.isConnecting = false;
      };

      // state.connection.send("connected")
    },

    RUN_COMMAND: (state, message) => {
      switch (message.command) {
        case actions.START_AUTOCHECK + "_success":
          console.log("autocheck");
          state.autoCheckComplete = true;
          break;

        case actions.START_SCAN + "_success":
          state.scanConnectorsComplete = true;
          console.log("scan conector");
          // code block
          break;

        case actions.START_PROCESS + "_success":
          store.commit("START2");
          console.log("START process");
          // code block
          break;

        case actions.PAUSE_PROCESS + "_success":
          store.commit("START2");
          console.log("PAUSE process");
          // code block
          break;

        case actions.RESTART_PROCESS + "_success":
          store.commit("RESTART");
          console.log("RESTART process");
          // code block
          break;

        case actions.STOP_PROCESS + "_success":
          store.commit("STOP")
          console.log("STOP Process")
          // code block
          break;

        case "update":
          state = Object.assign(state, message.parameter);
          console.log("update")
          console.log(state.configuration)
          // code block
          break;

        case "error":
          console.log("Back-end constata falha: ")
          console.log(message.parameter)
          state.dialogAlert.show = true
          state.dialogAlert.description = message.parameter.description
          state.dialogAlert.type = message.parameter.type
          state.dialogAlert.code = message.parameter.code
          state.dialogAlert.button_action = message.parameter.button_action
          state.dialogAlert.button_text = message.parameter.button_text

          // code block
          break;

        case actions.SERIAL_MONITOR + "_response":
          //confere se a ultimo intem da lista é uma msg recebida, se sim.. 
          var lastArrayItem = state.serialMonitor[state.serialMonitor.length - 1]

          if (lastArrayItem.sent == false) {
            lastArrayItem.message.push(message.parameter)
          } else {
            state.serialMonitor.push({ hour: Math.floor(Date.now() / 1000), sent: false, message: [message.parameter] })
          }

          // state = Object.assign(state, message.parameter);
          console.log("Update Serial Monitor Received");
          // code block
          break;

        default:
          console.log("default");
        // code block
      }
    },

    SCAN_COMPLETE_CHANGE: (state) => (state.scanConnectorsComplete = false),

    SEND_MESSAGE: (state, payload) => {
      state.ws_message.command = payload.command;
      state.ws_message.parameter = payload.parameter;
      wsConnection.send(JSON.stringify(state.ws_message));
      console.log("Enviado: " + JSON.stringify(state.ws_message));
    },

    START: (state) => {
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

    START2: (state) => {
      state.playing = true
      state.started = true
      state.stoped = false
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
      state.playing = false
      state.paused = true;
      state.finished = false;
      // state.started = false;
      state.stoped = true
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

    sendMessage(context, payload) {
      context.commit("SEND_MESSAGE", payload)
    }
    // sendMessage: ({ commit }, { command, parameter }) => commit("SEND_MESSAGE", { command, parameter }),
  },
});

export { store };
