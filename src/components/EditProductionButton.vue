<template>
  <div>
    <v-btn
      @click="dialog = true"
      class="ml-2"
      text
      icon
      x-small
      color="grey lighten-1"
    >
      <v-icon>mdi-pencil</v-icon>
    </v-btn>

    <v-row justify="center">
      <v-dialog v-model="dialog" max-width="450">
        <v-card>
          <v-card-title class="text-h5 pt-6 pb-8"
            >Edicionar peças
            <span class="green--text text--lighten-1">&nbsp;corretas</span
            >!<v-spacer></v-spacer>
            <v-btn
               text
        icon
              small
              @click="dialog = false"
            >
              <v-icon dark> mdi-close </v-icon>
            </v-btn></v-card-title
          >
          <v-card-subtitle
            >Aqui você consegue editar a quantidade de peças corretas. Coloque a
            quantidade de peças corrigidas manualmente.</v-card-subtitle
          >
          <v-card-text class="flex-column d-flex justify-center mt-6">
            <!-- <v-btn class="mx-2 mb-4" large> ilimitada </v-btn>
            <v-btn class="mx-2" large> quantidade especifica </v-btn> -->

            <v-row class="mt-1 ml-n7 d-flex justify-center mb-4">
              <div>
                <v-row class="d-flex align-baseline mb-6">
                  <v-btn
                    class="mx-2"
                    fab
                    small
                    @click="less()"
                    :disabled="buttomDisable"
                  >
                    <v-icon dark> mdi-minus </v-icon>
                  </v-btn>

                  <v-text-field
                    filled
                    dense
                    rounded
                    v-model="numberOfParts"
                    class="mt-0 pt-0 quantityToProduce"
                    hide-details
                    single-line
                    type="number"
                    min="1"
                  ></v-text-field>

                  <v-btn
                    class="mx-2"
                    fab
                    small
                    @click="numberOfParts++, (buttomDisable = false)"
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
                          command: actions.EDIT_PRODUCTION,
                          parameter: { numberOfParts },
                        });
                        //startStatusChage
                        dialog = false;
                      }
                    "
                  >
                    Salvar
                  </v-btn>
                </v-row>

                <v-row class="ml-n16 d-flex justify-center" v-if="selection">
                  <v-checkbox
                    v-model="state.operation.onlyCorrectParts"
                    label="Considerar apenas peças corretas"
                    color="orange"
                    hide-details
                  ></v-checkbox>
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
  name: "EditProductionButton",

  props: {},

  data: () => ({
    selectedPart: 1,
    // onlyCorrectParts: true,
    selection: false,
    actions,
    dialog: false,
    buttomDisable: false,
    numberOfParts: 0,
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

    less() {
      if (this.numberOfParts >= 1) {
        this.numberOfParts--;
      } else {
        this.buttomDisable = true;
      }
    },
  },
};
</script>

<style lang="scss">
.quantityToProduce {
  width: 100px;
}

.partItem {
  height: 320px;
  width: 250px;
}
.v-card--link:focus:before {
  opacity: 0;
}
</style>
