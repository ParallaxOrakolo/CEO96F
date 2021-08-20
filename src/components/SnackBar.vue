<template>
  <v-alert
    text
    border="bottom"
    class="alert"
    colored-border
    type="error"
    elevation="10"
    prominent
    
  >
    <v-row align="center">
      <v-col class="">
        <!-- <v-icon color="red" medium class="mr-6">mdi-lan-disconnect</v-icon
        > -->
        {{ connectionStatus }}
      </v-col>
      <v-col class="shrink">
        <v-btn
          small
          class="mr-6"
          @click="startConnection()"
          :loading="isConnecting"
          >Reconectar</v-btn
        >
      </v-col>
    </v-row>
  </v-alert>
</template>

<script>
// import { mapState } from "vuex";
import { mapActions, mapState } from "vuex";

export default {
  name: "SnackBar",
  data: () => ({
    snackbar: false,
    vertical: true,
    text:
      "Houve um problema de conexão com a maquina! Estamos tentando reconectar! ",
  }),

  methods: {
    ...mapActions(["startConnection"]),
  },

  computed: {
    ...mapState(["isConnecting", "connectionStatus"]),
  },
};
</script>

<style scoped lang="scss">
.alert {
  margin-top: 80px;

  .v-alert__icon.v-icon {
    /* margin: 0 auto; */
    /* font-size: 25px; */
    /* display: block; */
    padding-top: 27px;
}
}


</style>