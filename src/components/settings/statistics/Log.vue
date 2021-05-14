<template>
  <v-card class="mt-10">
    <v-card-title>
      Logs
      <v-spacer></v-spacer>
    </v-card-title>
    <v-data-table :headers="headers" :items="log" sort-by="date" dense>
      <template v-slot:item.date="{ item }">
        {{ timestampToData(item.date) }}
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
      headers: [
        {
          text: "Código",
          value: "code",
        },
        {
          text: "Descrição",
          value: "description",
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