<template>
  <v-expansion-panel>
    <v-expansion-panel-header
      ><div>
        <v-icon class="mr-2">mdi-screwdriver</v-icon>Definições de montagem
      </div></v-expansion-panel-header
    >
    <v-expansion-panel-content>
      <v-divider></v-divider>
      <div class="mt-3 d-flex align-center justify-center">
        <v-btn
          class="mr-3"
          v-for="item in configuration.assembly.listOfParts"
          :key="item.index"
          rounded
          text
          :color="selectedPart == item.index ? 'red' : ''"
          @click="selectedPart = item.index"
          >{{ item.partName }}</v-btn
        >
      </div>

      <div class="d-flex justify-space-around wrap">
        <div class="d-flex align-start flex-column justify-center title">
          <div class="text-h5">Escolha quais parafusos serão montados</div>
        </div>
        <div class="img">
          <transition name="fade">
            <v-img
              :src="
                require(`@/assets/img/${configuration.assembly.listOfParts[selectedPart].frontImg}`)
              "
              max-width="350"
              contain
              :key="configuration.assembly.listOfParts[selectedPart].frontImg"
            >
              <div
                v-for="item in configuration.assembly.listOfParts[selectedPart]
                  .listOfHoles"
                :key="item.index"
              >
                <v-checkbox
                  :style="item.checkboxPosition"
                  class="checkbox"
                  v-model="item.mount"
                  color="red"
                  hide-details
                  @click="
                    () => {
                      SEND_MESSAGE({
                        command: actions.UPDATE_ASSEMBLY,
                        parameter: configuration.assembly,
                      });
                    }
                  "
                ></v-checkbox>
              </div>
            </v-img>
          </transition>
        </div>
      </div>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import { actions } from "@/store/index";

// import EditableInfo from "./EditableInfo";

export default {
  components: {},
  name: "Assembly",
  data: () => ({
    actions,
    imgUrlSelected: "",
    selectedPart: 0,
  }),

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),
  },

  computed: {
    ...mapState(["configuration"]),
  },
};
</script>

<style scoped lang="scss">
.bounce-enter-active {
  animation: bounce-in 0.5s;
}

.slide-fade-enter-active {
  transition: all 0.3s ease;
}
.slide-fade-leave-active {
  //   transition: all .8s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}
.slide-fade-enter, .slide-fade-leave-to
/* .slide-fade-leave-active below version 2.1.8 */ {
  transform: translateX(10px);
  opacity: 1;
}
// .v-img{
//   width: 50px;
// }

.img {
  height: 100%;
}

.img2 {
  height: 150px;
}
.title {
  min-width: 120px;
}
.wrap {
  min-height: 300px;
}

.checkbox {
  position: absolute;
  //   object-checkboxPosition: 50% 50%
}
</style>