<template>
  <v-app>
    <NavBar/>
    <v-main>
      <router-view/>
      <!-- <Home/> -->
    </v-main>
  </v-app>
</template>

<script>
//import Home from "./views/Home";
import NavBar from "./components/NavBar";
 

export default {
  name: "App",

  components: {

    //Home,
    NavBar
  },

  data: () => ({
    //
  }),
};
</script>

<style lang="scss">

::-webkit-scrollbar {
    display: none;
}

html, body {
   width: 100%;
   height: 100%;
   margin: 0;
   padding: 0;
}

</style>