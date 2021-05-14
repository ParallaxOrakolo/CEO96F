<template>
  <v-expansion-panel>
    <v-expansion-panel-header
      >Configurações avançadas

      <template v-slot:actions>
        <span v-if="logged == true"
          >Olá, <b>{{ userLogged }}!</b>
          <v-btn x-small outlined color="warning" class="ma-2" @click="logout()"
            >Sair</v-btn
          ></span
        >
      </template>
    </v-expansion-panel-header>

    <v-expansion-panel-content>
      <v-divider></v-divider>

      <v-card-subtitle v-if="!logged"
        >Essa area é de acesso restrito
      </v-card-subtitle>
      <v-card-text v-show="!logged">
        <v-text-field
          outlined
          v-model="idInput"
          :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
          :type="show ? 'text' : 'password'"
          name="input-10-2"
          inputmode="numeric"
          label="ID de acesso"
          placeholder="Digite seu ID"
          class="input-group--focused"
          @click:append="show = !show"
          required
        >
        </v-text-field>
        <!-- <v-btn
          color="primary"
          text
          @click="checkPassword"
        >
          Acessar
        </v-btn> -->
      </v-card-text>
      <v-divider></v-divider>

      <v-card-text v-show="logged">
        <v-list three-line subheader>
          <v-subheader>User Controls</v-subheader>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Content filtering</v-list-item-title>
              <v-list-item-subtitle
                >Set the content filtering level to restrict apps that can be
                downloaded</v-list-item-subtitle
              >
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Password</v-list-item-title>
              <v-list-item-subtitle
                >Require password for purchase or use password to restrict
                purchase</v-list-item-subtitle
              >
            </v-list-item-content>
          </v-list-item>
        </v-list>
      <User-table v-if="logged"/>
      </v-card-text>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import { mapState } from "vuex";
import UserTable from './UserTable.vue';

export default {
  components: { UserTable },
  name: "AdvancedSettings",
  data: () => ({
    userLogged: null,
    logged: false,
    show: false,
    idInput: null,
    id: 1234,
    rules: {
      //   required: (value) => !!value || "Required.",
      //   min: (v) => v.length >= 4 || "Min 4 caracteres numéricos",
    },
    errorMessages: "",
    formHasErrors: false,

  }),

  computed: {
    ...mapState(["configuration"]),

    form() {
      return {
        idInput: this.idInput,
      };
    },
  },

  watch: {
    idInput() {
      this.configuration.informations.userList.forEach((user) => {
        if (user.id == parseInt(this.idInput)) {
          this.userLogged = user.name;
          this.logged = true;
          const currentDate = new Date();
          user.lastAcess = currentDate.getTime();
        }
      });
    },
  },

  methods: {
    logout() {
      this.logged = !this.logged;
      this.idInput = "";
    },
  },
};
</script>

<style scoped lang="scss">
</style>