<template>
  <div>
    <v-divider></v-divider>
    <v-card-title> Editor de JSON </v-card-title>

    <v-card-subtitle>Configurações avançadas</v-card-subtitle>

    <JsonEditor
      :options="{
        confirmText: 'salvar',
        cancelText: 'cancelarfgfd',
      }"
      :objData="jsonData"
      v-model="jsonData"
    >
    </JsonEditor>

    <v-row justify="center">
      <v-dialog v-model="dialog" persistent max-width="400">
        <template v-slot:activator="{ on, attrs }">
          <v-spacer></v-spacer>
          {{jsonData}}
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
            >Essas alterações podem comprometer o funcionamento da maquina, tem
            certeza que deseja executa-las?</v-card-text
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
                    command: actions.MODIFY_JSON,
                    parameter: jsonData,
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
                    command: actions.RESTORE_JSON,
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
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import { actions } from "../../store/index";

export default {
  name: "JsonEditor2",
  data: () => ({
    actions,
    dialog: false,
    selected: "",
    jsonData: {},
  }),

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),
  },

  mounted() {
  this.$nextTick(function () {
    this.jsonData = this.allJsons
  })
},

 watch: {
    allJsons: function () {
    this.jsonData = this.allJsons
    console.log(this.allJsons);
    },
 },

  computed: {
     ...mapState(["allJsons"]),
  },


  //   mounted: function () {
  //       console.log(this.configuration.json);
  //   },
};
</script>

<style>
</style>