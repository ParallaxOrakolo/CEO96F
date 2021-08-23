<template>
  <div>
    <v-menu offset-y>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          v-bind="attrs"
          v-on="on"
          v-haptic
          elevation="2"
          fab
          dark
          x-large
          color="blue"
        >
          <v-icon dark>mdi-home</v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-list-item v-for="(item, index) in items"
          :key="index">
          <v-list-item-title> <v-btn
          
          
          dark
          color="blue"
          @click="
            () => {
              SEND_MESSAGE({
                command: actions.SERIAL_MONITOR,
                parameter: item.command,
              });
            }
          "
        >
{{item.title}}
        </v-btn></v-list-item-title>
         
        </v-list-item>

      </v-list>
    </v-menu>
  </div>
</template>

<script>
//import { mapState, mapMutations } from "vuex"; mapState sem uso.
import { mapMutations } from "vuex";
import { actions } from "../../../store/index";

export default {
  name: "Homing",
  data() {
    return {
      actions,
      items: [
        { title: 'Home', command: 'G28'},
        { title: 'Home X', command: 'G28 X'},
        { title: 'Home Y', command: 'G28 Y'},
        { title: 'Home Z', command: 'G28 Z'},
      ],
    };
  },

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),
  },
};
</script>

<style scoped lang="scss">
.v-btn--round {
  border-radius: 26%;
}

.numberInput {
  max-width: 80px;
  margin-left: 15px;
}
</style>