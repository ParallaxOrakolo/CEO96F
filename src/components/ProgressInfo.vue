<template>
  <div class="container">
    <!-- <div  class="mx-auto"> -->
    <!-- <v-card class="mx-auto" v-if="series[0].data"> -->
    <div class="">
      <!-- <v-row>
          <div class="text--secondary ml-3 mb-6">
            Tempo produção de <b>hoje</b> por peça
          </div>
          <v-spacer></v-spacer>
        </v-row> -->
      <v-row>
        <v-fade-transition>
          <div class="pr-5 pl-3 d-flex justify-space-around statistics">
            <div
              class="d-flex justify-center"
              v-for="item in infoList"
              :key="item.text"
            >
              <div class="d-flex justify-center flex-column">
                <div>
                  <span class="text-h5 text--primary">
                    <v-icon class="ml-4" :color="item.color" large>{{
                      item.icon
                    }}</v-icon>
                    {{ item.number }}</span
                  ><span class="text--secondary">{{ item.unit }}</span>
                </div>
                <div class="text--secondary caption ml-3 d-flex justify-center">
                  {{ item.text }}
                  <span v-if="item.isEditable">
                    <EditProductionButton></EditProductionButton>
                  </span>
                </div>
              </div>
            </div>
          </div>
        </v-fade-transition>
      </v-row>

      <!-- <v-divider class="ml-2"></v-divider> -->

      <template>
        <div>
          <apexchart
            ref="sampleGender"
            type="area"
            height="200"
            width="100%"
            :options="chartOptions"
            :series="series"
          ></apexchart>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
//import ProgressStatus from "../components/ProgressStatus";
import { mapState } from "vuex";
import DropdownData from "@/components/dashboard/DropdownData.vue";
import EditProductionButton from "@/components/EditProductionButton.vue";

// import VideoProgress from "../components/VideoProgress"; Remove VideoProgress
export default {
  // mixins: [mixins],
  name: "ProgressInfo",

  components: {
    DropdownData,
    EditProductionButton,
  },

  props: {
    // averageTime: Number,
    right: Number,
    wrong: Number,
    total: Number,
  },

  data: () => ({
    dataSeries: null,
    icon: null,
    number: 6,
    unit: "peças",
    sampleGender: 1,
    intervalDays: 7,
    selectedDataSet: 0,

    chartOptions: {
      legend: {
        show: false,
      },
      type: "gradient",
      grid: {
        padding: {
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
        },
      },
      chart: {
        type: "area",
        height: 200,
        sparkline: {
          enabled: true,
        },
      },
      stroke: {
        curve: "straight",
      },
      fill: {
        opacity: 0.3,
      },
      yaxis: {
        min: 0,
        max: 100,
      },
      colors: ["#DCE6EC"],
    },
  }),

  methods: {
    selectedArray(event) {
      this.dataSeries = event;
      console.log("event: ", event);
    },
  },

  computed: {
    ...mapState({
      allParts: (state) => state.production.allParts,
      productionPartList: (state) => state.production.productionPartList,
    }),

    series: function () {
      let data = [
        {
          name: "Total",
          data: [],
        },
      ];

      data[0].data = this.allParts.production.today.timesPerCicles;

      // this.chartOptions.yaxis.min = Math.min(...data[0].data) - 15;
      this.chartOptions.yaxis.max = Math.max(...data[0].data) + 15;

      return data;
    },

    infoList: function () {
      let data;

      if (!this.dataSeries) {
        data = this.allParts;
        // console.log("data1 info", data);
      } else {
        data = this.dataSeries;
        // console.log("data2 info", data);
      }

      // console.log("infolist: ", data);

      let list = [
        {
          text: "Total",
          unit: "",
          number: this.total,
          icon: "mdi-chart-timeline-variant",
          color: "blue lighten-2",
          isEditable: false,
        },
        {
          text: "Certas",
          unit: "",
          number: this.right,
          isEditable: true,
          // number: this.state.production.today.rigth,
          icon: "mdi-check",
          color: "green lighten-2",
        },
        {
          text: "Erradas",
          unit: "",
          // number: this.state.production.today.wrong,
          number: this.wrong,
          isEditable: false,
          icon: "mdi-close",
          color: "red lighten-2",
        },
        {
          text: "Tempo médio",
          unit: "s",
          // number: this.state.production.today.timePerCicle.toFixed(1),
          isEditable: false,
          number: data.production.today.timePerCicle.toFixed(1),
          icon: "mdi-timer-outline",
          color: "blue lighten-2",
        },
      ];
      return list;
    },
  },
};
</script>

<style lang="scss" scopped>
.statistics .container {
  width: 100%;
  padding: 0;
}
</style>
