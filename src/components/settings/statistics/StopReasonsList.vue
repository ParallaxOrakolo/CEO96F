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
      :items="stopReasonsList"
      sort-by="date"
      sort-desc="date"
      :search="search"
      dense
    >
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
    ...mapState(["stopReasonsList"]),
  },

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),

    timestampToData(timestamp) {
      var d = new Date(timestamp * 1000);
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
      icons: {
        error: "alert-octagon",
        warning: "alert",
        info: "information",
        success: "check-circle",
      },
      headers: [
        {
          text: "Motivo",
          value: "description",
        },
        { text: "Data", value: "date" },
      ],
      search: "",
    };
  },

  created: function () {
    this.SEND_MESSAGE({ command: actions.STOP_REASONS_LIST_REQUEST });
  },
};
</script>

<style>
</style>