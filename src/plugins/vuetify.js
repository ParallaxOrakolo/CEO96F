import '@mdi/font/css/materialdesignicons.css'
import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

export default new Vuetify({
icons:{
iconsfont:'mdi'
},
// theme: {
//     themes: {
//       light: {
//         primary: '#3f51b5',
//         secondary: '#b0bec5',
//         accent: '#8c9eff',
//         error: '#b71c1c',
//       },
//     },
//   },
});
