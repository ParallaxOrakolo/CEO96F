<template>
  <div>
    <v-card class="mx-auto" min-width="300">
      <div class="mr-3">
        <v-row>
          <v-col cols="4" class="d-flex justify-center">
            <v-icon class="ml-4" :color="iconColor" large>{{ icon }}</v-icon>
          </v-col>
          <v-col cols="8">
            <div class="text-right text--secondary">{{ title }}</div>
            <div class="text-right">
              <span class="text-h4 text--primary">{{ number }}</span
              ><span class="text--secondary">{{ unit }}</span>
            </div>
          </v-col>
        </v-row>
        <v-divider class="ml-2"></v-divider>
        <v-card-actions>
          <p class="text--secondary caption">{{ description }}</p>

          <v-spacer></v-spacer>

          <p class="text--secondary mr-4">
            <v-icon class="" color="blue lighten-2" small
              >{{iconTypeAlternative? "mdi-check" : "mdi-arrow-up-thick"}}</v-icon
            >
            {{ correct }}
          </p>

          <p class="text--secondary">
            <v-icon class="" color="red lighten-2" small
              >{{iconTypeAlternative? "mdi-close" : "mdi-arrow-down-thick"}}</v-icon
            >
            {{ wrong }}
          </p>
        </v-card-actions>
      </div>
    </v-card>
  </div>
</template>

<script>
//import ProgressStatus from "../components/ProgressStatus";
//import { mapGetters, mapMutations } from "vuex"; mapMutation não tem uso.
import { mapGetters } from "vuex";
// import VideoProgress from "../components/VideoProgress"; Remove VideoProgress

export default {
  // mixins: [mixins],
  name: "TotalCard",

  data: () => ({}),

  props: {
    title: String,
    number: Number,
    unit: String,
    description: String,
    correct: Number,
    wrong: Number,
    icon: String,
    iconColor: String,
    iconTypeAlternative: Boolean

  },

  components: {
    //ProgressStatus,
    //VideoProgress, // Remove VideoProgress -HB
  },

  computed: {
    ...mapGetters(["state"]),
  },

  methods: {},
};
</script>

<style lang="scss" scopped>
p {
  margin-bottom: 0 !important;
}
</style>
