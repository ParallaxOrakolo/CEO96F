<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <div><v-icon class="mr-2">mdi-camera-control</v-icon> Controles</div>
    </v-expansion-panel-header>
    <v-expansion-panel-content>
      <!-- <v-divider></v-divider>
<SerialMonitor></SerialMonitor> -->
      <v-row no-gutters>
        <Camera></Camera>
        <ColorPikerHSV
          v-show="isUserAcessPermited('ColorPikerHSV')"
        ></ColorPikerHSV>
      </v-row>
      <ButtonsControls></ButtonsControls>

      <v-divider></v-divider>
      <SerialMonitor
        v-show="isUserAcessPermited('SerialMonitor')"
      ></SerialMonitor>

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
import ColorPikerHSV from "../controls/ColorPikerHSV.vue";
import ButtonsControls from "../controls/ButtonsControls.vue";
import Mixins from "@/mixins/mixins";

export default {
  components: { SerialMonitor, Camera, ColorPikerHSV, ButtonsControls },
  mixins: [Mixins],
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