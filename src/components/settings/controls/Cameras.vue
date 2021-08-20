<template>
  <div class="content mx-auto">
    <v-tabs>
      <v-tab
        v-for="item in configuration.cameraList"
        :key="item.name"
        @click="
          selectedCamera = item.cameraId;
          selectedFilter = item.filter;
          makeUrl(item.filter, item.cameraId);
          updateURL();
        "
        >{{ item.name }}</v-tab
      >
    </v-tabs>
    
    <div class="d-flex align-end mb-6">
      <div class="v-switch">
        <v-switch
          v-model="filter"
          inset
          :label="`Filtro`"
          @click="updateURL()"
        ></v-switch>
      </div>
      <!-- <v-img
        lazy-src="https://picsum.photos/id/11/100/60"
        class="cameraImg"
        alt="camera"
        :src="`http://${configuration.informations.ip}:${
          configuration.informations.portStream
        }/${stringUrl}?${Math.floor(Math.random() * (1000 - 1 + 1)) + 1}`"
      >
      </v-img> -->
      <v-img
        :lazy-src="require(`@/assets/img/estribo-pattern-low.jpg`)"
        class="cameraImg"
        alt="camera"
        :src="`http://${configuration.informations.ip}:${
          configuration.informations.portStream
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
      selectedFilter: "hole",
      filter: false,
      stringUrl: "normal/0",
      cameraList: [
        {
          name: "Camera Furação",
          cameraId: 0,
          filter: "hole",
        },
        {
          name: "Camera de Validação",
          cameraId: 2,
          filter: "screw",
        },
      ],
    };
  },

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),

    makeUrl(filter, cameraId) {
      this.stringUrl = "";

      if (filter) {
        this.stringUrl = filter + "/" + cameraId;
      } else {
        this.stringUrl = this.Normal + "/" + cameraId;
      }
      console.log(this.stringUrl);
    },

    updateURL() {
      this.stringUrl = " ";
      console.log(this.stringUrl);
      if (this.filter) {
        this.stringUrl = this.selectedFilter + "/" + this.selectedCamera;
      } else {
        this.stringUrl = "normal" + "/" + this.selectedCamera;
      }
      console.log(this.stringUrl);
    },
  },

  computed: {
    ...mapState(["configuration", "selectedFilter"]),
  },
};
</script>

<style scoped lang="scss">
.content {
  border-radius: 0.8em;
  display: block;
  width: 100%;

  .v-switch {
    margin-bottom: 0;
    position: absolute;
    z-index: 999;
    padding: 0 1em;
    border-top-right-radius: 1em;
    background-color: #ffffffe1;
  }

  .cameraImg {
    width: 100%;
    max-width: 720px;
    display: block;
    border-radius: 0px 10px 10px 10px;
  }

}
</style>