import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";
import Upload from "./views/Upload.vue"
import Login from "./views/Login"
import Signup from "./views/Signup";

Vue.use(Router);

const requireAuth = () => (to, from, next) => {
  const token = localStorage.getItem("userInfo") ? JSON.parse(localStorage.getItem("userInfo")).token : null;
  if (token !== null) {
    return next();
  }
  next('/');
};

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "login",
      component: Login
    },
    {
      path: "/signup",
      name: "signup",
      component: Signup
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () =>
        import(/* webpackChunkName: "about" */ "./views/About.vue")
    },
    {
      path: "/upload",
      name: "upload",
      component: Upload,
      beforeEnter: requireAuth()
    }
  ]
});
