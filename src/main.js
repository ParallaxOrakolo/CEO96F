import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import router from '@/router'
import {store} from './store/index'
import VueTheMask from 'vue-the-mask'
import VueHaptic from 'vue-haptic';
import JsonEditor from 'vue-json-edit'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

Vue.use(JsonEditor)

Vue.use(vuetify, {
  iconfont: 'md'
})

Vue.use(VueHaptic, {
  // Required. vue-haptic does not provide
  // any out-of-the-box patterns
  defaultHapticTrigger: 'touchstart',
  
  patterns: {
    success: [10, 100, 30],
    failure: [10, 50, 10, 50, 50, 100, 10],
    long: 200,
    default: 60,
  },
});

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

