<template>
  <section class="content d-flex align-center flex-column">
    <ScanAnimation class="animation" />
    <h1>Identificando o conector e o painel...</h1>
    <v-btn class="cancel" text large color="warning">cancelar</v-btn>
  </section>
</template>

<script>
// import mixins from "../_linkers/conectors.js";
import ScanAnimation from "../components/ScanAnimation";
import { mapState, mapMutations } from "vuex";
import { actions } from "../store/index";

export default {
  // mixins: [mixins],
  name: "Scan",
  components: {
    ScanAnimation,
  },
  data: () => ({
    //
  }),

  computed: {
    ...mapState(["scanConnectorsComplete"]),
  },

  methods: {
        ...mapMutations(["SEND_MESSAGE", "SCAN_COMPLETE_CHANGE"]),
  },

  watch: {
    scanConnectorsComplete(newValue, oldValue) {
      console.log(`Updating from ${oldValue} to ${newValue}`);
      this.$router.push({ path: "/progress" });
    },
  },

  created (){
    this.SEND_MESSAGE({command: actions.START_SCAN, parameter:2})
  },

  beforeDestroy() {
    this.SCAN_COMPLETE_CHANGE()
  },

};
</script>

<style scoped lang="scss">
.content {
  height: 100%;
  display: grid;
  place-items: center;

  .animation {
    margin-top: 30vh;
  }

  h1 {
    width: 360px;
    font-size: 2em;
    font-weight: 400;
    margin-top: 1em;
  }

  .cancel {
    margin-top: 15em;
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