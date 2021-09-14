<template class="mx-auto">
  <v-container fluid>
    <v-row dense>
      <v-col cols="card.flex">
        <Total-card
          title="Peças produzidas"
          :number="allParts.total.total"
          :correct="allParts.total.rigth"
          :wrong="allParts.total.wrong"
          description="Desde o começo"
          icon="mdi-chart-timeline-variant"
          :iconTypeAlternative="true"
          iconColor="blue lighten-2"
        ></Total-card>
      </v-col>
      <v-col cols="card.flex">
        <Total-card
          title="Tempo médio por peças"
          :number="Number(allParts.yesterday.timePerCicle.toFixed(1))"
          :correct="Number(allParts.total.timePerCicleMax.toFixed(1))"
          :wrong="Number(allParts.total.timePerCicleMin.toFixed(1))"
          description="Ultimo dia util"
          icon="mdi-timer-outline"
          unit="s"
          iconColor="blue lighten-2"
        ></Total-card>
      </v-col>
    </v-row>
     <v-row>  <v-col cols="card.flex"> <ProductionAverageChartCard></ProductionAverageChartCard> </v-col>  </v-row>
    <v-row><v-col cols="card.flex"> <TimeLineChartCard></TimeLineChartCard></v-col></v-row>
  </v-container>
</template>

<script>
//import ProgressStatus from "../components/ProgressStatus";
import { mapState, mapMutations } from "vuex";
import { actions } from "../store/index";
import TotalCard from "../components/dashboard/TotalCard.vue";
import ProductionAverageChartCard from "../components/dashboard/ProductionAverageChartCard.vue";
import TimeLineChartCard from "../components/dashboard/TimeLineChartCard.vue";

export default {
  // mixins: [mixins],
  name: "Dashboard",

  data: () => ({
    actions,
    buttomClicked: false,
    overlay: false,
    zIndex: 9,
    opacity: 1,
  }),

  components: {
    TotalCard,
    ProductionAverageChartCard,
    TimeLineChartCard,
  },

  computed: {
    ...mapState({
      allParts: state => state.production.allParts.production
      }),
  },

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),
  },
};
</script>

<style lang="scss" >
</style>
