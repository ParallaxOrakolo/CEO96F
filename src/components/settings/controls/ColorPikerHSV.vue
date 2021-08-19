<template>
  <v-expansion-panel>
    <v-expansion-panel-header>Filtros camera </v-expansion-panel-header>
    <v-expansion-panel-content>
      <div class="d-flex flex-column justify-center mb-6">
        <div class="total d-flex flex-column justify-center mb-6">
          <div class="wrap d-flex justify-center mb-6">
            <div
              class="right"
              :class="!selectedColor1 ? 'colorName' : 'colorNameSelected'"
            >
              <div class="d-flex align-center mb-6">
                Cor 1<br />
                {{
                  configuration.camera.filters[selectedFilter].gradient.color
                }}
              </div>
            </div>
            <div
              class="gradient"
              :style="`background: linear-gradient(to right, ${configuration.camera.filters[selectedFilter].gradient.color}, ${configuration.camera.filters[selectedFilter].gradient.color2})
`"
            >
              <div class="d-flex justify-space-between mb-6 circles">
                <v-btn
                  class="ma-2 selected"
                  fab
                  :color="
                    configuration.camera.filters[selectedFilter].gradient.color
                  "
                  @click="selectedColor1 = true"
                >
                </v-btn>
                <v-btn
                  class="ma-2 selected"
                  fab
                  :color="
                    configuration.camera.filters[selectedFilter].gradient.color2
                  "
                  @click="selectedColor1 = false"
                >
                </v-btn>
              </div>
            </div>
            <div :class="selectedColor1 ? 'colorName' : 'colorNameSelected'">
              <div class="d-flex align-center mb-6">
                Cor 2<br />
                {{
                  color2
                }}
              </div>
            </div>
          </div>

          <div class="colorPicker">
            <color-picker
              v-model="
                configuration.camera.filters[selectedFilter].gradient.color
              "
              v-if="selectedColor1"
            ></color-picker>
            <color-picker
              v-model="
                configuration.camera.filters[selectedFilter].gradient.color2
              "
              v-else
            ></color-picker>
          </div>
        </div>
      </div>
      <v-range-slider
        v-model="configuration.camera.filters[selectedFilter].area"
        :max="area_max"
        :min="area_min"
        hide-details
        class="slider"
        label="Area"
        @change="
          () => {
            SEND_MESSAGE({
              command: actions.UPDATE_CAMERA,
              parameter: configuration.camera,
              },
            );
          }
        "
      >
      </v-range-slider>
      <v-row justify="center" class="mb-6">
        <v-dialog v-model="dialog" persistent max-width="400">
          <template v-slot:activator="{ on, attrs }">
            <v-spacer></v-spacer>
            <v-btn
              dark
              v-bind="attrs"
              v-on="on"
              color="warning"
              class="ma-2 white--text"
              @click="selected = 'save'"
            >
              Salvar
              <v-icon right dark> mdi-content-save </v-icon></v-btn
            >
            <v-btn
              dark
              v-bind="attrs"
              v-on="on"
              color="warning"
              class="ma-2 white--text"
              @click="selected = 'restore'"
            >
              restaurar
              <v-icon right dark> mdi-backup-restore </v-icon></v-btn
            >
          </template>
          <v-card>
            <v-toolbar color="error" class="text-h5" dark>Cuidado</v-toolbar>

            <v-card-text class="mt-8"
              >Essas alterações podem comprometer o funcionamento da maquina,
              tem certeza que deseja executa-las?</v-card-text
            >
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="warning darken-1" text @click="dialog = false">
                cancelar
              </v-btn>
              <v-btn
                v-if="selected == 'save'"
                color="warning darken-1"
                text
                @click="
                  () => {
                    SEND_MESSAGE({
                      command: actions.SAVE_CAMERA,
                      parameter: configuration.camera,
                    });
                    dialog = false;
                  }
                "
              >
                salvar
              </v-btn>
              <v-btn
                v-if="selected == 'restore'"
                color="warning darken-1"
                text
                @click="
                  () => {
                    SEND_MESSAGE({
                      command: actions.RESTORE_CAMERA,
                    });
                    dialog = false;
                  }
                "
              >
                Restaurar
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-row>
      <v-divider></v-divider>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import ColorPicker from "vue-color-picker-wheel";
//import { mapState, mapMutations, mapActions } from "vuex"; mapActions sem uso.
import { mapState, mapMutations} from "vuex";
import { actions } from "@/store/index";

export default {
  name: "ColorPikerHSV",
  components: {
    ColorPicker,
  },
  data: () => ({
    actions,
    selected: "",
    selectedColor1: true,
    dialog: false,
    area_max:1000,
    area_min:0
  }),

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),
    // ...mapActions(["sendMessage"]),
  },

  computed: {
    ...mapState(["configuration", "selectedFilter"]),

    color1: function () {
      let colorA = this.configuration.camera.filters.hole.gradient.color;
      console.log("camera");

      this.$store.dispatch('sendMessage', {
        command: this.actions.UPDATE_CAMERA,
        parameter: this.configuration.camera,
      });

      // this.sendMessage({
      //   command: this.actions.UPDATE_CAMERA,
      //   parameter: this.configuration.camera,
      // })

      console.log("end camera");
      return colorA
    },

    color2: function () {
      let colorB = this.configuration.camera.filters.hole.gradient.color2;
      console.log("camera2");

      this.$store.dispatch('sendMessage', {
        command: this.actions.UPDATE_CAMERA,
        parameter: this.configuration.camera,
      });

      // this.sendMessage({
      //   command: this.actions.UPDATE_CAMERA,
      //   parameter: this.configuration.camera,
      // })

      console.log("end camera2");
      return colorB
    },
  },
};
</script>
<style lang="scss" scoped>
.total {
  margin: 0 auto;
}

.gradient {
  width: 284px;
  height: 56px;
  border-radius: 56px;
}
.selected {
  border: solid 5px black;
}
.circles {
  position: absolute;
  width: 300px;
  margin-top: -8px;
  margin-left: -7px;
}
.wrap {
  width: 490px;
}

.colorName {
  height: 56px;
  padding: 0 13px;
  // font-weight: 600;
}
.colorNameSelected {
  height: 56px;
  padding: 0 13px;
  font-weight: 600;
}
.right {
  text-align: end;
}

.colorPicker {
  margin: 0 auto;
}
.slider {
  width: 300px;
  margin: 37px auto 0;
}
</style>