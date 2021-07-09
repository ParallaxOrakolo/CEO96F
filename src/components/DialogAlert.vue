<template>
<div>
  <v-row justify="center">
    <!-- <v-dialog v-model="state.dialogAlert.show" persistent max-width="300"> -->

    <v-overlay v-model="state.dialogAlert.show">
      <v-alert
      class="alert"
        border="right"
        dense
        colored-border
        :type="state.dialogAlert.type"
        elevation="2"
      >
      <h2>{{ state.dialogAlert.description }}</h2>
        

        <v-row justify="center">
          <v-btn x-large class="mt-4 mb-3" color="darken-1"  @click="state.dialogAlert.show = false">
            Entendi
          </v-btn>
        </v-row>
      </v-alert>
    </v-overlay>
  </v-row>
  </div>
</template>


<script>
import { mapGetters} from "vuex"; // Remove mapMutations -HB

export default {
  name: "DialogAlert",
  data() {
    return {
      typeDictionary: {
        error: "Algo deu Errado",
        info: "Informação",
        warning: "Atenção",
      },
      icons: {
        error: "Algo deu Errado",
        info: "Informação",
        warning: "Atenção",
      },
    };
  },
  methods: {},
  computed: {
    ...mapGetters(["state"]),
  },
};
</script>

<style>
.alert{
  max-width:500px

}
</style>
