import Vue from 'vue'
import Router from 'vue-router'
// import Home from './views/Home.vue'

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    // {
    //   path: '/',
    //   name: 'home',
    //   component: Home
    // },
    {
      path: '/',
      name: 'index',
      component: () => import('./views/node.vue')
    },
    {
      path: '/node',
      name: 'node',
      component: () => import('./views/node.vue')
    },
    {
      path: '/software',
      name: 'software',
      component: () => import('./views/software.vue')
    },
    {
      path: '/properties',
      name: 'properties',
      component: () => import('./views/properties.vue')
    },
    {
      path: '/person',
      name: 'person',
      component: () => import('./views/person.vue')
    },
  ]
})
