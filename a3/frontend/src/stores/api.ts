import { acceptHMRUpdate, defineStore } from 'pinia'

export const useAPIStore = defineStore('api', () => {
  // set up ipAddr
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

  // set up api key
  const defaultApiKey = ''

  const apiKey = ref(defaultApiKey)

  const storedApiKey = localStorage.getItem('apiKey')
  if (storedApiKey)
    apiKey.value = storedApiKey

  watch(
    apiKey,
    (val) => {
      localStorage.setItem('apiKey', val)
    },
  )

  // other variables
  const baseURL = computed(() => `http://${ipAddr.addr}/`)
  const baseURLShort = computed(() => `${ipAddr.addr}`)

  const baseAxios = computed(() => axios.create({ baseURL: baseURL.value }))

  // API CALLS:

  // - Update API Key:
  //
  const updateApiKey = () => baseAxios.value.post('/api/set_api_key', apiKey.value)

  // ADD PAGE
  // ----------------------------------------------------------------
  //

  // - Generate Images:
  //
  // request format:
  // (POST)
  //   {
  //     "prompt": String,
  //   }
  //
  // response format:
  //   {
  //     "success": "true",
  //     "images" : [Image]
  //   }
  //
  // image obj format:
  //   {
  //     "key": String,
  //     "src": String
  //   }
  //
  //
  const generateImages = (data: FormData) => baseAxios.value.post('/api/generate', data)

  // - Save Images:
  //
  // request format:
  // (POST)
  //   {
  //     "selected_keys": [String], encoded into a JSON string  # can be decoded using json.loads()
  //   }
  //
  // response format:
  //   {
  //     "success": "true",
  //   }
  //
  //
  const saveImages = (data: FormData) => baseAxios.value.post('/api/save', data)

  // - Search Images By Prompt:
  //
  // request format:
  // (POST)
  //   {
  //     "prompt": String,
  //   }
  //
  // response format:
  //   {
  //     "success": "true",
  //     "images" : [Image]
  //   }
  //
  // image obj format:
  //   {
  //     "key": String,
  //     "src": String
  //   }
  //
  //
  const searchImagesByPrompt = (data: FormData) => baseAxios.value.post('/api/search/prompt', data)

  // - Get Tags:
  //
  // request format:
  // (GET)
  //
  // response format:
  //   {
  //     "success": "true",
  //     "tags" : [String]
  //   }
  //
  //
  //
  const getTags = () => baseAxios.value.get('/api/tags')

  // - Search Images By Tags:
  //
  // request format:
  // (POST)
  //   {
  //     "selected_tags": [String], encoded into a JSON string  # can be decoded using json.loads()
  //   }
  //
  // response format:
  //   {
  //     "success": "true",
  //     "images" : [Image]
  //   }
  //
  // image obj format:
  //   {
  //     "key": String,
  //     "src": String
  //   }
  //
  //
  const searchImagesByTags = (data: FormData) => baseAxios.value.post('/api/search/tags', data)

  // - Get All Images:
  //
  // request format:
  // (GET)
  //
  // response format:
  //   {
  //     "success": "true",
  //     "images" : [Image]
  //   }
  //
  // image obj format:
  //   {
  //     "key": String,
  //     "src": String
  //   }
  //
  //
  const getAllImages = () => baseAxios.value.get('/api/list_all')

  // - Delete All Images:
  //
  // request format:
  // (POST)
  //   No Payload
  //
  // response format:
  //   {
  //     "success": "true",
  //     "images" : [Image] # should be empty
  //   }
  //
  // image obj format:
  //   {
  //     "key": String,
  //     "src": String
  //   }
  //
  //
  const deleteAllImages = () => baseAxios.value.post('/api/delete_all')

  return {
    ipAddr,
    apiKey,
    baseURLShort,
    updateApiKey,
    generateImages,
    saveImages,
    searchImagesByPrompt,
    getTags,
    searchImagesByTags,
    getAllImages,
    deleteAllImages,
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useAPIStore, import.meta.hot))
