<template>
  <div class="content mx-auto">
    <v-tabs>
      <v-tab
        v-for="item in cameraList"
        :key="item.name"
        @click="
          selectedCamera = item.cameraId;
          selectedFilter = item.filter;
          makeUrl(item.filter, item.cameraId);
          updateURL()
        "
        >{{ item.name }}</v-tab
      >
    </v-tabs>
    <div class="d-flex align-end mb-6">
      <div class="v-switch">
        <v-switch
          dark
          v-model="filter"
          inset
          :label="`Filtro: ${filter.toString()}`"
          @click="updateURL()"
        ></v-switch>
      </div>
      <v-img
        class="cameraImg"
        alt="camera"
        :src="`http://${configuration.informations.ip}:${
          configuration.informations.port + 1
        }/${stringUrl}?${Math.floor(Math.random() * (1000 - 1 + 1)) + 1}`"
      >
      </v-img>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
// import { actions } from "../../../store/index";

export default {
  name: "Camera",
  data() {
    return {
      selectedCamera: "0",
      selectedFilter: "Hole",
      filter: false,
      stringUrl: "Normal/0",
      cameraList: [
        {
          name: "Camera Furação",
          cameraId: 0,
          filter: "Hole",
        },
        {
          name: "Camera de Validação",
          cameraId: 1,
          filter: "Screw",
        },
      ],
    };
  },

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),

    makeUrl(filter, cameraId) {
     this.stringUrl = ""

      if (filter) {
        this.stringUrl = filter + "/" + cameraId;
      } else {
        this.stringUrl = this.Normal + "/" + cameraId;
      }
      console.log(this.stringUrl);
    },

    updateURL() {
        this.stringUrl = " "
        console.log(this.stringUrl);
      if (this.filter) {
        this.stringUrl = this.selectedFilter + "/" + this.selectedCamera;
      } else {
        this.stringUrl = "Normal" + "/" + this.selectedCamera;
      }
      console.log(this.stringUrl);
    },
  },

  computed: {
    ...mapState(["configuration"]),
  },
};
</script>

<style scoped lang="scss">
.content {
  //   max-width: 600px;
  border-radius: 0.8em;
  display: block;
  width: 100%;
  .v-switch {
    margin-top: -20px;
    margin-left: 1.5em;
    position: absolute;
    z-index: 999;
  }

  .cameraImg {
    width: 100%;
    max-width: 720px;
    display: block;
    border-radius: 0px 10px 10px 10px;

  }

  .v-input--selection-controls {
    margin-top: -10px;
  }
}
</style>