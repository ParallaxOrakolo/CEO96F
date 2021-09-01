<template >
  <div>
    <v-divider></v-divider>
    <v-card-title> Editor de JSON </v-card-title>

    <v-card-subtitle>Configurações avançadas</v-card-subtitle>

    <JsonEditor
      v-if="loading"
      :options="{
        confirmText: 'salvar',
        cancelText: 'cancelar',
      }"
      :objData="jsonData"
      v-model="jsonData"
    >
    </JsonEditor>

    <v-row justify="center">
      <v-dialog v-model="dialog" persistent max-width="400">
        <template v-slot:activator="{ on, attrs }">
          <v-spacer></v-spacer>
          <transition name="fade">
            <div class="actionButtons " v-show="!hidden">
             
              <v-btn
                dark
                v-bind="attrs"
                v-on="on"
                color="warning"
                class="ma-2 white--text"
                @click="selected = 'restore'"
                large
                rounded
                elevation="15"
              >
                restaurar
                <v-icon right dark> mdi-backup-restore </v-icon></v-btn
              >
               <v-btn
                dark
                v-bind="attrs"
                v-on="on"
                color="warning"
                class="ma-2 white--text"
                @click="selected = 'save'"
                large
                rounded
                elevation="15"
              >
                Salvar
                <v-icon right dark> mdi-content-save </v-icon></v-btn
              >
            </div>
          </transition>
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
    scTimer: 0,
    scY: 0,
    hidden: false,
    loading: false
  }),

  mounted() {
    this.$nextTick(function () {
      this.jsonData = this.allJsons;
    });

    window.addEventListener("scroll", this.handleScroll);
    this.loading = true
    this.$emit("update-loading") //loading event 
  },

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),

    handleScroll: function () {
      if (this.scTimer) return;
      this.scTimer = setTimeout(() => {
        this.scY = window.scrollY;
        clearTimeout(this.scTimer);
        this.scTimer = 0;
      }, 100);
    },
  },

  watch: {
    allJsons: function () {
      this.jsonData = this.allJsons;
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

<style scoped lang="scss">
.actionButtons {
  position: fixed;
  bottom: 1em;
  right: 1em;
}
</style>