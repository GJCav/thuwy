import Vue from 'vue';
import VueRouter from 'vue-router';

import LoginView from "./views/LoginView.vue";
import MyProfileView from "./views/MyProfileView.vue"
import UserListView from "./views/UserListView.vue"
import UserPrivielegeView from "./views/UserPrivilegeView.vue"
import GroupListView from "./views/GroupListView.vue"


Vue.use(VueRouter);

const routes = [
  { path: "/", component: MyProfileView },
  { path: '/login', component: LoginView },
  { path: "/userlist", component: UserListView },
  { path: "/user_privilege", component: UserPrivielegeView, name: "user_privilege", props: true },
  { path: "/grouplist", component: GroupListView }
];

const router = new VueRouter({
  mode: 'history',
  base: "/",
  routes,
});

export default router;
