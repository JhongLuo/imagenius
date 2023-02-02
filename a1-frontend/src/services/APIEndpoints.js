import API from "@/services/API";

export default {
  // UPLOAD PAGE
  // ----------------------------------------------------------------

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
  // (SUCCESS)
  //   {
  //     "success": "true",
  //     "key" : [String]
  //   }
  //
  // (ERROR)
  //   {
  //     "success": "false",
  //     "error": {
  //       "code": server_error_code
  //       "message": error_message
  //     }
  //   }
  //
  postImage(data) {
    return API().post("/api/upload", data);
  },

  // QUERY PAGE
  // ----------------------------------------------------------------
  //

  // - Get Image:
  //
  // request format:
  // (GET)
  // None
  //
  // response format:
  // (SUCCESS)
  // {
  //   "success": "true",
  //   "key" : [String]
  //   "content": file
  // }
  // (ERROR)
  // {
  //   "success": "false",
  //   "error": {
  //     "code": server_error_code
  //     "message": error_message
  //   }
  // }
  //
  getImage(key) {
    return API().get("/api/key/" + key);
  },

  // KEYS PAGE
  // ----------------------------------------------------------------
  //

  // - Get All Keys:
  //
  // request format:
  // (GET)
  // None
  //
  // response format:
  // (SUCCESS)
  // {
  //   "success": "true",
  //   "key" : [String]
  //   "content": file
  // }
  // (ERROR)
  // {
  //   "success": "false",
  //   "error": {
  //     "code": server_error_code
  //     "message": error_message
  //   }
  // }
  //
  // TODO: change api to all keys instead of cache keys
  getAllKeys() {
    return API().get("/api/list_keys");
  },

  // - Delete All Keys and Values:
  //
  // request format:
  // (POST)
  // None
  //
  // response format:
  // (SUCCESS)
  // {
  //   "success": "true"
  // }
  //
  deleteAllKeysAndValues() {
    return API().post("/api/delete_all");
  },

  // CONFIG PAGE
  // ----------------------------------------------------------------
  //
  // TODO: implement api for cache keys
  getCacheKeys() {
    return 0;
  },

  // TODO: change URL?
  putReplacementPolicy(data) {
    return API().put("/api/statistics/replacement_policy", data);
  },

  // TODO: change URL?
  putMaxCacheSize(data) {
    return API().put("/api/statistics/max_size", data);
  },

  postClearCache() {
    return API().post("/api/delete_all");
  },

  // STATS PAGE
  // ----------------------------------------------------------------
  //
  getStats() {
    return API().get("/api/statistics");
  },
};
