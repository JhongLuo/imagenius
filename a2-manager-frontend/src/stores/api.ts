import { acceptHMRUpdate, defineStore } from 'pinia'
import axios from 'axios'

export const useAPIStore = defineStore('api', () => {
  const defaultAddr = 'localhost:5000'

  const ipAddr = reactive({
    addr: defaultAddr,
  })

  const storedIPAddr = localStorage.getItem('ipAddr')
  ipAddr.addr = storedIPAddr ? JSON.parse(storedIPAddr).addr : defaultAddr

  watch(
    ipAddr,
    (val) => {
      localStorage.setItem('ipAddr', JSON.stringify(val))
    },
    { deep: true },
  )

  const baseURL = computed(() => `http://${ipAddr.addr}/`)
  const baseURLShort = computed(() => `${ipAddr.addr}`)

  const baseAxios = computed(() => axios.create({ baseURL: baseURL.value }))

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
  const postImage = (data: FormData) => baseAxios.value.post('/api/upload', data)

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
  const getImage = (key: string) => baseAxios.value.get(`/api/key/${key}`)

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
  const getAllKeys = () => baseAxios.value.get('/api/list_keys')
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
  const postDeleteAllData = () => baseAxios.value.post('/api/delete_all')

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
  const getCacheKeys = () => baseAxios.value.get('/api/cache_keys')
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
  const getCacheConfigs = () => baseAxios.value.get('/api/cache_configs')
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
  const putCacheConfigs = (data: { replacement_policy: string; max_size: number }) =>
    baseAxios.value.put('/api/cache_configs', data)
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
  const postClearCache = () => baseAxios.value.post('/api/clear_cache')

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
  const getStats = () => baseAxios.value.get('/api/stats')

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
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useAPIStore, import.meta.hot))
