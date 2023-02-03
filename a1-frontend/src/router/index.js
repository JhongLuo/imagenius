import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import UploadView from "@/views/UploadView.vue";
import QueryView from "@/views/QueryView.vue";
import KeysView from "@/views/KeysView.vue";
import ConfigView from "@/views/ConfigView.vue";
import StatsView from "@/views/StatsView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/upload",
      name: "upload",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: UploadView,
    },
    {
      path: "/query",
      name: "query",
      component: QueryView,
    },
    {
      path: "/keys",
      name: "keys",
      component: KeysView,
    },
    {
      path: "/config",
      name: "config",
      component: ConfigView,
    },
    {
      path: "/stats",
      name: "stats",
      component: StatsView,
    },
  ],
});

export default router;
