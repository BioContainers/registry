// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store/store.js'
import iView from 'iview';
import './assets/iviewtheme/iview.css';
//import 'iview/dist/styles/iview.css';//we could use our own theme directory:import './assets/my-theme/index.less'; 'index.css' need to be created properly according to iview instruction.
import locale from 'iview/dist/locale/en-US';
import VueResource  from 'vue-resource'
import ReadMore from 'vue-read-more';
import ECharts from 'vue-echarts/components/ECharts'
// import ECharts modules manually to reduce bundle size
import 'echarts/lib/chart/heatmap'


import 'echarts/lib/chart/bar'
import 'echarts/lib/component/tooltip'
import 'echarts/lib/chart/line'
import 'echarts/lib/chart/sunburst'
import 'echarts/lib/chart/sankey'
import 'echarts/lib/chart/tree'
import 'echarts/lib/component/polar'
import 'echarts/lib/chart/pie'
import 'echarts/lib/component/legend'
import 'echarts/lib/component/legend/ScrollableLegendModel.js'
import 'echarts/lib/component/legend/ScrollableLegendView.js'
import 'echarts/lib/component/legend/scrollableLegendAction.js'
import 'echarts/lib/component/visualMap'//these two used for dividing the data accoridng to Y
import 'echarts/lib/component/visualMapContinuous'//these two used for dividing the data accoridng to Y
import 'echarts/lib/component/dataZoom.js'
import 'echarts/lib/chart/map'
import 'echarts/map/json/world.json'
import 'echarts/map/js/world.js'



Vue.config.productionTip = false
Vue.use(iView, { locale });
Vue.use(VueResource);
Vue.use(ReadMore);
Vue.component('chart', ECharts)

 

const bus = new Vue();
Object.defineProperty(Vue.prototype, '$bus', { get(){return this.$root.bus} });

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  data:{bus},
  store,
  components: { App },
  template: '<App/>'
})
