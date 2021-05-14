<template>
  <v-card>
    <v-card-title>
      Lista de paradas
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Pesquisa"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="configuration.statistics.stopReasonsList"
      sort-by="date"
      :search="search"
    >
      <template v-slot:item.date="{ item }">
        {{ timestampToData(item.date) }}
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
import { mapState } from "vuex";

export default {
  computed: {
    ...mapState(["configuration"]),
  },

  methods: {
    timestampToData(timestamp) {
      var d = new Date(timestamp*1000);
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
      headers: [
        {
          text: "Motivo",
          value: "reason",
        },
        { text: "Data", value: "date" },
      ],
      search: "",
    };
  },
};

</script>

<style>
</style>