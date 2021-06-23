<template>
  <v-expansion-panel>
    <v-expansion-panel-header>Camera </v-expansion-panel-header>
    <v-expansion-panel-content>
      <!-- <v-divider></v-divider>
<SerialMonitor></SerialMonitor> -->
      <v-row no-gutters>
        <!-- <v-col cols="1"> </v-col> -->
        <v-col class="pa-2" cols="7">
          <template>
            <div class="d-flex flex-column justify-space-between align-center">
              <v-img
                :width="cam_width"
                :src="`http://192.168.1.57:5050/${radios}`"
              ></v-img>
              <v-slider
                v-model="cam_width"
                class="align-self-stretch"
                min="200"
                max="720"
                step="1"
              ></v-slider>
              <p>{{ process || "Algo" }}</p>
              <v-radio-group v-model="radios" mandatory row>
                <v-radio
                  label="N-0"
                  value="Normal/0"
                  @click="process = 'Normal';
                  SEND_MESSAGE({ command: actions.UPDATE_SLIDER, parameter:process});"
                ></v-radio>
                <v-radio
                  label="N-1"
                  value="Normal/1"
                  @click="process = 'Normal';
                  SEND_MESSAGE({ command: actions.UPDATE_SLIDER, parameter:process});"
                ></v-radio>
                <v-divider class="mx-4" vertical></v-divider>
                <v-radio
                  label="S-1"
                  value="Screw/1"
                  @click="process = 'Screw';
                  SEND_MESSAGE({ command: actions.UPDATE_SLIDER, parameter:process});"
                ></v-radio>
                <v-radio
                  label="Edge-1"
                  value="Edge/1"
                  @click="process = 'Edge';
                  SEND_MESSAGE({ command: actions.UPDATE_SLIDER, parameter:process});"
                ></v-radio>
                <v-divider class="mx-4" vertical></v-divider>
                <v-radio
                  label="H-0"
                  value="Hole/0"
                  @click="process = 'Hole';
                  SEND_MESSAGE({ command: actions.UPDATE_SLIDER, parameter:process});"
                ></v-radio>
              </v-radio-group>
            </div>
          </template>
        </v-col>

        <v-col class="pa-2 col-md-3">
          <template>
            <v-btn
              class="ma-1"
              color="success"
              plain
              @click="
                () => {
                  SEND_MESSAGE({ command: actions.SAVE_JSON });
                }
              "
            >
              Salvar
            </v-btn>

            <v-btn
              class="ma-1"
              color="grey darken-1"
              plain
              @click="radios = 'exit'"
            >
              Parar Transmissão
            </v-btn>

            <v-btn
              class="ma-1"
              color="grey darken-1"
              plain
              @click="
                () => {
                  getFilter();
                }
              "
            >
              Iniciar Transmissão
            </v-btn>
            <v-card flat color="transparent">
              <v-subheader>HUE</v-subheader>
              <v-card-text>
                <v-row>
                  <v-col class="px-4">
                    <v-range-slider
                      v-model="configuration.camera.hue"
                      :max="slid_max"
                      :min="slid_min"
                      hide-details
                      class="align-center"
                      @change="
                        () => {
                          SEND_MESSAGE({
                            command: actions.UPDATE_FILTER,
                            parameter: {
                              process: process,
                              h_min: configuration.camera.hue[0],
                              h_max: configuration.camera.hue[1],
                            },
                          });
                        }
                      "
                    >
                      <template v-slot:prepend>
                        <v-text-field
                          :value="configuration.camera.hue[0]"
                          class="mt-0 pt-0"
                          hide-details
                          single-line
                          type="number"
                          style="width: 60px"
                          @change="$set(configuration.camera.hue, 0, $event)"
                        ></v-text-field>
                      </template>
                      <template v-slot:append>
                        <v-text-field
                          :value="configuration.camera.hue[1]"
                          class="mt-0 pt-0"
                          hide-details
                          single-line
                          type="number"
                          style="width: 60px"
                          @change="$set(configuration.camera.hue, 1, $event)"
                        ></v-text-field>
                      </template>
                    </v-range-slider>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
            <v-divider></v-divider>
            <v-card flat color="transparent">
              <v-subheader>Saturation</v-subheader>
              <v-card-text>
                <v-row>
                  <v-col class="px-4">
                    <v-range-slider
                      v-model="configuration.camera.sat"
                      :max="slid_max"
                      :min="slid_min"
                      hide-details
                      class="align-center"
                      @change="
                        () => {
                          SEND_MESSAGE({
                            command: actions.UPDATE_FILTER,
                            parameter: {
                              process: process,
                              s_min: configuration.camera.sat[0],
                              s_max: configuration.camera.sat[1],
                            },
                          });
                        }
                      "
                    >
                      <template v-slot:prepend>
                        <v-text-field
                          :value="configuration.camera.sat[0]"
                          class="mt-0 pt-0"
                          hide-details
                          single-line
                          type="number"
                          style="width: 60px"
                          @change="$set(configuration.camera.sat, 0, $event)"
                        ></v-text-field>
                      </template>
                      <template v-slot:append>
                        <v-text-field
                          :value="configuration.camera.sat[1]"
                          class="mt-0 pt-0"
                          hide-details
                          single-line
                          type="number"
                          style="width: 60px"
                          @change="$set(configuration.camera.sat, 1, $event)"
                        ></v-text-field>
                      </template>
                    </v-range-slider>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
            <v-divider></v-divider>
            <v-card flat color="transparent">
              <v-subheader>Valor</v-subheader>
              <v-card-text>
                <v-row>
                  <v-col class="px-4">
                    <v-range-slider
                      v-model="configuration.camera.val"
                      :max="slid_max"
                      :min="slid_min"
                      hide-details
                      class="align-center"
                      @change="
                        () => {
                          SEND_MESSAGE({
                            command: actions.UPDATE_FILTER,
                            parameter: {
                              process: process,
                              v_min: configuration.camera.val[0],
                              v_max: configuration.camera.val[1],
                            },
                          });
                        }
                      "
                    >
                      <template v-slot:prepend>
                        <v-text-field
                          :value="configuration.camera.val[0]"
                          class="mt-0 pt-0"
                          hide-details
                          single-line
                          type="number"
                          style="width: 60px"
                          @change="$set(configuration.camera.val, 0, $event)"
                        ></v-text-field>
                      </template>
                      <template v-slot:append>
                        <v-text-field
                          :value="configuration.camera.val[1]"
                          class="mt-0 pt-0"
                          hide-details
                          single-line
                          type="number"
                          style="width: 60px"
                          @change="$set(configuration.camera.val, 1, $event)"
                        ></v-text-field>
                      </template>
                    </v-range-slider>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>

            <v-card flat color="transparent">
              <v-subheader>Area</v-subheader>
              <v-card-text>
                <v-row>
                  <v-col class="px-4">
                    <v-range-slider
                      v-model="configuration.camera.are"
                      :max="are_slid_max"
                      :min="are_slid_min"
                      hide-details
                      class="align-center"
                      @change="
                        () => {
                          SEND_MESSAGE({
                            command: actions.UPDATE_FILTER,
                            parameter: {
                              process: process,
                              areaMin: configuration.camera.are[0],
                              areaMax: configuration.camera.are[1],
                            },
                          });
                        }
                      "
                    >
                      <template v-slot:prepend>
                        <v-text-field
                          :value="configuration.camera.are[0]"
                          class="mt-0 pt-0"
                          hide-details
                          single-line
                          type="number"
                          style="width: 60px"
                          @change="$set(configuration.camera.are, 0, $event)"
                        ></v-text-field>
                      </template>
                      <template v-slot:append>
                        <v-text-field
                          :value="configuration.camera.are[1]"
                          class="mt-0 pt-0"
                          hide-details
                          single-line
                          type="number"
                          style="width: 60px"
                          @change="$set(configuration.camera.are, 1, $event)"
                        ></v-text-field>
                      </template>
                    </v-range-slider>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
            <v-divider></v-divider>

          </template>
        </v-col>
      </v-row>
      <v-divider></v-divider>
      <!-- seção 2 -->
      <SerialMonitor></SerialMonitor>
      <!-- 
    <v-btn elevation="2" fab dark x-large color="blue">
      <v-icon dark> mdi-arrow-up-bold </v-icon>
    </v-btn>

    <v-btn elevation="2" fab dark x-large color="blue">
      <v-icon dark> mdi-arrow-down-bold </v-icon>
    </v-btn> -->
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import { actions } from "../../store/index.js";
import SerialMonitor from "../SerialMonitor.vue";
import json from "../../../engine_H/Json/config.json";
export default {
  components: { SerialMonitor },
  name: "CameraConfig",
  data() {
    return {
      actions,
      led: false,
      s_camera: true,
      ledRGB: null,
      speed: 100,
      vacuumPosition: 0,
      vacuum: false,
      claw: false,
      distance: 1,
      rotationZ: 0,
      distancesLabels: ["0.1", "1", "10", "100"],
      distanceList: [0.1, 1, 10, 100],

      lastBValue: 0,
      lastZAValue: 0,
      json_Data: json,
      radios: "Normal/0",
      process: "Normal",

      slid_min: 0,
      slid_max: 255,

      are_slid_min: 0,
      are_slid_max: 100000,
      cam_width: 720,

      // loadingb1: false,
      // loadingb2: false
    };
  },

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),

    getMaxFeedrate(axis) {
      var machine = this.configuration.informations.machine.maxFeedrate;
      var maxFeedrate;

      console.log(machine);
      switch (axis) {
        case "x":
          maxFeedrate = machine.xyMax;
          break;
        case "y":
          maxFeedrate = machine.xyMax;
          break;
        case "z":
          maxFeedrate = machine.zMax;
          break;
        case "a":
          maxFeedrate = machine.aMax;
          break;
        case "b":
          maxFeedrate = machine.bMax;
          break;
        default:
          break;
      }

      return " F" + maxFeedrate;
    },

    //faz uma regra de tres pra passar o valor verdadeiro de
    getRealValueToMove(value, axis) {
      var machine = this.configuration.informations.machine.limits;
      var axisLimit;

      switch (axis) {
        case "x":
          axisLimit = machine.xMax;
          break;
        case "y":
          axisLimit = machine.yMax;
          break;
        case "z":
          axisLimit = machine.zMax;
          break;
        case "a":
          axisLimit = machine.aMax;
          break;
        case "b":
          axisLimit = machine.bMax;
          break;
        default:
          break;
      }

      return ((value * 100) / axisLimit).toFixed(2);
    },

    moveAxis(axis, negative = false) {
      var msg = "G91 \n G0 ";

      if (axis == "y") {
        msg = msg.concat("Y");
      }
      if (axis == "x") {
        msg = msg.concat("X");
        console.log("entrou");
      }
      if (axis == "z") {
        msg = msg.concat("Z");
      }
      if (negative) {
        msg = msg.concat("-");
      }
      msg = msg.concat(this.distanceList[this.distance]);
      msg = msg.concat(" F" + this.speed);

      return msg;
    },

    getFilter() {
      var camera = this.configuration.camera;
      console.log(camera);
    },
  },

  computed: {
    ...mapState(["configuration"]),
  },
};
</script>

<style scoped lang="scss">
div {
  // border: 1px solid;;
}
.v-btn--round {
  border-radius: 26%;
}
</style>