<template>
  <v-expansion-panel>
    <v-expansion-panel-header>Controles </v-expansion-panel-header>
    <v-expansion-panel-content>
      <!-- <v-divider></v-divider>
<SerialMonitor></SerialMonitor> -->

      <v-row no-gutters>
        <!-- <v-col cols="1"> </v-col> -->
        <Camera></Camera>
        <ColorPikerHSV/>
        <v-col class="pa-2" cols="7">
          <v-row no-gutters class="mb-6">
            <v-col class="pa-2 d-flex justify-end">
              <v-btn
                v-haptic
                elevation="2"
                fab
                dark
                x-large
                color="blue"
                @click="
                  () => {
                    SEND_MESSAGE({
                      command: actions.SERIAL_MONITOR,
                      parameter: 'G28 X Y',
                    });
                  }
                "
              >
                <v-icon dark>mdi-home</v-icon>
              </v-btn>
            </v-col>

            <v-col class="pa-2 d-flex justify-center col-md-2">
              <!-- buttom X+ -->
              <v-btn
                v-haptic
                elevation="2"
                fab
                dark
                x-large
                color="blue"
                @click="
                  () => {
                    SEND_MESSAGE({
                      command: actions.SERIAL_MONITOR,
                      parameter: moveAxis('x', false),
                    });
                  }
                "
              >
                <v-icon dark> mdi-arrow-up-bold </v-icon>+X
              </v-btn>
            </v-col>

            <v-col class="pa-2">
              <!-- Z buttom -->
              <v-btn
                v-haptic
                elevation="2"
                fab
                dark
                x-large
                color="blue"
                @click="
                  () => {
                    SEND_MESSAGE({
                      command: actions.SERIAL_MONITOR,
                      parameter: moveAxis('z'),
                    });
                  }
                "
              >
                <v-icon dark> mdi-arrow-up-bold </v-icon>+z
              </v-btn>
            </v-col>
          </v-row>

          <v-row no-gutters class="mb-6">
            <v-col class="pa-2 d-flex justify-end">
              <!-- -Y buttom -->
              <v-btn
                v-haptic
                elevation="2"
                fab
                dark
                x-large
                color="blue"
                @click="
                  () => {
                    SEND_MESSAGE({
                      command: actions.SERIAL_MONITOR,
                      parameter: moveAxis('y', true),
                    });
                  }
                "
              >
                <v-icon dark> mdi-arrow-left-bold </v-icon>-Y
              </v-btn>
            </v-col>

            <v-col class="pa-2 col-md-2 d-flex justify-center"> </v-col>

            <v-col class="pa-2">
              <!-- +Y buttom -->
              <v-btn
                v-haptic
                elevation="2"
                fab
                dark
                x-large
                color="blue"
                @click="
                  () => {
                    SEND_MESSAGE({
                      command: actions.SERIAL_MONITOR,
                      parameter: moveAxis('y'),
                    });
                  }
                "
              >
                <v-icon dark> mdi-arrow-right-bold </v-icon>+Y
              </v-btn>
            </v-col>
          </v-row>

          <v-row no-gutters class="mb-6">
            <v-col class="pa-2 d-flex justify-end">
              <v-btn v-haptic elevation="2" fab dark x-large color="blue"
              @click="
                  () => {
                    SEND_MESSAGE({
                      command: actions.PARAFUSA,
                      parameter: {pos:160, mm:2, voltas:20}
                    });
                  }
                ">
                <v-icon dark> mdi-screw-lag</v-icon>
              </v-btn>
            </v-col>

            <v-col class="pa-2 d-flex justify-center col-md-2">
              <!-- -X Buttom -->
              <v-btn
                v-haptic
                elevation="2"
                fab
                dark
                x-large
                color="blue"
                @click="
                  () => {
                    SEND_MESSAGE({
                      command: actions.SERIAL_MONITOR,
                      parameter: moveAxis('x', true),
                    });
                  }
                "
              >
                <v-icon dark> mdi-arrow-down-bold </v-icon>-x
              </v-btn>
            </v-col>

            <v-col class="pa-2">
              <!-- -Z Buttom -->
              <v-btn
                v-haptic
                elevation="2"
                fab
                dark
                x-large
                color="blue"
                @click="
                  () => {
                    SEND_MESSAGE({
                      command: actions.SERIAL_MONITOR,
                      parameter: moveAxis('z', true),
                    });
                  }
                "
              >
                <v-icon dark> mdi-arrow-down-bold </v-icon>-z
              </v-btn>
            </v-col>
          </v-row>
        </v-col>

        <v-col class="pa-2 col-md-3">
          
          <!-- <v-switch
            v-haptic
            v-model="vacuum"
            inset
            color="success"
            label="Vácuo"
            @click="
              () => {
                SEND_MESSAGE({
                  command: actions.SERIAL_MONITOR,
                  parameter: this.vacuum ? 'M106 P0 S128 ' : 'M107 P0',
                });
              }
            "
          ></v-switch>
          <v-subheader class="pl-0">
            Pinça a vácuo
            <v-text-field
              filled
              dense
              rounded
              v-model="vacuumPosition"
              class="mt-0 ml-4 pt-0 numberInput"
              hide-details
              single-line
              type="number"
            ></v-text-field>
          </v-subheader>
          <v-slider
            @click="
              () => {
                SEND_MESSAGE({
                  command: actions.SERIAL_MONITOR,
                  parameter:
                    'G90 E1 \n G0 E' +
                    getRealValueToMove(this.vacuumPosition, 'a') +
                    getMaxFeedrate('a'),
                });
              }
            "
            v-model="vacuumPosition"
            class="align-center"
            max="100"
            min="0"
            hide-details
          >
          </v-slider>
          <v-divider></v-divider> -->

          <v-switch
            v-haptic
            v-model="claw"
            inset
            color="success"
            label="Garra"
            @click="
              () => {
                SEND_MESSAGE({
                  command: actions.SERIAL_MONITOR,
                  parameter: this.claw ? 'M42 P31 S255' : 'M42 P31 S0',
                });
              }
            "
          ></v-switch>
          <v-subheader class="pl-0"
            >Rotação Garra (Graus)
            <v-text-field
              filled
              dense
              rounded
              v-model="rotationZ"
              class="mt-0 pt-0 numberInput"
              hide-details
              single-line
              type="number"
            ></v-text-field>
          </v-subheader>
          <v-slider
            @click="
              () => {
                SEND_MESSAGE({
                  command: actions.SERIAL_MONITOR,
                  parameter:
                    'T1 \n G90 E0 \n G0 E' + this.rotationZ
                    // getRealValueToMove(this.rotationZ, 'b') +
                    // getMaxFeedrate('b'),
                });
              }
            "
            v-model="rotationZ"
            class="align-center"
            max="360"
            min="0"
            hide-details
          >
          </v-slider>
           <v-divider></v-divider>
          <v-switch
          v-haptic
          v-model="light1"
          inset
          class="mr-4"
          color="success"
          label="Luz Camera de Validação"
          @click="
            () => {
              SEND_MESSAGE({
                command: actions.SERIAL_MONITOR,
                parameter: this.light1 ? 'M42 P33 S255' : 'M42 P33 S0',
              });
            }
          "
        ></v-switch>
        <v-switch
          v-haptic
          v-model="light2"
          inset
          color="success"
          label="Luz camera furação"
          @click="
            () => {
              SEND_MESSAGE({
                command: actions.SERIAL_MONITOR,
                parameter: this.light2 ? 'M42 P34 S255' : 'M42 P34 S0',
              });
            }
          "
        ></v-switch>
        </v-col>
      </v-row>
      <v-divider></v-divider>
      <!-- seção 2 -->
      <v-row no-gutters>
        <v-col class="pa-2 col-md-3 col">
          <v-subheader> Passo(mm) </v-subheader>
          <v-slider
            v-model="distance"
            :tick-labels="distancesLabels"
            :max="3"
            step="1"
            ticks="always"
            tick-size="4"
          ></v-slider>

          <!-- <v-switch
            v-model="led"
            inset
            color="success"
            label="Led Camera"
            @click="
              () => {
                SEND_MESSAGE({
                  command: actions.SERIAL_MONITOR,
                  parameter: this.led
                    ? 'M150 R' +
                      this.ledRGB.rgba.r +
                      ' I' +
                      this.ledRGB.rgba.g +
                      ' B' +
                      this.ledRGB.rgba.b
                    : 'M150 R0 I0 B0',
                });
              }
            "
          ></v-switch> -->
          <!-- <v-color-picker
            v-model="ledRGB"
            v-on:mouseup="
              () => {
                SEND_MESSAGE({
                  command: actions.SERIAL_MONITOR,
                  parameter: this.led
                    ? 'M150 R' +
                      this.ledRGB.rgba.r +
                      ' I' +
                      this.ledRGB.rgba.g +
                      ' B' +
                      this.ledRGB.rgba.b
                    : 'M150 R0 I0 B0',
                });
              }
            "
            hide-canvas
            dot-size="32"
            hide-mode-switch
            hide-sliders
            mode="rgba"
            swatches-max-height="200"
          ></v-color-picker> -->
        </v-col>

        <v-col class="pa-2 col-md-3 col">
          <v-subheader class="pl-0">
            Velocidade
            <v-text-field
              filled
              dense
              rounded
              v-model="speed"
              class="mt-0 pt-0 numberInput"
              hide-details
              single-line
              type="number"
            ></v-text-field
          ></v-subheader>

          <v-slider
            v-model="speed"
            class="align-center"
            :max="this.configuration.informations.machine.maxFeedrate.xyMax"
            min="0"
            hide-details
          >
          </v-slider>
        </v-col>
      </v-row>
      <v-divider></v-divider>
      <SerialMonitor></SerialMonitor>
      <!-- 
    <v-btn v-haptic elevation="2" fab dark x-large color="blue">
      <v-icon dark> mdi-arrow-up-bold </v-icon>
    </v-btn>

    <v-btn v-haptic elevation="2" fab dark x-large color="blue">
      <v-icon dark> mdi-arrow-down-bold </v-icon>
    </v-btn> -->
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import { actions } from "../../../store/index";
import SerialMonitor from "../../SerialMonitor.vue";
import Camera from "../controls/Cameras.vue";
import ColorPikerHSV from "../controls/ColorPikerHSV.vue"

export default {
  components: { SerialMonitor, Camera, ColorPikerHSV },
  name: "Controls",
  data() {
    return {
      actions,
      light1: false,
      light2: false,
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
      msg = msg.concat(" F" + this.speed * 10);

      return msg;
    },
  },

  computed: {
    ...mapState(["configuration"]),
  },
};
</script>

<style scoped lang="scss">
.v-btn--round {
  border-radius: 26%;
}

.numberInput {
  max-width: 80px;
  margin-left: 15px;
}
</style>