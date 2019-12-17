import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../views/Home.vue';
import SuiVue from 'semantic-ui-vue';

import 'semantic-ui-css/semantic.min.css';

Vue.use(VueRouter);
Vue.use(SuiVue);

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/TheDashboard.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
