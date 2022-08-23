import Vue from 'vue';
import VueRouter from 'vue-router';
import HomeView from '@/views/Home.vue';
import LoginView from '@/views/Login.vue';
import ProfileView from '@/views/Profile.vue';
import RsvLayout from '@/views/_layout/RsvLayout.vue';
import IssueLayout from '@/views/_layout/IssueLayout.vue';
import BlogView from '@/views/_layout/BlogLayout.vue';

Vue.use(VueRouter);

const routes = [{
    path: '/',
    name: 'Home',
    component: HomeView
},
{
    path: '/login',
    name: 'Login',
    component: LoginView
},
{
    path: '/about',
    name: 'About',
    component: () =>
        import('@/views/About.vue')
},
{
    path: '/profile/',
    name: 'Profile',
    component: ProfileView
},
{
    path: '/blog/',
    component: BlogView,
    children: [{
        path: ':id(\\d+)',
        name: 'BlogDetail',
        component: () => import('@/views/Blog/BlogDetail.vue')
    }, {
        path: ':id(\\d+)/edit/',
        name: 'BlogEdit',
        component: () => import('@/views/Blog/BlogEdit.vue')
    }, {
        path: '*',
        name: 'BlogHome',
        component: () => import('@/views/Blog/BlogHome.vue')
    }]
},
{
    path: '/issue/',
    component: IssueLayout,
    children: [{
        path: ':id(\\d+)',
        name: 'IssueDetail',
        component: () =>
            import('@/views/Issue/IssueDetail.vue')
    },
    {
        path: 'list',
        name: 'IssueList',
        component: () =>
            import('@/views/Issue/IssueList.vue')
    },
    {
        path: '*',
        name: 'IssueHome',
        component: () =>
            import('@/views/Issue/IssueHome.vue')
    }
    ]
},
{
    path: '/rsv/',
    component: RsvLayout,
    children: [{
        path: 'item',
        name: 'ItemManage',
        component: () =>
            import('@/views/Rsv/ItemManage.vue')
    },
    {
        path: 'item/:id(\\d+)',
        name: 'ItemInfo',
        component: () =>
            import('@/views/Rsv/ItemInfo.vue')
    },
    {
        path: 'item/:id/edit',
        name: 'ItemEdit',
        component: () =>
            import('@/views/Rsv/ItemEdit.vue')
    },
    {
        path: 'reservation',
        name: 'RsvManage',
        component: () =>
            import('@/views/Rsv/RsvManage.vue')
    },
    {
        path: '*',
        name: 'RsvHome',
        component: () =>
            import('@/views/Rsv/RsvHome.vue')
    }]
},
{
    path: '*',
    name: 'NotFound',
    component: () =>
        import('@/views/404.vue')
},
];

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
});

export default router;