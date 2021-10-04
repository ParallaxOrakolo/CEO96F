<template>
  <v-expansion-panel>
    <v-expansion-panel-header>
      <div>
        <v-icon class="mr-2">mdi-shield-outline</v-icon> Configurações avançadas
      </div>
      <v-progress-linear
        :active="loading"
        :indeterminate="loading"
        absolute
        bottom
      ></v-progress-linear>

      <template v-slot:actions>
        <span v-if="configuration.informations.users.logged"
          >Olá, <b>{{ configuration.informations.users.logged.name }}!</b>
          <v-btn x-small outlined color="warning" class="ma-2" @click="logout()"
            >Sair</v-btn
          ></span
        >
      </template>
    </v-expansion-panel-header>

    <v-expansion-panel-content>
      <v-divider></v-divider>

      <v-card-subtitle
        class="mt-10"
        v-if="!configuration.informations.users.logged"
        >Essa area é de acesso restrito
      </v-card-subtitle>

      <v-card-text
        v-if="!configuration.informations.users.logged"
        class="d-flex justify-row"
      >
        <v-text-field
          outlined
          v-model="idInput"
          :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
          :type="show ? 'number' : 'password'"
          name="input-10-2"
          inputmode="numeric"
          label="CPF"
          placeholder="Digite seu CPF (apenas números)"
          class="input-group--focused"
          @click:append="show = !show"
          rounded
          required
          @keyup.enter="checkPassword()"
        >
        </v-text-field>

        <v-btn
          v-if="idInput"
          class="mt-1 ml-2"
          color="primary"
          rounded
          x-large
          @click="checkPassword()"
        >
          Acessar
        </v-btn>
      </v-card-text>
      <v-card-text v-if="isUserAcessPermited(this.$options.name)">
        <UserTable v-if="isUserAcessPermited('UserTable')" />
        <JsonEditor2 @update-loading="loading=false" v-if="isUserAcessPermited('JsonEditor2')" />
      </v-card-text>
      <!-- <JsonEditor2 /> -->
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import { actions } from "../../store/index";
import UserTable from "./UserTable.vue";
import JsonEditor2 from "./JsonEditor2.vue";
import Mixins from "@/mixins/mixins";

export default {
  components: { UserTable, JsonEditor2 },
  mixins: [Mixins],
  name: "AdvancedSettings",
  data: () => ({
    show: false,
    idInput: null,
    id: 1234,
    rules: {
      //   required: (value) => !!value || "Required.",
      //   min: (v) => v.length >= 4 || "Min 4 caracteres numéricos",
    },
    errorMessages: "",
    formHasErrors: false,
    loading: false,
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
    // idInput() {
    //   this.configuration.informations.userList.forEach((user) => {
    //     if (user.id == parseInt(this.idInput)) {
    //       this.userLogged = user.name;
    //       this.configuration.logged = true;
    //       const currentDate = new Date();
    //       user.lastAcess = currentDate.getTime();
    //     }
    //   });
    // },
  },

  methods: {
        ...mapMutations(["SEND_MESSAGE"]),

     updateBack() {
      this.SEND_MESSAGE({command: actions.UPDATE_USERS,  parameter: this.configuration.informations.users,});
    },
    
    logout() {
      this.configuration.informations.users.logged = false;
      this.idInput = "";
      this.updateBack()
      console.log(this.configuration.informations.users.logged);

    },
    // logout() {
    //   this.configuration.logged = !this.configuration.logged;
    //   this.idInput = "";
    // },

    checkPassword() {
      this.configuration.informations.users.userList.forEach((user) => {
        if (user.id == parseInt(this.idInput)) {
          this.configuration.informations.users.logged = user;
          console.log(this.configuration.informations.users.logged);
          const currentDate = new Date();
          user.lastAcess = currentDate.getTime();
          this.idInput = "";
          this.updateBack()
        }
      });
    },
  },

  created: function () {},
};
</script>

<style scoped lang="scss">
</style>