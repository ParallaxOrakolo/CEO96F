
<template>
  <v-expansion-panel>
    <v-expansion-panel-header>Estatísticas </v-expansion-panel-header>
    <v-expansion-panel-content>
      <Stop-reasons-list></Stop-reasons-list>
      <Log></Log>
      <Stop-reasons-chart></Stop-reasons-chart>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import Log from "./statistics/Log.vue";
import StopReasonsList from "./statistics/StopReasonsList.vue";
import StopReasonsChart from "./statistics/StopReasonsChart.vue";

export default {
  components: { StopReasonsList, Log, StopReasonsChart },
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