import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from '@/router'
import {store} from './store/index'
import VueTheMask from 'vue-the-mask'

Vue.use(VueTheMask)
//soket.io instance creat
// import socketio from 'socket.io';
// import VueSocketIO from 'vue-socket.io';
// Vue.use(VueSocketIO, SocketInstance, store)


Vue.config.productionTip = false
import "@/assets/scss/main.scss";
import "@/assets/scss/_variables.scss";
// import './registerServiceWorker'
import wb from "./registerServiceWorker";
Vue.prototype.$workbox = wb;


new Vue({
  vuetify,
  render: h => h(App),

  router,
  store,
}).$mount('#app')
