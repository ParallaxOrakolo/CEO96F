<template>
  <div>
    <v-card class="mx-auto" v-on="updateChart()" v-if="series[0].data">
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
  name: "LineChartCard",

  data: () => ({
    // infoList: [
    //   {
    //     ref: "total",
    //     text: "Total",
    //     unit: "",
    //     number: 2,
    //     icon: "mdi-chart-timeline-variant",
    //     color: "blue lighten-2",
    //   },
    //   {
    //     ref: "right",
    //     text: "Certas",
    //     unit: "",
    //     number: 20,
    //     icon: "mdi-check",
    //     color: "green lighten-2",
    //   },
    //   {
    //     ref: "wrong",
    //     text: "Erradas",
    //     unit: "",
    //     number: 20,
    //     icon: "mdi-close",
    //     color: "red lighten-2",
    //   },
    //   {
    //     ref: "times",
    //     text: "Tempo médio",
    //     unit: "s",
    //     number: 20,
    //     icon: "mdi-timer-outline",
    //     color: "blue lighten-2",
    //   },
    // ],

    icon: null,
    number: 6,
    title: "Média Total Produção Diaria",
    unit: "peças",
    sampleGender: 1,
    intervalDays: 7,
    series: [
      {
        name: "Total",
        data: [],
      },
      {
        name: "Certas",
        data: [],
      },
      {
        name: "Erradas",
        data: [],
      },
    ],

    chartOptions: {
      colors: ["#2E93fA", "#81C784", "#E57373"],
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
        type: "datetime",

        // min: new Date().getTime(),
        // max: new Date().setDate(new Date().getDate() + 4),

        categories: [],
      },
      tooltip: {
        x: {
          format: "dd/MM",
          // format: "dd/MM/yy HH:mm",
        },
      },
    },
  }),

  // props: {
  //   title: String,
  //   number: Number,
  //   unit: String,
  //   description: String,
  //   correct:  Number,
  //   wrong:  Number,
  //   icon: String,
  // },

  components: {
    //ProgressStatus,
    //VideoProgress, // Remove VideoProgress -HB
  },

  computed: {
    ...mapGetters(["state"]),
    // week_total: function () {
    //   this.series[0].data = this.state.production.dailyAvarege.week_total;
    // },
    infoList: function () {
      let list = [
        {
          text: "Total",
          unit: "",
          number: this.state.production.dailyAvarege.total,
          icon: "mdi-chart-timeline-variant",
          color: "blue lighten-2",
        },
        {
          text: "Certas",
          unit: "",
          number: this.state.production.dailyAvarege.rigth,
          icon: "mdi-check",
          color: "green lighten-2",
        },
        {
          text: "Erradas",
          unit: "",
          number: this.state.production.dailyAvarege.wrong,
          icon: "mdi-close",
          color: "red lighten-2",
        },
        {
          text: "Tempo médio",
          unit: "s",
          number: this.state.production.dailyAvarege.times.toFixed(1),
          icon: "mdi-timer-outline",
          color: "blue lighten-2",
        },
      ];
      return list;
    },
  },

  methods: {
    updateChart() {
      setTimeout(() => {
        this.series[0].data = this.state.production.dailyAvarege.week_total;
        this.series[1].data = this.state.production.dailyAvarege.week_rigth;
        this.series[2].data = this.state.production.dailyAvarege.week_wrong;

        for (var i = 0; i < 5; i++) {
          var result = new Date();
          result.setDate(result.getDate() + i);
          result = result.getTime();
          this.chartOptions.xaxis.categories.push(result);
          console.log(this.chartOptions.xaxis.categories);
          console.log(this.series[0].data);
        }
        this.$refs.sampleGender = i;
        window.dispatchEvent(new Event("resize"));
      }, 1000);
    },
  },

  mounted: {},
};
</script>

<style lang="scss" scopped>
</style>
