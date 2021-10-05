<template>
  <div>
    <!-- <v-card class="mx-auto" v-if="series[0].data"> -->
    <v-card class="mx-auto">
      <div class="pa-3">
        <v-row>
          <div class="text--secondary ml-3 mb-6">
            Tempo produção de <b>hoje</b> por peça
          </div>
          <v-spacer></v-spacer>
          <DropdownData @selected-item="selectedArray"></DropdownData>
        </v-row>
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
                  <div
                    class="text--secondary caption ml-3 d-flex justify-center"
                  >
                    {{ item.text }}
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
              height="350"
              :options="chartOptions"
              :series="series"
            ></apexchart>
          </div>
        </template>
      </div>
    </v-card>
  </div>
</template>

<script>
//import ProgressStatus from "../components/ProgressStatus";
import { mapState } from "vuex";
import DropdownData from "@/components/dashboard/DropdownData.vue";

// import VideoProgress from "../components/VideoProgress"; Remove VideoProgress
export default {
  // mixins: [mixins],
  name: "TimeLineChartCard",

  components: {
    DropdownData,
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
      colors: ["#2E93fA"],
      fill: {},
      type: "gradient",
      zoom: {
        enabled: true,
      },
      chart: {
        height: 400,
        type: "area",
        toolbar: {
          show: false,
        },
        selection: {
          enabled: true,
          xaxis: {
            min: 0,
            max: 10,
          },
        },
      },
      dataLabels: {
        enabled: false,
        background: {
          enabled: true,
          borderRadius: 15,
          borderWidth: 3,
        },
      },
      stroke: {
        curve: "smooth",
      },
      xaxis: {
        tickPlacement: "between",
        // type: "datetime",
      },
      yaxis: {
        min: 20,
        max: 80,
        labels: {
          formatter: (value) => {
            return value.toFixed(1);
          },
        },
      },

      tooltip: {
        x: {
          format: "dd/MM",
        },
      },
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
          data: null,
        },
      ];

      if (!this.dataSeries) {
        data[0].data = this.allParts.production.today.timesPerCicles;
        // console.log("data1", data);
      } else {
        data[0].data = this.dataSeries.production.today.timesPerCicles;
        // console.log("data2", data);
      }

      // console.log("ultima data: ", data[0].data);
      // this.chartOptions.yaxis.min =  20;
      // this.chartOptions.yaxis.max =  80;
      // this.chartOptions.yaxis.min = Math.min(...data[0].data) - 15;
      // this.chartOptions.yaxis.max = Math.max(...data[0].data) + 15;

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
          number: data.production.today.total,
          icon: "mdi-chart-timeline-variant",
          color: "blue lighten-2",
        },
        {
          text: "Certas",
          unit: "",
          number: data.production.today.rigth,

          // number: this.state.production.today.rigth,
          icon: "mdi-check",
          color: "green lighten-2",
        },
        {
          text: "Erradas",
          unit: "",
          // number: this.state.production.today.wrong,
          number: data.production.today.wrong,

          icon: "mdi-close",
          color: "red lighten-2",
        },
        {
          text: "Tempo médio",
          unit: "s",
          // number: this.state.production.today.timePerCicle.toFixed(1),
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
.statistics {
  width: 100%;
}
</style>
