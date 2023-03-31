import { reactive, computed, watch } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

export const useAPIStore = defineStore("api", () => {
  let ipAddr = reactive({
    host: "localhost",
    port: "5000",
  });

  if (localStorage.getItem("ipAddr")) {
    ipAddr.host = JSON.parse(localStorage.getItem("ipAddr")).host;
    ipAddr.port = JSON.parse(localStorage.getItem("ipAddr")).port;
  }

  watch(
    ipAddr,
    (val) => {
      localStorage.setItem("ipAddr", JSON.stringify(val));
    },
    { deep: true }
  );

  const baseURL = computed(() => `http://${ipAddr.host}:${ipAddr.port}/`);
  const baseURLShort = computed(() => `${ipAddr.host}:${ipAddr.port}`);

  const baseAxios = computed(() => axios.create({ baseURL: baseURL.value }));

  // UPLOAD PAGE
  // ----------------------------------------------------------------
  //

  // - Post Image:
  //
  // request format:
  // (POST)
  //   {
  //     "key": String,
  //     "file": file
  //   }
  //
  // response format:
  //   {
  //     "success": "true",
  //     "key" : [String]
  //   }
  //
  //
  const postImage = (data) => baseAxios.value.post("/api/upload", data);

  // RETRIEVE PAGE
  // ----------------------------------------------------------------
  //

  // - Retrieve Image:
  //
  // request format:
  //   (GET)
  //   None
  //
  // response format:
  //   {
  //     "success": "true",
  //     "key" : [String]
  //     "content": file
  //   }
  //
  const getImage = (key) => baseAxios.value.get("/api/key/" + key);

  // KEYS PAGE
  // ----------------------------------------------------------------
  //

  // - Retrieve All Keys:
  //
  // request format:
  //   (GET)
  //   None
  //
  // response format:
  //   {
  //     "success": "true",
  //     "keys" : [String]
  //   }
  //
  const getAllKeys = () => baseAxios.value.get("/api/list_keys");
  // - Delete All Data (Keys and Values):
  //
  // request format:
  //   (POST)
  //   None
  //
  // response format:
  //   {
  //     "success": "true"
  //   }
  //
  const postDeleteAllData = () => baseAxios.value.post("/api/delete_all");

  // CONFIG PAGE
  // ----------------------------------------------------------------
  //

  // - Get All Cache Keys:
  //
  // request format:
  //   (GET)
  //   None
  //
  // response format:
  //   {
  //     "success": "true",
  //     "keys" : [String]
  //   }
  //
  const getCacheKeys = () => baseAxios.value.get("/api/cache_keys");
  // - Get Cache Configs:
  //
  // request format:
  //   (GET)
  //   None
  //
  // response format:
  //   {
  //     "success": "true",
  //     "replacement_policy": String,
  //     "max_size": Number
  //   }
  //
  const getCacheConfigs = (data) =>
    baseAxios.value.get("/api/cache_configs", data);
  // - Put Cache Configs:
  //
  // request format:
  //   (POST)
  //   {
  //     "replacement_policy": String ("LRU" / "random"),
  //     "max_size": Int (in bytes)
  //   }
  //
  // response format:
  //   {
  //     "success": "true",
  //     "replacement_policy": String,
  //     "max_size": Number
  //   }
  //
  const putCacheConfigs = (data) =>
    baseAxios.value.put("/api/cache_configs", data);
  // - Clear All Cache Data (reset cache):
  //
  // request format:
  //   (POST)
  //   None
  //
  // response format:
  //   {
  //     "success": "true",
  //     "replacement_policy": String,
  //     "max_size": String
  //   }
  //
  const postClearCache = () => baseAxios.value.post("/api/clear_cache");

  // STATS PAGE
  // ----------------------------------------------------------------
  //

  // - Get Stats:
  //
  // request format:
  //   (GET)
  //   None
  //
  // response format:
  //   {
  //     "success": "true",
  //     "stats" : [Object]
  //   }
  //
  const getStats = () => baseAxios.value.get("/api/stats");

  return {
    ipAddr,
    baseURLShort,
    postImage,
    getImage,
    getAllKeys,
    postDeleteAllData,
    getCacheKeys,
    getCacheConfigs,
    putCacheConfigs,
    postClearCache,
    getStats,
  };
});
