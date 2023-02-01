import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "@/App.vue";
import router from "@/router";

// Import our bootstrap CSS
import "@/styles/base-bootstrap.scss";

// Import all of Bootstrap's JS
// import * as bootstrap from "bootstrap";

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.mount("#app");
