<template>
  <div>
    <v-card-title>
      Peças/dia
      <v-spacer></v-spacer>
    </v-card-title>
    <apexchart
      type="bar"
      height="350"
      :options="chartOptions"
      :series="series"
    ></apexchart>
  </div>
</template>


<script>
import { mapState } from "vuex";
import { actions } from "../../../store/index";
import { mapMutations } from "vuex";

export default {
  name: "StopReasonsChart",
  computed: {
    ...mapState(["log"]),
  },

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),
    timestampToData(timestamp) {
      var d = new Date(timestamp * 1000);
      console.log(d);
      var options = {
        year: "numeric",
        month: "numeric",
        day: "numeric",
        hour: "numeric",
        minute: "numeric",
        second: "numeric",
        hour12: true,
      };
      return new Intl.DateTimeFormat("pt-BR", options).format(d);
    },
  },

  data() {
    return {
      actions,

      series: [
        {
          name: "Peças boas",
          data: [44, 55, 41, 67, 22, 43, 55, 41, 67, 22, 43, 55, 41, 67, 22, 43, 55, 41, 67, 22, 43, 55, 41, 67, 22, 43],
        },
        {
          name: "Peças Ruins",
          data: [13, 23, 20,  8, 13, 27, 55, 41, 67, 22, 43, 55, 41, 67, 22, 43, 55, 41, 67, 22, 43, 55, 41, 67, 22, 43],
        },
      ],
      chartOptions: {
        chart: {
          type: "bar",
          height: 350,
          stacked: true,
          toolbar: {
            show: true,
          },
          zoom: {
            enabled: true,
          },
        },
        colors: ["#54ad42", "#f58c8c"],

        responsive: [
          {
            breakpoint: 480,
            options: {
              legend: {
                position: "bottom",
                offsetX: -10,
                offsetY: 0,
              },
            },
          },
        ],
        plotOptions: {
          bar: {
            horizontal: false,
            borderRadius: 10,
          },
        },
        xaxis: {
          type: "datetime",
          categories: [
            "01/01/2011 GMT",
            "01/02/2011 GMT",
            "01/03/2011 GMT",
            "01/04/2011 GMT",
            "01/05/2011 GMT",
            "01/06/2011 GMT",
          ],
        },
        legend: {
          position: "top",
          offsetY: 10,
        },
        fill: {
          opacity: 1,
        },
      },
    };
  },

  created: function () {
    this.SEND_MESSAGE({ command: actions.LOG_REQUEST });
  },
};
</script>

<style>
</style>