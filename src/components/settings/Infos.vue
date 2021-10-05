<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <div>
        <v-icon class="mr-2">mdi-information-outline</v-icon> Informações
      </div>
    </v-expansion-panel-header>
    <v-expansion-panel-content>
      <v-divider></v-divider>

      <v-list three-line subheader>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>Endereço de acesso</v-list-item-title>
            <v-list-item-subtitle
              ><a :href="ip">{{ ip }}</a>
              <!-- <v-btn class="ma-2"
        text
        icon
        x-small
              ><v-icon>mdi-content-copy</v-icon></v-btn
            > -->
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <v-list-item>
          <v-list-item-content>
            <v-list-item-title>Versões</v-list-item-title>
            <v-list-item-subtitle
              ><b>Frontend </b>
              <!-- {{ configuration.informations.version.frontend }}  -->
              {{ getFrontVersion() }}
              |
              <b>Backend</b> {{ configuration.informations.version.backend }} |
              <b>Marlin</b> {{ configuration.informations.version.marlin }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import { mapState } from "vuex";

export default {
  components: {},
  name: "Infos",
  data: () => ({
    show1: false,
    ip: document.location.host,
  }),

  methods: {
    getFrontVersion() {
      var pjson = require("../../../package.json");
      console.log("font version: ", pjson.version);
      return pjson.version;
    },

    IsVisible() {
      this.snackbar = true;
    },
  },

  computed: {
    ...mapState(["configuration", "selectedFilter"]),
  },
};
</script>

<style scoped lang="scss">
.v-list-item__title {
  font-weight: 600;
}
</style>