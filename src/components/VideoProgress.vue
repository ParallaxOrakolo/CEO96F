<template>
  <div class="video" justify="center">
    <v-icon class="videoIcon" x-large v-show="!running && !finished"
      >mdi-pause</v-icon
    >
    <video loop autoplay @canplay="getElement" muted="muted">
      <source src="../assets/img/estribo-animation.mp4" type="video/mp4" />
    </video>
  </div>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import { actions } from "../store/index";

export default {
  name: "VideoProgress",

  data: () => ({
    actions,
    videoElement: null,
    paused: null,
  }),

  components: {
    //ProgressStatus,
  },

  computed: {
    ...mapState({
      running: (state) => {
        // if (state.operation.running) {
        this.videoElement.play();
        // document.querySelector(".videoContent").play();
        // } else {
        //   this.videoElement.pause();
        // }
        return state.operation.running;
      },

      started: (state) => state.operation.started,
      running: (state) => state.operation.running,
      finished: (state) => state.operation.finished,
    }),
    ...mapGetters(["state"]),
  },

  // watch: {
  //  .running(newValue, oldValue) {
  //     console.log(`Updating .running" from ${oldValue} to ${newValue}`);
  //     if (newValue) {
  //       this.videoElement.play();
  //       // document.querySelector(".videoContent").play();
  //     } else {
  //       this.videoElement.pause();
  //     }
  //   },
  // },

  methods: {
    getElement(event) {
      this.videoElement = event.target;
    },
  },
};
</script>

<style lang="scss" >
section {
  .video {
    display: flex;
    justify-content: center;
    align-items: center;

    video {
      width: 100vw;
      max-width: 800px;
    }

    .v-icon {
      display: block;
      position: absolute;
      margin-top: 100px;
    }
  }

  video::-internal-media-controls-overlay-cast-button {
    display: none;
  }
}
</style>
