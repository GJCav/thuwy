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

router.beforeEach((to, from, next) => {
  const vue = router.app;
  if (to.path === "/login") { // 若已经登陆，检测是否需要跳转到根
    // eslint-disable-next-line prefer-destructuring
    let session = vue.$store.getters.session;
    if (!session) {
      session = localStorage.getItem("session")
      if (session) {
        vue.$store.dispatch("verifySession", { session }).then(r => {
          if (r) next("/");
          else next();
        })
      } else {
        next();
      }
    }
  } else {  // 跳转到其他页面前验证 session 是否合法，不合法跳转 /login
    // eslint-disable-next-line prefer-destructuring
    let session = vue.$store.getters.session;
    if (!session) {
      session = localStorage.getItem("session");
      vue.$store.dispatch("verifySession", { session }).then((r) => {
        if (r) next();
        else next("/login");
      })
    } else {
      next();
    }
  }
})

export default router;
