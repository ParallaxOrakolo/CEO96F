<template>
  <div>
    <v-card class="mx-auto" v-if="series[0].data">
      <div class="pa-3">
        <v-row>
          <div class="text--secondary ml-3 mb-4">{{ title }}</div>
        </v-row>
        <v-row>
          <div class="pr-5 pl-3 d-flex justify-space-around statistics">
            <div
              class="d-flex justify-space-around"
              v-for="item in infoList"
              :key="item.text"
            >
              <div>
                <span class="text-h5 text--primary">
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
            </div>
          </div>
        </v-row>

        <!-- <v-divider class="ml-2"></v-divider> -->

        <template>
          <div>
            <apexchart
              ref="sampleGender"
              type="bar"
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
  name: "ProductionAverageChartCard",
  data: () => ({
    icon: null,
    number: 6,
    title: "Média Total Produção Diaria",
    unit: "peças",
    sampleGender: 1,
    intervalDays: 7,
    

    chartOptions: {
       colors: [ "#81C784", "#E57373"],
      //  colors: ["#2E93fA", "#81C784", "#E57373"],
      // fill: {
      //   type: "gradient",
      // },
      // markers: {
      //   size: 6,
      //   hover: {
      //     size: 9,
      //   },
      // },
      plotOptions: {
        bar: {
          horizontal: false,
          borderRadius: 10,
        },
      },

      chart: {
        height: 400,
        type: "bar",
        stacked: true,

        toolbar: {
          show: false,
        },

        zoom: {
          enabled: false,
        },
      },

      //  fill: {
      //     opacity: 1
      //   },

      dataLabels: {
        enabled: false,
        background: {
          enabled: true,
          borderRadius: 15,
          borderWidth: 3,
        },
      },
      // stroke: {
      //   curve: "smooth",
      // },

      xaxis: {
        type: "datetime",
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

 

  computed: {
    ...mapGetters(["state"]),
    // week_total: function () {
    //   this.series[0].data = this.state.production.dailyAvarege.week_total;
    // },

    series: function() {
      let list = [
        {
          name: "Certas",
          data: [],
        },
        {
          name: "Erradas",
          data: [],
        },
      ]

      list[0].data = this.state.production.dailyAvarege.week_rigth.slice(0).reverse()
      list[1].data = this.state.production.dailyAvarege.week_wrong.slice(0).reverse()
      // this.series[0].data = this.state.production.dailyAvarege.week_total.slice(0).reverse();
      // this.series[1].data = this.state.production.dailyAvarege.week_rigth.slice(0).reverse();
      // this.series[2].data = this.state.production.dailyAvarege.week_wrong.slice(0).reverse();

      for (var i = 0; i < 7; i++) {
        var result = new Date();
        result.setDate(result.getDate() - i - 1);
        result = result.getTime();
        this.chartOptions.xaxis.categories.push(result);
        // console.log(this.chartOptions.xaxis.categories);
        // console.log(this.series[0].data);
      }
        

    return list
    },

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
        // this.series[0].data = this.state.production.dailyAvarege.week_total.slice(0).reverse();
        // this.series[1].data = this.state.production.dailyAvarege.week_rigth.slice(0).reverse();
        // this.series[2].data = this.state.production.dailyAvarege.week_wrong.slice(0).reverse();

        for (var i = 0; i < 7; i++) {
          var result = new Date();
          result.setDate(result.getDate() - i - 1);
          result = result.getTime();
          this.chartOptions.xaxis.categories.push(result);
          // console.log(this.chartOptions.xaxis.categories);
          // console.log(this.series[0].data);
        }

        this.$refs.sampleGender = i;
        window.dispatchEvent(new Event("resize"));
        console.log(this.series);
      }, 1000);
    },
  },
};
</script>

<style lang="scss" scopped>
.statistics {
  width: 100%;
}
</style>
