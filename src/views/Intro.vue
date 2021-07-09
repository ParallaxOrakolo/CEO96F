<template>
  <section class="content d-flex align-center flex-column">
    <div  v-if="!autoCheckComplete" class="intro">
      <h2>Aguarde! Estamos preparando tudo...</h2>
      <v-progress-linear
        color="orange"
        indeterminate
        rounded
        height="5"
      ></v-progress-linear>
      <h2 class="typed-text" transition="slide-x-transition">
        {{
          autoCheckComplete == null
            ? "Conectando com a máquina..."
            : connectionStatus
        }}
      </h2>
    </div>

    <div v-else v-on="nextPage()" class="intro">
      <h2>Tudo pronto!</h2>
      <v-progress-linear
        color="green"
        rounded
        height="5"
      ></v-progress-linear>
      <h2 class="typed-text" transition="slide-x-transition">
        <v-icon color="green"  large>mdi-check</v-icon>
        {{
          autoCheckComplete == null
            ? "Conectando com a máquina..."
            : connectionStatus
        }}
      </h2>
    </div>
  </section>
</template>

<script>
// import mixins from "../_linkers/conectors.js";
import { mapActions, mapState } from "vuex";

export default {
  // mixins: [mixins],
  name: "Intro",
  data: () => ({
    steps: ["a condição da luminação", "Folgas", "Confiabilidade"],
    //
  }),

  computed: mapState({
    connectionStatus: (state) => state.connectionStatus,
    autoCheckComplete: (state) => state.autoCheckComplete,
  }),

  methods: {
    ...mapActions(["startConnection", "sendMessage"]),

    nextPage() {
      setTimeout(() => this.$router.push({ path: "/progress" }).catch(()=>{}), 3000);
    },
  },

  created: function () {
    this.startConnection();
  },
};
</script>

<style scoped lang="scss">
@import "@/assets/scss/_variables.scss";

.content {
  display: grid;
  place-items: center;

  .intro {
    margin: auto;
    text-align: left;
    height: initial;
    transition: opacity 2s;

    margin: auto;
    h2 {
      width: 400px;

      &:first-child {
        color: $second-color;
        margin-bottom: 1em;
      }
      &:last-child {
        margin-top: 0.5em;
      }
    }
  }

  > img {
    width: 100%;
    height: auto;
  }
}
</style>