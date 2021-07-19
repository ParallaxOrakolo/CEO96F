<template>
  <v-expansion-panel>
    <v-expansion-panel-header>Filtros camera </v-expansion-panel-header>
    <v-expansion-panel-content>
      <div class="d-flex flex-row justify-space-between mb-6">
        <div>
          <color-picker v-model="gradient.color"></color-picker>
          <p>Selected color:</p>
          <svg height="32" width="32">
            <circle cx="16" cy="16" r="15" :fill="gradient.color" />
          </svg>

          <p>{{ gradient.color }}</p>
        </div>
        <div class="d-flex flex-column justify-center ">
          <p>Escala</p>
          <div
            class="gradient"
            :style="`background: linear-gradient(to right, ${gradient.color}, ${gradient.color2})
`"
          ></div>
          +
        </div>
        <div>
          <color-picker v-model="gradient.color2"></color-picker>
          <p>Selected color:</p>
          <svg height="32" width="32">
            <circle cx="16" cy="16" r="15" :fill="gradient.color2" />
          </svg>

          <p>{{ gradient.color2 }}</p>
        </div>
      </div>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import ColorPicker from "vue-color-picker-wheel";

export default {
  name: "ColorPikerHSV",
  components: {
    ColorPicker,
  },
  data: () => ({
    gradient: {
      color: "#a02727",
      color2: "#e261ae",
    },
  }),
};
</script>
<style lang="scss" scoped>
.gradient {
  width: 200px;
  height: 30px;
  border-radius: 20px;
}
</style>