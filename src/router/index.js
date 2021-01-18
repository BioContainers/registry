import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import Registry from '@/components/Registry'

import Tool from '@/components/Tool'
import NotFound from '@/components/NotFound'
import Mappingdata from '@/components/Mappingdata'
import Multipackage from '@/components/Multipackage'

Vue.use(Router);

let router = new Router({
  mode: 'history',
  base: location.hostname.match(/localhost/)?'':'/',
  //   base:'',
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/registry',
      name: 'Registry',
      component: Registry

    },
    {
      path: '/tools/:id',
      name: 'tools',
      component: Tool
    },
    {
      path: '/mappingdata',
      name: 'Mappingdata',
      component: Mappingdata
    },
    {
      path: '/multipackage',
      name: 'Multipackage',
      component: Multipackage
    },
    {
      path:'*',
      name: 'NotFound',
      component: NotFound,
    },
  ]
});

export default router;


router.beforeEach((to, from, next) => {
  // Redirect if fullPath begins with a hash (ignore hashes later in path)
  if (to.fullPath.substr(0,2) === "/#") {
    const path = to.fullPath.substr(2);
    next(path);
    return;
  }
  next();
});
