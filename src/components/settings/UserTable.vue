<template>
  <v-data-table
    :headers="headers"
    :items="configuration.informations.userList"
    sort-by="lastAcess"
    class="elevation-1"
  >
    <template v-slot:item.name="{ item }" class="name">
      {{ item.name }}
      <v-chip
        v-if="
          configuration.informations.userList.indexOf(item) ==
          editedItem.newUserIndex
        "
        class="ma-2"
        close
        color="green"
        outlined
        rounded
        @click:close="editedItem.newUserIndex = null"
      >
        Novo
      </v-chip>
    </template>

    <template v-slot:item.lastAcess="{ item }">
      {{ timestampToData(item.lastAcess) }}
    </template>

    <template v-slot:top>
      <validation-observer ref="observer" v-slot="{ invalid }">
        <form @submit.prevent="submit">
          <v-toolbar flat>
            <v-toolbar-title>Gerenciador de usuários</v-toolbar-title>
            <!-- <v-divider class="mx-4" inset vertical></v-divider> -->
            <v-spacer></v-spacer>

            <v-dialog v-model="dialog" max-width="500px">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  class="mx-2"
                  fab
                  dark
                  small
                  color="orange"
                  v-bind="attrs"
                  v-on="on"
                >
                  <v-icon dark>mdi-plus </v-icon></v-btn
                >
              </template>
              <v-card>
                <v-card-title>
                  <span class="headline">{{ formTitle }}</span>
                </v-card-title>

                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-col cols="12" sm="8" md="12">
                        <!-- <v-text-field
                          v-model="editedItem.name"
                          label="Name"
                        ></v-text-field> -->

                        <validation-provider
                          v-slot="{ errors }"
                          name="Name"
                          rules="required|max:100"
                        >
                          <v-text-field
                            v-model="editedItem.name"
                            :error-messages="errors"
                            label="Name"
                          ></v-text-field>
                        </validation-provider>
                      </v-col>
                      <v-col cols="12" sm="8" md="12">

                        <!-- precisa incerir validação de numeric -->
                        <validation-provider
                          v-slot="{ errors }"
                          name="ID"
                          rules="required"
                        >
                          <v-text-field
                            v-model.number="editedItem.id"
                            :error-messages="errors"
                            label="ID"
                            inputmode="numeric"
                            :type="show ? 'text' : 'password'"
                            :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                            @click:append="show = !show"
                          ></v-text-field>
                        </validation-provider>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>

                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="close">
                    Cancelar
                  </v-btn>
                  <v-btn
                    color="blue darken-1"
                    text
                    @click="save"
                    :disabled="invalid"
                  >
                    Salvar
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>

            <v-dialog v-model="dialogDelete" max-width="500px">
              <v-card>
                <v-card-title class="headline"
                  >Você tem certeza que quer deletar esse usuario?</v-card-title
                >
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="blue darken-1" text @click="closeDelete"
                    >Cancelar</v-btn
                  >
                  <v-btn color="blue darken-1" text @click="deleteItemConfirm"
                    >Sim</v-btn
                  >
                  <v-spacer></v-spacer>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-toolbar>
        </form>
      </validation-observer>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon small class="mr-2" @click="editItem(item)"> mdi-pencil </v-icon>
      <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize"> Reset </v-btn>
    </template>
  </v-data-table>
</template>

<script>
import { mapState } from "vuex";

import { required, digits, max, regex } from "vee-validate/dist/rules";
import {
  extend,
  ValidationObserver,
  ValidationProvider,
  setInteractionMode,
} from "vee-validate";

setInteractionMode("eager");

extend("digits", {
  ...digits,
  message: "{_field_} needs to be {length} digits. ({_value_})",
});

extend("numeric", {
  ...digits,
  message: " seu {_field_} só pode conter numeros.",
});

extend("required", {
  ...required,
  message: "{_field_} não pode ficar vazio",
});

extend("max", {
  ...max,
  message: "O {_field_}  não pode ser maior q {length} caracteres",
});

extend("regex", {
  ...regex,
  message: "{_field_} {_value_} does not match {regex}",
});

export default {
  name: "UserTable",
  components: {
    ValidationProvider,
    ValidationObserver,
  },

  data: () => ({
    show: false,
    rules: {
      required: (value) => !!value || "Required.",
      min: (v) => v.length >= 4 || "Min 8 characters",
    },

    dialog: false,
    dialogDelete: false,
    headers: [
      {
        text: "Nome",
        value: "name",
      },
      { text: "Ultimo acesso", value: "lastAcess" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    editedIndex: -1,
    editedItem: {
      name: "",
      lastAcess: null,
      id: Number,
      newUserIndex: null,
    },
    defaultItem: {
      name: "",
      lastAcess: null,
      id: Number,
    },
  }),

  computed: {
    ...mapState(["configuration"]),

    formTitle() {
      return this.editedIndex === -1
        ? "Adicionar novo usuário"
        : "Editar usuário";
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  created() {
    // this.initialize();
  },

  methods: {
    timestampToData(timestamp) {
      var d = new Date(timestamp);
      var options = {
        year: "numeric",
        month: "numeric",
        day: "numeric",
        hour: "numeric",
        minute: "numeric",
        second: "numeric",
        hour12: true,
      };

      return new Intl.DateTimeFormat("pt-BR", options).format(d);
    },

    editItem(item) {
      this.editedIndex = this.configuration.informations.userList.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      this.editedIndex = this.configuration.informations.userList.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      this.informations.userList.splice(this.editedIndex, 1);
      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.editedItem.newUser = true;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });

      this.$refs.observer.reset();
    },

    save() {
      if (this.editedIndex > -1) {
        console.log("entrei");
        Object.assign(
          this.configuration.informations.userList[this.editedIndex],
          this.editedItem
        );
        console.log("sai");
      } else {
        this.configuration.informations.userList.push(this.editedItem);
      }
      //save timestamp
      const currentDate = new Date();
      this.editedItem.lastAcess = currentDate.getTime();

      this.$refs.observer.reset();

      this.close();
    },
  },
};
</script>

<style scoped lang="scss">

.name{
  text-transform: capitalize;
}
</style>