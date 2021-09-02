<template>
  <v-card class="mt-10">
    <v-card-title>
      Logs
      <v-spacer></v-spacer>
    </v-card-title>
    <v-data-table :headers="headers" :items="log" sort-by="date" sort-desc="date"
 dense>
      <template v-slot:item.date="{ item }">
        {{ timestampToData(item.date) }}
      </template>
      <template v-slot:item.description="{ item }">
        <v-icon small :color="item.type"> mdi-{{ icons[item.type] }} </v-icon>
        {{ item.description }}
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
import { mapState } from "vuex";
import { actions } from "../../../store/index";
import { mapMutations } from "vuex";

export default {
  computed: {
    ...mapState(["log"]),
  },

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),
    timestampToData(timestamp) {
      var d = new Date(timestamp * 1000);
      // console.log(d);
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

    // getIcon(type) {
    //   if (type = info) return "information-outline";
    //   else if (type = warning) return "alert-outline";
    //   else if (type = error) return "alert-octagon-outline";
    //   else if (type = error) return "check-circle-outline";
    //   else return "green";
    // },
  },

  data() {
    return {
      actions,
      icons: {
        error: "alert-octagon",
        warning: "alert",
        info: "information",
        success: "check-circle",
      },

      headers: [
        {
          text: "Descrição",
          value: "description",
        },
        {
          text: "Código",
          value: "code",
        },
        { text: "Data", value: "date" },
      ],
      search: "",
    };
  },

  created: function () {
    this.SEND_MESSAGE({ command: actions.LOG_REQUEST });
  },
};
</script>

<style>
</style>