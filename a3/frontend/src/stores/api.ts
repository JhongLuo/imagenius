import { acceptHMRUpdate, defineStore } from 'pinia'

export const useAPIStore = defineStore('api', () => {
  // set up ipAddr
  const defaultAddr = 'http://localhost:5000'

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
  // const baseURL = computed(() => `http://${ipAddr.addr}/`)
  // const baseURLShort = computed(() => `${ipAddr.addr}`)

  const baseAxios = computed(() => axios.create({ baseURL: ipAddr.addr }))

  // API CALLS:

  // ################
  //
  // Image obj format:
  //  {
  //    "key": String,
  //    "src": String
  //  }
  //
  // ################

  // ################
  //
  // Error format:
  //
  //  {
  //    "success": "false",
  //    "error": {
  //      "code": Int,
  //      "message": String
  //    }
  //  }
  //
  // ################

  // - Update API Key:
  //
  // request format:
  // (POST)
  //    No Payload
  //
  // response format:
  //   {
  //     "success": "true",
  //   }
  //
  //
  const updateApiKey = () => baseAxios.value.post('/api/set_api_key', apiKey.value)

  // ADD PAGE
  // ----------------------------------------------------------------
  //

  // - Generate Images:
  //
  // request format:
  // (GET)
  //
  // response format:
  //   {
  //     "success": "true",
  //     "word" : String
  //   }
  //
  //
  const generateRandomWord = () => baseAxios.value.get('/api/random_word')

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
  //
  const searchImagesByTags = (data: FormData) => baseAxios.value.post('/api/search/tags', data)

  // - Search Images By Key:
  //
  // request format:
  // (POST)
  //   {
  //     "key": String
  //   }
  //
  // response format:
  //   {
  //     "success": "true",
  //     "image" : Image
  //   }
  //
  //
  const searchImagesByKey = (data: FormData) => baseAxios.value.post('/api/search/key', data)

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
  //
  const deleteAllImages = () => baseAxios.value.post('/api/delete_all')

  // - Edit Image:
  //
  // request format:
  // (POST)
  //   {
  //      "parent_key": String
  //      "prompt": String
  //      "x_pos": Int
  //      "y_pos": Int
  //      "radius": Int
  //   }
  //
  // response format:
  //   {
  //     "success": "true",
  //     "image" : Image
  //   }
  //
  //
  const editImage = (data: FormData) => baseAxios.value.post('/api/edit', data)

  return {
    ipAddr,
    apiKey,
    updateApiKey,
    generateRandomWord,
    generateImages,
    saveImages,
    searchImagesByPrompt,
    getTags,
    searchImagesByTags,
    searchImagesByKey,
    getAllImages,
    deleteAllImages,
    editImage,
  }
})

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useAPIStore, import.meta.hot))
