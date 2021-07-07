<template>
  <section class="content d-flex align-center flex-column">
    <div class="start">
      <h1 class>
        Certifique-se que a maquina possui insumos para montagem.
      </h1>
      <router-link to="/scan">
        <v-btn
          rounded
          elevation-12
          x-large
          class="align-self-center"
          color="warning"
        >Iniciar</v-btn>
      </router-link>
    </div>

    <img src="../assets/img/estribo-pattern.jpg" />
  </section>
</template>

<script>
import { mapState } from "vuex";
// import mixins from "../_linkers/conectors.js";
import { actions } from "../store/index";

export default {
  // mixins: [mixins],
  name: "Home",
  data: () => ({
    actions,
    buttomClicked: false,
  }),

  computed: {
    ...mapState(["scanConnectorsComplete"]),
  },

  methods: {
    // // ...mapActions(["sendMessage"]),
    // ...mapMutations(["SEND_MESSAGE", "changeStatusSpinner"]),
  },
};
</script>

<style scoped lang="scss">
.content {
  height: 100%;
  display: grid;
  place-items: center;

  .start {
    display: grid;
    place-items: center;

    h1 {
      width: 450px;
      font-size: 2em;
    }

    v-btn {
      display: block;
    }
  }

  div {
    height: 100%;
  }

  > img {
    width: 100%;
    height: auto;
  }
}
</style>