import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import request from "./util/request"
import './assets/css/global.css'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import echarts from 'echarts'
Vue.prototype.$echarts = echarts;
//代码编辑器
import ace from 'ace-builds'
import componentsInstall from './components/install'
Vue.use(ace)
Vue.use(componentsInstall)

import animated from 'animate.css'
Vue.use(animated)
Vue.use(BootstrapVue)
Vue.config.productionTip = false
Vue.prototype.request=request
Vue.use(ElementUI)
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
