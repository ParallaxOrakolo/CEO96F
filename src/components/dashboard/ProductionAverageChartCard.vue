<template>
  <div>
    <v-card class="mx-auto" v-if="series[0].data">
      <div class="pa-3">
        <v-row>
          <div class="text--secondary ml-3 mb-6">{{ title }}</div>
          <v-spacer></v-spacer>
          <DropdownData @selected-item="selectedArray"></DropdownData>
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
import { mapState } from "vuex";
import DropdownData from "@/components/dashboard/DropdownData.vue";

export default {
  // mixins: [mixins],
  name: "ProductionAverageChartCard",

  components: {
    DropdownData,
  },

  data: () => ({
    dataSeries: null,
    icon: null,
    number: 6,
    title: "Média Total Produção Diaria",
    unit: "peças",
    sampleGender: 1,
    intervalDays: 7,
    chartOptions: {
      stroke: {
        curve: "smooth",
      },
      colors: ["#E57373", "#81C784"],
      plotOptions: {
        bar: {
          horizontal: false,
          borderRadius: 8,
        },
      },

      chart: {
        height: 400,
        // type: "gradient",
        stacked: true,

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

      xaxis: {
        type: "datetime",
        categories: [],
        tickPlacement: "on",
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
    // ...mapGetters(["state"]),

    ...mapState({
      allParts: (state) => state.production.allParts,
      productionPartList: (state) => state.production.productionPartList,
    }),

    series: function () {
      let data;

      if (!this.dataSeries) {
        data = this.allParts;
        // console.log("data1 info", data);
      } else {
        data = this.dataSeries;
        // console.log("data2 info", data);
      }

      let serie = [
        {
          name: "Erradas",
          type: "column",
          data: [],
        },
        {
          name: "Certas",
          type: "column",

          data: [],
        },
      ];

      serie[0].data = data.production.dailyAvarege.week_wrong.slice(0);
      serie[1].data = data.production.dailyAvarege.week_rigth.slice(0);
      // this.series[0].data = this.state.production.dailyAvarege.week_total.slice(0).reverse();
      // this.series[1].data = this.state.production.dailyAvarege.week_rigth.slice(0).reverse();
      // this.series[2].data = this.state.production.dailyAvarege.week_wrong.slice(0).reverse();
      this.chartOptions.xaxis.categories = [];
      for (var i = 0; i < this.intervalDays; i++) {
        var result = new Date();
        result.setDate(result.getDate() - this.intervalDays + i);
        result = result.getTime();

        this.chartOptions.xaxis.categories.push(result);
        // console.log(this.chartOptions.xaxis.categories);
        console.log(new Date(result).getDate());
      }

      console.log("series: ", serie);
      return serie;
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

      let list = [
        {
          text: "Total",
          unit: "",
          number: data.production.dailyAvarege.total,
          icon: "mdi-chart-timeline-variant",
          color: "blue lighten-2",
        },
        {
          text: "Certas",
          unit: "",
          number: data.production.dailyAvarege.rigth,
          icon: "mdi-check",
          color: "green lighten-2",
        },
        {
          text: "Erradas",
          unit: "",
          number: data.production.dailyAvarege.wrong,
          icon: "mdi-close",
          color: "red lighten-2",
        },
        {
          text: "Tempo médio",
          unit: "s",
          number: data.production.dailyAvarege.times.toFixed(1),
          icon: "mdi-timer-outline",
          color: "blue lighten-2",
        },
      ];
      return list;
    },
  },

  methods: {
    selectedArray(event) {
      this.dataSeries = event;
      console.log("event: ", event);
    },

    updateChart() {
      setTimeout(() => {
        this.series[0].data = this.state.production.dailyAvarege.week_total;
        this.series[1].data = this.state.production.dailyAvarege.week_rigth;
        this.series[2].data = this.state.production.dailyAvarege.week_wrong;
        // this.series[0].data = this.state.production.dailyAvarege.week_total.slice(0).reverse();
        // this.series[1].data = this.state.production.dailyAvarege.week_rigth.slice(0).reverse();
        // this.series[2].data = this.state.production.dailyAvarege.week_wrong.slice(0).reverse();

        for (var i = 0; i < this.intervalDays; i++) {
          var result = new Date();
          result.setDate(result.getDate() - i - 1);
          result = result.getTime();
          this.chartOptions.xaxis.categories.push(result);
          // console.log(this.chartOptions.xaxis.categories);
          // console.log(this.series[0].data);
        }

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
