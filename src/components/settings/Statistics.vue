<template>
  <v-expansion-panel>
    <v-expansion-panel-header
      ><div>
        <v-icon class="mr-2">mdi-chart-timeline-variant</v-icon> Estatísticas
      </div>
    </v-expansion-panel-header>
    <v-expansion-panel-content>
      <v-divider></v-divider>
      <Stop-reasons-list></Stop-reasons-list>
      <Log></Log>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import Log from "./statistics/Log.vue";
import StopReasonsList from "./statistics/StopReasonsList.vue";

export default {
  components: { StopReasonsList, Log },
  name: "Statistics",
  data: () => ({
    text: "Houve um problema de conexão com a maquina! Estamos tentando reconectar! ",
  }),

  methods: {},

  computed: {},
};
</script>

<style scoped lang="scss">
</style>