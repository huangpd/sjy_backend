import Vue from 'vue'
import App from '@/App.vue'
import router from '@/router'
import store from '@/store'
import '@/plugins/element.js'
import VePie from 'v-charts/lib/pie.common'
import VeHistogram from 'v-charts/lib/histogram.common'
import VeMap from 'v-charts/lib/map.common'
import VeLine from 'v-charts/lib/line.common'
import VeCandle from 'v-charts/lib/candle.common'

import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.component(VePie.name, VePie)
Vue.component( VeHistogram.name,VeHistogram)
Vue.component( VeMap.name,VeMap)
Vue.component(VeLine.name, VeLine)
Vue.component(VeCandle.name, VeCandle)


Vue.use(VueAxios,axios)


Vue.config.productionSourceMap = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
