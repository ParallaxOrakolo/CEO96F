<template>
  <section class="mt-6 mb-6">
    <div class="d-flex">
      <v-dialog v-model="dialog" width="600px"><gcode></gcode></v-dialog>
      <div class="mr-auto pa-2" outlined tile>
        <h1 class="ml-auto mb-2">
          Monitor Serial
          <v-btn text icon x-small @click="dialog = true">
            <v-icon>mdi-information</v-icon>
          </v-btn>
        </h1>
      </div>
      <div class="ml-auto pa-2" outlined tile small>
        <div>
          <!-- <v-row class="d-flex">
            <v-btn v-model="toggle_exclusive" rounded class="mr-auto">
              <v-btn>
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>
              <v-btn>
                <v-icon>mdi-arrow-right</v-icon>
              </v-btn>
              <v-btn @click="clearSerialMonitor()">
                <v-icon>mdi-trash-can-outline</v-icon>
              </v-btn>
              <v-btn-toggle>
                <v-icon>mdi-format-letter-case-upper</v-icon>
              </v-btn-toggle>
            </v-btn>
          </v-row> -->
        </div>
      </div>
    </div>
    <div class="mb-4">
      <v-chip
        
        class="mr-2 mb-2"
        v-for="item in shortcutsList"
        :key="item.text"
        link
        @click="sendChip(item.sendDirect, item.command)"
        >{{ item.text }}{{ item.sendDirect ? "" : "+" }}</v-chip
      >
    </div>
    <div class="textArea" ref="textArea">
      <div v-for="item in serialMonitor" :key="item.index">
        <v-row v-if="item.sent" class="item pl-2">
          <v-col class="col-2 d-flex justify-end">
            <v-chip class="pa-2" color="orange" outlined small chip>
              Enviada
            </v-chip>
          </v-col>
          <v-col class="message">
            <div class="pa-1">
              <p v-for="msg in item.message" :key="msg.index">{{ msg }}</p>
            </div>
          </v-col>
        </v-row>

        <v-row v-else class="item pl-2">
          <v-col class="col-2 d-flex justify-end">
            <v-chip class="pa-2" color="blue" outlined small chip>
              Recebida
            </v-chip>
          </v-col>
          <v-col class="message">
            <div class="pa-1">
              <p v-for="msg in item.message" :key="msg.index">{{ msg }}</p>
            </div>
          </v-col>
        </v-row>
      </div>
    </div>

    <div>
      <v-text-field
        filled
        dense
        rounded
        v-model="message"
        append-outer-icon="mdi-send"
        append-outer-color="orange"
        class="mt-6 pt-0"
        ref="input"
        hide-details
        single-line
        type="text"
        v-on:keyup.enter="send()"
        @click:append-outer="send()"
      >
        <!-- botão de upercase -->
        <v-btn
          class="pb-2 mr-2"
          text
          icon
          small
          color="primary"
          slot="prepend"
          @click="upperCase = !upperCase"
        >
          <v-icon v-if="upperCase">mdi-format-letter-case-upper</v-icon>
          <v-icon v-else color="grey">mdi-format-letter-case</v-icon>
        </v-btn>
        <!-- fim botão de upercase -->

        <v-btn
          class="pb-2 mr-2"
          text
          icon
          small
          color="greu"
          slot="prepend"
          @click="leftItem()"
        >
          <v-icon> mdi-arrow-left </v-icon>
        </v-btn>

        <v-btn
          class="pb-2"
          text
          icon
          small
          color="grey"
          slot="prepend"
          @click="rigthItem()"
        >
          <v-icon> mdi-arrow-right </v-icon>
        </v-btn>
      </v-text-field>
    </div>
  </section>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import { actions } from "../store/index";
import Gcode from "./settings/Gcode";

export default {
  components: { Gcode },
  name: "SerialMonitor",
  data() {
    return {
      actions,
      upperCase: true,
      dialog: false,
      message: null,
      scrolled: false,
      sendCommandList: [],
      selectedItemCommandList: null,

      shortcutsList: [
        {
          text: "G0",
          command: "G0 X ",
          sendDirect: false,
        },
        {
          text: "G90 - Absoluto",
          command: "G90 ",
          sendDirect: true,
        },
        {
          text: "G91 - Relativo",
          command: "G91 ",
          sendDirect: true,
        },
        {
          text: "G28 E",
          command: "G28 E",
          sendDirect: true,
        },
        {
          text: "M114 - Posição Atual",
          command: "M114",
          sendDirect: true,
        },
      ],
    };
  },

  methods: {
    ...mapMutations(["SEND_MESSAGE"]),

    send() {
      if (this.message != "") {
        let msg;
        this.upperCase
          ? (msg = this.message.toUpperCase())
          : (msg = this.message);

        this.SEND_MESSAGE({
          command: actions.SERIAL_MONITOR,
          parameter: msg,
        });

        this.serialMonitor.push({
          hour: Math.floor(Date.now() / 1000),
          sent: true,
          message: [msg],
        });

        this.sendCommandList.push(this.message);
        this.selectedItemCommandList = this.sendCommandList.length;
        this.clearMessage();
      }
      setTimeout(()=> this.scrollToEnd(), 200)
      this.setFocus();
    },

    setFocus() {
      this.$refs.input.focus();
    },

    sendChip(sendDirect, command) {
      this.message = command;

      if (sendDirect) {
        this.send();
      } else {
        this.setFocus();
      }
    },

    scrollToEnd() {
      // console.log("scroll");
      var container = this.$refs.textArea;
      container.scrollTop = container.scrollHeight;
      container.scrollIntoView({ behavior: "smooth" });
    },

    clearMessage() {
      this.message = "";
    },

    clearSerialMonitor() {
      // console.log(this.serialMonitor);
      this.serialMonitor.length = 0;
    },

    leftItem() {
        // console.log(this.sendCommandList.length)
      if (
        this.sendCommandList.length >= this.selectedItemCommandList &&
        this.selectedItemCommandList >= 1
      ) {
                console.log(this.sendCommandList.length)

        //decrementa a lista
        this.selectedItemCommandList = this.selectedItemCommandList - 1;
        this.message = this.sendCommandList[this.selectedItemCommandList];
        // console.log(this.sendCommandList[this.selectedItemCommandList - 1]);
      }
    },

    rigthItem() {
      // console.log(this.sendCommandList.length + "  " + this.selectedItemCommandList);

      if (this.selectedItemCommandList < this.sendCommandList.length) {
        this.selectedItemCommandList = this.selectedItemCommandList + 1;
        this.message = this.sendCommandList[this.selectedItemCommandList - 1];
        // console.log(this.sendCommandList[this.selectedItemCommandList - 1]);
      }
    },
  },
  computed: {
    ...mapState(["serialMonitor"]),
  },
};
</script>

<style scoped lang="scss">
.textArea {
  max-height: 200px;
  overflow-y: scroll !important;
  flex-direction: column-reverse;
  /* border: solid 1px rgb(196, 196, 196); */

  .message {
    background-color: rgb(248, 248, 248);
    border-radius: 0.5em;
    padding: 6px;
    margin: 0.2em;

    p {
      font-size: 0.8em;
      margin: 0;
    }
  }
}
</style>