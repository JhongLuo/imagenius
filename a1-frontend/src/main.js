import { createApp } from "vue";

import App from "@/App.vue";
import router from "@/router";

// Import our bootstrap CSS
import "@/styles/base-bootstrap.scss";

// Import all of Bootstrap's JS
import * as bootstrap from "bootstrap"; // important for modals to work

const app = createApp(App);
app.use(router);
app.mount("#app");
