<template>
  <div>
    <v-card class="mx-auto" v-if="series[0].data">
      <div class="pa-3">
        <v-row>
          <div class="text--secondary ml-3">{{ title }}</div>
        </v-row>
        <v-row>
          <v-row class="pr-5">
            <v-col
              cols="3"
              class="d-flex justify-center"
              v-for="item in infoList"
              :key="item.text"
            >
              <div>
                <span class="text-h4 text--primary">
                  <v-icon class="ml-4" :color="item.color" large>{{
                    item.icon
                  }}</v-icon>
                  {{ item.number }}</span
                ><span class="text--secondary">{{ item.unit }}</span>
                <!-- <v-divider class="ml-2"></v-divider> -->
                <div class="text--secondary caption ml-3 d-flex justify-center">
                  {{ item.text }}
                </div>
              </div>
            </v-col>
          </v-row>
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
import { mapGetters } from "vuex";
// import VideoProgress from "../components/VideoProgress"; Remove VideoProgress

export default {
  // mixins: [mixins],
  name: "TimeLineChartCard",

  data: () => ({
    icon: null,
    number: 6,
    title: "Produção de hoje",
    unit: "peças",
    sampleGender: 1,
    intervalDays: 7,

    chartOptions: {
      colors: ["#2E93fA"],
      fill: {
        type: "gradient",
        // gradient: {
        //   shadeIntensity: 1,
        //   opacityFrom: 0.7,
        //   opacityTo: 0.9,
        //   stops: [0, 90, 100],
        // },
      },
      markers: {
        size: 6,
        hover: {
          size: 9,
        },
      },
      chart: {
        height: 400,
        type: "area",
        toolbar: {
          show: false,
        },
        zoom: {
          enabled: false,
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
        // type: "datetime",
      },
      yaxis:{
         labels: {
          formatter: (value) => { return value.toFixed(1) },
      }
      },

      tooltip: {
        x: {
          format: "dd/MM",
        },
      },
    },
  }),

  components: {},

  computed: {
    ...mapGetters(["state"]),
    // week_total: function () {
    //   this.series[0].data = this.state.production.dailyAvarege.week_total;
    // },
    series: function () {
      let data = [
        {
          name: "Total",
          data: this.state.production.today.timesPerCicles,
        },
      ];

      return data
    },

    infoList: function () {
      let list = [
        {
          text: "Total",
          unit: "",
          number: this.state.production.today.total,
          icon: "mdi-chart-timeline-variant",
          color: "blue lighten-2",
        },
        {
          text: "Certas",
          unit: "",
          number: this.state.production.today.rigth,
          icon: "mdi-check",
          color: "green lighten-2",
        },
        {
          text: "Erradas",
          unit: "",
          number: this.state.production.today.wrong,
          icon: "mdi-close",
          color: "red lighten-2",
        },
        {
          text: "Tempo médio",
          unit: "s",
          number: this.state.production.today.timePerCicle.toFixed(1),
          icon: "mdi-timer-outline",
          color: "blue lighten-2",
        },
      ];
      return list;
    },
  },

  methods: {},

  mounted: {},
};
</script>

<style lang="scss" scopped>
</style>
