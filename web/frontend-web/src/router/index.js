import Vue from 'vue';
import VueRouter from 'vue-router';
import DefaultLayout from '@/views/layout/DefaultLayout.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    component: DefaultLayout,
    children: [
      {
        path: '/',
        name: 'Home',
        component: () => import('@/views/Home.vue')
      },
      {
        path: '/item',
        name: 'ItemManage',
        component: () => import('@/views/ItemManage.vue')
      },
      {
        path: '/item/:id(\\d+)',
        name: 'ItemInfo',
        component: () => import('@/views/ItemInfo.vue')
      },
      {
        path: '/item/:id/edit',
        name: 'ItemEdit',
        component: () => import('@/views/ItemEdit.vue')
      },
      {
        path: '/item/new',
        name: 'ItemCreate'
      },
      {
        path: '/user',
        name: 'UserManage',
        component: () => import('@/views/UserManage.vue')
      },
      {
        path: '/reservation',
        name: 'RsvManage',
        component: () => import('@/views/RsvManage.vue')
      },
      {
        path: '/about',
        name: 'About',
        component: () => import('@/views/About.vue')
      },
      {
        path: '*',
        name: 'NotFound',
        component: () => import('@/views/404.vue')
      }
    ]
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

export default router;
