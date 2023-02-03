import { createApp } from "vue";

import App from "@/App.vue";
import router from "@/router";

// Import bootstrap CSS
import "@/styles/base-bootstrap.scss";

// Import all of Bootstrap's JS
// eslint-disable-next-line no-unused-vars
import * as bootstrap from "bootstrap"; // <- important for modals to work

const app = createApp(App);
app.use(router);
app.mount("#app");
