<template>
  <section class="content">
    <video
      autoplay
      class="video"
      id="video"
      preload="auto"
      muted="muted"
      @canplay="getElement"
    >
      <source src="../assets/img/logo-red-white.mp4" type="video/mp4" />
    </video>
  
  </section>
</template>

<script>
// import mixins from "../_linkers/conectors.js";
import { mapActions, mapState } from "vuex";

export default {
  // mixins: [mixins],
  name: "IntroLogo",
  data: () => ({
    videoElement: null,
    loaded: false,
    duration: null,
  }),

  computed: mapState({
    connectionStatus: (state) => state.connectionStatus,
    autoCheckComplete: (state) => state.autoCheckComplete,
  }),

  mounted() {},

  methods: {
    ...mapActions(["startConnection", "sendMessage"]),
    getElement(event) {
      if (!isNaN(event.target.duration) && !this.loaded) {
        this.duration = event.target.duration;
        this.nextPage(event.target.duration);
        event.target.currentTime = 0;
       event.target.play();
        this.loaded = true;
      }
    },

    nextPage(timeout) {
      setTimeout(
        () => this.$router.push({ path: "/progress" }).catch(() => {}),
        timeout*1000+500
      );
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
  height: 100%;
  background-color: #e93926;

  .video {
    width: 80vw;
    max-width: 600px;
  }
}
</style>