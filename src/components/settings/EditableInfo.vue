<template>
   <v-form class="d-inline-flex pa-0">
    <v-container>
          <v-text-field
            v-model="editedinfo"
            clear-icon="mdi-content-save"
            clearable
            label="IP do Servidor"
            type="text"
            @click:append="toggleMarker"
            @click:clear="sendMessage"
          ></v-text-field>
    </v-container>
  </v-form>
</template>

<script>
import { mapState } from "vuex";

  export default {
    data: () => ({
      editedinfo: '',
      show: false,
      marker: true,
      iconIndex: 0,

    }),

    computed: {
       ...mapState(["configuration"]),
      icon () {
        return this.icons[this.iconIndex]
      },
    },

    methods: {
      toggleMarker () {
        this.marker = !this.marker
      },
      sendMessage () {
        this.resetIcon()
        this.clearMessage()
        this.configuration.informations.ip = this.editedinfo 
        console.log(this.configuration.informations.ip);
      },
      clearMessage () {
        this.message = ''
      },
      resetIcon () {
        this.iconIndex = 0
      },
    },

    created(){
        this.editedinfo = this.configuration.informations.ip
        console.log(this.editedinfo);
    }
    
  }
</script>

<style>

</style>