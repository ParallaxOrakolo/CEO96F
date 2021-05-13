<template>
  <v-snackbar v-model="isConnected" :vertical="vertical">
    <template v-slot:action="{ attrs }">
      <v-btn color="pink" text v-bind="attrs" @click="snackbar = false">
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "SnackBar",
  data: () => ({
    snackbar: false,
    vertical: true,
    text:
      "Houve um problema de conexão com a maquina! Estamos tentando reconectar! ",
  }),

  methods: {
    IsVisible() {

      this.snackbar = true;
    },
  },

  computed: {
    ...mapState(["isConnected"]),
  },
};
</script>

<style scoped lang="scss">
</style>