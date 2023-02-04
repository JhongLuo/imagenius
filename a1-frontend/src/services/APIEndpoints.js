import API from "@/services/API";

// (ERROR format)
//   {
//     "success": "false",
//     "error": {
//       "code": String (server_error_code)
//       "message": String (error_message)
//     }
//   }

export default {
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
  postImage(data) {
    return API().post("/api/upload", data);
  },

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
  getImage(key) {
    return API().get("/api/key/" + key);
  },

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
  getAllKeys() {
    return API().get("/api/list_keys");
  },

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
  postDeleteAllData() {
    return API().post("/api/delete_all");
  },

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
  getCacheKeys() {
    return API().get("/api/cache_keys");
  },

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
  getCacheConfigs(data) {
    return API().get("/api/cache_configs", data);
  },

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
  putCacheConfigs(data) {
    return API().put("/api/cache_configs", data);
  },

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
  postClearCache() {
    return API().post("/api/clear_cache");
  },

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
  //     TODO: specify response format
  //     "success": "true",
  //     "stats" : [String]
  //   }
  //
  getStats() {
    return API().get("/api/stats");
  },
};
