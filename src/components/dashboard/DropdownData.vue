<template>
  <div class="text-center">
    <v-menu offset-y :close-on-click="closeOnClick">
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          class="mr-5"
          small
          rounded
          outlined
          color="primary"
          dark
          v-bind="attrs"
          v-on="on"
        >
          {{ selectedArray ? selectedArray.name : defaultArrayName }}
        </v-btn>
      </template>

      <v-list>
        <v-list-item
          v-for="(item, index) in allArrays"
          :key="index"
          @click="select(item)"
        >
          <v-list-item-title>{{ item.name.toUpperCase() }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "DropdownData",
  data: () => ({
    selectedArray: null,
    selectedArrayName: null,
    closeOnClick: true,
  }),

  computed: {
    ...mapState({
      allParts: (state) => state.production.allParts,
      allArrays: (state) => {
        let concatenatedArray = [];
        concatenatedArray = state.production.productionPartList;
        concatenatedArray = concatenatedArray.concat([
          state.production.allParts,
        ]);
        // console.log(concatenatedArray);
        return concatenatedArray;
      },
      defaultArrayName: (state) => state.production.allParts.name,
    }),
  },

  methods: {
    select(selectedItem) {
      this.selectedArray = selectedItem;
      this.$emit("selected-item", selectedItem);
      // console.log(selectedItem);
    },
  },
};
</script>

<style lang="scss" >
</style>
