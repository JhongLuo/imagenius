import axios from "axios";
import * as Constants from "@/composables/constants";

let apiMode;
let selected_host;
let selected_port;

// ******** PLEASE SELECT THE CORRECT MODE ********
// apiMode = "production";
apiMode = "dev";
// ********************************

if (apiMode === "dev") {
  selected_host = Constants.PROXYMAN_HOST_PREFIX;
  selected_port = Constants.PORT_JSON_SERVER;
} else {
  selected_host = Constants.LOCALHOST_HOST_PREFIX;
  selected_port = Constants.PORT_FLASK_APP;
}

// Compose
const API_URL = "http://" + selected_host + ":" + selected_port;

export default (url = API_URL) => {
  return axios.create({
    baseURL: url,
  });
};
