<template>
  <div>
    <v-btn rounded x-large @click="dialog = true" color="warning" dark>
      <span><v-icon left>mdi-play</v-icon></span>
      Iniciar
    </v-btn>

    <v-row justify="center">
      <v-dialog v-model="dialog" max-width="400">
        <v-card>
          <v-card-title class="text-h5"
            >Quantas peças deseja produzir?</v-card-title
          >

          <v-card-text class="flex-column d-flex justify-center mt-6">
            <v-btn-toggle
              v-model="selection"
              color="warning"
              class="d-flex justify-center"
            >
              <v-btn
                value=""
                v-on:click="
                  () => {
                    SEND_MESSAGE({ command: actions.START_PROCESS });
                    //startStatusChage
                    dialog = false;
                    state.operation.total = 0
                  }
                "
              >
                <span>ilimitada</span>
              </v-btn>

              <v-btn :value="state.operation.total">
                <span>quantidade especifica</span>
              </v-btn>
            </v-btn-toggle>

            <!-- <v-btn class="mx-2 mb-4" large> ilimitada </v-btn>
            <v-btn class="mx-2" large> quantidade especifica </v-btn> -->

            <v-row class="mt-6 d-flex justify-center mb-4" v-if="selection">
              <div>
                <v-row class="d-flex align-baseline mb-6">
                  <v-btn
                    class="mx-2"
                    fab
                    small
                    @click="state.operation.total--"
                  >
                    <v-icon dark> mdi-minus </v-icon>
                  </v-btn>

                  <v-text-field
                    filled
                    dense
                    rounded
                    v-model="state.operation.total"
                    class="mt-0 pt-0 quantityToProduce"
                    hide-details
                    single-line
                    type="number"
                  ></v-text-field>

                  <v-btn
                    class="mx-2"
                    fab
                    small
                    @click="state.operation.total++"
                  >
                    <v-icon dark> mdi-plus </v-icon>
                  </v-btn>
                  <v-btn
                  class="ml-6"
                    color="warning"
                    rounded
                    v-on:click="
                      () => {
                        SEND_MESSAGE({
                          command: actions.START_PROCESS,
                          parameter: selection,
                        });
                        //startStatusChage
                        dialog = false;
                      }
                    "
                  >
                    iniciar
                  </v-btn>
                </v-row>
              </div>
            </v-row>

            <!-- <v-divider></v-divider> -->
          </v-card-text>

          <!-- <v-card-actions class="d-flex justify-center">
              <v-btn color=" darken-1" text @click="dialog = false">
                Cancelar
              </v-btn>
              
          </v-card-actions> -->
        </v-card>
      </v-dialog>
    </v-row>
  </div>
</template>

<script>
//import ProgressStatus from "../components/ProgressStatus";
import { mapGetters, mapMutations } from "vuex";
import { actions } from "../store/index";
// import VideoProgress from "../components/VideoProgress"; Remove VideoProgress

export default {
  // mixins: [mixins],
  name: "StartButton",

  data: () => ({
    selection: "",
    actions,
    dialog: false,
  }),

  components: {
    //ProgressStatus,
    //VideoProgress, // Remove VideoProgress -HB
  },

  computed: {
    ...mapGetters(["state"]),
  },

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),
  },
};
</script>

<style lang="scss">
.quantityToProduce {
  width: 100px;
}
</style>
