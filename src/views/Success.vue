<template>
  <section class="mx-auto section">
    <div class="content d-flex align-end flex-column">
      <div
        class="
          text
          font-weight-bold
          text-h3 text-end
          indigo--text
          text--indigo
          darken-3
        "
      >
        Montagem concluida!
      </div>

      <div class="d-flex justify-space-between flex-column data">
        <div
          class="d-flex justify-end"
          v-for="item in infoList"
          :key="item.text"
        >
          <div class="d-flex justify-end flex-column">
            <div>
              <span class="text-h3 text--primary">
                <v-icon class="ml-4" :color="item.color" large>{{
                  item.icon
                }}</v-icon>
                {{ item.number }}</span
              ><span class="subtitle-1">{{ item.unit }}</span>
            </div>

            <!-- <v-divider class="ml-2"></v-divider> -->
            <div class="subtitle-1 caption ml-3 d-flex justify-end">
              {{ item.text }}
            </div>
          </div>
        </div>
      </div>

      <StartButton
        text="Reiniciar Processo"
        icon="mdi-restart"
        @click="state.operation.finished = false"
      />
    </div>
  </section>
</template>

<script>
import { mapGetters, mapMutations } from "vuex";
import { actions } from "../store/index";
import StartButton from "../components/StartButton";

export default {
  // mixins: [mixins],
  name: "Success",

  data: () => ({
    actions,
    buttomClicked: false,
    overlay: false,
    zIndex: 9,
    opacity: 1,
  }),

  components: {
    StartButton,
  },

  computed: {
    ...mapGetters(["state"]),

    infoList: function () {
      let list = [
        {
          text: "Total de peças",
          unit: "",
          number: this.state.operation.right + this.state.operation.wrong,
          icon: "mdi-chart-timeline-variant",
          color: "blue lighten-2",
        },
        {
          text: "Certas",
          unit: "",
          number: this.state.operation.right,
          icon: "mdi-check",
          color: "green lighten-2",
        },
        {
          text: "Erradas",
          unit: "",
          number: this.state.operation.wrong,
          icon: "mdi-close",
          color: "red lighten-2",
        },
      ];
      return list;
    },
  },

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),

    stopReasonsMessage(code) {
      var message = {
        code: code,
        date: Math.floor(Date.now() / 1000),
      };
      return message;
    },
  },
};
</script>

<style scoped lang="scss" >
.section {
  max-width: 700px;
  height: 100%;

  .content {
    background-image: url("../assets/img/estribo-quadrado-mirror-perspective.jpg");
    width: 100%;
    // margin-top: 2em;
    padding: 6em 5em 0em 0em;
    background-position: -22em 5em;

    .text {
      width: 5em;
    }
    .data {
      margin-top: 6em;
      margin-bottom: 10em;
      height: 15em;
    }
  }
}

// section {
//   .buttons {
//     display: flex;
//     flex-flow: column;
//     justify-content: center;
//     height: 100%;
//     margin: 0 auto;

//     button {
//       margin-bottom: 2em;
//     }
//   }
// }
</style>
