import axios from "axios";

// TODO: set correct port for production
// const API_PORT = 5000;
const API_PORT = 3000; // local testing
const API_URL = "http://localhost:" + API_PORT;
export default (url = API_URL) => {
  return axios.create({
    baseURL: url,
  });
};
