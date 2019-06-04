import Vue from 'vue'
import Router from 'vue-router'
import TownHome from '@/views/TownHome.vue'
import TownEnter from '@/views/TownEnter.vue'
import TownCompany from '@/views/TownCompany.vue'
import CompanyDetails from '@/views/CompanyDetails.vue'


Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/town_home/',
      name: 'town_home',
      component: TownHome
    },
    {
      path: '/town_enter/',
      name: 'town_enter',
      component: TownEnter
    },
    {
      path: '/town_company/',
      name: 'town_company',
      component: TownCompany
    },
    {
      path: '/Company_Details/:id',
      name: 'Company_Details',
      component: CompanyDetails
    },

    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    // }
  ]
})
